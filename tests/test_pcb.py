"""Unit tests for Smart Pen Rev E PCB design.
"""
import json
import unittest
from pathlib import Path

class TestPCBDesign(unittest.TestCase):
    def setUp(self):
        self.pcb_path = Path('output/RevE_work/SmartPen_RevE_PCB.json')
        self.assertTrue(self.pcb_path.exists(), "PCB JSON file must exist")
        with open(self.pcb_path, 'r', encoding='utf-8') as f:
            self.pcb = json.load(f)

    def test_pcb_metadata(self):
        head = self.pcb.get('head', {})
        self.assertEqual(str(head.get('docType')), '3', "Document type must be PCB (3)")

    def test_pcb_components_count(self):
        lib_parts = [s for s in self.pcb.get('shape', []) if isinstance(s, str) and s.startswith('LIB~')]
        self.assertEqual(len(lib_parts), 60, "All 60 components must be placed on the PCB")

    def test_board_outline_dimensions(self):
        outline_found = False
        length_mm = 0.0
        width_mm = 0.0
        for item in self.pcb.get('shape', []):
            if isinstance(item, str) and item.startswith('TRACK~'):
                toks = item.split('~')
                if toks[2] == '10': # Board outline layer
                    coords = [float(c) for c in toks[4].split()]
                    xs = [(coords[i] - 4000.0) * 0.254 for i in range(0, len(coords)-1, 2)]
                    ys = [(coords[i+1] - 3000.0) * 0.254 for i in range(0, len(coords)-1, 2)]
                    length_mm = max(xs) - min(xs)
                    width_mm = max(ys) - min(ys)
                    outline_found = True
                    break

        self.assertTrue(outline_found, "Board outline track must be present on layer 10")
        self.assertAlmostEqual(length_mm, 84.0, delta=0.2, msg="Board length must be 84.0 mm")
        self.assertAlmostEqual(width_mm, 9.2, delta=0.2, msg="Board width must be 9.2 mm")

    def test_copper_ground_zones(self):
        ca_count = sum(1 for s in self.pcb.get('shape', []) if isinstance(s, str) and s.startswith('COPPERAREA~'))
        self.assertGreaterEqual(ca_count, 2, "Must contain Top and Bottom ground planes (COPPERAREA)")

if __name__ == '__main__':
    unittest.main()

