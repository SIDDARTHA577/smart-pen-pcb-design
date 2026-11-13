"""Unit tests for Smart Pen Rev E netlist and pin-to-pad electrical parity.
"""
import json
import unittest
from pathlib import Path

class TestNetlistParity(unittest.TestCase):
    def setUp(self):
        with open('output/RevE_work/SmartPen_RevE_Schematic.json', 'r', encoding='utf-8') as f:
            self.sch = json.load(f)
        with open('output/RevE_work/SmartPen_RevE_PCB.json', 'r', encoding='utf-8') as f:
            self.pcb = json.load(f)

    def test_component_parity(self):
        sch_refs = set()
        for item in self.sch.get('shape', []):
            if isinstance(item, str) and item.startswith('LIB~'):
                subs = item.split('#@$')
                for sub in subs:
                    if sub.startswith('T~'):
                        t = sub.split('~')
                        if len(t) >= 13 and t[1] == 'P':
                            sch_refs.add(t[12] if t[11] == 'comment' else t[11])

        pcb_refs = set()
        for item in self.pcb.get('shape', []):
            if isinstance(item, str) and item.startswith('LIB~'):
                subs = item.split('#@$')
                for sub in subs:
                    if sub.startswith('TEXT~P~'):
                        pcb_refs.add(sub.split('~')[10])

        self.assertEqual(len(sch_refs), 60)
        self.assertEqual(len(pcb_refs), 60)
        self.assertEqual(sch_refs, pcb_refs, "Schematic and PCB component sets must match exactly")

    def test_net_continuity(self):
        nets = set()
        for item in self.pcb.get('shape', []):
            if isinstance(item, str) and item.startswith('LIB~'):
                subs = item.split('#@$')
                for sub in subs:
                    if sub.startswith('PAD~'):
                        ptoks = sub.split('~')
                        if len(ptoks) > 7 and ptoks[7]:
                            nets.add(ptoks[7])

        # Essential nets that must exist
        essential = ['3V3', 'GND', 'VBAT', 'VBAT_SW', 'USB_VBUS', 'I2C_SDA', 'I2C_SCL', 'SD_SCK', 'RF_LNA', 'RF_OUT']
        for net in essential:
            self.assertIn(net, nets, f"Essential electrical net {net} must exist on PCB")

if __name__ == '__main__':
    unittest.main()

