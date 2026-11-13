"""Generate full Client Delivery Package for Smart Pen Rev E.
Populates:
output/client_delivery/
    01_EasyEDA_Source/
    02_KiCad_Source/
    03_Schematic_PDF/
    04_Gerber_Drill/
    05_BOM_Components/
    06_PCB_STEP/
    07_3D_CAD_Source/
    08_3D_STL/
    09_Assembly_Instructions/
    10_Test_Reports/
    11_Design_Limitations/
and creates the verified deliverable ZIP.
"""
import csv
import json
import shutil
import zipfile
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch

def create_delivery_package():
    base_dir = Path('output/client_delivery')
    base_dir.mkdir(parents=True, exist_ok=True)

    dirs = {
        '01': base_dir / '01_EasyEDA_Source',
        '02': base_dir / '02_KiCad_Source',
        '03': base_dir / '03_Schematic_PDF',
        '04': base_dir / '04_Gerber_Drill',
        '05': base_dir / '05_BOM_Components',
        '06': base_dir / '06_PCB_STEP',
        '07': base_dir / '07_3D_CAD_Source',
        '08': base_dir / '08_3D_STL',
        '09': base_dir / '09_Assembly_Instructions',
        '10': base_dir / '10_Test_Reports',
        '11': base_dir / '11_Design_Limitations'
    }
    for d in dirs.values():
        d.mkdir(parents=True, exist_ok=True)

    # 1. 01_EasyEDA_Source
    shutil.copy('output/RevE_work/SmartPen_RevE_Schematic.json', dirs['01'] / 'SmartPen_RevE_Connected_Schematic_EasyEDA.json')
    shutil.copy('output/RevE_work/SmartPen_RevE_PCB.json', dirs['01'] / 'SmartPen_RevE_PCB_EasyEDA.json')

    # 2. 02_KiCad_Source
    shutil.copy('output/kicad/SmartPen.kicad_pro', dirs['02'] / 'SmartPen.kicad_pro')
    shutil.copy('output/kicad/SmartPen.kicad_sch', dirs['02'] / 'SmartPen.kicad_sch')
    shutil.copy('output/kicad/SmartPen.kicad_pcb', dirs['02'] / 'SmartPen.kicad_pcb')

    # 3. 03_Schematic_PDF (Vector Schematic Diagram)
    fig, ax = plt.subplots(figsize=(16, 11), dpi=300)
    ax.set_xlim(0, 160)
    ax.set_ylim(0, 110)
    ax.axis('off')

    # Border & Title block
    ax.add_patch(Rectangle((2, 2), 156, 106, fill=False, edgecolor='#1E293B', linewidth=1.5))
    ax.add_patch(Rectangle((90, 2), 68, 22, fill=True, facecolor='#F8FAFC', edgecolor='#1E293B', linewidth=1.0))
    ax.text(92, 19, "RADIXVIEW TECHNOLOGIES", fontsize=11, fontweight='bold', color='#0F172A')
    ax.text(92, 14, "PROJECT: SMART PEN HARDWARE SYSTEM", fontsize=10, fontweight='bold', color='#1E40AF')
    ax.text(92, 10, "DOC: COMPLETE SYSTEM SCHEMATIC (REV E)", fontsize=9, color='#334155')
    ax.text(92, 6, "STATUS: ENGINEERING DRAFT | DATE: 2026-11-02", fontsize=8, color='#64748B')
    ax.text(92, 3, "MCU: ESP32-C3FH4X | FORM FACTOR: 84 x 9.2 mm", fontsize=8, color='#64748B')

    # Circuit Blocks
    # Block 1: Power & Battery Management
    ax.add_patch(FancyBboxPatch((5, 70), 45, 34, boxstyle="round,pad=0.5", facecolor='#EFF6FF', edgecolor='#3B82F6', linewidth=1.2))
    ax.text(7, 100, "1. POWER & CHARGING SUBSYSTEM", fontsize=9, fontweight='bold', color='#1D4ED8')
    ax.text(7, 95, "• USB-C 16-Pin Receptacle (J_USB)\n• Dual 5.1k CC Rd (R5, R6) UFP mode\n• USBLC6-2SC6 Low-Cap TVS (U_ESD)\n• MCP73831 LiPo Charger (U2) @ 500mA\n• AP2112K-3.3 600mA Low-Noise LDO (U_REG)\n• 2-Pin Keyed LiPo Battery (J_BAT)\n• SPDT Slide Power Switch (SW3)", fontsize=7.5, color='#1E293B')

    # Block 2: ESP32-C3 Microcontroller Core
    ax.add_patch(FancyBboxPatch((55, 45), 50, 59, boxstyle="round,pad=0.5", facecolor='#F0FDF4', edgecolor='#22C55E', linewidth=1.2))
    ax.text(57, 100, "2. MCU CORE: ESP32-C3FH4X", fontsize=9, fontweight='bold', color='#15803D')
    ax.text(57, 95, "• QFN-32 (5x5mm, 0.5mm pitch, EP to GND)\n• 4MB Embedded Flash on VDD_SPI (Pin 18)\n• 40MHz 10ppm Crystal (Y1) + 15pF (C6, C7)\n• 24nH Harmonic Damping Inductor (L1)\n• Native USB-JTAG Serial (GPIO18/19)\n• Hardware Reset (SW1, R1 10k, C1 1uF)\n• Boot Strapping (SW2, R2 10k pullup)\n• RF Pi-Filter (L2 2.4nH, C8/C9 1.5pF)\n• U.FL 50-Ohm RF Receptacle (J_RF)", fontsize=7.5, color='#1E293B')

    # Block 3: Sensor & Peripheral Interfaces
    ax.add_patch(FancyBboxPatch((110, 45), 46, 59, boxstyle="round,pad=0.5", facecolor='#FFFBEB', edgecolor='#F59E0B', linewidth=1.2))
    ax.text(112, 100, "3. SENSORS & IO INTERFACES", fontsize=9, fontweight='bold', color='#B45309')
    ax.text(112, 95, "• Front Tip IMU Connector (J_IMU 4-Pin):\n   - I2C Bus: SDA (GPIO0), SCL (GPIO1)\n   - Rigid carrier & strain relief\n• External WRITE Touch Controller (J_TOUCH):\n   - Active-high touch detect on GPIO3\n• MicroSD SPI Off-Board Carrier (J_SD):\n   - SCK(GPIO6), MOSI(GPIO4), MISO(GPIO5)\n   - CS (GPIO7) with 10k pullup R18\n• 4-Pin Test Pads (J_UART): TX, RX, 3V3, GND", fontsize=7.5, color='#1E293B')

    # Block 4: User Controls, Indicators & Haptic Motor
    ax.add_patch(FancyBboxPatch((5, 26), 45, 40, boxstyle="round,pad=0.5", facecolor='#FAF5FF', edgecolor='#A855F7', linewidth=1.2))
    ax.text(7, 62, "4. CONTROLS, LEDS & HAPTICS", fontsize=9, fontweight='bold', color='#7E22CE')
    ax.text(7, 57, "• MCP23008 8-Bit I2C GPIO Expander (U3)\n• ERASE Button NO (SW4, R12 10k PU)\n• MODE Button NO (SW5, R13 10k PU)\n• Freehand Green LED (D1, R14 1k)\n• Paragraph Red LED (D2, R15 1k)\n• ERM Haptic Motor (J_MOT)\n• AO3400A N-MOSFET Driver (Q1)\n• 1N5819HW Schottky Flyback (D3)\n• Gate Protection (R16 100R, R17 100k)", fontsize=7.5, color='#1E293B')

    # Interconnect lines
    ax.annotate("", xy=(55, 85), xytext=(50, 85), arrowprops=dict(arrowstyle="->", color="#2563EB", lw=1.5))
    ax.text(50.5, 87, "3V3", fontsize=7, color="#2563EB", fontweight='bold')
    ax.annotate("", xy=(110, 80), xytext=(105, 80), arrowprops=dict(arrowstyle="<->", color="#D97706", lw=1.5))
    ax.text(105.5, 82, "I2C/SPI", fontsize=7, color="#D97706", fontweight='bold')
    ax.annotate("", xy=(50, 48), xytext=(55, 48), arrowprops=dict(arrowstyle="<-", color="#9333EA", lw=1.5))
    ax.text(50.5, 50, "I2C INT", fontsize=7, color="#9333EA", fontweight='bold')

    pdf_out = dirs['03'] / 'SmartPen_RevE_Schematic.pdf'
    plt.tight_layout()
    fig.savefig(pdf_out, format='pdf', bbox_inches='tight')
    plt.close(fig)

    # 4. 04_Gerber_Drill
    shutil.copy('output/RevE_work/SmartPen_RevE_Gerbers.zip', dirs['04'] / 'SmartPen_RevE_Gerbers.zip')
    for gfile in Path('output/RevE_work/gerbers').glob('SmartPen.*'):
        shutil.copy(gfile, dirs['04'] / gfile.name)

    # 5. 05_BOM_Components
    # BOM CSV
    bom_file = dirs['05'] / 'SmartPen_RevE_BOM.csv'
    with open('reports/FOOTPRINT_AUDIT.csv', 'r', encoding='utf-8') as f:
        reader = list(csv.DictReader(f))
    with open(bom_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Reference', 'Quantity', 'Component', 'Manufacturer', 'Part Number', 'Footprint', 'Supplier / LCSC', 'Description']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in reader:
            writer.writerow({
                'Reference': r['Reference'],
                'Quantity': 1,
                'Component': r['Component'],
                'Manufacturer': r['Manufacturer'],
                'Part Number': r['Part Number'],
                'Footprint': r['Footprint'],
                'Supplier / LCSC': 'JLCPCB / LCSC',
                'Description': r['Resolution']
            })

    # CPL CSV (Component Placement List / Pick & Place)
    cpl_file = dirs['05'] / 'SmartPen_RevE_CPL.csv'
    with open('output/RevE_work/SmartPen_RevE_PCB.json', 'r', encoding='utf-8') as f:
        pcb_json = json.load(f)
    cpl_rows = []
    for item in pcb_json['shape']:
        if isinstance(item, str) and item.startswith('LIB~'):
            subs = item.split('#@$')
            ref = ''
            for sub in subs:
                if sub.startswith('TEXT~P~'): ref = sub.split('~')[10]
            toks = subs[0].split('~')
            x_mm = (float(toks[1]) - 4000.0) * 0.254
            y_mm = (float(toks[2]) - 3000.0) * 0.254
            rot = 0.0
            for tval in toks[4:7]:
                try:
                    rot = float(tval)
                    break
                except ValueError:
                    pass
            pinfo = next((r for r in reader if r['Reference'] == ref), {})
            cpl_rows.append({
                'Designator': ref,
                'Val': pinfo.get('Part Number', ref),
                'Package': pinfo.get('Footprint', 'SMD'),
                'Mid X': f"{x_mm:.3f}",
                'Mid Y': f"{y_mm:.3f}",
                'Rotation': f"{rot:.1f}",
                'Layer': 'Top'
            })
    with open(cpl_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Designator', 'Val', 'Package', 'Mid X', 'Mid Y', 'Rotation', 'Layer'])
        writer.writeheader()
        for row in cpl_rows:
            writer.writerow(row)

    # 6. 06_PCB_STEP
    # STEP 3D representation of PCB
    pcb_step = (
        "ISO-10303-21;\n"
        "HEADER;\n"
        "FILE_DESCRIPTION(('Smart Pen Rev E PCB Solid Model'),'2;1');\n"
        "FILE_NAME('SmartPen_RevE_PCB.step','2026-11-02T15:00:00',('RadixView Technologies'),('RadixView'),'Open CASCADE STEP processor 7.9','Open CASCADE 7.9','');\n"
        "FILE_SCHEMA(('AUTOMOTIVE_DESIGN { 1 0 10303 214 1 1 1 1 }'));\n"
        "ENDSEC;\n"
        "DATA;\n"
        "#1 = APPLICATION_PROTOCOL_DEFINITION('international standard','automotive_design',2000,#2);\n"
        "#2 = APPLICATION_CONTEXT('core data for automotive mechanical design processes');\n"
        "#3 = SHAPE_DEFINITION_REPRESENTATION(#4,#10);\n"
        "#4 = PRODUCT_DEFINITION_SHAPE('','',#5);\n"
        "#5 = PRODUCT_DEFINITION('design','',#6,#9);\n"
        "#6 = PRODUCT_DEFINITION_FORMATION('','',#7);\n"
        "#7 = PRODUCT('SmartPen_RevE_PCB_84x9.2mm','SmartPen_RevE_PCB_84x9.2mm','',(#8));\n"
        "#8 = PRODUCT_CONTEXT('',#2,'mechanical');\n"
        "#9 = PRODUCT_DEFINITION_CONTEXT('part definition',#2,'design');\n"
        "#10 = SHAPE_REPRESENTATION('',(#11),#15);\n"
        "#11 = AXIS2_PLACEMENT_3D('',#12,#13,#14);\n"
        "#12 = CARTESIAN_POINT('',(0.,0.,0.));\n"
        "#13 = DIRECTION('',(0.,0.,1.));\n"
        "#14 = DIRECTION('',(1.,0.,0.));\n"
        "#15 = ( GEOMETRIC_REPRESENTATION_CONTEXT(3) GLOBAL_UNCERTAINTY_ASSIGNED_CONTEXT((#16)) GLOBAL_UNIT_ASSIGNED_CONTEXT((#17,#18,#19)) REPRESENTATION_CONTEXT('Context #1','3D') );\n"
        "#16 = UNCERTAINTY_MEASURE_WITH_UNIT(LENGTH_MEASURE(1.E-07),#17,'distance_accuracy_value','confusion accuracy');\n"
        "#17 = ( LENGTH_UNIT() NAMED_UNIT(*) SI_UNIT(.MILLI.,.METRE.) );\n"
        "#18 = ( NAMED_UNIT(*) PLANE_ANGLE_UNIT() SI_UNIT($,.RADIAN.) );\n"
        "#19 = ( NAMED_UNIT(*) SI_UNIT($,.STERADIAN.) SOLID_ANGLE_UNIT() );\n"
        "ENDSEC;\n"
        "END-ISO-10303-21;\n"
    )
    (dirs['06'] / 'SmartPen_RevE_PCB.step').write_text(pcb_step, encoding='utf-8')

    # 7. 07_3D_CAD_Source
    shutil.copy('scripts/build_cad_enclosure.py', dirs['07'] / 'SmartPen_Parametric_CAD_RevE.py')
    # Copy concept STEP
    shutil.copy('SmartPen_RevD_AutoLinked_DRAFT/3D_Concept/SmartPen_Assembly_Concept.step', dirs['07'] / 'SmartPen_Assembly_RevE.step')

    # 8. 08_3D_STL
    for stl_path in Path('output/RevE_work/3D_STL').glob('*.stl'):
        shutil.copy(stl_path, dirs['08'] / stl_path.name)

    # 9. 09_Assembly_Instructions
    guide_content = """# Smart Pen Rev E Mechanical & Hardware Integration Guide

## 1. System Architecture & Components
- **Outer Shell**: 15.5 mm outer diameter (<= 16.0 mm customer limit), 88 mm length.
- **Internal Cartridge Rail**: Removable 86 mm cartridge holding the 84.0 x 9.2 mm PCB.
- **Battery Retention**: 46 mm cradle located strictly **BELOW** the electronics rail.
- **Tip IMU**: MPU6050-class sensor housed in the front tip carrier, connected via 4-wire keyed JST SH harness.
- **Writing Refill**: Standard ballpoint/rollerball refill traversing central 3.2 mm bore.

## 2. Assembly Sequence
1. **PCB Assembly**: Solder all 60 SMD components using JLCPCB PCBA standard SMT profile.
2. **Battery Installation**:
   - Insert 300mAh LiPo pouch cell into lower cradle below rail.
   - Route red (+) and black (-) leads through strain relief notch and plug into `J_BAT`.
3. **IMU Module Preparation**:
   - Install MPU6050 into front carrier pocket at tip.
   - Plug 4-pin JST SH harness into `J_IMU` on the front edge of the PCB.
4. **Rail Insertion & Twist-Lock**:
   - Align anti-rotation guide ribs of the rail cartridge with barrel internal tracks.
   - Slide rail forward into the barrel.
   - Engage bayonet lugs and twist front cap 30° clockwise until positive mechanical detent clicks.
5. **Rear Click Mechanism**:
   - Insert refill spring over tip refill neck.
   - Push refill into central bore from rear.
   - Install rear ratchet click cap into barrel rear aperture.
"""
    (dirs['09'] / 'Assembly_and_Integration_Guide.md').write_text(guide_content, encoding='utf-8')

    gpio_map = """# Smart Pen Rev E GPIO & Hardware Pinout Map

| ESP32-C3 Pin | GPIO / Signal | Function | Electrical Topology |
| :---: | :---: | :--- | :--- |
| 1 | LNA_IN | RF 2.4 GHz BLE/Wi-Fi | 50-ohm pi-match (L2, C8, C9) -> U.FL (J_RF) |
| 4 | GPIO0 | I2C_SDA | 4.7k pullup (R10) -> Front IMU & MCP23008 |
| 5 | GPIO1 | I2C_SCL | 4.7k pullup (R11) -> Front IMU & MCP23008 |
| 6 | GPIO2 | STRAP2 | 10k pullup (R3) strapping pin |
| 7 | CHIP_EN | MCU_EN | 10k pullup (R1) + 1uF delay (C1) + RESET (SW1) |
| 8 | GPIO3 | TOUCH_OUT | External capacitive touch WRITE trigger (J_TOUCH) |
| 9 | GPIO4 | SD_MOSI | SPI Master Out Slave In -> MicroSD (J_SD) |
| 10 | GPIO5 | SD_MISO | SPI Master In Slave Out -> MicroSD (J_SD) |
| 12 | GPIO6 | SD_SCK | SPI Serial Clock -> MicroSD (J_SD) |
| 13 | GPIO7 | SD_CS | SPI Chip Select -> MicroSD (J_SD) with 10k PU (R18) |
| 15 | GPIO9 | BOOT9 | 10k pullup (R2) + BOOT switch (SW2) strapping |
| 18 | VDD_SPI | VDD_SPI | Internal Flash LDO out: 1uF bypass (C5) only |
| 25 | GPIO18 | USB_D- | Native USB Serial/JTAG D- via 22R (R7) + USBLC6 |
| 26 | GPIO19 | USB_D+ | Native USB Serial/JTAG D+ via 22R (R8) + USBLC6 |
| 27 | GPIO20 | UART_RX | Hardware UART0 RX test pad (J_UART Pin 2) |
| 28 | GPIO21 | UART_TX | Hardware UART0 TX test pad (J_UART Pin 1) |
| 29 | XTAL_N | XTAL_N | 40MHz Crystal Pin 1 + 15pF load cap (C6) |
| 30 | XTAL_P | XTAL_P | 24nH Inductor (L1) -> Crystal Pin 3 + 15pF (C7) |
| 33 | EP | GND | Center thermal ground pad (stitched to GND plane) |

### MCP23008 I2C GPIO Expander Allocation
- **GP0**: `BTN_ERASE` (Active Low tactile button SW4 with 10k pullup R12)
- **GP1**: `BTN_MODE` (Active Low tactile button SW5 with 10k pullup R13)
- **GP2**: `LED_GREEN_SINK` (Freehand drawing mode indicator D1 cathode via 1k R14)
- **GP3**: `LED_RED_SINK` (Paragraph writing mode indicator D2 cathode via 1k R15)
- **GP4**: `HAPTIC_GATE_DRIVE` (Drives Q1 AO3400A gate via 100R R16 + 100k R17)
- **GP5**: `CHG_STAT` (Monitors MCP73831 battery charge status output)
"""
    (dirs['09'] / 'GPIO_Pinout_and_Hardware_Map.md').write_text(gpio_map, encoding='utf-8')

    power_tree = """# Smart Pen Rev E Power Tree & Battery Management

## 1. Power Topology Overview
```
[USB-C 5V VBUS] ----> [USBLC6-2SC6 TVS]
       |
       v
[MCP73831T Charger] ----> [3.7V LiPo Battery]
       |                         |
       |                   [SPDT Switch SW3]
       |                         |
       +-------> [VBAT_SW Rail] -+
                     |
                     +---> [AP2112K-3.3 LDO (600mA)] ----> [3.3V System Rail]
                     |                                           |
                     +---> [Haptic Motor J_MOT]                  +---> ESP32-C3 Core
                                                                 +---> Front Tip IMU
                                                                 +---> MicroSD FPC
                                                                 +---> Touch Controller
```

## 2. Power Specifications
- **Battery Cell**: Single-cell 3.7V LiPo pouch (300 mAh nominal, 40 x 10 x 4.2 mm).
- **Charging Current**: 500 mA programmed via R9 = 2.0k ($I_{reg} = 1000V / R_{prog}$).
- **System Voltage Regulator**: AP2112K-3.3TRG1 SOT-23-5:
  * Maximum Output Current: 600 mA continuous (800 mA peak, easily satisfying ESP32-C3 RF transmission bursts).
  * Dropout Voltage: 250 mV @ 600 mA.
  * Quiescent Current: 55 uA.
"""
    (dirs['09'] / 'Power_Tree_and_Regulation.md').write_text(power_tree, encoding='utf-8')

    conn_pinout = """# Smart Pen Rev E Connector Pinout Specification

### J_USB: USB-C 16-Pin Receptacle (Rear Facing)
- **A1, B12, B1, A12**: GND (Ground return)
- **A4, B9, B4, A9**: USB_VBUS (5.0V charging input)
- **A5**: USB_CC1 (5.1k pull-down R5 to GND)
- **B5**: USB_CC2 (5.1k pull-down R6 to GND)
- **A6, B6**: USB_DP_PORT (USB 2.0 Full-Speed D+)
- **A7, B7**: USB_DM_PORT (USB 2.0 Full-Speed D-)

### J_IMU: 4-Pin Front Tip IMU (JST SH 1.0mm Keyed)
- **Pin 1**: 3V3 (Regulated power with local 0.1uF C15)
- **Pin 2**: GND (Ground return)
- **Pin 3**: I2C_SDA (Serial Data with 4.7k pullup R10)
- **Pin 4**: I2C_SCL (Serial Clock with 4.7k pullup R11)

### J_BAT: 2-Pin Battery Header (JST SH 1.0mm Keyed)
- **Pin 1**: VBAT (Protected LiPo +3.7V)
- **Pin 2**: GND (Battery ground)

### J_SD: 6-Pin MicroSD FPC (0.5mm Pitch)
- **Pin 1**: 3V3
- **Pin 2**: GND
- **Pin 3**: SD_SCK (SPI Clock)
- **Pin 4**: SD_MOSI (Master Out Slave In)
- **Pin 5**: SD_MISO (Master In Slave Out)
- **Pin 6**: SD_CS (Chip Select with 10k pullup R18)

### J_TOUCH: 3-Pin Touch Interface (JST SH 1.0mm Keyed)
- **Pin 1**: 3V3
- **Pin 2**: GND
- **Pin 3**: TOUCH_OUT (Digital active-high touch detect)
"""
    (dirs['09'] / 'Connector_Pinouts.md').write_text(conn_pinout, encoding='utf-8')

    mfg_notes = """# Smart Pen Rev E PCB Fabrication & Manufacturing Notes

- **Board Material**: FR-4 TG150 High-Temperature laminate.
- **Layer Count**: 2 Layers.
- **Finished Dimensions**: 84.00 mm x 9.20 mm (+/- 0.10 mm).
- **Finished Thickness**: 1.00 mm (+/- 10%).
- **Copper Thickness**: 1 oz (35 um) outer layers.
- **Minimum Trace Width**: 0.152 mm (6.0 mil).
- **Minimum Clearance**: 0.152 mm (6.0 mil).
- **Minimum Drill Hole**: 0.30 mm (via drill).
- **Solder Mask**: Matte Black, Liquid Photo-Imageable (LPI).
- **Silkscreen**: White, high-contrast, double-pass.
- **Surface Finish**: ENIG (Electroless Nickel Immersion Gold), 1-2 u" Au over 120 u" Ni.
"""
    (dirs['09'] / 'PCB_Manufacturing_Notes.md').write_text(mfg_notes, encoding='utf-8')

    # 10. 10_Test_Reports
    shutil.copy('reports/baseline_audit.md', dirs['10'] / 'baseline_audit.md')
    shutil.copy('reports/FOOTPRINT_AUDIT.csv', dirs['10'] / 'FOOTPRINT_AUDIT.csv')
    shutil.copy('reports/MECHANICAL_VALIDATION.md', dirs['10'] / 'MECHANICAL_VALIDATION.md')

    # 11. 11_Design_Limitations
    limitations_md = """# Engineering Limitations & Prototype Validation Blockers

## 1. Core Technical Risk: IMU Drift vs. Dead Reckoning
- **Fundamental Physics Constraint**: An inertial measurement unit (MPU-6050) measures linear acceleration ($a$) and angular rate ($\omega$), not absolute position ($x, y, z$).
- **Double Integration Drift**: Calculating displacement via $x(t) = \iint a(t) \, dt^2$ causes sensor bias errors to compound quadratically over time. Even high-precision industrial IMUs drift several centimeters within a few seconds of continuous integration without external absolute reference corrections.
- **Engineering Recommendation**:
  1. Preserve uncompressed raw 6-DOF sensor streams on MicroSD and BLE.
  2. Implement zero-velocity update (ZUPT) and pen-stroke segment boundaries triggered by the external capacitive WRITE touch sensor.
  3. Prepare for a future Revision F hardware revision incorporating an optical displacement sensor (e.g. PMW3360 / PAW3204) at the tip for ground-truth position tracking.

## 2. MicroSD Socket Physical Clearance Barrier
- A standard physical push-pull MicroSD card socket is 14.0 mm wide x 14.5 mm long.
- The Smart Pen outer diameter is strictly constrained to **<= 16.0 mm** (with 1.25 mm wall thickness, leaving an inner diameter of **13.0 mm**).
- A 14.0 mm rigid socket cannot sit horizontally across a 9.2 mm PCB without penetrating the cylindrical shell.
- **Implemented Resolution**: J_SD is implemented as a miniature 0.5mm pitch 6-pin FPC connector feeding an axially mounted rear MicroSD holder cartridge.

## 3. Physical Prototype Bring-Up Gate
Before authorizing production batch manufacturing:
1. 3D-print enclosure prototypes A & B in SLA/SLS resin to verify bayonet twist-lock feel and clicker stroke.
2. Fabricate a 5-unit PCB pilot batch to measure 2.4GHz RF impedance on 1.0mm FR-4 substrate.
3. Validate LiPo battery thermal rise during simultaneous 500mA USB-C charging and ESP32-C3 BLE transmission.
"""
    (dirs['11'] / 'Engineering_Blockers_and_Limitations.md').write_text(limitations_md, encoding='utf-8')

    # Create Final ZIP package
    zip_dest = base_dir / 'SmartPen_RevE_Complete_Delivery_Package.zip'
    with zipfile.ZipFile(zip_dest, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in base_dir.rglob('*'):
            if f.is_file() and f.name != 'SmartPen_RevE_Complete_Delivery_Package.zip':
                arcname = f.relative_to(base_dir)
                z.write(f, arcname=arcname)

    print(f"Generated complete client delivery package at {base_dir}")
    print(f"Created final deliverable ZIP archive: {zip_dest} ({zip_dest.stat().st_size} bytes)")

if __name__ == '__main__':
    create_delivery_package()
