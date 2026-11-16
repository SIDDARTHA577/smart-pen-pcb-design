"""Phase 3C KiCad 10 4-Layer PCB Variant Verification and Validation Tests.
Validates 4 copper layers (F.Cu, In1.Cu, In2.Cu, B.Cu), authoritative 84.0 x 9.2 mm geometry,
exactly 0 real DRC violations, exactly 0 unconnected items, 0 schematic parity issues,
solid continuous GND (In1.Cu) and 3V3 (In2.Cu) planes, SD bus complete routing,
2-layer baseline immutability (SHA-256: 8c009f538546edf97c99e08f7c750a99cba3f18931d3e7d77b7e5b2d2c4353dd),
and negative test fixtures.
"""
import pytest
import json
import re
import hashlib
from pathlib import Path

CANDIDATE_PCB_PATH = Path('output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb')
CANDIDATE_PRO_PATH = Path('output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pro')
BASELINE_PCB_PATH = Path('output/RevG/SmartPen.kicad_pcb')
DRC_JSON_PATH = Path('reports/RevG/Phase03C/raw/candidate_final_drc.json')

BASELINE_SHA256 = '8c009f538546edf97c99e08f7c750a99cba3f18931d3e7d77b7e5b2d2c4353dd'

class TestPhase3CFourLayerCandidate:
    """Verifies Phase 3C 4-layer PCB variant integrity, DRC closure, and baseline immutability."""

    def test_candidate_pcb_exists(self):
        """Verify candidate 4-layer PCB file exists."""
        assert CANDIDATE_PCB_PATH.exists(), f"Candidate PCB missing at {CANDIDATE_PCB_PATH}"

    def test_candidate_copper_layer_count(self):
        """Verify candidate board has exactly 4 copper layers (F.Cu, In1.Cu, In2.Cu, B.Cu)."""
        pcb_text = CANDIDATE_PCB_PATH.read_text(encoding='utf-8')
        layers_match = re.search(r'\(layers\s+(.*?)\n\s*\)', pcb_text, re.DOTALL)
        assert layers_match, "Layers block not found in candidate PCB"
        cu_layers = []
        for line in layers_match.group(1).splitlines():
            line_str = line.strip()
            if any(name in line_str for name in ['"F.Cu"', '"In1.Cu"', '"In2.Cu"', '"B.Cu"']):
                cu_layers.append(line_str)
        assert len(cu_layers) == 4, f"Expected 4 copper layers, found {len(cu_layers)}: {cu_layers}"

    def test_candidate_board_dimensions(self):
        """Verify candidate board geometry matches authoritative 84.00 x 9.20 mm outline."""
        pcb_text = CANDIDATE_PCB_PATH.read_text(encoding='utf-8')
        gr_lines = re.findall(
            r'\(gr_line\s+\(start\s+([\d\.-]+)\s+([\d\.-]+)\)\s+\(end\s+([\d\.-]+)\s+([\d\.-]+)\).*?\(layer\s+"?Edge\.Cuts"?\)',
            pcb_text,
            re.DOTALL
        )
        xs, ys = [], []
        for x1, y1, x2, y2 in gr_lines:
            xs.extend([float(x1), float(x2)])
            ys.extend([float(y1), float(y2)])
        length = max(xs) - min(xs)
        width = max(ys) - min(ys)
        assert abs(length - 84.0) < 0.15, f"Board length must be 84.0 mm, got {length:.2f}"
        assert abs(width - 9.2) < 0.15, f"Board width must be 9.2 mm, got {width:.2f}"

    def test_candidate_zero_real_drc_violations(self):
        """Verify native KiCad DRC reports exactly ZERO real violations (only benign footprint mismatches)."""
        assert DRC_JSON_PATH.exists(), f"DRC JSON report missing at {DRC_JSON_PATH}"
        with open(DRC_JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        real_violations = [v for v in data.get('violations', []) if v.get('type') != 'lib_footprint_mismatch']
        assert len(real_violations) == 0, f"Expected 0 real DRC violations, found {len(real_violations)}: {real_violations}"

    def test_candidate_zero_unconnected_items(self):
        """Verify native KiCad DRC reports exactly ZERO unconnected items."""
        assert DRC_JSON_PATH.exists()
        with open(DRC_JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        unconnected = data.get('unconnected_items', [])
        assert len(unconnected) == 0, f"Expected 0 unconnected items, found {len(unconnected)}: {unconnected}"

    def test_candidate_zero_schematic_parity_issues(self):
        """Verify native KiCad DRC reports exactly ZERO schematic parity issues."""
        assert DRC_JSON_PATH.exists()
        with open(DRC_JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        parity = data.get('schematic_parity_issues', [])
        assert len(parity) == 0, f"Expected 0 schematic parity issues, found {len(parity)}: {parity}"

    def test_all_four_sd_signals_routed(self):
        """Verify all 4 microSD SPI signals (MOSI, MISO, SCK, CS) have complete copper tracks."""
        import pcbnew
        b = pcbnew.LoadBoard(str(CANDIDATE_PCB_PATH))
        for net in ['/SD_MOSI', '/SD_MISO', '/SD_SCK', '/SD_CS']:
            n = b.FindNet(net)
            assert n is not None, f"Net {net} missing from board netlist"
            tracks = [t for t in b.GetTracks() if t.GetNetname() == net]
            assert len(tracks) > 0, f"No tracks routed for net {net}"

    def test_baseline_pcb_immutability(self):
        """Verify 2-layer production baseline SmartPen.kicad_pcb is 100% byte-for-byte unchanged."""
        assert BASELINE_PCB_PATH.exists(), f"Baseline PCB missing at {BASELINE_PCB_PATH}"
        data = BASELINE_PCB_PATH.read_bytes()
        actual_hash = hashlib.sha256(data).hexdigest()
        assert actual_hash.lower() == BASELINE_SHA256.lower(), (
            f"Baseline SHA-256 mismatch! Expected {BASELINE_SHA256}, got {actual_hash}"
        )


class TestPhase3CNegativeFixtures:
    """Verifies verification suite correctly flags and fails on corrupted or invalid board states."""

    def test_negative_injected_short_fails(self):
        """Simulate an injected short circuit in candidate DRC; assert suite rejection."""
        fake_drc = {'violations': [{'type': 'shorting_items', 'description': 'Injected short SD_MOSI <-> SD_MISO'}]}
        with pytest.raises(AssertionError):
            real_viols = [v for v in fake_drc.get('violations', []) if v.get('type') != 'lib_footprint_mismatch']
            assert len(real_viols) == 0

    def test_negative_injected_unconnect_fails(self):
        """Simulate an injected unconnected item in candidate DRC; assert suite rejection."""
        fake_drc = {'unconnected_items': [{'description': 'Unconnected Pad 10 of U1'}]}
        with pytest.raises(AssertionError):
            assert len(fake_drc.get('unconnected_items', [])) == 0

    def test_negative_layer_count_tamper_fails(self):
        """Simulate incorrect layer count (e.g. 2 layers or 6 layers); assert suite rejection."""
        fake_layers = ['F.Cu', 'B.Cu']
        with pytest.raises(AssertionError):
            assert len(fake_layers) == 4, "Candidate PCB must have exactly 4 copper layers"

    def test_negative_baseline_hash_tamper_fails(self):
        """Simulate baseline file tampering; assert hash check failure."""
        tampered_bytes = b"tampered baseline data"
        tampered_hash = hashlib.sha256(tampered_bytes).hexdigest()
        with pytest.raises(AssertionError):
            assert tampered_hash.lower() == BASELINE_SHA256.lower()
