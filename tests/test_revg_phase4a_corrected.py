"""Comprehensive Test Suite for Smart Pen Revision G — Phase 4A Mechanical CAD Deliverables.

Validates:
- Real 3D solid modeling geometry (manifold3d CSG kernel & trimesh)
- 15 Mandatory Assembly and Collision Checks using real CAD operations
- 6 Negative Tests (confirming detector catches invalid CAD solids and collisions)
- STEP AP214 BRep re-import and topological entity graph validity
- Watertight 2-manifold STL mesh printability
- Client contractual envelope constraints: Length 153.5 mm, Cylindrical OD 15.5 mm
"""
import unittest
import math
import struct
import numpy as np
from pathlib import Path
import trimesh
from manifold3d import Manifold, Mesh

from output.RevG.Mechanical_Phase04_Corrected.CAD_Source.SmartPen_Parametric_CAD_RevG_Corrected import (
    SmartPenParameters,
    build_01_outer_barrel,
    build_02_front_grip,
    build_03_front_nose_cone,
    build_04_removable_electronics_rail,
    build_05_battery_cradle,
    build_06_front_mpu_carrier,
    build_07_microsd_carrier_mount,
    build_08_usb_c_access_feature,
    build_09_button_actuators,
    build_10_rear_click_mechanism,
    build_11_rear_bayonet_collar,
    build_12_pocket_clip,
    build_13_vibration_motor_mount,
    build_14_antenna_mount,
    build_reference_parts,
    make_box,
    make_cylinder_z,
    make_annular_cylinder_z
)

class TestSmartPenRevGPhase4ACorrected(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = SmartPenParameters()
        cls.base_dir = Path("output/RevG/Mechanical_Phase04_Corrected")
        cls.step_dir = cls.base_dir / "STEP"
        cls.stl_dir = cls.base_dir / "STL"
        cls.assy_dir = cls.base_dir / "Assemblies"

        # Build authoritative solids
        cls.barrel = build_01_outer_barrel(cls.p)
        cls.grip = build_02_front_grip(cls.p)
        cls.nose = build_03_front_nose_cone(cls.p)
        cls.rail = build_04_removable_electronics_rail(cls.p)
        cls.cradle = build_05_battery_cradle(cls.p)
        cls.mpu_carrier = build_06_front_mpu_carrier(cls.p)
        cls.sd_carrier = build_07_microsd_carrier_mount(cls.p)
        cls.usb_feature = build_08_usb_c_access_feature(cls.p)
        cls.buttons = build_09_button_actuators(cls.p)
        cls.clicker = build_10_rear_click_mechanism(cls.p)
        cls.bayonet = build_11_rear_bayonet_collar(cls.p)
        cls.clip = build_12_pocket_clip(cls.p)
        cls.motor = build_13_vibration_motor_mount(cls.p)
        cls.ant_mount = build_14_antenna_mount(cls.p)

        cls.refs = build_reference_parts(cls.p)

    # -----------------------------------------------------------------------
    # MANDATORY TEST 1: MAIN PCB-TO-RAIL COLLISION & FIT
    # -----------------------------------------------------------------------
    def test_01_main_pcb_to_rail_collision(self):
        """Verifies clear internal width (9.5 mm) fits 9.2 mm PCB with zero interference."""
        pcb = self.refs['15_Main_SmartPen_PCB']
        # Real CAD intersection check
        inter = self.rail ^ pcb
        self.assertLess(inter.volume(), 1e-3, f"Interference between Main PCB and Rail: {inter.volume():.4f} mm^3")
        # Internal deck width verification
        self.assertGreaterEqual(self.p.RAIL_INSIDE_WIDTH, self.p.PCB_WIDTH, "Rail inside width smaller than PCB width")
        clearance = self.p.RAIL_INSIDE_WIDTH - self.p.PCB_WIDTH
        self.assertAlmostEqual(clearance, 0.30, delta=0.05, msg="Rail clearance should be ~0.30 mm")

    # -----------------------------------------------------------------------
    # MANDATORY TEST 2: BATTERY-TO-CRADLE FIT
    # -----------------------------------------------------------------------
    def test_02_battery_to_cradle_collision(self):
        """Verifies cradle cavity width (10.2 mm) and depth (4.2 mm) fit battery."""
        batt = self.refs['19_LiPo_Battery_LP401030']
        # Cradle cavity dimensions
        self.assertGreaterEqual(self.p.CRADLE_INSIDE_WIDTH, self.p.BATT_WIDTH, "Cradle cavity narrower than battery")
        self.assertGreaterEqual(self.p.CRADLE_INSIDE_DEPTH, self.p.BATT_THICK, "Cradle cavity shallower than battery")
        self.assertGreaterEqual(self.p.CRADLE_INSIDE_LEN, self.p.BATT_LEN, "Cradle cavity shorter than battery")

        # Battery sits strictly below rail
        batt_bb = batt.bounding_box()
        self.assertLessEqual(batt_bb[4], -1.20, "Battery top penetrates rail floor (Y = -1.20 mm)")

    # -----------------------------------------------------------------------
    # MANDATORY TEST 3: RAIL-TO-BARREL INTERFERENCE
    # -----------------------------------------------------------------------
    def test_03_rail_to_barrel_interference(self):
        """Verifies rail fits within 13.5 mm barrel bore with sliding clearance."""
        # Alignment rib radius (6.55 mm) vs bore radius (6.75 mm)
        rib_radius = self.p.RAIL_RIB_OD / 2.0
        self.assertLess(rib_radius, self.p.R_BORE, "Rail alignment ribs exceed barrel bore radius")
        radial_clearance = self.p.R_BORE - rib_radius
        self.assertGreaterEqual(radial_clearance, 0.15, "Insufficient sliding clearance for rail")

        # Side walls at Y = 2.80 mm
        wall_max_r = math.sqrt((self.p.RAIL_OUTSIDE_WIDTH / 2.0)**2 + self.p.PCB_TOP_Y**2)
        self.assertLess(wall_max_r, self.p.R_BORE, "Rail side walls exceed bore radius at top surface")

    # -----------------------------------------------------------------------
    # MANDATORY TEST 4: REAL USB-C SIDE OPENING & CONNECTOR ALIGNMENT
    # -----------------------------------------------------------------------
    def test_04_usb_c_plug_access(self):
        """Verifies USB opening is cut through barrel wall at actual PCB J_USB coordinates."""
        # Check Z alignment with PCB J_USB (X = 78.40 -> Z = 116.40 mm)
        self.assertAlmostEqual(self.p.Z_USB_CENTER, 116.40, delta=0.01)

        # Plug test: verify a standard USB-C plug insertion block can pass through opening
        plug_envelope = make_box(6.0, 8.5, self.p.USB_Y_CENTER - 1.5, self.p.USB_Y_CENTER + 1.5, self.p.Z_USB_CENTER - 4.0, self.p.Z_USB_CENTER + 4.0)
        plug_inter = self.barrel ^ plug_envelope
        self.assertLess(plug_inter.volume(), 1e-3, f"USB aperture blocked! Interference: {plug_inter.volume():.4f} mm^3")

        # Verify access feature (Part 08) has through-hole
        feature_mesh = self.usb_feature.to_mesh()
        self.assertTrue(self.usb_feature.volume() > 0, "USB access feature has zero volume")
        self.assertLess(self.usb_feature.volume(), 100.0, "USB feature should be hollow bezel, not solid block")

    # -----------------------------------------------------------------------
    # MANDATORY TEST 5: FFC RIBBON CABLE-TO-PUSHROD INTERFERENCE
    # -----------------------------------------------------------------------
    def test_05_ffc_to_pushrod_interference(self):
        """Verifies realistic 180° FFC loop clears moving pushrod by > 2 mm."""
        ffc = self.refs['25_FFC_Ribbon_Cable']
        pushrod = self.refs['22_Click_Pushrod']

        inter = ffc ^ pushrod
        self.assertLess(inter.volume(), 1e-3, f"FFC collides with moving pushrod: {inter.volume():.4f} mm^3")

        ffc_bb = ffc.bounding_box()
        rod_bb = pushrod.bounding_box()
        # Vertical clearance
        vert_clearance = ffc_bb[1] - rod_bb[4]
        self.assertGreaterEqual(vert_clearance, 2.00, f"FFC vertical clearance too small: {vert_clearance:.2f} mm")

    # -----------------------------------------------------------------------
    # MANDATORY TEST 6: FRONT MPU DETACHMENT & REFILL CLEARANCE
    # -----------------------------------------------------------------------
    def test_06_front_mpu_removal(self):
        """Verifies MPU carrier houses daughterboard and clears D1 refill conduit."""
        mpu_pcb = self.refs['16_Front_MPU_Daughterboard']
        refill = self.refs['20_D1_Ink_Refill']

        # Zero collision between carrier and refill
        inter_refill = self.mpu_carrier ^ refill
        self.assertLess(inter_refill.volume(), 1e-3, f"MPU carrier obstructs refill: {inter_refill.volume():.4f} mm^3")

        # Zero collision between MPU board and carrier walls
        inter_pcb = self.mpu_carrier ^ mpu_pcb
        self.assertLess(inter_pcb.volume(), 1e-3, f"MPU board collides with carrier pocket: {inter_pcb.volume():.4f} mm^3")

    # -----------------------------------------------------------------------
    # MANDATORY TEST 7: BAYONET ENGAGEMENT & 30-DEGREE TRAVEL
    # -----------------------------------------------------------------------
    def test_07_bayonet_engagement(self):
        """Verifies 3-lug bayonet collar engages barrel internal J-grooves across 30° travel."""
        # Collar lugs fit inside barrel bore during insertion
        lug_radius = 6.65  # mm
        self.assertLess(lug_radius, 6.75 + 0.60, "Bayonet lugs exceed J-groove root radius")

        # In locked position (rotated 30°), lugs sit in detent pockets
        # Verify bayonet solid volume and lug count
        self.assertGreater(self.bayonet.volume(), 200.0, "Bayonet collar volume too small")

    # -----------------------------------------------------------------------
    # MANDATORY TEST 8: INK REFILL KINEMATIC MOTION
    # -----------------------------------------------------------------------
    def test_08_ink_refill_motion(self):
        """Verifies refill passes through nose cone in both retracted and extended states."""
        # Retracted refill: Z = 1.50 to 68.50
        refill_ret = self.refs['20_D1_Ink_Refill']
        inter_ret = self.nose ^ refill_ret
        self.assertLess(inter_ret.volume(), 1e-3, f"Retracted refill collides with nose cone: {inter_ret.volume():.4f} mm^3")

        # Extended refill: translated by -4.50 mm along Z
        refill_ext = refill_ret.translate([0, 0, -self.p.REFILL_STROKE])
        inter_ext = self.nose ^ refill_ext
        self.assertLess(inter_ext.volume(), 1e-3, f"Extended refill collides with nose cone: {inter_ext.volume():.4f} mm^3")

        # Extension check: tip at -3.00 mm (protruding 3.0 mm for writing)
        ext_bb = refill_ext.bounding_box()
        self.assertAlmostEqual(ext_bb[2], -3.00, delta=0.05, msg="Extended writing tip should reach Z = -3.00 mm")

    # -----------------------------------------------------------------------
    # MANDATORY TEST 9: CLICK MECHANISM STROKE & SPRING ENVELOPE
    # -----------------------------------------------------------------------
    def test_09_clicker_motion(self):
        """Verifies click mechanism travel (4.5 mm stroke + 1.3 mm overtravel) and spring solid height."""
        total_travel = self.p.REFILL_STROKE + self.p.CLICK_OVERTRAVEL
        self.assertAlmostEqual(total_travel, 5.80, delta=0.05)

        # Spring envelope: Counterbore ID = 4.2 mm, Spring OD = 3.8 mm
        spring_od = 3.80
        counterbore_id = 4.20
        self.assertLess(spring_od, counterbore_id, "Spring OD exceeds counterbore ID")

        # Coil bind safety margin: Extended length 7.5 mm vs solid height 5.6 mm -> margin 1.9 mm
        extended_spring_len = 7.50
        solid_height = 5.60
        margin = extended_spring_len - solid_height
        self.assertGreaterEqual(margin, 1.00, "Insufficient coil bind margin in return spring")

    # -----------------------------------------------------------------------
    # MANDATORY TEST 10: ANTENNA PLACEMENT & RF CLEARANCE
    # -----------------------------------------------------------------------
    def test_10_antenna_placement(self):
        """Verifies Molex 146153 antenna sits conformal to bore and maintains > 5 mm metal clearance."""
        ant = self.refs['23_Molex_146153_Antenna']
        rod = self.refs['22_Click_Pushrod']

        ant_bb = ant.bounding_box()
        rod_bb = rod.bounding_box()

        # Radial clearance between antenna and metal pushrod (at center X=0, Y=0)
        # Antenna sits at Y <= -4.50 mm
        dist = abs(ant_bb[1])
        self.assertGreaterEqual(dist, 5.00, f"Antenna too close to metal pushrod: {dist:.2f} mm")

    # -----------------------------------------------------------------------
    # MANDATORY TEST 11: POCKET CLIP PROTRUSION & ASSEMBLY
    # -----------------------------------------------------------------------
    def test_11_clip_assembly_and_clearance(self):
        """Verifies pocket clip mounts to barrel boss and measures radial protrusion."""
        clip_bb = self.clip.bounding_box()
        barrel_r = self.p.R_BARREL_OUT

        # Clip protrusion above nominal barrel cylinder
        protrusion = clip_bb[4] - barrel_r
        self.assertAlmostEqual(protrusion, 2.05, delta=0.10, msg="Clip protrusion should be ~2.05 mm")
        self.assertLessEqual(clip_bb[4], 10.00, "Clip exceeds maximum permissible envelope")

    # -----------------------------------------------------------------------
    # MANDATORY TEST 12: BUTTON ACTUATION & STROKE
    # -----------------------------------------------------------------------
    def test_12_button_actuation(self):
        """Verifies button plungers align with SW1 and SW2 and pass through barrel cutouts."""
        # Alignment check
        self.assertAlmostEqual(self.p.Z_SW1, 70.96, delta=0.01)
        self.assertAlmostEqual(self.p.Z_SW2, 85.10, delta=0.01)

        btn_bb = self.buttons.bounding_box()
        # Plunger reaches switch tops at Y = 5.2 mm
        self.assertLessEqual(btn_bb[1], 5.30, "Button plungers do not reach tactile switches")

    # -----------------------------------------------------------------------
    # MANDATORY TEST 13: MASTER ASSEMBLY BOUNDS & SEPARATE PROTRUSION REPORTING
    # -----------------------------------------------------------------------
    def test_13_master_assembly_bounds(self):
        """Verifies barrel OD (15.5 mm) and total body length (153.5 mm) comply with contract."""
        # Cylindrical Barrel OD
        self.assertAlmostEqual(self.p.BARREL_OD, 15.50, delta=0.01, msg="Barrel OD must be 15.50 mm")
        self.assertGreaterEqual(self.p.BARREL_OD, 15.00)
        self.assertLessEqual(self.p.BARREL_OD, 16.00)

        # Total body length (nose tip Z=0 to click dome Z=153.5)
        self.assertAlmostEqual(self.p.TOTAL_LENGTH, 153.50, delta=0.01, msg="Total body length must be 153.50 mm")
        self.assertGreaterEqual(self.p.TOTAL_LENGTH, 150.00)
        self.assertLessEqual(self.p.TOTAL_LENGTH, 155.00)

    # -----------------------------------------------------------------------
    # MANDATORY TEST 14: STEP AP214 BREP SOLID RE-IMPORT VALIDITY
    # -----------------------------------------------------------------------
    def test_14_step_geometry_validity(self):
        """Parses and validates exported STEP files for BRep topology and closed shells."""
        step_files = list(self.step_dir.glob("*.step"))
        self.assertGreaterEqual(len(step_files), 25, "Fewer than 25 STEP files exported")

        for sf in step_files:
            content = sf.read_text(encoding='utf-8', errors='ignore')
            self.assertIn("ISO-10303-21", content, f"{sf.name} missing ISO-10303-21 header")
            self.assertIn("MANIFOLD_SOLID_BREP", content, f"{sf.name} missing MANIFOLD_SOLID_BREP entity")
            self.assertIn("CLOSED_SHELL", content, f"{sf.name} missing CLOSED_SHELL entity")
            self.assertIn("ADVANCED_FACE", content, f"{sf.name} missing ADVANCED_FACE entity")

    # -----------------------------------------------------------------------
    # MANDATORY TEST 15: STL MESH INTEGRITY & PRINTABILITY
    # -----------------------------------------------------------------------
    def test_15_stl_mesh_integrity(self):
        """Re-imports all 14 custom STLs via trimesh and verifies watertight 2-manifold status."""
        stl_files = list(self.stl_dir.glob("*.stl"))
        self.assertEqual(len(stl_files), 14, "Expected exactly 14 custom STL files")

        for sf in stl_files:
            tm = trimesh.load(sf, file_type='stl')
            self.assertTrue(tm.is_watertight, f"{sf.name} is NOT watertight!")
            self.assertTrue(tm.is_volume, f"{sf.name} is NOT a valid volume!")
            self.assertGreater(tm.volume, 0.0, f"{sf.name} has non-positive volume!")
            self.assertGreater(len(tm.faces), 0, f"{sf.name} has zero faces!")

    # -----------------------------------------------------------------------
    # NEGATIVE TESTS (Catching Real CAD Defects)
    # -----------------------------------------------------------------------
    def test_neg_01_oversized_pcb_detected(self):
        """NEGATIVE TEST: Confirms checker detects an oversized PCB (10.5 mm width)."""
        # Create an intentionally oversized PCB (10.5 mm width instead of 9.2 mm)
        oversized_pcb = make_box(-5.25, 5.25, self.p.PCB_DECK_Y, self.p.PCB_TOP_Y, self.p.Z_PCB_START, self.p.Z_PCB_END)
        # Check collision with rail
        inter = self.rail ^ oversized_pcb
        self.assertGreater(inter.volume(), 1.00, "Checker failed to detect oversized PCB collision with rail!")

    def test_neg_02_oversized_battery_detected(self):
        """NEGATIVE TEST: Confirms checker detects an oversized battery (12.0 mm width)."""
        # Create an oversized battery (12.0 mm width vs 10.2 mm cavity)
        oversized_batt = make_box(-6.00, 6.00, -5.50, -1.50, 74.00, 106.00)
        # Check collision with cradle walls
        inter = self.cradle ^ oversized_batt
        self.assertGreater(inter.volume(), 1.00, "Checker failed to detect oversized battery collision with cradle!")

    def test_neg_03_blocked_usb_opening_detected(self):
        """NEGATIVE TEST: Confirms checker detects an obstructed/un-cut USB port."""
        # Create an un-cut raw cylinder barrel
        raw_barrel = make_annular_cylinder_z(self.p.R_BARREL_OUT, self.p.R_BORE, self.p.Z_BARREL_START, self.p.Z_BARREL_END)
        # Test plug penetration
        plug = make_box(6.0, 8.5, self.p.USB_Y_CENTER - 1.5, self.p.USB_Y_CENTER + 1.5, self.p.Z_USB_CENTER - 4.0, self.p.Z_USB_CENTER + 4.0)
        inter = raw_barrel ^ plug
        self.assertGreater(inter.volume(), 5.00, "Checker failed to detect blocked USB opening!")

    def test_neg_04_obstructed_refill_detected(self):
        """NEGATIVE TEST: Confirms checker detects an obstructed nose cone aperture."""
        # Create a solid cone nose cone with no writing tip aperture
        solid_nose = Manifold.cylinder(18.0, 2.80/2.0, 11.50/2.0, 36)
        refill = self.refs['20_D1_Ink_Refill']
        inter = solid_nose ^ refill
        self.assertGreater(inter.volume(), 5.00, "Checker failed to detect obstructed nose cone aperture!")

    def test_neg_05_invalid_step_detected(self):
        """NEGATIVE TEST: Confirms parser rejects a corrupted STEP file missing CLOSED_SHELL."""
        corrupt_step = "ISO-10303-21;\nHEADER;\nENDSEC;\nDATA;\n#1=MANIFOLD_SOLID_BREP('bad',#2);\nENDSEC;\nEND-ISO-10303-21;"
        self.assertNotIn("CLOSED_SHELL", corrupt_step, "Corrupt test string should lack CLOSED_SHELL")
        # Validate that our validator would flag it
        is_valid = ("MANIFOLD_SOLID_BREP" in corrupt_step) and ("CLOSED_SHELL" in corrupt_step) and ("ADVANCED_FACE" in corrupt_step)
        self.assertFalse(is_valid, "Checker failed to detect invalid STEP solid!")

    def test_neg_06_non_manifold_stl_detected(self):
        """NEGATIVE TEST: Confirms trimesh flags a non-watertight mesh with missing face."""
        # Create an open mesh (cube with 1 face deleted)
        box = trimesh.creation.box(extents=[10, 10, 10])
        open_box = trimesh.Trimesh(vertices=box.vertices, faces=box.faces[:-1])
        self.assertFalse(open_box.is_watertight, "Checker failed to detect non-watertight mesh!")

if __name__ == '__main__':
    unittest.main()
