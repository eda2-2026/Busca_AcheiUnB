import csv
from pathlib import Path

from .models import ItemRecord

CSV_FIELDS = [
    "item_id",
    "status",
    "category",
    "location",
    "name",
    "description",
    "barcode",
    "found_lost_date",
]


def load_records_from_csv(path: str | Path) -> list[ItemRecord]:
    file_path = Path(path)
    records: list[ItemRecord] = []

    with file_path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            records.append(
                ItemRecord(
                    item_id=int(row["item_id"]),
                    status=row["status"],
                    category=row["category"],
                    location=row["location"],
                    name=row["name"],
                    description=row["description"],
                    barcode=row["barcode"],
                    found_lost_date=row["found_lost_date"],
                )
            )

    return records


def write_records_to_csv(path: str | Path, records: list[ItemRecord]) -> None:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for record in records:
            writer.writerow(
                {
                    "item_id": record.item_id,
                    "status": record.status,
                    "category": record.category,
                    "location": record.location,
                    "name": record.name,
                    "description": record.description,
                    "barcode": record.barcode,
                    "found_lost_date": record.found_lost_date,
                }
            )
