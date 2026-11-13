"""Unit tests for Smart Pen Rev E schematic design.
"""
import json
import unittest
from pathlib import Path

class TestSchematicDesign(unittest.TestCase):
    def setUp(self):
        self.sch_path = Path('output/RevE_work/SmartPen_RevE_Schematic.json')
        self.assertTrue(self.sch_path.exists(), "Schematic JSON file must exist")
        with open(self.sch_path, 'r', encoding='utf-8') as f:
            self.sch = json.load(f)

    def test_document_metadata(self):
        head = self.sch.get('head', {})
        self.assertEqual(str(head.get('docType')), '1', "Document type must be schematic (1)")
        self.assertEqual(head.get('c_para', {}).get('Revision'), 'Rev E')

    def test_component_count(self):
        lib_parts = [s for s in self.sch.get('shape', []) if isinstance(s, str) and s.startswith('LIB~')]
        self.assertEqual(len(lib_parts), 60, "Must contain exactly 60 components")

    def test_no_tbd_placeholders(self):
        for item in self.sch.get('shape', []):
            if isinstance(item, str) and item.startswith('LIB~'):
                self.assertNotIn('_TBD', item, "No component should have _TBD placeholder footprint")
                self.assertNotIn('TBD', item, "No component should have TBD metadata")

    def test_esp32_c3_core_pins(self):
        u1_part = None
        for item in self.sch.get('shape', []):
            if isinstance(item, str) and item.startswith('LIB~') and 'ESP32-C3' in item:
                u1_part = item
                break
        self.assertIsNotNone(u1_part, "ESP32-C3 component U1 must be present")
        subs = u1_part.split('#@$')
        pins = [s for s in subs if s.startswith('P~')]
        self.assertGreaterEqual(len(pins), 32, "ESP32-C3 must have at least 32 pins defined")

if __name__ == '__main__':
    unittest.main()

