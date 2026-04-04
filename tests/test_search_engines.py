import sys
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from eda2_indexing.index_core import build_primary_index
from eda2_indexing.models import ItemRecord
from eda2_indexing.search_engines import indexed_search, sequential_search


RECORDS = [
    ItemRecord(1, "found", "eletronicos", "biblioteca", "notebook preto", "", "01010001", "2026-01-01"),
    ItemRecord(2, "found", "eletronicos", "biblioteca", "mouse", "", "01010002", "2026-01-02"),
    ItemRecord(3, "found", "documentos", "icc", "carteira", "", "02020001", "2026-01-03"),
]


class TestSearchEngines(unittest.TestCase):
    def test_sequential_search_scans_global_records(self):
        results = sequential_search(RECORDS, name_contains="mouse")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].item_id, 2)

    def test_indexed_search_uses_composite_key_and_binary_barcode(self):
        index = build_primary_index(RECORDS, order_by="barcode")
        results = indexed_search(
            index,
            status="found",
            category="eletronicos",
            location="biblioteca",
            barcode="01010002",
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].item_id, 2)

    def test_indexed_search_fallback_filters_inside_block(self):
        index = build_primary_index(RECORDS, order_by="barcode")
        results = indexed_search(
            index,
            status="found",
            category="eletronicos",
            location="biblioteca",
            name_contains="notebook",
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].item_id, 1)


if __name__ == "__main__":
    unittest.main()
