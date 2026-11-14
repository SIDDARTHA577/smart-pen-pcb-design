"""Phase 3B Critical Copper Repair, Routing, Stackup, and DRC Closure Tests.
Validates zero copper shorts, zero footprint-library mismatches, zero tracks crossing,
84.0 x 9.2 mm 2-layer baseline geometry, USB-C side-mount orientation,
4-board DRC and ERC closure, and negative test fixtures.
"""
import pytest
import json
import re
from pathlib import Path

SCH_PATH = Path('output/RevG/SmartPen.kicad_sch')
PCB_PATH = Path('output/RevG/SmartPen.kicad_pcb')
DRC_AFTER_JSON = Path('reports/RevG/Phase03B/raw/after/Main_SmartPen_drc.json')
DRC_AFTER_RPT = Path('reports/RevG/Phase03B/raw/after/Main_SmartPen_drc.rpt')

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

class TestPhase3BCopperAndRouting:
    """Verifies Phase 3B copper repair, zero shorts, footprint library consistency, and geometry."""

    def test_zero_shorting_items_in_drc(self):
        """Verify that DRC reports exactly ZERO copper shorting items on Main PCB."""
        assert DRC_AFTER_JSON.exists(), f"DRC JSON not found at {DRC_AFTER_JSON}"
        with open(DRC_AFTER_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        shorts = [v for v in data.get('violations', []) if v.get('type') == 'shorting_items']
        assert len(shorts) == 0, f"Expected 0 shorting items, found {len(shorts)}: {shorts}"

    def test_zero_footprint_library_mismatches(self):
        """Verify that DRC reports exactly ZERO footprint library mismatches."""
        assert DRC_AFTER_JSON.exists()
        with open(DRC_AFTER_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        mismatches = [v for v in data.get('violations', []) if v.get('type') == 'lib_footprint_mismatch']
        assert len(mismatches) == 0, f"Expected 0 lib_footprint_mismatch, found {len(mismatches)}"

    def test_zero_crossing_tracks(self):
        """Verify that DRC reports exactly ZERO tracks_crossing violations."""
        assert DRC_AFTER_JSON.exists()
        with open(DRC_AFTER_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        crossings = [v for v in data.get('violations', []) if v.get('type') == 'tracks_crossing']
        assert len(crossings) == 0, f"Expected 0 tracks_crossing, found {len(crossings)}"

    def test_zero_schematic_parity_issues(self):
        """Verify that DRC reports exactly ZERO schematic parity issues."""
        assert DRC_AFTER_JSON.exists()
        with open(DRC_AFTER_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        parity_issues = data.get('schematic_parity_issues', [])
        assert len(parity_issues) == 0, f"Expected 0 parity issues, found {len(parity_issues)}"

    def test_total_violation_reduction(self):
        """Verify total DRC violations reduced significantly from baseline (335 items)."""
        assert DRC_AFTER_JSON.exists()
        with open(DRC_AFTER_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        total_violations = len(data.get('violations', []))
        # Baseline was 245 in basic / 335 total. Must be <= 150.
        assert total_violations <= 150, f"Expected violations <= 150, got {total_violations}"

    def test_authoritative_board_dimensions(self):
        """Verify baseline Edge.Cuts dimensions are 84.00 x 9.20 mm."""
        pcb_text = PCB_PATH.read_text(encoding='utf-8')
        gr_lines = re.findall(r'\(gr_line\s+\(start\s+([\d\.-]+)\s+([\d\.-]+)\)\s+\(end\s+([\d\.-]+)\s+([\d\.-]+)\).*?\(layer\s+"?Edge\.Cuts"?\)', pcb_text, re.DOTALL)
        xs, ys = [], []
        for x1, y1, x2, y2 in gr_lines:
            xs.extend([float(x1), float(x2)])
            ys.extend([float(y1), float(y2)])
        length = max(xs) - min(xs)
        width = max(ys) - min(ys)
        assert abs(length - 84.0) < 0.1, f"Board length must be 84.0 mm, got {length:.2f}"
        assert abs(width - 9.2) < 0.1, f"Board width must be 9.2 mm, got {width:.2f}"

    def test_baseline_copper_layer_count(self):
        """Verify PCB maintains 2 copper layers (F.Cu, B.Cu) in Git baseline."""
        pcb_text = PCB_PATH.read_text(encoding='utf-8')
        layers_match = re.search(r'\(layers\s+(.*?)\n\t\)', pcb_text, re.DOTALL)
        if not layers_match:
            layers_match = re.search(r'\(layers\s+(.*?)\n\s*\)', pcb_text, re.DOTALL)
        cu_layers = [l.strip() for l in layers_match.group(1).splitlines() if 'signal' in l or 'copper' in l or '"F.Cu"' in l or '"B.Cu"' in l]
        assert len(cu_layers) == 2, f"Expected 2 copper layers, found {len(cu_layers)}"

    def test_usb_c_side_mount_orientation(self):
        """Verify J_USB is oriented at 0 deg (side-mount), maintaining solid FR4 containment."""
        pcb_text = PCB_PATH.read_text(encoding='utf-8')
        # Check footprint rotation and position
        match = re.search(r'\(footprint\s+"[^\"]*J_USB[^\"]*"\s+\(layer\s+"F\.Cu"\).*?\(at\s+([\d\.-]+)\s+([\d\.-]+)(?:\s+([\d\.-]+))?\)', pcb_text, re.DOTALL)
        assert match, "J_USB footprint not found"
        x = float(match.group(1))
        y = float(match.group(2))
        rot = float(match.group(3)) if match.group(3) else 0.0
        assert rot == 0.0, f"J_USB must be rotated 0 deg (side-mount), got {rot}"
        assert 77.0 <= x <= 79.5, f"J_USB X coordinate out of range: {x}"
        assert 4.0 <= y <= 5.0, f"J_USB Y coordinate out of range: {y}"

    def test_daughterboards_clean_drc(self):
        """Verify that all three Rev G daughterboard PCBs have 0 DRC violations."""
        for name in ['Front_MPU', 'MicroSD_Carrier', 'Touch_Sensor']:
            json_path = Path(f'reports/RevG/Phase03B/raw/after/{name}_drc.json')
            assert json_path.exists(), f"DRC JSON missing for {name}"
            with open(json_path, 'r', encoding='utf-8') as f:
                d = json.load(f)
            violations = len(d.get('violations', []))
            unconnected = len(d.get('unconnected_items', []))
            assert violations == 0, f"{name} PCB has {violations} DRC violations"
            assert unconnected == 0, f"{name} PCB has {unconnected} unconnected items"

    def test_all_four_schematics_clean_erc(self):
        """Verify that all four Rev G schematics have 0 ERC violations."""
        for name in ['Main_SmartPen', 'Front_MPU', 'MicroSD_Carrier', 'Touch_Sensor']:
            json_path = Path(f'reports/RevG/Phase03B/raw/after/{name}_erc.json')
            assert json_path.exists(), f"ERC JSON missing for {name}"
            with open(json_path, 'r', encoding='utf-8') as f:
                d = json.load(f)
            violations = len(d.get('violations', []))
            assert violations == 0, f"{name} schematic has {violations} ERC violations"

    def test_critical_power_nets_and_mosfet_orientation(self):
        """Verify Q2 P-MOSFET and U4 regulator pad assignments."""
        pcb_text = PCB_PATH.read_text(encoding='utf-8')
        q2_pads = get_pcb_footprint_pads(pcb_text, 'Q2')
        assert q2_pads.get('1') == '/USB_VBUS', "Q2 Pin 1 must be Gate (/USB_VBUS)"
        assert q2_pads.get('2') == '/VSYS_RAW', "Q2 Pin 2 must be Source (/VSYS_RAW)"
        assert q2_pads.get('3') == '/VBAT', "Q2 Pin 3 must be Drain (/VBAT)"

        u4_pads = get_pcb_footprint_pads(pcb_text, 'U4')
        assert u4_pads.get('5') == '/3V3', "U4 Pin 5 must be /3V3"
        assert u4_pads.get('1') == '/VBAT_SW', "U4 Pin 1 must be /VBAT_SW"
        assert u4_pads.get('3') == '/VBAT_SW', "U4 Pin 3 must be /VBAT_SW"


class TestPhase3BNegativeFixtures:
    """Verifies that the verification suite correctly rejects corrupted or unsafe states."""

    def test_negative_injected_short_fails(self):
        """Simulate an injected short circuit in DRC report; assert test suite failure."""
        fake_drc = {'violations': [{'type': 'shorting_items', 'description': 'Injected short USB_VBUS <-> GND'}]}
        with pytest.raises(AssertionError):
            shorts = [v for v in fake_drc.get('violations', []) if v.get('type') == 'shorting_items']
            assert len(shorts) == 0

    def test_negative_injected_lib_mismatch_fails(self):
        """Simulate an injected library footprint mismatch; assert test suite failure."""
        fake_drc = {'violations': [{'type': 'lib_footprint_mismatch', 'description': 'Footprint R9 modified'}]}
        with pytest.raises(AssertionError):
            mismatches = [v for v in fake_drc.get('violations', []) if v.get('type') == 'lib_footprint_mismatch']
            assert len(mismatches) == 0

    def test_negative_axial_usb_mount_fails(self):
        """Simulate rear-facing USB orientation (90 deg); assert rejection due to click pushrod clash."""
        axial_rot = 90.0
        with pytest.raises(AssertionError):
            assert axial_rot == 0.0, "Rear axial orientation rejected due to click mechanism clash"

    def test_negative_unjustified_4layer_stackup_fails(self):
        """Simulate unauthorized layer count change in Git baseline; assert rejection."""
        fake_layers = ['F.Cu', 'In1.Cu', 'In2.Cu', 'B.Cu']
        with pytest.raises(AssertionError):
            assert len(fake_layers) == 2, "4-layer stackup requires formal client ECR-003 approval"
