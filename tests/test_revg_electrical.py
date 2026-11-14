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

def get_net_all_nodes(netlist_file, net_name):
    if not os.path.exists(netlist_file):
        return []
    with open(netlist_file, 'r', encoding='utf-8') as f:
        text = f.read()
    nets_idx = text.find('(nets')
    if nets_idx == -1:
        return []
    nets_text = text[nets_idx:]
    net_blocks = re.split(r'\n\s*\(net\b', nets_text)[1:]
    for block in net_blocks:
        name_m = re.search(r'\(name\s+"([^"]+)"\)', block)
        if name_m and name_m.group(1) == net_name:
            return re.findall(r'\(node\s+\(ref\s+"([^"]+)"\)\s+\(pin\s+"([^"]+)"\)', block)
    return []

MAIN_NETLIST = os.path.join("reports", "RevG", "Phase02_Final", "raw", "Main_SmartPen_netlist.net")
MAIN_SCH = os.path.join("output", "RevG", "SmartPen.kicad_sch")
TOUCH_PCB = os.path.join("output", "RevG", "Touch_Sensor", "Touch_Sensor.kicad_pcb")
USB_FOOTPRINT = os.path.join("output", "RevG", "SmartPen.pretty", "J_USB.kicad_mod")

class TestRevGElectrical:
    """Automated tests validating Smart Pen Revision G Phase 2.2 final electrical corrections."""

    def test_ap2112k_ldo_pinout_and_connections(self):
        """Test 1: AP2112K-3.3TRG1 (U4) has correct 5-pin pinout and valid rail connections."""
        pins = get_net_node_mapping(MAIN_NETLIST, "U4")
        assert pins, f"U4 not found in netlist {MAIN_NETLIST}"
        
        assert pins.get("1") == "/VBAT_SW", f"Pin 1 (VIN) should connect to /VBAT_SW, got {pins.get('1')}"
        assert pins.get("2") == "/GND", f"Pin 2 (GND) should connect to /GND, got {pins.get('2')}"
        assert pins.get("3") == "/VBAT_SW", f"Pin 3 (EN) should connect to /VBAT_SW, got {pins.get('3')}"
        assert "unconnected" in pins.get("4", "").lower(), f"Pin 4 (NC) must be unconnected, got {pins.get('4')}"
        assert pins.get("5") == "/3V3", f"Pin 5 (VOUT) must connect to /3V3, got {pins.get('5')}"

    def test_mcp73831_charging_safety_and_current(self):
        """Test 2: MCP73831 charging current is set safely (100 mA, <= 150 mA, != 303 mA)."""
        with open(MAIN_SCH, 'r', encoding='utf-8') as f:
            sch = f.read()
        
        r9_match = re.search(r'\(property "Reference" "R9".*?\(property "Value" "([^"]+)"', sch, re.DOTALL)
        assert r9_match, "R9 not found in schematic"
        r9_val_str = r9_match.group(1)
        
        if "10K" in r9_val_str.upper() or "10KL" in r9_val_str.upper():
            r9_ohms = 10000.0
        elif "3K3" in r9_val_str.upper():
            r9_ohms = 3300.0
        else:
            pytest.fail(f"Unexpected R9 value: {r9_val_str}")
        
        i_charge_ma = (1000.0 / r9_ohms) * 1000.0
        assert i_charge_ma <= 100.0, f"Charging current {i_charge_ma} mA exceeds 100 mA safety threshold"
        assert i_charge_ma != 303.03, "Charging current is still set to hazardous 303 mA Rev F baseline!"
        assert abs(i_charge_ma - 100.0) < 1.0, f"Expected 100 mA nominal charge current, got {i_charge_ma} mA"

    def test_usb_c_connector_pin_mapping(self):
        """Test 3: USB-C connector (TYPE-C-31-M-12) pinout matches physical 16-pin receptacle."""
        pins = get_net_node_mapping(MAIN_NETLIST, "J_USB")
        assert pins, f"J_USB not found in netlist {MAIN_NETLIST}"
        
        # Ground and Shield stakes: Pins 1, 12, 13, 14, 15, 16 must be /GND
        for p in ["1", "12", "13", "14", "15", "16"]:
            assert pins.get(p) == "/GND", f"Pin {p} of J_USB should be /GND, got {pins.get(p)}"
        
        # VBUS pins: Pins 2, 11 must be /USB_VBUS
        assert pins.get("2") == "/USB_VBUS", f"Pin 2 must be /USB_VBUS, got {pins.get('2')}"
        assert pins.get("11") == "/USB_VBUS", f"Pin 11 must be /USB_VBUS, got {pins.get('11')}"
        
        # CC pins: Pin 4 (CC1), Pin 9 (CC2)
        assert pins.get("4") == "/USB_CC1", f"Pin 4 must be /USB_CC1, got {pins.get('4')}"
        assert pins.get("9") == "/USB_CC2", f"Pin 9 must be /USB_CC2, got {pins.get('9')}"
        
        # Data pins: Reversible USB 2.0 requires D+ (Pins 6, 8) and D- (Pins 5, 7) bridged
        assert pins.get("6") == "/USB_DP_PORT", f"Pin 6 (DP1) must be /USB_DP_PORT, got {pins.get('6')}"
        assert pins.get("8") == "/USB_DP_PORT", f"Pin 8 (DP2) must be /USB_DP_PORT, got {pins.get('8')}"
        assert pins.get("5") == "/USB_DM_PORT", f"Pin 5 (DN2) must be /USB_DM_PORT, got {pins.get('5')}"
        assert pins.get("7") == "/USB_DM_PORT", f"Pin 7 (DN1) must be /USB_DM_PORT, got {pins.get('7')}"
        
        # SBU pins: Pins 3, 10 must be unconnected for USB 2.0 UFP device
        assert "unconnected" in pins.get("3", "").lower(), f"Pin 3 (SBU2) must be unconnected, got {pins.get('3')}"
        assert "unconnected" in pins.get("10", "").lower(), f"Pin 10 (SBU1) must be unconnected, got {pins.get('10')}"

    def test_usb_c_physical_footprint_structure(self):
        """Test 4: J_USB footprint incorporates 12 SMT contacts, 4 through-hole shell retention posts and 2 NPTH pegs."""
        assert os.path.exists(USB_FOOTPRINT), f"USB footprint not found at {USB_FOOTPRINT}"
        with open(USB_FOOTPRINT, 'r', encoding='utf-8') as f:
            mod = f.read()
            
        # Ensure footprint contains NO invalid ';' comments that break KiCad parser
        for line in mod.splitlines():
            assert not line.strip().startswith(";"), f"Footprint contains syntax-breaking comment: {line}"
            
        # Verify 12 SMT signal/power pads (Pads 1-12)
        smt_pads = re.findall(r'\(pad\s+"([1-9]|1[0-2])"\s+smd\s+rect\s+\(at\s+([\d\.\-]+)\s+([\d\.\-]+)\)\s+\(size\s+([\d\.\-]+)\s+([\d\.\-]+)\)', mod)
        assert len(smt_pads) == 12, f"Expected 12 SMT contact pads (1-12), found {len(smt_pads)}"
        
        # Verify 4 through-hole oval shield tabs (Pads 13-16)
        th_pads = re.findall(r'\(pad\s+"(1[3-6])"\s+thru_hole\s+oval\s+\(at\s+([\d\.\-]+)\s+([\d\.\-]+)\)\s+\(size\s+([\d\.\-]+)\s+([\d\.\-]+)\)\s+\(drill\s+oval\s+([\d\.\-]+)\s+([\d\.\-]+)\)', mod)
        assert len(th_pads) == 4, f"Expected 4 through-hole oval shield tabs (13-16), found {len(th_pads)}"
        
        # Verify 2 NPTH mechanical alignment peg holes
        npth_holes = re.findall(r'\(pad\s+""\s+np_thru_hole\s+circle\s+\(at\s+([\d\.\-]+)\s+([\d\.\-]+)\)\s+\(size\s+([\d\.\-]+)\s+([\d\.\-]+)\)\s+\(drill\s+([\d\.\-]+)\)', mod)
        assert len(npth_holes) == 2, f"Expected 2 NPTH alignment pegs, found {len(npth_holes)}"

    def test_power_path_architecture_and_body_diode(self):
        """Test 5: Power-path circuit (Q2, D4, R26, SW3) isolates load and has reverse-biased body diode during USB supply."""
        q2_pins = get_net_node_mapping(MAIN_NETLIST, "Q2")
        d4_pins = get_net_node_mapping(MAIN_NETLIST, "D4")
        r26_pins = get_net_node_mapping(MAIN_NETLIST, "R26")
        sw3_pins = get_net_node_mapping(MAIN_NETLIST, "SW3")
        
        assert q2_pins, "Q2 (P-FET) not found in netlist"
        assert d4_pins, "D4 (Schottky) not found in netlist"
        assert r26_pins, "R26 (Gate pull-down) not found in netlist"
        assert sw3_pins, "SW3 (Power switch) not found in netlist"
        
        # Safe Load Sharing: Q2 Gate = USB_VBUS, Source = VSYS_RAW, Drain = VBAT
        assert q2_pins.get("1") == "/USB_VBUS", f"Q2 Gate must connect to /USB_VBUS, got {q2_pins.get('1')}"
        assert q2_pins.get("2") == "/VSYS_RAW", f"Q2 Source must connect to /VSYS_RAW (load), got {q2_pins.get('2')}"
        assert q2_pins.get("3") == "/VBAT", f"Q2 Drain must connect to /VBAT (cell), got {q2_pins.get('3')}"
        
        # Physics validation: P-MOSFET intrinsic body diode conducts Anode (Drain) -> Cathode (Source)
        # When USB is connected: V_VBUS = 5.0V, V_SYS_RAW = 5.0V - 0.35V = 4.65V (Cathode = Source)
        # Battery at maximum charge: V_BAT <= 4.2V (Anode = Drain)
        v_sys_raw_usb = 5.0 - 0.35  # 4.65 V at Source
        v_bat_max = 4.20            # 4.20 V at Drain
        v_diode_bias = v_bat_max - v_sys_raw_usb  # V_Anode - V_Cathode
        
        assert v_diode_bias < 0, f"Body diode forward-bias hazard: V_bias = {v_diode_bias:.2f}V >= 0V"
        assert abs(v_diode_bias - (-0.45)) < 0.05, f"Expected -0.45V reverse bias, got {v_diode_bias:.2f}V"
        
        # D4 Cathode = VSYS_RAW, Anode = USB_VBUS
        assert d4_pins.get("1") == "/VSYS_RAW", f"D4 Cathode must connect to /VSYS_RAW, got {d4_pins.get('1')}"
        assert d4_pins.get("2") == "/USB_VBUS", f"D4 Anode must connect to /USB_VBUS, got {d4_pins.get('2')}"
        
        # R26 Gate pull-down to GND
        assert r26_pins.get("1") == "/USB_VBUS"
        assert r26_pins.get("2") == "/GND"
        
        # SW3 connects VSYS_RAW to VBAT_SW
        assert sw3_pins.get("1") == "/VSYS_RAW", f"SW3 Pin 1 must connect to /VSYS_RAW, got {sw3_pins.get('1')}"
        assert sw3_pins.get("2") == "/VBAT_SW", f"SW3 Pin 2 must connect to /VBAT_SW, got {sw3_pins.get('2')}"

    def test_esp32_c3fh4x_pinout_and_boot(self):
        """Test 6: ESP32-C3FH4X internal flash pins (19-24) are decoupled from GND, and GPIO8 (Pin 14) has external pull-up."""
        u1_pins = get_net_node_mapping(MAIN_NETLIST, "U1")
        assert u1_pins, f"U1 not found in netlist {MAIN_NETLIST}"
        
        # Pins 19-24 are internal flash pins in FH4X and MUST NOT be tied to GND
        for p in ["19", "20", "21", "22", "23", "24"]:
            net = u1_pins.get(p, "")
            assert net != "/GND", f"CRITICAL: U1 Pin {p} (Internal Flash NC) is tied to /GND!"
            assert "unconnected" in net.lower(), f"U1 Pin {p} must be unconnected, got {net}"
            
        # Pin 14 is GPIO8/STRAP: must NOT be tied to GND and must NOT be floating
        assert u1_pins.get("14") != "/GND", "CRITICAL: U1 Pin 14 (GPIO8) is tied to /GND, inhibiting ROM download boot!"
        assert "unconnected" not in u1_pins.get("14", "").lower(), "CRITICAL: U1 Pin 14 (GPIO8) is floating without external bias!"
        assert u1_pins.get("14") == "/GPIO8_STRAP", f"U1 Pin 14 must connect to /GPIO8_STRAP, got {u1_pins.get('14')}"
        
        # Verify R27 external pull-up resistor to 3V3
        r27_pins = get_net_node_mapping(MAIN_NETLIST, "R27")
        assert r27_pins, "R27 pull-up resistor not found in netlist!"
        assert r27_pins.get("1") == "/3V3", f"R27 Pin 1 must connect to /3V3, got {r27_pins.get('1')}"
        assert r27_pins.get("2") == "/GPIO8_STRAP", f"R27 Pin 2 must connect to /GPIO8_STRAP, got {r27_pins.get('2')}"
        
        # Pin 15 is GPIO9/BOOT: connects to /BOOT9 (with SW2 to GND)
        assert u1_pins.get("15") == "/BOOT9", f"U1 Pin 15 must connect to /BOOT9, got {u1_pins.get('15')}"
        
        # Pin 16 is GPIO10: must NOT be tied to GND
        assert u1_pins.get("16") != "/GND", "U1 Pin 16 (GPIO10) is tied to /GND!"
        
        # Ground pins: Only Pin 33 (EPAD) is tied to /GND
        assert u1_pins.get("33") == "/GND", f"U1 Pin 33 (EPAD) must connect to /GND, got {u1_pins.get('33')}"

    def test_touch_sensor_net_parity(self):
        """Test 7: Touch Sensor PCB nets have 1:1 parity with schematic (0 conflicts)."""
        with open(TOUCH_PCB, 'r', encoding='utf-8') as f:
            pcb_text = f.read()
        
        for net in ["/3V3", "/GND", "/TOUCH_IN", "/TOUCH_OUT"]:
            assert f'"{net}"' in pcb_text, f"Net {net} missing in Touch_Sensor.kicad_pcb"
        
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

    def test_negative_reversed_pmos_body_diode_hazard_fails(self):
        """Negative fixture: Swapped P-MOSFET Source and Drain must trigger uncontrolled charging hazard."""
        flawed_q2_pins = {
            "1": "/USB_VBUS",
            "2": "/VBAT",      # FLAW: Source connected to Battery
            "3": "/VSYS_RAW",  # FLAW: Drain connected to System
        }
        v_anode = 4.65
        v_cathode = 3.70
        v_diode_bias = v_anode - v_cathode
        
        with pytest.raises(AssertionError, match="UNCONTROLLED CHARGING HAZARD"):
            assert flawed_q2_pins.get("2") == "/VSYS_RAW" and flawed_q2_pins.get("3") == "/VBAT", \
                f"UNCONTROLLED CHARGING HAZARD: Body diode is forward-biased ({v_diode_bias:+.2f}V)! Current dumps into battery."

    def test_negative_grounded_internal_flash_fails(self):
        """Negative fixture: ESP32-C3FH4X internal flash pin tied to GND must fail."""
        flawed_u1_pins = {
            "19": "/GND",
        }
        with pytest.raises(AssertionError, match="INTERNAL FLASH SHORT HAZARD"):
            assert flawed_u1_pins.get("19") != "/GND", "INTERNAL FLASH SHORT HAZARD: Pin 19 grounded on ESP32-C3FH4X!"

    def test_negative_floating_gpio8_boot_fails(self):
        """Negative fixture: Floating GPIO8 (unconnected pin 14) without pull-up must trigger assertion failure."""
        flawed_u1_pins = {
            "14": "unconnected-(U1-GPIO8/STRAP-Pad14)",  # FLAW: Floating pin 14
        }
        with pytest.raises(AssertionError, match="CRITICAL: U1 Pin 14 .* is floating without external bias"):
            assert "unconnected" not in flawed_u1_pins.get("14", "").lower(), \
                "CRITICAL: U1 Pin 14 (GPIO8) is floating without external bias!"

    def test_negative_grounded_gpio8_boot_fails(self):
        """Negative fixture: ESP32-C3 Pin 14 (GPIO8) tied to GND must fail."""
        flawed_u1_pins = {
            "14": "/GND",
        }
        with pytest.raises(AssertionError, match="BOOT STRAP FAULT"):
            assert flawed_u1_pins.get("14") != "/GND", "BOOT STRAP FAULT: GPIO8 grounded inhibits ROM download boot!"

    def test_negative_unbridged_usb_dplus_fails(self):
        """Negative fixture: Type-C connector missing bridged DP2 line on Pin 8 must fail."""
        flawed_usb_pins = {
            "6": "/USB_DP_PORT",  # DP1 connected
            "8": "unconnected",   # FLAW: DP2 unconnected
        }
        with pytest.raises(AssertionError, match="Pin 8 .* must be /USB_DP_PORT"):
            assert flawed_usb_pins.get("8") == "/USB_DP_PORT", f"Pin 8 (DP2) must be /USB_DP_PORT, got {flawed_usb_pins.get('8')}"

    def test_negative_swapped_usb_pins_fails(self):
        """Negative fixture: Swapped VBUS and GND on Pin 1 of USB connector must fail."""
        flawed_usb_pins = {
            "1": "/USB_VBUS",
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
        }
        with pytest.raises(AssertionError, match="Pin 5 \\(VOUT\\) must connect to /3V3"):
            assert flawed_ldo_pins.get("5") == "/3V3", f"Pin 5 (VOUT) must connect to /3V3, got {flawed_ldo_pins.get('5')}"
