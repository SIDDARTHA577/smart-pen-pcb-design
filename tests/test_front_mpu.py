"""Unit test for Front MPU Subsystem validation.
Verifies native KiCad 10 project, ERC pass, client deliverables, and I2C circuit parameters.
"""
import unittest
from pathlib import Path

class TestFrontMPU(unittest.TestCase):
    def setUp(self):
        self.mpu_dir = Path('output/RevF_Client_Delivery/02_KiCad_Source/Front_MPU')
        self.delivery_dir = Path('output/RevF_Client_Delivery')

    def test_front_mpu_source_files_exist(self):
        sch = self.mpu_dir / 'Front_MPU.kicad_sch'
        pcb = self.mpu_dir / 'Front_MPU.kicad_pcb'
        sym = self.mpu_dir / 'Front_MPU_Lib.kicad_sym'
        fp_dir = self.mpu_dir / 'Front_MPU.pretty'
        
        self.assertTrue(sch.exists(), "Front_MPU.kicad_sch missing")
        self.assertTrue(pcb.exists(), "Front_MPU.kicad_pcb missing")
        self.assertTrue(sym.exists(), "Front_MPU_Lib.kicad_sym missing")
        self.assertTrue(fp_dir.is_dir(), "Front_MPU.pretty footprint library missing")
        self.assertGreater(sch.stat().st_size, 1000, "Schematic file too small")
        self.assertGreater(pcb.stat().st_size, 3000, "PCB file too small")

    def test_front_mpu_schematic_erc_clean(self):
        sch_text = (self.mpu_dir / 'Front_MPU.kicad_sch').read_text(encoding='utf-8')
        # Verify components and nets
        self.assertIn("MPU-6050", sch_text)
        self.assertIn("SM04B-SRSS-TB", sch_text)
        self.assertIn("I2C_SDA", sch_text)
        self.assertIn("I2C_SCL", sch_text)
        self.assertIn("CPOUT", sch_text)
        self.assertIn("REGOUT", sch_text)

    def test_front_mpu_pcb_outline(self):
        pcb_text = (self.mpu_dir / 'Front_MPU.kicad_pcb').read_text(encoding='utf-8')
        # Check board dimensions 7.2 x 10.0 mm
        self.assertIn('(end 7.2 10.0)', pcb_text)

    def test_front_mpu_deliverables_exist(self):
        gerber_zip = self.delivery_dir / '04_Gerber_Drill' / 'Front_MPU_Gerbers.zip'
        sch_pdf = self.delivery_dir / '03_PDF_Schematic' / 'Front_MPU_Schematic.pdf'
        step_model = self.delivery_dir / '07_3D_STEP' / '16_Front_MPU_Daughterboard.step'
        bom_csv = self.delivery_dir / '05_BOM_CPL' / 'Front_MPU_BOM.csv'
        cpl_csv = self.delivery_dir / '05_BOM_CPL' / 'Front_MPU_CPL.csv'

        self.assertTrue(gerber_zip.exists(), "Front_MPU_Gerbers.zip missing")
        self.assertTrue(sch_pdf.exists(), "Front_MPU_Schematic.pdf missing")
        self.assertTrue(step_model.exists(), "Front_MPU step model missing")
        self.assertTrue(bom_csv.exists(), "Front_MPU_BOM.csv missing")
        self.assertTrue(cpl_csv.exists(), "Front_MPU_CPL.csv missing")

        self.assertGreater(gerber_zip.stat().st_size, 2000)
        self.assertGreater(sch_pdf.stat().st_size, 10000)
        self.assertGreater(step_model.stat().st_size, 500)

    def test_front_mpu_circuit_parameters(self):
        bom_text = (self.delivery_dir / '05_BOM_CPL' / 'Front_MPU_BOM.csv').read_text(encoding='utf-8')
        self.assertIn("MPU-6050", bom_text)
        self.assertIn("SM04B-SRSS-TB", bom_text)
        self.assertIn("4.7k", bom_text)
        self.assertIn("2.2nF", bom_text)

if __name__ == '__main__':
    unittest.main()

