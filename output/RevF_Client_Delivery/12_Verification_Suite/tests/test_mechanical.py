"""Unit tests for Smart Pen Rev E mechanical enclosure STL models.
"""
import unittest
from pathlib import Path
from scripts.validate_mechanical import validate_mesh

class TestMechanicalEnclosure(unittest.TestCase):
    def setUp(self):
        self.stl_dir = Path('output/RevE_work/3D_STL')
        self.stl_files = sorted(self.stl_dir.glob('*.stl'))

    def test_stl_files_exist(self):
        self.assertGreaterEqual(len(self.stl_files), 10, "Must contain all 10 STL components")

    def test_all_meshes_watertight_and_manifold(self):
        for stl_path in self.stl_files:
            res = validate_mesh(stl_path)
            self.assertEqual(res['status'], 'PASS', f"Mesh {stl_path.name} must be PASS")
            self.assertTrue(res['watertight'], f"Mesh {stl_path.name} must be watertight")
            self.assertEqual(res['non_manifold_edges'], 0, f"Mesh {stl_path.name} must have 0 non-manifold edges")
            self.assertEqual(res['degenerate_faces'], 0, f"Mesh {stl_path.name} must have 0 degenerate faces")
            self.assertGreater(res['volume_mm3'], 0.0, f"Mesh {stl_path.name} must have positive volume")

    def test_pen_outer_diameter_constraint(self):
        barrel = validate_mesh(self.stl_dir / '01_Outer_Barrel.stl')
        dims = barrel['bounding_box_mm']['dims']
        max_d = max(dims[0], dims[1])
        self.assertLessEqual(max_d, 16.0, "Maximum outer diameter must not exceed 16.0 mm")

if __name__ == '__main__':
    unittest.main()

