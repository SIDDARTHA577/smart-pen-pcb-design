"""Unit tests for 3D assembly clearance and mechanical fit.
"""
import unittest
from scripts.validate_3d_assembly import validate_assembly

class TestAssemblyClearances(unittest.TestCase):
    def test_assembly_interference_and_envelope(self):
        result = validate_assembly()
        self.assertTrue(result, "All 3D assembly clearances must pass")

if __name__ == '__main__':
    unittest.main()

