"""Unit tests for Gerber and Excellon drill manufacturing export and KiCad PCB parity.
"""
import unittest
from pathlib import Path
from scripts.validate_gerbers import validate_gerbers
from scripts.compare_kicad_pcb_gerbers import compare_kicad_and_gerbers

class TestGerberExport(unittest.TestCase):
    def setUp(self):
        self.gerber_dir = Path('output/client_delivery/04_Gerber_Drill')

    def test_gerber_layers_and_dimensions(self):
        res = validate_gerbers(self.gerber_dir)
        for ext in ['GTL', 'GBL', 'GTS', 'GBS', 'GTO', 'GBO', 'GKO', 'DRL']:
            self.assertIn(ext, res)
            self.assertEqual(res[ext]['status'], 'PASS', f"Layer {ext} must pass validation")

        gko_info = res['GKO']
        self.assertAlmostEqual(gko_info['length_mm'], 84.0, delta=0.2)
        self.assertAlmostEqual(gko_info['width_mm'], 9.2, delta=0.2)

        drl_info = res['DRL']
        self.assertGreaterEqual(drl_info['hole_count'], 20)

    def test_kicad_pcb_to_gerber_parity(self):
        # Must execute without assertions failing
        compare_kicad_and_gerbers()

if __name__ == '__main__':
    unittest.main()
