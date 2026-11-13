"""Unit test for Master Client Delivery Package Integrity.
Verifies all 12 deliverable directories and mandatory manufacturing outputs.
"""
import unittest
from pathlib import Path

class TestDeliveryIntegrity(unittest.TestCase):
    def setUp(self):
        self.root = Path('output/RevF_Client_Delivery')

    def test_all_12_delivery_directories_exist(self):
        expected_dirs = [
            '01_EasyEDA_Source',
            '02_KiCad_Source',
            '03_PDF_Schematic',
            '04_Gerber_Drill',
            '05_BOM_CPL',
            '06_Fabrication_Drawing',
            '07_3D_STEP',
            '08_3D_STL',
            '09_Mechanical_Drawings',
            '10_Assembly_Guide',
            '11_Reports',
            '12_Verification_Suite'
        ]
        for d in expected_dirs:
            p = self.root / d
            self.assertTrue(p.exists(), f"Delivery directory missing: {d}")
            self.assertTrue(p.is_dir(), f"Expected directory: {d}")

    def test_kicad_source_delivery_files(self):
        kicad_dir = self.root / '02_KiCad_Source'
        main_sch = kicad_dir / 'SmartPen.kicad_sch'
        main_pcb = kicad_dir / 'SmartPen.kicad_pcb'
        carrier_dir = kicad_dir / 'MicroSD_Carrier'
        carrier_sch = carrier_dir / 'MicroSD_Carrier.kicad_sch'
        carrier_pcb = carrier_dir / 'MicroSD_Carrier.kicad_pcb'
        touch_dir = kicad_dir / 'Touch_Sensor'
        touch_sch = touch_dir / 'Touch_Sensor.kicad_sch'
        touch_pcb = touch_dir / 'Touch_Sensor.kicad_pcb'
        mpu_dir = kicad_dir / 'Front_MPU'
        mpu_sch = mpu_dir / 'Front_MPU.kicad_sch'
        mpu_pcb = mpu_dir / 'Front_MPU.kicad_pcb'

        self.assertTrue(main_sch.exists(), "SmartPen.kicad_sch missing from 02_KiCad_Source")
        self.assertTrue(main_pcb.exists(), "SmartPen.kicad_pcb missing from 02_KiCad_Source")
        self.assertTrue(carrier_sch.exists(), "MicroSD_Carrier.kicad_sch missing from 02_KiCad_Source")
        self.assertTrue(carrier_pcb.exists(), "MicroSD_Carrier.kicad_pcb missing from 02_KiCad_Source")
        self.assertTrue(touch_sch.exists(), "Touch_Sensor.kicad_sch missing from 02_KiCad_Source")
        self.assertTrue(touch_pcb.exists(), "Touch_Sensor.kicad_pcb missing from 02_KiCad_Source")
        self.assertTrue(mpu_sch.exists(), "Front_MPU.kicad_sch missing from 02_KiCad_Source")
        self.assertTrue(mpu_pcb.exists(), "Front_MPU.kicad_pcb missing from 02_KiCad_Source")

    def test_gerbers_and_drills_delivery(self):
        gerber_dir = self.root / '04_Gerber_Drill'
        main_gerbers = gerber_dir / 'SmartPen_RevF_Gerbers.zip'
        carrier_gerbers = gerber_dir / 'MicroSD_Carrier_Gerbers.zip'
        touch_gerbers = gerber_dir / 'Touch_Sensor_Gerbers.zip'
        mpu_gerbers = gerber_dir / 'Front_MPU_Gerbers.zip'

        self.assertTrue(main_gerbers.exists(), "SmartPen_RevF_Gerbers.zip missing")
        self.assertTrue(carrier_gerbers.exists(), "MicroSD_Carrier_Gerbers.zip missing")
        self.assertTrue(touch_gerbers.exists(), "Touch_Sensor_Gerbers.zip missing")
        self.assertTrue(mpu_gerbers.exists(), "Front_MPU_Gerbers.zip missing")

    def test_pdf_schematics_delivery(self):
        pdf_dir = self.root / '03_PDF_Schematic'
        main_pdf = pdf_dir / 'SmartPen_RevF_Schematic.pdf'
        carrier_pdf = pdf_dir / 'MicroSD_Carrier_Schematic.pdf'
        touch_pdf = pdf_dir / 'Touch_Sensor_Schematic.pdf'
        mpu_pdf = pdf_dir / 'Front_MPU_Schematic.pdf'

        self.assertTrue(main_pdf.exists(), "SmartPen_RevF_Schematic.pdf missing")
        self.assertTrue(carrier_pdf.exists(), "MicroSD_Carrier_Schematic.pdf missing")
        self.assertTrue(touch_pdf.exists(), "Touch_Sensor_Schematic.pdf missing")
        self.assertTrue(mpu_pdf.exists(), "Front_MPU_Schematic.pdf missing")

    def test_bom_and_cpl_delivery(self):
        bom_dir = self.root / '05_BOM_CPL'
        main_bom = bom_dir / 'SmartPen_RevF_BOM.csv'
        carrier_bom = bom_dir / 'MicroSD_Carrier_BOM.csv'
        touch_bom = bom_dir / 'Touch_Sensor_BOM.csv'
        mpu_bom = bom_dir / 'Front_MPU_BOM.csv'
        main_cpl = bom_dir / 'SmartPen_RevF_CPL.csv'
        carrier_cpl = bom_dir / 'MicroSD_Carrier_CPL.csv'
        touch_cpl = bom_dir / 'Touch_Sensor_CPL.csv'
        mpu_cpl = bom_dir / 'Front_MPU_CPL.csv'

        self.assertTrue(main_bom.exists(), "SmartPen_RevF_BOM.csv missing")
        self.assertTrue(carrier_bom.exists(), "MicroSD_Carrier_BOM.csv missing")
        self.assertTrue(touch_bom.exists(), "Touch_Sensor_BOM.csv missing")
        self.assertTrue(mpu_bom.exists(), "Front_MPU_BOM.csv missing")
        self.assertTrue(main_cpl.exists(), "SmartPen_RevF_CPL.csv missing")
        self.assertTrue(carrier_cpl.exists(), "MicroSD_Carrier_CPL.csv missing")
        self.assertTrue(touch_cpl.exists(), "Touch_Sensor_CPL.csv missing")
        self.assertTrue(mpu_cpl.exists(), "Front_MPU_CPL.csv missing")

if __name__ == '__main__':
    unittest.main()

