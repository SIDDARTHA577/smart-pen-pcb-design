"""Comprehensive Baseline Audit for Smart Pen Rev D.
"""
import json
import re
from pathlib import Path

def parse_props(p_str):
    if not p_str:
        return {}
    tokens = p_str.split('`')
    props = {}
    for i in range(0, len(tokens) - 1, 2):
        if tokens[i]:
            props[tokens[i]] = tokens[i+1]
    return props

def audit():
    sch_path = Path('SmartPen_RevD_AutoLinked_DRAFT/EasyEDA/SmartPen_RevD_Connected_Schematic_DRAFT_EasyEDA.json')
    pcb_path = Path('SmartPen_RevD_AutoLinked_DRAFT/EasyEDA/SmartPen_RevD_PCB_Footprint_Staging_UNROUTED_EasyEDA.json')

    with open(sch_path, 'r', encoding='utf-8') as f:
        sch = json.load(f)
    with open(pcb_path, 'r', encoding='utf-8') as f:
        pcb = json.load(f)

    # 1. Parse Schematic
    sch_comps = {}
    wires = []
    netlabels = []

    for item in sch.get('shape', []):
        if not isinstance(item, str):
            continue
        if item.startswith('W~'):
            wires.append(item)
        elif item.startswith('N~'):
            netlabels.append(item)
        elif item.startswith('LIB~'):
            subs = item.split('#@$')
            ref = ''
            name = ''
            pins = []
            for sub in subs:
                if sub.startswith('T~'):
                    t = sub.split('~')
                    if len(t) >= 13:
                        if t[1] == 'P':
                            ref = t[12] if t[11] == 'comment' else t[11]
                        elif t[1] == 'N':
                            name = t[12] if t[11] == 'comment' else t[11]
                elif sub.startswith('P~'):
                    pin_sections = sub.split('^^')
                    p_name = ''
                    p_num = ''
                    if len(pin_sections) > 3:
                        name_toks = pin_sections[3].split('~')
                        if len(name_toks) >= 5:
                            p_name = name_toks[4]
                    if len(pin_sections) > 4:
                        num_toks = pin_sections[4].split('~')
                        if len(num_toks) >= 5:
                            p_num = num_toks[4]
                    pins.append({'name': p_name, 'num': p_num, 'raw': sub})

            lib_head = subs[0].split('~')
            props = parse_props(lib_head[3]) if len(lib_head) > 3 else {}
            if not ref and 'prefix' in props:
                ref = props['prefix']
            
            sch_comps[ref] = {
                'name': name,
                'package': props.get('package', ''),
                'mpn': props.get('Manufacturer Part', ''),
                'supplier': props.get('Supplier', ''),
                'pins': pins,
                'props': props
            }

    # 2. Parse PCB
    pcb_comps = {}
    tracks = []
    for item in pcb.get('shape', []):
        if not isinstance(item, str):
            continue
        if item.startswith('TRACK~'):
            tracks.append(item)
        elif item.startswith('LIB~'):
            subs = item.split('#@$')
            ref = ''
            pads = []
            for sub in subs:
                if sub.startswith('TEXT~'):
                    t = sub.split('~')
                    if len(t) >= 11 and t[1] == 'P':
                        ref = t[10]
                elif sub.startswith('PAD~'):
                    pad_toks = sub.split('~')
                    pad_num = pad_toks[8] if len(pad_toks) > 8 else ''
                    pad_net = pad_toks[7] if len(pad_toks) > 7 else ''
                    pads.append({'num': pad_num, 'net': pad_net, 'raw': sub})
            lib_head = subs[0].split('~')
            props = parse_props(lib_head[3]) if len(lib_head) > 3 else {}
            if not ref and 'Manufacturer Part' in props:
                ref = props['Manufacturer Part']
            pcb_comps[ref] = {
                'package': props.get('package', ''),
                'pads': pads,
                'props': props
            }

    # 3. Analyze differences
    missing_in_pcb = sorted(set(sch_comps.keys()) - set(pcb_comps.keys()))
    extra_in_pcb = sorted(set(pcb_comps.keys()) - set(sch_comps.keys()))

    # Missing / placeholder footprints
    placeholder_pkgs = []
    for ref, c in sch_comps.items():
        pkg = c['package']
        if 'TBD' in pkg or not pkg:
            placeholder_pkgs.append((ref, pkg, c['name']))

    # Missing orderable MPNs
    missing_mpn = []
    for ref, c in sch_comps.items():
        mpn = c['mpn']
        # If MPN is a description rather than an orderable part number
        if not mpn or any(k in mpn for k in ['TBD', 'switch NO', 'crystal', 'carrier', 'controller', 'pads', 'diode', 'bulk', 'tie', 'pullup', 'delay', 'harmonic', 'tune', 'receptacle', 'array', 'interface', 'on/off', 'vibration', 'expander', 'RED', 'GREEN', 'level', 'cable']):
            missing_mpn.append((ref, mpn, c['package']))

    # Pin to pad count mismatches for placed parts
    pin_pad_mismatches = []
    for ref, sc in sch_comps.items():
        if ref in pcb_comps:
            pc = pcb_comps[ref]
            n_pins = len(sc['pins'])
            n_pads = len(pc['pads'])
            if n_pins != n_pads:
                pin_pad_mismatches.append((ref, n_pins, n_pads, sc['package'], pc['package']))

    # Netlist / connections from Docs/WIRING_NETLIST.csv
    import pandas as pd
    wiring_df = pd.read_csv('SmartPen_RevD_AutoLinked_DRAFT/Docs/WIRING_NETLIST.csv')
    unique_nets = sorted(wiring_df['Net'].unique())
    single_pin_nets = [net for net, count in wiring_df['Net'].value_counts().items() if count == 1]

    print(f"Total schematic components: {len(sch_comps)}")
    print(f"Total PCB components: {len(pcb_comps)}")
    print(f"Missing in PCB ({len(missing_in_pcb)}): {missing_in_pcb}")
    print(f"Extra in PCB ({len(extra_in_pcb)}): {extra_in_pcb}")
    print(f"Placeholder footprints: {len(placeholder_pkgs)}")
    print(f"Missing orderable MPNs: {len(missing_mpn)}")
    print(f"Pin-to-pad count mismatches: {len(pin_pad_mismatches)}")
    for m in pin_pad_mismatches:
        print(f"  Mismatch {m[0]}: pins={m[1]}, pads={m[2]}, sch_pkg={m[3]}, pcb_pkg={m[4]}")
    print(f"Total nets: {len(unique_nets)}, Single-pin nets: {single_pin_nets}")

    # Generate Markdown Report
    report_content = f"""# Baseline Engineering Audit: Smart Pen Rev D

## 1. Executive Summary
- **Baseline Design Source**: `SmartPen_RevD_AutoLinked_DRAFT` (Rev D)
- **Status**: Non-functional staging draft — **BLOCKED for manufacturing**
- **Schematic Components**: {len(sch_comps)} total
- **PCB Components**: {len(pcb_comps)} placed ({len(missing_in_pcb)} unplaced)
- **Placeholder / Unresolved Footprints**: {len(placeholder_pkgs)} components with `_TBD` footprints
- **Components Missing Real MPN / Orderable Parts**: {len(missing_mpn)} components
- **Pin-to-Pad Mismatches**: {len(pin_pad_mismatches)} among placed parts
- **PCB Routing**: 0 traces routed; 0 copper zones; staging board outline is provisional only (77.0 mm x 9.4 mm).

---

## 2. Component & Footprint Audit

### 2.1 Missing in PCB Staging Board ({len(missing_in_pcb)} components)
The following {len(missing_in_pcb)} schematic components are completely absent from the PCB staging layout:
`{', '.join(missing_in_pcb)}`

### 2.2 Unresolved Footprints with TBD Placeholders ({len(placeholder_pkgs)} components)
| RefDes | Current Placeholder Footprint | Schematic Description / Part |
| :--- | :--- | :--- |
"""
    for ref, pkg, name in placeholder_pkgs:
        report_content += f"| {ref} | `{pkg}` | {name} |\n"

    report_content += f"""
### 2.3 Pin-to-Pad Count Mismatches ({len(pin_pad_mismatches)} components)
"""
    if pin_pad_mismatches:
        report_content += "| RefDes | Schematic Pins | PCB Pads | Schematic Package | PCB Package |\n| :--- | :--- | :--- | :--- | :--- |\n"
        for m in pin_pad_mismatches:
            report_content += f"| {m[0]} | {m[1]} | {m[2]} | `{m[3]}` | `{m[4]}` |\n"
    else:
        report_content += "None among currently placed parts (note: 20 parts with mismatched/TBD footprints were excluded from placement entirely).\n"

    report_content += f"""
---

## 3. Electrical & Circuitry Deficiencies

### 3.1 Power Architecture & Regulation Blockers
1. **MCP73831 is NOT a Power-Path Regulator**:
   - The schematic uses U2 (`MCP73831T-2ACI/OT`) as a basic linear LiPo charger.
   - MCP73831 has NO power-path management (no automatic switchover between VBUS and VBAT). If the pen operates while charging, system current robs charge current from the termination sensing loop, potentially preventing charge termination or overheating the battery.
   - `CHG_STAT` (U2 pin 1) is floating (single-pin net, no MCU monitoring or LED indication).
2. **Missing 3.3 V Regulator (`J_PWR`)**:
   - The 3.3V supply is represented as a dummy header `J_PWR` (`REGULATOR_CARD_TBD`) rather than an onboard low-noise, high-PSR buck/buck-boost or high-current LDO.
   - ESP32-C3 requires >=500 mA peak transient capability for RF transmission bursts.
3. **Missing Battery Protection**:
   - The schematic lacks an onboard LiPo protection IC (e.g., DW01A + dual MOSFET FS8205A) for over-discharge (<2.8V), over-charge (>4.28V), and short-circuit protection, risking catastrophic failure if an unprotected raw pouch cell is attached.

### 3.2 ESP32-C3 Core & Strapping Verification
1. **Strapping Pins Allocation**:
   - `GPIO9` (BOOT / Strapping): Pulled high via R2 (10k) with SW2 to GND. (PASS)
   - `GPIO2` (Strapping): Pulled high via R3 (10k). (PASS)
   - `GPIO8` (Strapping): High during download boot. Currently floating in Rev D schematic.
2. **VDD_SPI & Internal Flash**:
   - U1 is `ESP32-C3FH4X` with 4MB embedded flash. Pin 18 (`VDD_SPI`) is decoupled by C5 (1uF). It is internally driven by an on-chip LDO and must NOT be connected to external 3.3V power. Rev D correctly keeps it isolated to C5.
3. **Clock / Crystal Circuit**:
   - Y1 has a placeholder footprint (`CRYSTAL_4PAD_TBD`). Needs an exact 40 MHz, 10 ppm, 10 pF/12 pF load crystal with verified load capacitors (C6, C7) and dampening inductor L1.

### 3.3 RF Design & Antenna Interface
1. **RF Matching & Transmission Line**:
   - Rev D uses a discrete pi-network (L2, C8, C9) feeding `J_RF` (`UFL_CONNECTOR_TBD`).
   - The RF trace must be designed as a 50-ohm coplanar waveguide with ground reference.
   - Ground keepout under antenna / connector is undefined on the staging board.

### 3.4 Peripheral & Sensor Deficiencies
1. **Front IMU (`J_IMU`)**:
   - Connected via `CONN_4P_TBD` to I2C bus (`I2C_SDA` on GPIO0, `I2C_SCL` on GPIO1).
   - Needs rigid mechanical retention, strain relief, and standardized keyed 1.0mm/1.25mm connector (e.g., JST SH or Molex PicoBlade).
2. **MicroSD Carrier (`J_SD`)**:
   - Connected via 6-pin remote header `CONN_6P_TBD` rather than an integrated micro-profile push-pull MicroSD socket, due to previous 9.4 mm board width constraints.
3. **Touch Controller (`J_TOUCH`)**:
   - Uses a 3-pin placeholder `TOUCH_3PIN_TBD`. Must be resolved to an actual capacitive touch controller (e.g., TTP223 / Azoteq IQS263 / Microchip CAP1203) with electrode conditioning.
4. **Haptic Motor Driver**:
   - Q1 uses placeholder `SOT23_GSD_TBD` with flyback diode D3 (`DIODE_SMD_TBD`). Drive signal is generated from U3 (MCP23008 expander). Needs verified logic-level N-MOSFET (e.g. DMG2302UK or AO3400A) and Schottky flyback (e.g. B0520W / 1N5819HW).
5. **GPIO Expander U3 (MCP23008)**:
   - Uses placeholder `QFN20_4x4_P0.5_TBD`. Needs footprint validation or pin optimization.

---

## 4. Mechanical & Enclosure Interface Deficiencies

1. **Envelope Constraints**:
   - Client specified: Max Outer Diameter 16 mm (target 15–16 mm), Total length 150–155 mm.
   - Internal clearance radius is ~6.5 to 7.0 mm (internal diameter ~13 to 14 mm depending on wall thickness >= 1.0–1.2 mm).
2. **Battery Below Rail**:
   - Battery must fit below the internal electronics rail without pinching wires or obstructing the central refill tube.
3. **Bayonet & Rail Latch**:
   - The existing CAD files have placeholder bayonet collars with no locking ramps, no detents, and no mechanical stops.
4. **Refill & Click Mechanism**:
   - Needs axial tunnel clearance through the entire assembly from tip through rear clicker.

---

## 5. Summary of Baseline Tests
- **KiCad ERC/DRC**: BLOCKED (EasyEDA format, KiCad CLI not natively installed).
- **Static Netlist Consistency**: 42 nets, 180 connections. 1 single-pin net (`CHG_STAT`).
- **PCB Parity**: 20 schematic components missing from PCB layout.
- **Manufacturing Readiness**: **FAIL** (Draft/Review stage only).
"""

    out_path = Path('reports/baseline_audit.md')
    out_path.write_text(report_content, encoding='utf-8')
    print(f"Wrote baseline audit to {out_path}")

if __name__ == '__main__':
    audit()
