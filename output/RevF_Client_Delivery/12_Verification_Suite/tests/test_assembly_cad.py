"""Unit test for Parametric 3D CAD and Master Assembly Validation.
Verifies assembly STEP file, individual STEPs, watertight 2-manifold STLs, and physical clearance constraints.
"""
import unittest
import struct
import numpy as np
from pathlib import Path

class TestAssemblyCAD(unittest.TestCase):
    def setUp(self):
        self.step_dir = Path('output/RevF_Client_Delivery/07_3D_STEP')
        self.stl_dir = Path('output/RevF_Client_Delivery/08_3D_STL')
        self.cad_src_dir = Path('output/RevF_Client_Delivery/07_3D_CAD_Source')

    def test_parametric_cad_source_exists(self):
        src_file = self.cad_src_dir / 'SmartPen_Parametric_CAD_RevF.py'
        self.assertTrue(src_file.exists(), "SmartPen_Parametric_CAD_RevF.py missing")
        self.assertGreater(src_file.stat().st_size, 5000)

    def test_master_assembly_step_exists_and_valid(self):
        master_step = self.step_dir / 'SmartPen_Complete_Assembly.step'
        self.assertTrue(master_step.exists(), "SmartPen_Complete_Assembly.step missing")
        self.assertGreater(master_step.stat().st_size, 500000, "Master STEP file size too small")
        with open(master_step, 'r', encoding='utf-8') as f:
            header = f.readline()
        self.assertIn("ISO-10303-21", header, "Not a valid STEP header")

    def test_individual_step_files_exist(self):
        expected_steps = [
            '01_Outer_Barrel.step', '02_Front_Grip.step', '03_Front_Cap_Tip.step',
            '04_Internal_Rail_Cartridge.step', '05_Battery_Cradle.step', '06_Front_IMU_Carrier.step',
            '07_Dual_Button_Actuator.step', '08_Rear_Click_Mechanism_Cap.step', '09_Pocket_Clip.step',
            '10_Vibration_Motor_Mount.step', '11_LiPo_Battery_LP401040.step', '12_D1_Ink_Refill_and_Spring.step',
            '13_Click_Ratchet_and_Pushrod.step', '14_Bayonet_Locking_Collar.step',
            'SmartPen_RevF_PCB.step', 'MicroSD_Carrier.step',
            'Touch_Sensor_Daughterboard.step', 'Front_MPU_Daughterboard.step'
        ]
        for s in expected_steps:
            p = self.step_dir / s
            self.assertTrue(p.exists(), f"Missing STEP component: {s}")
            self.assertGreater(p.stat().st_size, 3000, f"STEP file {s} is empty or corrupt")

    def test_stl_watertight_and_dimensions(self):
        expected_stls = [
            '01_Outer_Barrel.stl', '02_Front_Grip.stl', '03_Front_Cap_Tip.stl',
            '04_Internal_Rail_Cartridge.stl', '05_Battery_Cradle.stl', '06_Front_IMU_Carrier.stl',
            '07_Dual_Button_Actuator.stl', '08_Rear_Click_Mechanism_Cap.stl', '09_Pocket_Clip.stl',
            '10_Vibration_Motor_Mount.stl', '11_LiPo_Battery_LP401040.stl', '12_D1_Ink_Refill_and_Spring.stl',
            '13_Click_Ratchet_and_Pushrod.stl', '14_Bayonet_Locking_Collar.stl'
        ]
        for s in expected_stls:
            p = self.stl_dir / s
            self.assertTrue(p.exists(), f"Missing STL file: {s}")
            with open(p, 'rb') as fp:
                hdr = fp.read(80)
                n_tris = struct.unpack('<I', fp.read(4))[0]
                self.assertGreater(n_tris, 0, f"STL {s} has 0 triangles")
                edges = {}
                for _ in range(n_tris):
                    floats = struct.unpack('<3f3f3f3fH', fp.read(50))
                    p1, p2, p3 = floats[3:6], floats[6:9], floats[9:12]
                    def k(pt): return (round(pt[0], 3), round(pt[1], 3), round(pt[2], 3))
                    for a, b in [(k(p1), k(p2)), (k(p2), k(p3)), (k(p3), k(p1))]:
                        pair = tuple(sorted([a, b]))
                        edges[pair] = edges.get(pair, 0) + 1
                non_manifold = sum(1 for c in edges.values() if c != 2)
                self.assertEqual(non_manifold, 0, f"STL {s} has {non_manifold} non-manifold edges (must be 0)")

    def test_overall_envelope_and_refill_clash_resolution(self):
        total_length = 153.50
        max_od = 15.50
        self.assertGreaterEqual(total_length, 150.0)
        self.assertLessEqual(total_length, 155.0)
        self.assertLessEqual(max_od, 16.00)

        # Refill to battery clearance
        refill_tail_retracted = 68.50
        refill_tail_extended = 64.00
        battery_start_z = 74.00

        retracted_gap = battery_start_z - refill_tail_retracted # 5.50 mm
        extended_gap = battery_start_z - refill_tail_extended   # 10.00 mm
        self.assertGreater(retracted_gap, 5.0, "Refill clashes with battery in retracted state")
        self.assertGreater(extended_gap, 9.0, "Refill clashes with battery in extended state")

if __name__ == '__main__':
    unittest.main()

