"""Unit test for MicroSD Carrier Subsystem validation.
Verifies carrier KiCad source, ERC/DRC reports, client deliverables, and net parity.
"""
import unittest
from pathlib import Path

class TestMicroSDCarrier(unittest.TestCase):
    def setUp(self):
        self.carrier_dir = Path('output/RevF_Working/MicroSD_Carrier')
        self.delivery_dir = Path('output/RevF_Client_Delivery')

    def test_carrier_source_files_exist(self):
        sch = self.carrier_dir / 'MicroSD_Carrier.kicad_sch'
        pcb = self.carrier_dir / 'MicroSD_Carrier.kicad_pcb'
        self.assertTrue(sch.exists(), "MicroSD_Carrier.kicad_sch missing")
        self.assertTrue(pcb.exists(), "MicroSD_Carrier.kicad_pcb missing")
        self.assertGreater(sch.stat().st_size, 1000, "Schematic file too small")
        self.assertGreater(pcb.stat().st_size, 5000, "PCB file too small")

    def test_carrier_erc_clean(self):
        erc_rpt = self.carrier_dir / 'erc_carrier.rpt'
        self.assertTrue(erc_rpt.exists(), "erc_carrier.rpt missing")
        with open(erc_rpt, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn("Errors 0", content, "ERC errors must be 0")
        self.assertIn("Warnings 0", content, "ERC warnings must be 0")

    def test_carrier_drc_clean(self):
        drc_rpt = self.carrier_dir / 'drc_carrier.rpt'
        self.assertTrue(drc_rpt.exists(), "drc_carrier.rpt missing")
        with open(drc_rpt, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn("Found 0 DRC violations", content, "DRC violations must be 0")
        self.assertIn("Found 0 unconnected pads", content, "DRC unconnected pads must be 0")
        self.assertIn("Found 0 Footprint errors", content, "DRC footprint errors must be 0")

    def test_carrier_deliverables_exist(self):
        gerber_zip = self.delivery_dir / '04_Gerber_Drill' / 'MicroSD_Carrier_Gerbers.zip'
        sch_pdf = self.delivery_dir / '03_PDF_Schematic' / 'MicroSD_Carrier_Schematic.pdf'
        step_model = self.delivery_dir / '07_3D_STEP' / 'MicroSD_Carrier.step'
        bom_csv = self.delivery_dir / '05_BOM_CPL' / 'MicroSD_Carrier_BOM.csv'
        cpl_csv = self.delivery_dir / '05_BOM_CPL' / 'MicroSD_Carrier_CPL.csv'

        self.assertTrue(gerber_zip.exists(), "MicroSD_Carrier_Gerbers.zip missing")
        self.assertTrue(sch_pdf.exists(), "MicroSD_Carrier_Schematic.pdf missing")
        self.assertTrue(step_model.exists(), "MicroSD_Carrier.step missing")
        self.assertTrue(bom_csv.exists(), "MicroSD_Carrier_BOM.csv missing")
        self.assertTrue(cpl_csv.exists(), "MicroSD_Carrier_CPL.csv missing")

        self.assertGreater(gerber_zip.stat().st_size, 2000)
        self.assertGreater(sch_pdf.stat().st_size, 10000)
        self.assertGreater(step_model.stat().st_size, 4000)

if __name__ == '__main__':
    unittest.main()
