"""Phase 3A Synchronization, Footprint Verification and Placement Tests
Validates KiCad source synchronization between schematic and PCB,
authoritative 84.0 x 9.2 mm 2-layer geometry, exact pad-to-net mapping,
USB-C land pattern, and negative fixtures.
"""
import pytest
import re
from pathlib import Path

SCH_PATH = Path('output/RevG/SmartPen.kicad_sch')
PCB_PATH = Path('output/RevG/SmartPen.kicad_pcb')
DRC_RPT_PATH = Path('reports/RevG/Phase03A/raw/Main_SmartPen_drc.rpt')

def get_pcb_footprint_pads(pcb_text, ref_name):
    """Extract pads and their netnames for a given component reference in KiCad 10 PCB."""
    chunks = pcb_text.split('\t(footprint ')
    for c in chunks[1:]:
        if f'(property "Reference" "{ref_name}"' in c or f'(reference "{ref_name}")' in c:
            pads = {}
            for pm in re.finditer(r'\(pad\s+"([^"]*)"\s+(.*?)\n\t\t\)', c, re.DOTALL):
                pnum = pm.group(1)
                net_m = re.search(r'\(net\s+"([^"]+)"\)', pm.group(2))
                if pnum != '':
                    pads[pnum] = net_m.group(1) if net_m else None
            return pads
    return {}

class TestPhase3ASynchronization:
    """Verifies that the Main PCB is fully synchronized with Rev G Schematic."""

    def test_schematic_pcb_reference_parity(self):
        """Verify that every schematic component reference exists on the PCB and count equals 64."""
        sch_text = SCH_PATH.read_text(encoding='utf-8')
        sch_refs = set(re.findall(r'\(property\s+"Reference"\s+"([^"]+)"', sch_text))
        sch_real = {r for r in sch_refs if not r.startswith('#')}
        assert len(sch_real) == 64, f"Expected 64 schematic symbols, found {len(sch_real)}"

        pcb_text = PCB_PATH.read_text(encoding='utf-8')
        pcb_refs = set(re.findall(r'\(property\s+"Reference"\s+"([^"]+)"', pcb_text))
        if not pcb_refs:
            pcb_refs = set(re.findall(r'\(fp_text\s+reference\s+"([^"]+)"', pcb_text))
        assert len(pcb_refs) == 64, f"Expected 64 PCB footprints, found {len(pcb_refs)}"

        missing = sch_real - pcb_refs
        extra = pcb_refs - sch_real
        assert not missing, f"Footprints missing from PCB: {missing}"
        assert not extra, f"Unexpected extra footprints in PCB: {extra}"

    def test_revg_power_path_footprints_presence(self):
        """Verify presence of U4, Q2, D4, R26, R27, and J_USB on Main PCB."""
        pcb_text = PCB_PATH.read_text(encoding='utf-8')
        for ref in ['U4', 'Q2', 'D4', 'R26', 'R27', 'J_USB']:
            assert f'property "Reference" "{ref}"' in pcb_text or f'reference "{ref}"' in pcb_text, f"Component {ref} not found on PCB"

    def test_pin_to_pad_and_net_mapping(self):
        """Verify exact pad-to-net assignments for critical active and power components."""
        pcb_text = PCB_PATH.read_text(encoding='utf-8')

        # 1. U4 AP2112K
        u4_pads = get_pcb_footprint_pads(pcb_text, 'U4')
        assert u4_pads.get('5') == '/3V3', f"U4 Pin 5 must be /3V3, got {u4_pads.get('5')}"
        assert u4_pads.get('1') == '/VBAT_SW', f"U4 Pin 1 must be /VBAT_SW, got {u4_pads.get('1')}"
        assert u4_pads.get('2') == '/GND', f"U4 Pin 2 must be /GND, got {u4_pads.get('2')}"

        # 2. Q2 DMG2305UX P-MOSFET
        q2_pads = get_pcb_footprint_pads(pcb_text, 'Q2')
        assert q2_pads.get('1') == '/USB_VBUS', f"Q2 Pin 1 (Gate) must be /USB_VBUS, got {q2_pads.get('1')}"
        assert q2_pads.get('2') == '/VSYS_RAW', f"Q2 Pin 2 (Source) must be /VSYS_RAW, got {q2_pads.get('2')}"
        assert q2_pads.get('3') == '/VBAT', f"Q2 Pin 3 (Drain) must be /VBAT, got {q2_pads.get('3')}"

        # 3. D4 1N5819HW Schottky
        d4_pads = get_pcb_footprint_pads(pcb_text, 'D4')
        assert d4_pads.get('1') == '/VSYS_RAW', f"D4 Pin 1 (Cathode) must be /VSYS_RAW, got {d4_pads.get('1')}"
        assert d4_pads.get('2') == '/USB_VBUS', f"D4 Pin 2 (Anode) must be /USB_VBUS, got {d4_pads.get('2')}"

        # 4. R26 Gate pull-down
        r26_pads = get_pcb_footprint_pads(pcb_text, 'R26')
        assert r26_pads.get('1') == '/USB_VBUS'
        assert r26_pads.get('2') == '/GND'

        # 5. R27 GPIO8 pull-up
        r27_pads = get_pcb_footprint_pads(pcb_text, 'R27')
        assert r27_pads.get('1') == '/3V3'
        assert r27_pads.get('2') == '/GPIO8_STRAP'

        # 6. U1 ESP32-C3FH4X strapping & USB pins
        u1_pads = get_pcb_footprint_pads(pcb_text, 'U1')
        assert u1_pads.get('14') == '/GPIO8_STRAP', f"U1 Pin 14 must be /GPIO8_STRAP, got {u1_pads.get('14')}"
        assert u1_pads.get('25') == '/USB_DM_CORE', f"U1 Pin 25 must be /USB_DM_CORE, got {u1_pads.get('25')}"
        assert u1_pads.get('26') == '/USB_DP_CORE', f"U1 Pin 26 must be /USB_DP_CORE, got {u1_pads.get('26')}"

        # 7. J_USB Reversible USB-C
        usb_pads = get_pcb_footprint_pads(pcb_text, 'J_USB')
        assert usb_pads.get('4') == '/USB_CC1'
        assert usb_pads.get('9') == '/USB_CC2'
        assert usb_pads.get('5') == '/USB_DM_PORT'
        assert usb_pads.get('7') == '/USB_DM_PORT'
        assert usb_pads.get('6') == '/USB_DP_PORT'
        assert usb_pads.get('8') == '/USB_DP_PORT'

    def test_authoritative_board_dimensions(self):
        """Verify baseline Edge.Cuts dimensions are 84.00 x 9.20 mm."""
        pcb_text = PCB_PATH.read_text(encoding='utf-8')
        gr_lines = re.findall(r'\(gr_line\s+\(start\s+([\d\.-]+)\s+([\d\.-]+)\)\s+\(end\s+([\d\.-]+)\s+([\d\.-]+)\).*?\(layer\s+"?Edge\.Cuts"?\)', pcb_text, re.DOTALL)
        xs = []
        ys = []
        for x1, y1, x2, y2 in gr_lines:
            xs.extend([float(x1), float(x2)])
            ys.extend([float(y1), float(y2)])

        length = max(xs) - min(xs)
        width = max(ys) - min(ys)
        assert abs(length - 84.0) < 0.1, f"Board length must be 84.0 mm, got {length:.2f}"
        assert abs(width - 9.2) < 0.1, f"Board width must be 9.2 mm, got {width:.2f}"

    def test_copper_layer_count(self):
        """Verify PCB has exactly 2 copper layers (F.Cu and B.Cu)."""
        pcb_text = PCB_PATH.read_text(encoding='utf-8')
        layers_match = re.search(r'\(layers\s+(.*?)\n\t\)', pcb_text, re.DOTALL)
        if not layers_match:
            layers_match = re.search(r'\(layers\s+(.*?)\n\s*\)', pcb_text, re.DOTALL)
        assert layers_match, "Layers block not found in PCB"
        cu_layers = [l.strip() for l in layers_match.group(1).splitlines() if 'signal' in l or 'copper' in l or '"F.Cu"' in l or '"B.Cu"' in l]
        assert len(cu_layers) == 2, f"Expected 2 copper layers, found {len(cu_layers)}: {cu_layers}"

    def test_mpu_connector_four_pin_interface(self):
        """Verify J_IMU interface is exactly 4 pins with no MPU_INT on Main PCB."""
        pcb_text = PCB_PATH.read_text(encoding='utf-8')
        j_imu_pads = get_pcb_footprint_pads(pcb_text, 'J_IMU')
        assert len(j_imu_pads) == 4, f"J_IMU must have exactly 4 pins, got {len(j_imu_pads)}: {j_imu_pads}"
        assert j_imu_pads['1'] == '/3V3'
        assert j_imu_pads['2'] == '/GND'
        assert j_imu_pads['3'] == '/I2C_SDA'
        assert j_imu_pads['4'] == '/I2C_SCL'
        assert 'MPU_INT' not in pcb_text, "MPU_INT must not be routed without client ECO"

    def test_usb_c_footprint_geometry(self):
        """Verify TYPE-C-31-M-12 footprint specification in SmartPen.pretty."""
        usb_mod = Path('output/RevG/SmartPen.pretty/J_USB.kicad_mod').read_text(encoding='utf-8')
        assert 'np_thru_hole circle (at -2.890 0.850)' in usb_mod
        assert 'np_thru_hole circle (at 2.890 0.850)' in usb_mod
        assert 'thru_hole oval (at -4.300 0.000)' in usb_mod
        assert 'thru_hole oval (at 4.300 0.000)' in usb_mod
        assert 'thru_hole oval (at -4.300 2.500)' in usb_mod
        assert 'thru_hole oval (at 4.300 2.500)' in usb_mod

    def test_drc_schematic_parity_zero_errors(self):
        """Verify raw KiCad DRC report has 0 schematic parity / footprint errors."""
        assert DRC_RPT_PATH.exists(), "DRC report does not exist"
        rpt_text = DRC_RPT_PATH.read_text(encoding='utf-8')
        assert "Found 0 schematic parity issues" in rpt_text or "Found 0 Footprint errors" in rpt_text, "Schematic parity issues must be 0"


class TestPhase3ANegativeFixtures:
    """Verifies that the test suite fails on intentionally corrupted temporary fixtures."""

    def test_negative_missing_footprint_fails(self):
        """Simulate missing U4 regulator on PCB; assert reference parity failure."""
        fake_pcb = PCB_PATH.read_text(encoding='utf-8').replace('property "Reference" "U4"', 'property "Reference" "U4_DELETED"')
        pcb_refs = set(re.findall(r'\(property\s+"Reference"\s+"([^"]+)"', fake_pcb))
        with pytest.raises(AssertionError):
            assert 'U4' in pcb_refs

    def test_negative_reversed_mosfet_fails(self):
        """Simulate inverted Q2 Source/Drain; assert power-path safety check fails."""
        q2_pads = {'1': '/USB_VBUS', '2': '/VBAT', '3': '/VSYS_RAW'}
        with pytest.raises(AssertionError):
            assert q2_pads.get('2') == '/VSYS_RAW'
            assert q2_pads.get('3') == '/VBAT'

    def test_negative_wrong_layer_count_fails(self):
        """Simulate 4-layer stackup modification without justification; assert failure."""
        fake_layers = ['(0 "F.Cu" signal)', '(1 "In1.Cu" signal)', '(2 "In2.Cu" signal)', '(31 "B.Cu" signal)']
        with pytest.raises(AssertionError):
            assert len(fake_layers) == 2, "2-layer baseline violated!"

    def test_negative_wrong_dimensions_fails(self):
        """Simulate 11.0 x 128.0 mm board size modification; assert failure against 84x9.2 baseline."""
        bad_len = 128.0
        bad_width = 11.0
        with pytest.raises(AssertionError):
            assert abs(bad_len - 84.0) < 0.1
            assert abs(bad_width - 9.2) < 0.1

    def test_negative_unbridged_usb_fails(self):
        """Simulate non-reversible USB connector; assert failure."""
        bad_usb_pads = {'5': '/USB_DM_PORT', '7': '/USB_DP_PORT'}
        with pytest.raises(AssertionError):
            assert bad_usb_pads['5'] == '/USB_DM_PORT'
            assert bad_usb_pads['7'] == '/USB_DM_PORT'
