import argparse
import random
from datetime import date, timedelta

from eda2_indexing.csv_io import write_records_to_csv
from eda2_indexing.models import ItemRecord

CATEGORIES = [
    "acessorios",
    "eletronicos",
    "documentos",
    "roupas",
    "mochilas",
    "garrafas",
]
LOCATIONS = ["biblioteca", "icc", "ru", "fga", "ft", "beijodromo"]
STATUSES = ["found", "lost"]


def build_barcode(category_idx: int, location_idx: int, item_idx: int) -> str:
    return f"{category_idx:02d}{location_idx:02d}{item_idx % 10000:04d}"


def generate_records(rows: int, seed: int) -> list[ItemRecord]:
    random.seed(seed)
    start_date = date(2026, 1, 1)

    target_category = "eletronicos"
    target_location = "biblioteca"

    records: list[ItemRecord] = []
    for i in range(rows):
        if i % 5 == 0:
            status = "found"
            category = target_category
            location = target_location
            name = f"item_target_{i:05d}"
            description = "item alvo para benchmark"
        else:
            status = random.choice(STATUSES)
            category = random.choice(CATEGORIES)
            location = random.choice(LOCATIONS)
            name = f"item_random_{i:05d}"
            description = "item aleatorio"

        category_idx = CATEGORIES.index(category) if category in CATEGORIES else 99
        location_idx = LOCATIONS.index(location) if location in LOCATIONS else 99

        records.append(
            ItemRecord(
                item_id=i + 1,
                status=status,
                category=category,
                location=location,
                name=name,
                description=description,
                barcode=build_barcode(category_idx, location_idx, i + 1),
                found_lost_date=(start_date + timedelta(days=(i % 90))).isoformat(),
            )
        )

    return records


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate benchmark CSV dataset.")
    parser.add_argument("--rows", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=str, default="data/items_benchmark.csv")
    args = parser.parse_args()

    records = generate_records(rows=args.rows, seed=args.seed)
    write_records_to_csv(args.output, records)
    print(f"Dataset generated: {args.output} ({len(records)} rows)")


if __name__ == "__main__":
    main()
