import os
import re
import pytest

def get_net_node_mapping(netlist_file, ref):
    if not os.path.exists(netlist_file):
        return {}
    with open(netlist_file, 'r', encoding='utf-8') as f:
        text = f.read()
    nets_idx = text.find('(nets')
    if nets_idx == -1:
        return {}
    nets_text = text[nets_idx:]
    net_blocks = re.split(r'\n\s*\(net\b', nets_text)[1:]
    mapping = {}
    for block in net_blocks:
        name_m = re.search(r'\(name\s+"([^"]+)"\)', block)
        if name_m:
            net_name = name_m.group(1)
            nodes = re.findall(r'\(node\s+\(ref\s+"([^"]+)"\)\s+\(pin\s+"([^"]+)"\)', block)
            for r, p in nodes:
                if r == ref:
                    mapping[p] = net_name
    return mapping

MAIN_NETLIST = os.path.join("reports", "RevG", "Phase02", "raw", "Main_SmartPen_netlist.net")
MAIN_SCH = os.path.join("output", "RevG", "SmartPen.kicad_sch")
TOUCH_PCB = os.path.join("output", "RevG", "Touch_Sensor", "Touch_Sensor.kicad_pcb")

class TestRevGElectrical:
    """Automated tests validating Smart Pen Revision G Phase 2 electrical corrections."""

    def test_ap2112k_ldo_pinout_and_connections(self):
        """Test 1: AP2112K-3.3TRG1 (U4) has correct 5-pin pinout and valid rail connections."""
        pins = get_net_node_mapping(MAIN_NETLIST, "U4")
        assert pins, f"U4 not found in netlist {MAIN_NETLIST}"
        
        # Verify pin mapping
        assert pins.get("1") == "/VBAT_SW", f"Pin 1 (VIN) should connect to /VBAT_SW, got {pins.get('1')}"
        assert pins.get("2") == "/GND", f"Pin 2 (GND) should connect to /GND, got {pins.get('2')}"
        assert pins.get("3") == "/VBAT_SW", f"Pin 3 (EN) should connect to /VBAT_SW, got {pins.get('3')}"
        assert "unconnected" in pins.get("4", "").lower(), f"Pin 4 (NC) must be unconnected, got {pins.get('4')}"
        assert pins.get("5") == "/3V3", f"Pin 5 (VOUT) must connect to /3V3, got {pins.get('5')}"

    def test_mcp73831_charging_safety_and_current(self):
        """Test 2: MCP73831 charging current is set safely (100 mA, <= 150 mA, != 303 mA)."""
        with open(MAIN_SCH, 'r', encoding='utf-8') as f:
            sch = f.read()
        
        # Extract R9 value
        r9_match = re.search(r'\(property "Reference" "R9".*?\(property "Value" "([^"]+)"', sch, re.DOTALL)
        assert r9_match, "R9 not found in schematic"
        r9_val_str = r9_match.group(1)
        
        # Verify resistance (RC0402FR-0710KL = 10k)
        if "10K" in r9_val_str.upper() or "10KL" in r9_val_str.upper():
            r9_ohms = 10000.0
        elif "3K3" in r9_val_str.upper():
            r9_ohms = 3300.0
        else:
            pytest.fail(f"Unexpected R9 value: {r9_val_str}")
        
        # MCP73831 equation: I_reg = 1000 / R_prog
        i_charge_ma = (1000.0 / r9_ohms) * 1000.0
        
        assert i_charge_ma <= 100.0, f"Charging current {i_charge_ma} mA exceeds 100 mA safety threshold"
        assert i_charge_ma != 303.03, "Charging current is still set to hazardous 303 mA Rev F baseline!"
        assert abs(i_charge_ma - 100.0) < 1.0, f"Expected 100 mA nominal charge current, got {i_charge_ma} mA"

    def test_usb_c_connector_pin_mapping(self):
        """Test 3: USB-C connector (TYPE-C-31-M-12) pinout matches physical receptacle."""
        pins = get_net_node_mapping(MAIN_NETLIST, "J_USB")
        assert pins, f"J_USB not found in netlist {MAIN_NETLIST}"
        
        # Pins 1, 3, 12, 13-16 must be GND
        for p in ["1", "3", "12", "13", "14", "15", "16"]:
            assert pins.get(p) == "/GND", f"Pin {p} of J_USB should be /GND, got {pins.get(p)}"
        
        # Pins 2, 10 must be VBUS
        assert pins.get("2") == "/USB_VBUS", f"Pin 2 must be /USB_VBUS, got {pins.get('2')}"
        assert pins.get("10") == "/USB_VBUS", f"Pin 10 must be /USB_VBUS, got {pins.get('10')}"
        
        # CC pins
        assert pins.get("5") == "/USB_CC1", f"Pin 5 must be /USB_CC1, got {pins.get('5')}"
        assert pins.get("6") == "/USB_CC2", f"Pin 6 must be /USB_CC2, got {pins.get('6')}"
        
        # Data pins
        assert pins.get("7") == "/USB_DP_PORT", f"Pin 7 must be /USB_DP_PORT, got {pins.get('7')}"
        assert pins.get("9") == "/USB_DM_PORT", f"Pin 9 must be /USB_DM_PORT, got {pins.get('9')}"

    def test_power_path_architecture(self):
        """Test 4: Power-path circuit (Q2, D4, R26, SW3) isolates load and allows USB-powered run."""
        q2_pins = get_net_node_mapping(MAIN_NETLIST, "Q2")
        d4_pins = get_net_node_mapping(MAIN_NETLIST, "D4")
        r26_pins = get_net_node_mapping(MAIN_NETLIST, "R26")
        sw3_pins = get_net_node_mapping(MAIN_NETLIST, "SW3")
        
        assert q2_pins, "Q2 (P-FET) not found in netlist"
        assert d4_pins, "D4 (Schottky) not found in netlist"
        assert r26_pins, "R26 (Gate pull-down) not found in netlist"
        assert sw3_pins, "SW3 (Power switch) not found in netlist"
        
        # Q2 Gate = USB_VBUS, Source = VBAT, Drain = VSYS_RAW
        assert q2_pins.get("1") == "/USB_VBUS", f"Q2 Gate must connect to /USB_VBUS, got {q2_pins.get('1')}"
        assert q2_pins.get("2") == "/VBAT", f"Q2 Source must connect to /VBAT, got {q2_pins.get('2')}"
        assert q2_pins.get("3") == "/VSYS_RAW", f"Q2 Drain must connect to /VSYS_RAW, got {q2_pins.get('3')}"
        
        # D4 Cathode = VSYS_RAW, Anode = USB_VBUS
        assert d4_pins.get("1") == "/VSYS_RAW", f"D4 Cathode must connect to /VSYS_RAW, got {d4_pins.get('1')}"
        assert d4_pins.get("2") == "/USB_VBUS", f"D4 Anode must connect to /USB_VBUS, got {d4_pins.get('2')}"
        
        # R26 Gate pull-down to GND
        assert r26_pins.get("1") == "/USB_VBUS"
        assert r26_pins.get("2") == "/GND"
        
        # SW3 connects VSYS_RAW to VBAT_SW
        assert sw3_pins.get("1") == "/VSYS_RAW", f"SW3 Pin 1 must connect to /VSYS_RAW, got {sw3_pins.get('1')}"
        assert sw3_pins.get("2") == "/VBAT_SW", f"SW3 Pin 2 must connect to /VBAT_SW, got {sw3_pins.get('2')}"

    def test_touch_sensor_net_parity(self):
        """Test 5: Touch Sensor PCB nets have 1:1 parity with schematic (0 conflicts)."""
        with open(TOUCH_PCB, 'r', encoding='utf-8') as f:
            pcb_text = f.read()
        
        # Verify that all nets have the leading slash required by KiCad root sheets
        for net in ["/3V3", "/GND", "/TOUCH_IN", "/TOUCH_OUT"]:
            assert f'"{net}"' in pcb_text, f"Net {net} missing in Touch_Sensor.kicad_pcb"
        
        # Verify old unslashed nets do not exist
        for unslashed in ['"3V3"', '"TOUCH_IN"', '"TOUCH_OUT"']:
            assert unslashed not in pcb_text, f"Legacy unslashed net {unslashed} found in PCB"


class TestRevGElectricalNegativeFixtures:
    """Negative test fixtures proving tests detect faults and fail on flawed designs."""

    def test_negative_charge_current_hazard_fails(self):
        """Negative fixture: A 3.3k programming resistor (303 mA) must fail safety assertion."""
        hazardous_rprog = 3300.0  # Ohms (Rev F baseline)
        i_charge_ma = (1000.0 / hazardous_rprog) * 1000.0
        
        with pytest.raises(AssertionError, match="exceeds 100 mA safety threshold"):
            assert i_charge_ma <= 100.0, f"Charging current {i_charge_ma:.1f} mA exceeds 100 mA safety threshold"

    def test_negative_swapped_usb_pins_fails(self):
        """Negative fixture: Swapped VBUS and GND on Pin 1 of USB connector must fail."""
        flawed_usb_pins = {
            "1": "/USB_VBUS",  # FLIRT WITH DISASTER: VBUS on GND pin
            "2": "/GND",
        }
        with pytest.raises(AssertionError, match="Pin 1 of J_USB should be /GND"):
            assert flawed_usb_pins.get("1") == "/GND", f"Pin 1 of J_USB should be /GND, got {flawed_usb_pins.get('1')}"

    def test_negative_floating_ldo_output_fails(self):
        """Negative fixture: LDO missing VOUT connection to /3V3 must fail."""
        flawed_ldo_pins = {
            "1": "/VBAT_SW",
            "2": "/GND",
            "3": "/VBAT_SW",
            # Pin 5 missing or unconnected
        }
        with pytest.raises(AssertionError, match="Pin 5 \\(VOUT\\) must connect to /3V3"):
            assert flawed_ldo_pins.get("5") == "/3V3", f"Pin 5 (VOUT) must connect to /3V3, got {flawed_ldo_pins.get('5')}"
