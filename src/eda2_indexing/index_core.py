from bisect import bisect_left, bisect_right
from dataclasses import dataclass

from .models import ItemRecord

CompositeKey = tuple[str, str, str]


@dataclass(frozen=True)
class PrimarySequentialIndex:
    order_by: str
    blocks: dict[CompositeKey, list[ItemRecord]]


def _normalize(value: str | None) -> str:
    return (value or "").strip().lower()


def build_composite_key(status: str | None, category: str | None, location: str | None) -> CompositeKey:
    return (_normalize(status), _normalize(category), _normalize(location))


def build_primary_index(records: list[ItemRecord], order_by: str = "barcode") -> PrimarySequentialIndex:
    if order_by not in {"barcode", "found_lost_date"}:
        raise ValueError("order_by must be 'barcode' or 'found_lost_date'")

    blocks: dict[CompositeKey, list[ItemRecord]] = {}

    for record in records:
        key = build_composite_key(record.status, record.category, record.location)
        blocks.setdefault(key, []).append(record)

    for key, block in blocks.items():
        if order_by == "barcode":
            block.sort(key=lambda item: (item.barcode, item.found_lost_date, item.item_id))
        else:
            block.sort(key=lambda item: (item.found_lost_date, item.barcode, item.item_id))
        blocks[key] = block

    return PrimarySequentialIndex(order_by=order_by, blocks=blocks)


def _probe_value(item: ItemRecord, order_by: str) -> str:
    if order_by == "barcode":
        return item.barcode
    return item.found_lost_date


def binary_search_block(block: list[ItemRecord], target: str, order_by: str) -> list[ItemRecord]:
    if not block:
        return []

    probe = [_probe_value(item, order_by) for item in block]

    left = bisect_left(probe, target)
    right = bisect_right(probe, target)

    if left == right:
        return []
    return block[left:right]
