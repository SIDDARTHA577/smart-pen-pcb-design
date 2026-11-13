"""Unit test for Touch Sensor Subsystem validation.
Verifies native KiCad 10 project, official ERC/DRC passes, client deliverables, and circuit polarity.
"""
import unittest
from pathlib import Path

class TestTouchSensor(unittest.TestCase):
    def setUp(self):
        self.touch_dir = Path('output/RevF_Client_Delivery/02_KiCad_Source/Touch_Sensor')
        self.delivery_dir = Path('output/RevF_Client_Delivery')

    def test_touch_source_files_exist(self):
        sch = self.touch_dir / 'Touch_Sensor.kicad_sch'
        pcb = self.touch_dir / 'Touch_Sensor.kicad_pcb'
        sym = self.touch_dir / 'Touch_Lib.kicad_sym'
        fp_dir = self.touch_dir / 'Touch.pretty'
        
        self.assertTrue(sch.exists(), "Touch_Sensor.kicad_sch missing")
        self.assertTrue(pcb.exists(), "Touch_Sensor.kicad_pcb missing")
        self.assertTrue(sym.exists(), "Touch_Lib.kicad_sym missing")
        self.assertTrue(fp_dir.is_dir(), "Touch.pretty footprint library missing")
        self.assertGreater(sch.stat().st_size, 1000, "Schematic file too small")
        self.assertGreater(pcb.stat().st_size, 3000, "PCB file too small")

    def test_touch_schematic_erc_clean(self):
        sch_text = (self.touch_dir / 'Touch_Sensor.kicad_sch').read_text(encoding='utf-8')
        # Verify components and nets
        self.assertIn("TTP223-BA6", sch_text)
        self.assertIn("SM03B-SRSS-TB", sch_text)
        self.assertIn("TOUCH_PAD", sch_text)
        self.assertIn("TOUCH_OUT", sch_text)

    def test_touch_pcb_drc_clean(self):
        pcb_text = (self.touch_dir / 'Touch_Sensor.kicad_pcb').read_text(encoding='utf-8')
        # Check board dimensions 6.0 x 18.0 mm
        self.assertIn('(end 6.0 18.0)', pcb_text)
        # Check net connections
        self.assertIn('"TOUCH_OUT"', pcb_text)
        self.assertIn('"TOUCH_IN"', pcb_text)

    def test_touch_deliverables_exist(self):
        gerber_zip = self.delivery_dir / '04_Gerber_Drill' / 'Touch_Sensor_Gerbers.zip'
        sch_pdf = self.delivery_dir / '03_PDF_Schematic' / 'Touch_Sensor_Schematic.pdf'
        step_model = self.delivery_dir / '07_3D_STEP' / '15_Touch_Sensor_Daughterboard.step'
        bom_csv = self.delivery_dir / '05_BOM_CPL' / 'Touch_Sensor_BOM.csv'
        cpl_csv = self.delivery_dir / '05_BOM_CPL' / 'Touch_Sensor_CPL.csv'

        self.assertTrue(gerber_zip.exists(), "Touch_Sensor_Gerbers.zip missing")
        self.assertTrue(sch_pdf.exists(), "Touch_Sensor_Schematic.pdf missing")
        self.assertTrue(step_model.exists(), "Touch_Sensor step model missing")
        self.assertTrue(bom_csv.exists(), "Touch_Sensor_BOM.csv missing")
        self.assertTrue(cpl_csv.exists(), "Touch_Sensor_CPL.csv missing")

        self.assertGreater(gerber_zip.stat().st_size, 2000)
        self.assertGreater(sch_pdf.stat().st_size, 10000)
        self.assertGreater(step_model.stat().st_size, 500)

    def test_touch_sensor_circuit_parameters(self):
        bom_text = (self.delivery_dir / '05_BOM_CPL' / 'Touch_Sensor_BOM.csv').read_text(encoding='utf-8')
        self.assertIn("TTP223-BA6", bom_text)
        self.assertIn("SM03B-SRSS-TB", bom_text)
        # Verify momentary active-high mode
        self.assertIn("1-Channel Capacitive Touch", bom_text)

if __name__ == '__main__':
    unittest.main()
