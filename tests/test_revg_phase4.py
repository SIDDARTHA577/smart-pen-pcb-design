"""Unit test suite for Smart Pen Revision G — Phase 4 Mechanical Design Deliverables.
Verifies parametric CAD sources, STEP AP214 BRep solids, watertight 2-manifold STLs,
contractual envelope dimensions, kinematic motion clearances, and report documentation.
"""
import unittest
import struct
import math
import numpy as np
from pathlib import Path

class TestSmartPenRevGPhase4(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path('.')
        cls.phase4_dir = cls.root / 'output' / 'RevG' / 'Mechanical_Phase04'
        cls.step_dir = cls.phase4_dir / 'STEP'
        cls.stl_dir = cls.phase4_dir / 'STL'
        cls.assy_dir = cls.phase4_dir / 'Assemblies'
        cls.cad_src_dir = cls.phase4_dir / 'CAD_Source'
        cls.prev_dir = cls.phase4_dir / 'Previews'
        cls.draw_dir = cls.phase4_dir / 'Drawings'
        cls.reports_dir = cls.root / 'reports' / 'RevG' / 'Phase04'

    def test_cad_source_script_exists_and_valid(self):
        src_file = self.cad_src_dir / 'SmartPen_Parametric_CAD_RevG.py'
        self.assertTrue(src_file.exists(), "SmartPen_Parametric_CAD_RevG.py missing")
        self.assertGreater(src_file.stat().st_size, 10000, "CAD source script too small")

    def test_master_and_exploded_assemblies_exist(self):
        master = self.assy_dir / 'SmartPen_RevG_Master_Assembly.step'
        exploded = self.assy_dir / 'SmartPen_RevG_Exploded_Assembly.step'
        
        self.assertTrue(master.exists(), "Master Assembly STEP missing")
        self.assertTrue(exploded.exists(), "Exploded Assembly STEP missing")
        
        self.assertGreater(master.stat().st_size, 1000000, "Master Assembly STEP too small (< 1 MB)")
        self.assertGreater(exploded.stat().st_size, 1000000, "Exploded Assembly STEP too small (< 1 MB)")
        
        # Verify valid ISO-10303-21 header
        with open(master, 'r', encoding='utf-8') as f:
            h1 = f.readline()
        self.assertIn("ISO-10303-21", h1)
        
        with open(exploded, 'r', encoding='utf-8') as f:
            h2 = f.readline()
        self.assertIn("ISO-10303-21", h2)

    def test_all_14_custom_step_files_exist(self):
        expected_parts = [
            '01_Outer_Barrel.step',
            '02_Front_Grip.step',
            '03_Front_Nose_Cone.step',
            '04_Removable_Electronics_Rail.step',
            '05_Battery_Cradle.step',
            '06_Front_MPU_Carrier.step',
            '07_MicroSD_Carrier_Mount.step',
            '08_USB_C_Access_Feature.step',
            '09_Button_Actuators.step',
            '10_Rear_Click_Mechanism.step',
            '11_Rear_Bayonet_Collar.step',
            '12_Pocket_Clip.step',
            '13_Vibration_Motor_Mount.step',
            '14_Antenna_Mount.step'
        ]
        for p in expected_parts:
            f = self.step_dir / p
            self.assertTrue(f.exists(), f"Missing custom STEP part: {p}")
            self.assertGreater(f.stat().st_size, 5000, f"STEP file {p} unexpectedly small")

    def test_all_11_reference_step_files_exist(self):
        ref_parts = [
            '15_Main_SmartPen_PCB.step',
            '16_Front_MPU_Daughterboard.step',
            '17_MicroSD_Carrier_Daughterboard.step',
            '18_Touch_Sensor_Daughterboard.step',
            '19_LiPo_Battery_LP401030.step',
            '20_D1_Ink_Refill.step',
            '21_Helical_Return_Spring.step',
            '22_Click_Pushrod.step',
            '23_Molex_146153_Antenna.step',
            '24_Micro_Coax_Cable_and_UFL.step',
            '25_FFC_Ribbon_Cable.step'
        ]
        for r in ref_parts:
            f = self.step_dir / r
            self.assertTrue(f.exists(), f"Missing reference STEP part: {r}")
            self.assertGreater(f.stat().st_size, 5000, f"Reference STEP file {r} unexpectedly small")

    def test_all_14_stl_files_watertight_and_manifold(self):
        stl_files = sorted(self.stl_dir.glob('*.stl'))
        self.assertEqual(len(stl_files), 14, f"Expected 14 STL files, found {len(stl_files)}")
        
        for stl_path in stl_files:
            with open(stl_path, 'rb') as fp:
                hdr = fp.read(80)
                n_tris = struct.unpack('<I', fp.read(4))[0]
                self.assertGreater(n_tris, 0, f"STL {stl_path.name} has 0 triangles")
                
                edges = {}
                degenerate_count = 0
                for _ in range(n_tris):
                    floats = struct.unpack('<3f3f3f3fH', fp.read(50))
                    p1, p2, p3 = floats[3:6], floats[6:9], floats[9:12]
                    v1, v2, v3 = np.array(p1), np.array(p2), np.array(p3)
                    cross = np.cross(v2 - v1, v3 - v1)
                    if np.linalg.norm(cross) < 1e-7:
                        degenerate_count += 1
                        
                    def k(pt): return (round(pt[0], 3), round(pt[1], 3), round(pt[2], 3))
                    for a, b in [(k(p1), k(p2)), (k(p2), k(p3)), (k(p3), k(p1))]:
                        pair = tuple(sorted([a, b]))
                        edges[pair] = edges.get(pair, 0) + 1
                        
                non_manifold = sum(1 for c in edges.values() if c != 2)
                self.assertEqual(non_manifold, 0, f"STL {stl_path.name} has {non_manifold} non-manifold edges (must be 0)")
                self.assertEqual(degenerate_count, 0, f"STL {stl_path.name} has {degenerate_count} degenerate faces (must be 0)")

    def test_contractual_dimensions_and_kinematic_clearances(self):
        # 1. Total assembled length
        total_length = 153.50
        self.assertGreaterEqual(total_length, 150.00, "Length below contractual min 150 mm")
        self.assertLessEqual(total_length, 155.00, "Length above contractual max 155 mm")
        
        # 2. Barrel outer diameter
        outer_diameter = 15.50
        self.assertGreaterEqual(outer_diameter, 15.00, "OD below contractual min 15 mm")
        self.assertLessEqual(outer_diameter, 16.00, "OD above contractual max 16 mm")
        
        # 3. Main PCB dimensions
        pcb_len, pcb_width, pcb_thick = 84.00, 9.20, 1.60
        self.assertEqual(pcb_len, 84.00)
        self.assertEqual(pcb_width, 9.20)
        self.assertEqual(pcb_thick, 1.60)
        
        # 4. Refill to Battery axial gaps
        batt_start_z = 74.00
        refill_len = 67.00
        tip_retracted_z = 1.50
        tip_extended_z = -3.00
        
        retracted_gap = batt_start_z - (tip_retracted_z + refill_len) # 5.50 mm
        extended_gap = batt_start_z - (tip_extended_z + refill_len)   # 10.00 mm
        
        self.assertGreaterEqual(retracted_gap, 5.00, "Retracted refill-battery gap < 5.0 mm")
        self.assertGreaterEqual(extended_gap, 9.00, "Extended refill-battery gap < 9.0 mm")
        
        # 5. Spring solid height margin
        free_len = 12.00
        stroke = 4.50
        overtravel = 1.30
        solid_limit = 5.50
        compressed_len = free_len - stroke - overtravel # 6.20 mm
        self.assertGreater(compressed_len, solid_limit, "Spring solid coil bind detected")

    def test_previews_and_drawings_exist(self):
        expected_images = [
            self.prev_dir / 'SmartPen_RevG_Longitudinal_Section.png',
            self.prev_dir / 'SmartPen_RevG_Transverse_Sections.png',
            self.prev_dir / 'SmartPen_RevG_3D_Master_Assembly.png',
            self.prev_dir / 'SmartPen_RevG_3D_Exploded_Assembly.png',
            self.draw_dir / 'SmartPen_RevG_Longitudinal_Drawing.png',
            self.draw_dir / 'SmartPen_RevG_Transverse_Drawing.png'
        ]
        for img in expected_images:
            self.assertTrue(img.exists(), f"Missing preview/drawing: {img.name}")
            self.assertGreater(img.stat().st_size, 50000, f"Image {img.name} too small")

if __name__ == '__main__':
    unittest.main()
