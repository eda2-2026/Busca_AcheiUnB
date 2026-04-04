import sys
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from eda2_indexing.index_core import binary_search_block, build_composite_key, build_primary_index
from eda2_indexing.models import ItemRecord


def sample_records():
    return [
        ItemRecord(1, "found", "eletronicos", "biblioteca", "a", "", "01010001", "2026-01-01"),
        ItemRecord(2, "found", "eletronicos", "biblioteca", "b", "", "01010003", "2026-01-03"),
        ItemRecord(3, "found", "eletronicos", "biblioteca", "c", "", "01010002", "2026-01-02"),
        ItemRecord(4, "lost", "documentos", "icc", "d", "", "02020001", "2026-01-04"),
    ]


class TestIndexCore(unittest.TestCase):
    def test_build_composite_key_normalizes_values(self):
        self.assertEqual(
            build_composite_key(" Found ", " Eletronicos ", " Biblioteca "),
            ("found", "eletronicos", "biblioteca"),
        )

    def test_build_primary_index_groups_and_sorts_by_barcode(self):
        index = build_primary_index(sample_records(), order_by="barcode")
        block = index.blocks[("found", "eletronicos", "biblioteca")]
        self.assertEqual(
            [item.barcode for item in block],
            ["01010001", "01010002", "01010003"],
        )

    def test_binary_search_block_finds_exact_barcode(self):
        index = build_primary_index(sample_records(), order_by="barcode")
        block = index.blocks[("found", "eletronicos", "biblioteca")]
        found = binary_search_block(block, "01010002", order_by="barcode")
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].item_id, 3)


if __name__ == "__main__":
    unittest.main()
