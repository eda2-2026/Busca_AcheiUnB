from dataclasses import dataclass


@dataclass(frozen=True)
class ItemRecord:
    item_id: int
    status: str
    category: str
    location: str
    name: str
    description: str
    barcode: str
    found_lost_date: str
