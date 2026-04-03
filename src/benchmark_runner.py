import argparse
import json
import statistics
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from eda2_indexing.csv_io import load_records_from_csv
from eda2_indexing.index_core import build_primary_index
from eda2_indexing.search_engines import indexed_search, sequential_search


@dataclass(frozen=True)
class Scenario:
    name: str
    params: dict[str, str]


def percentile(sorted_values: list[float], p: int) -> float:
    if not sorted_values:
        return 0.0
    idx = int(round((p / 100) * (len(sorted_values) - 1)))
    return sorted_values[idx]


def measure(func, warmup: int, iterations: int):
    for _ in range(warmup):
        func()

    elapsed_ms: list[float] = []
    last_count = 0
    for _ in range(iterations):
        start = time.perf_counter_ns()
        results = func()
        elapsed = (time.perf_counter_ns() - start) / 1_000_000
        elapsed_ms.append(elapsed)
        last_count = len(results)

    elapsed_ms.sort()
    return {
        "result_count": last_count,
        "avg_ms": statistics.fmean(elapsed_ms),
        "p50_ms": percentile(elapsed_ms, 50),
        "p95_ms": percentile(elapsed_ms, 95),
        "min_ms": elapsed_ms[0],
        "max_ms": elapsed_ms[-1],
        "runs": iterations,
    }


def build_scenarios(records):
    target = next(
        item
        for item in records
        if item.status == "found"
        and item.category == "eletronicos"
        and item.location == "biblioteca"
    )

    return [
        Scenario(
            name="key_only_block_scan",
            params={
                "status": "found",
                "category": "eletronicos",
                "location": "biblioteca",
            },
        ),
        Scenario(
            name="key_plus_barcode",
            params={
                "status": "found",
                "category": "eletronicos",
                "location": "biblioteca",
                "barcode": target.barcode,
            },
        ),
        Scenario(
            name="key_plus_name_filter",
            params={
                "status": "found",
                "category": "eletronicos",
                "location": "biblioteca",
                "name_contains": "target",
            },
        ),
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run benchmark for sequential and indexed search.")
    parser.add_argument("--csv", type=str, default="data/items_benchmark.csv")
    parser.add_argument("--mode", choices=["sequential", "indexed", "both"], default="both")
    parser.add_argument("--order-by", choices=["barcode", "found_lost_date"], default="barcode")
    parser.add_argument("--warmup", type=int, default=5)
    parser.add_argument("--iterations", type=int, default=30)
    parser.add_argument("--output", type=str, default="")
    args = parser.parse_args()

    records = load_records_from_csv(args.csv)
    scenarios = build_scenarios(records)

    started = datetime.now()
    report = {
        "benchmark": "eda2_sequential_vs_indexed",
        "started_at": started.isoformat(),
        "dataset_csv": args.csv,
        "dataset_size": len(records),
        "warmup": args.warmup,
        "iterations": args.iterations,
        "order_by": args.order_by,
        "results": [],
    }

    index_build_ms = None
    index = None
    if args.mode in {"indexed", "both"}:
        t0 = time.perf_counter_ns()
        index = build_primary_index(records, order_by=args.order_by)
        index_build_ms = (time.perf_counter_ns() - t0) / 1_000_000
        report["index_build_ms"] = index_build_ms

    for scenario in scenarios:
        if args.mode in {"sequential", "both"}:
            sequential_metrics = measure(
                lambda: sequential_search(records, **scenario.params),
                warmup=args.warmup,
                iterations=args.iterations,
            )
            report["results"].append(
                {
                    "algorithm": "sequential",
                    "scenario": scenario.name,
                    "query_params": scenario.params,
                    **sequential_metrics,
                }
            )

        if args.mode in {"indexed", "both"} and index is not None:
            indexed_metrics = measure(
                lambda: indexed_search(index, **scenario.params),
                warmup=args.warmup,
                iterations=args.iterations,
            )
            report["results"].append(
                {
                    "algorithm": "indexed",
                    "scenario": scenario.name,
                    "query_params": scenario.params,
                    **indexed_metrics,
                }
            )

    report["finished_at"] = datetime.now().isoformat()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_output = Path("results") / f"benchmark_{args.mode}_{timestamp}.json"
    output = Path(args.output) if args.output else default_output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"Benchmark finished. Report: {output}")
    if index_build_ms is not None:
        print(f"Index build: {index_build_ms:.2f} ms")


if __name__ == "__main__":
    main()
