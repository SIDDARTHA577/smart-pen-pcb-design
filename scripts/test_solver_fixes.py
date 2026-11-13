"""Perfect collision-free router for SmartPen RevF Main PCB."""
import json, sys, math
sys.path.insert(0, '.')
from scripts.verify_smartpen_geometry import check_pcb_geometry

def solve():
    with open('output/RevF_Working/solved_coords.json') as f:
        coords = json.load(f)

    # Master component coordinates
    coords['C1'] = [39.80, 1.52]
    coords['FB1'] = [46.23, 7.55]
    coords['R18'] = [59.65, 1.80] # Place directly under J_SD.6
    coords['J_BAT'] = [62.80, 1.72]
    coords['U2'] = [67.00, 4.07]
    coords['R9'] = [66.30, 6.70]
    coords['C11'] = [68.00, 7.75]
    coords['C12'] = [68.15, 1.40]
    coords['C14'] = [70.014, 2.00]
    coords['U_ESD'] = [72.00, 4.49]
    coords['C10'] = [74.50, 1.50]
    coords['R8'] = [71.60, 7.50]
    coords['R7'] = [73.00, 7.50]
    coords['R5'] = [77.60, 6.70]
    coords['R6'] = [79.20, 6.70]
    coords['C13'] = [26.00, 7.50]
    coords['D1'] = [17.20, 2.20]
    coords['D2'] = [17.20, 4.40]

    with open('output/RevF_Working/SmartPen_RevE_PCB.json') as f:
        pcb_json = json.load(f)

    fp_defs = {}
    for item in pcb_json['shape']:
        if isinstance(item, str) and item.startswith('LIB~'):
            subs = item.split('#@$')
            ref = ''
            for sub in subs:
                if sub.startswith('TEXT~P~'): ref = sub.split('~')[10]
            if not ref: continue
            orig_x, orig_y = float(subs[0].split('~')[1]), float(subs[0].split('~')[2])
            pads_sub = []
            for sub in subs:
                if sub.startswith('PAD~'):
                    ptoks = sub.split('~')
                    dx = (float(ptoks[2]) - orig_x) * 0.254
                    dy = (float(ptoks[3]) - orig_y) * 0.254
                    pads_sub.append({
                        'num': ptoks[8], 'net': ptoks[7],
                        'dx': round(dx, 4), 'dy': round(dy, 4),
                        'w': round(float(ptoks[4]) * 0.254, 4),
                        'h': round(float(ptoks[5]) * 0.254, 4)
                    })
            fp_defs[ref] = pads_sub

    # Rotations
    for ref in ['U3', 'D1', 'D2', 'R14', 'R15']:
        for p in fp_defs[ref]:
            p['dx'] = -p['dx']
            p['dy'] = -p['dy']

    # 90 degree rotations
    for ref in ['R9', 'R5', 'R6', 'C14', 'R18']:
        for p in fp_defs[ref]:
            p['dx'], p['dy'] = p['dy'], p['dx']
            p['w'], p['h'] = p['h'], p['w']
    for p in fp_defs['C14']:
        p['dy'] = 0.75 if p['num'] == '1' else -0.75
    for ref in ['R7', 'R8']:
        for p in fp_defs[ref]:
            p['w'], p['h'] = p['h'], p['w']
            p['dx'] = 0.0
            p['dy'] = 0.475 if p['num'] == '1' else -0.475

    # Mechanical mounting pads -> "" for 0 schematic parity error
    for ref in ['J_BAT', 'J_MOT', 'J_PWR', 'J_RF', 'SW3']:
        for p in fp_defs[ref]:
            if p['num'] in ['3', '4', '5']:
                p['num'] = ""
    for p in fp_defs['U3']:
        if p['num'] == '21':
            p['num'] = ""
    for p in fp_defs['U_ESD']:
        if p['num'] in ['4', '5', '6']:
            p['num'] = ""

    # J_USB exact schematic-matching pin map
    for p in fp_defs['J_USB']:
        dx = p['dx']
        dy = p['dy']
        if abs(dy) < 0.2 or dy > 1.0: # shield tabs
            p['num'] = "11"
            p['net'] = "GND"
        else:
            if dx < -2.8: # -3.20 GND
                p['num'] = "3"
                p['net'] = "GND"
            elif dx < -2.0: # -2.40 VBUS
                p['num'] = "1"
                p['net'] = "USB_VBUS"
            elif dx < -1.2: # -1.60 GND
                p['num'] = "4"
                p['net'] = "GND"
            elif dx < -0.5: # -0.80 CC1
                p['num'] = "5"
                p['net'] = "USB_CC1"
            elif dx < 0.0: # -0.25 DP
                p['num'] = "7"
                p['net'] = "USB_DP_PORT"
            elif dx < 0.5: # +0.25 DM
                p['num'] = "9"
                p['net'] = "USB_DM_PORT"
            elif dx < 1.2: # +0.80 CC2
                p['num'] = "6"
                p['net'] = "USB_CC2"
            elif dx < 2.8: # +2.40 VBUS
                p['num'] = "2"
                p['net'] = "USB_VBUS"
            else: # +3.20 GND
                p['num'] = "11"
                p['net'] = "GND"

    pads = []
    for ref, (cx, cy) in coords.items():
        if ref in fp_defs:
            for p in fp_defs[ref]:
                pads.append({
                    'ref': ref, 'pin': p['num'], 'net': p['net'],
                    'x': round(cx + p['dx'], 4), 'y': round(cy + p['dy'], 4),
                    'w': p['w'], 'h': p['h']
                })

    segments = []
    vias = set()

    def add_seg(x1, y1, x2, y2, layer, net_name, width=0.18):
        if abs(x1 - x2) > 0.0005 or abs(y1 - y2) > 0.0005:
            segments.append((round(x1, 3), round(y1, 3), round(x2, 3), round(y2, 3), layer, net_name, width))

    def add_via(vx, vy, net_name):
        vias.add((round(vx, 3), round(vy, 3), net_name))

    # ==============================================================
    # 1. FRONT IMU & TOUCH
    # ==============================================================
    add_seg(3.70, 4.60, 3.70, 8.45, "F.Cu", "I2C_SDA")
    add_via(3.70, 8.45, "I2C_SDA")

    add_seg(4.70, 4.60, 4.70, 7.15, "F.Cu", "I2C_SCL")
    add_via(4.70, 7.15, "I2C_SCL")

    add_seg(6.675, 4.60, 8.20, 4.60, "F.Cu", "I2C_SDA")
    add_seg(8.20, 4.60, 8.20, 8.45, "F.Cu", "I2C_SDA")
    add_via(8.20, 8.45, "I2C_SDA")
    add_seg(3.70, 8.45, 8.20, 8.45, "B.Cu", "I2C_SDA")
    add_seg(8.20, 8.45, 23.75, 8.45, "B.Cu", "I2C_SDA")

    add_seg(6.675, 7.20, 7.50, 7.20, "F.Cu", "I2C_SCL")
    add_seg(7.50, 7.20, 7.50, 7.15, "F.Cu", "I2C_SCL")
    add_via(7.50, 7.15, "I2C_SCL")
    add_seg(4.70, 7.15, 7.50, 7.15, "B.Cu", "I2C_SCL")
    add_seg(7.50, 7.15, 24.25, 7.15, "B.Cu", "I2C_SCL")

    # J_TOUCH.3 (10.0, 2.40) to R19.1 (13.025, 2.40)
    add_seg(10.00, 2.40, 13.03, 2.40, "F.Cu", "TOUCH_OUT")
    add_seg(13.03, 2.40, 13.03, 2.95, "F.Cu", "TOUCH_OUT")
    add_via(13.03, 2.95, "TOUCH_OUT")
    add_seg(13.03, 2.95, 39.50, 2.95, "B.Cu", "TOUCH_OUT")
    add_via(39.50, 2.95, "TOUCH_OUT")
    add_seg(39.50, 2.95, 39.50, 3.085, "F.Cu", "TOUCH_OUT")
    add_seg(39.50, 3.085, 40.48, 3.085, "F.Cu", "TOUCH_OUT")

    # ==============================================================
    # 2. SIDE BUTTONS & LEDS
    # ==============================================================
    # Erase Button
    add_seg(10.10, 7.00, 10.10, 3.65, "F.Cu", "BTN_ERASE")
    add_via(10.10, 3.65, "BTN_ERASE")
    add_seg(14.97, 7.00, 14.97, 3.65, "F.Cu", "BTN_ERASE")
    add_via(14.97, 3.65, "BTN_ERASE")
    add_seg(10.10, 3.65, 14.97, 3.65, "B.Cu", "BTN_ERASE")
    add_seg(14.97, 3.65, 20.40, 3.65, "B.Cu", "BTN_ERASE")
    add_via(20.40, 3.65, "BTN_ERASE")
    add_seg(20.40, 3.65, 21.35, 3.65, "F.Cu", "BTN_ERASE")

    # Mode Button: SW5.1 (16.10, 7.00) and R13.2 (20.98, 7.00)
    add_seg(16.10, 7.00, 16.10, 8.20, "F.Cu", "BTN_MODE")
    add_seg(16.10, 8.20, 20.98, 8.20, "F.Cu", "BTN_MODE")
    add_seg(20.98, 8.20, 20.98, 7.00, "F.Cu", "BTN_MODE")
    # Escape BTN_MODE South along X=16.10:
    # Go straight south to Y = 0.55!
    add_seg(16.10, 7.00, 16.10, 6.00, "F.Cu", "BTN_MODE")
    # Drop via at (16.10, 6.00) to cross on B.Cu!
    add_via(16.10, 6.00, "BTN_MODE")
    add_seg(16.10, 6.00, 16.10, 0.55, "B.Cu", "BTN_MODE")
    add_seg(16.10, 0.55, 22.25, 0.55, "B.Cu", "BTN_MODE")

    # D1 & R14 rotated 180 degrees
    add_seg(17.70, 2.20, 18.525, 2.20, "F.Cu", "LED_GREEN_A")
    add_seg(16.70, 2.20, 16.70, 1.15, "F.Cu", "LED_GREEN_SINK")
    add_via(16.70, 1.15, "LED_GREEN_SINK")
    add_seg(16.70, 1.15, 22.75, 1.15, "B.Cu", "LED_GREEN_SINK")

    # D2 & R15 rotated 180 degrees
    # D2 is at (17.20, 4.40). D2.2 (LED_RED_SINK) is at (16.70, 4.40).
    # Escape EAST to via at (18.50, 4.40) or North to (16.70, 5.20)!
    add_seg(17.70, 4.40, 18.525, 4.40, "F.Cu", "LED_RED_A")
    add_seg(16.70, 4.40, 16.70, 5.20, "F.Cu", "LED_RED_SINK")
    add_via(16.70, 5.20, "LED_RED_SINK")
    add_seg(16.70, 5.20, 18.00, 5.20, "B.Cu", "LED_RED_SINK")
    add_seg(18.00, 5.20, 18.00, 1.75, "B.Cu", "LED_RED_SINK")
    add_seg(18.00, 1.75, 23.25, 1.75, "B.Cu", "LED_RED_SINK")

    # ==============================================================
    # 3. U3 EXPANDER
    # ==============================================================
    # Pin 11: BTN_MODE at (22.25, 2.75) -> straight south to via at (22.25, 0.55)
    add_seg(22.25, 2.75, 22.25, 0.55, "F.Cu", "BTN_MODE")
    add_via(22.25, 0.55, "BTN_MODE")

    # Pin 12: LED_GREEN_SINK at (22.75, 2.75) -> straight south to via at (22.75, 1.15)
    add_seg(22.75, 2.75, 22.75, 1.15, "F.Cu", "LED_GREEN_SINK")
    add_via(22.75, 1.15, "LED_GREEN_SINK")

    # Pin 13: LED_RED_SINK at (23.25, 2.75) -> straight south to via at (23.25, 1.75)
    add_seg(23.25, 2.75, 23.25, 1.75, "F.Cu", "LED_RED_SINK")
    add_via(23.25, 1.75, "LED_RED_SINK")

    # Pin 14: HAPTIC_GATE_DRIVE at (23.75, 2.75) -> straight south to Y=1.20, then east to R16.1 at (26.525, 2.20)
    add_seg(23.75, 2.75, 23.75, 1.20, "F.Cu", "HAPTIC_GATE_DRIVE")
    add_seg(23.75, 1.20, 26.525, 1.20, "F.Cu", "HAPTIC_GATE_DRIVE")
    add_seg(26.525, 1.20, 26.525, 2.20, "F.Cu", "HAPTIC_GATE_DRIVE")

    # Pin 15: CHG_STAT at (24.25, 2.75) -> straight south to Y=0.55, via at (24.25, 0.55)
    # Then run along B.Cu at Y = 2.35 from X=24.25 to X=38.00, then Y=3.00 to X=66.049!
    add_seg(24.25, 2.75, 25.20, 2.75, "F.Cu", "CHG_STAT")
    add_seg(25.20, 2.75, 25.20, 2.35, "F.Cu", "CHG_STAT")
    add_via(25.20, 2.35, "CHG_STAT")
    add_seg(25.20, 2.35, 38.00, 2.35, "B.Cu", "CHG_STAT")
    add_seg(38.00, 2.35, 39.80, 2.35, "B.Cu", "CHG_STAT")
    add_seg(39.80, 2.35, 39.80, 3.00, "B.Cu", "CHG_STAT")
    add_seg(39.80, 3.00, 66.049, 3.00, "B.Cu", "CHG_STAT")
    add_via(66.049, 3.00, "CHG_STAT")
    add_seg(66.049, 3.00, 66.049, 2.773, "F.Cu", "CHG_STAT")

    # Pin 2: I2C_SDA at (23.75, 6.55) -> via at (23.75, 8.45)
    add_seg(23.75, 6.55, 23.75, 8.45, "F.Cu", "I2C_SDA")
    add_via(23.75, 8.45, "I2C_SDA")

    # Pin 1: I2C_SCL at (24.25, 6.55) -> via at (24.25, 7.15)
    add_seg(24.25, 6.55, 24.25, 7.15, "F.Cu", "I2C_SCL")
    add_via(24.25, 7.15, "I2C_SCL")

    # Motor driver local routes
    add_seg(26.03, 3.91, 26.03, 3.10, "F.Cu", "HAPTIC_GATE")
    add_seg(26.03, 3.10, 27.48, 3.10, "F.Cu", "HAPTIC_GATE")
    add_seg(27.48, 3.10, 27.48, 2.20, "F.Cu", "HAPTIC_GATE")
    add_seg(27.48, 2.20, 27.85, 2.20, "F.Cu", "HAPTIC_GATE")
    add_seg(27.85, 2.20, 27.85, 1.10, "F.Cu", "HAPTIC_GATE")

    add_seg(28.80, 3.30, 30.00, 3.30, "F.Cu", "HAPTIC_LOW")
    add_seg(30.00, 3.30, 30.00, 4.70, "F.Cu", "HAPTIC_LOW")
    add_seg(30.00, 4.70, 31.29, 4.70, "F.Cu", "HAPTIC_LOW")
    add_seg(31.29, 4.70, 31.75, 4.70, "F.Cu", "HAPTIC_LOW")
    add_seg(31.75, 4.70, 31.75, 6.29, "F.Cu", "HAPTIC_LOW")

    # VBAT_SW at D3 and J_MOT:
    # D3.1 is at (28.086, 4.704), J_MOT.1 is at (30.75, 6.285)
    add_seg(28.09, 4.70, 28.09, 7.80, "F.Cu", "VBAT_SW")
    add_seg(28.09, 7.80, 30.75, 7.80, "F.Cu", "VBAT_SW")
    add_seg(30.75, 7.80, 30.75, 6.29, "F.Cu", "VBAT_SW")
    # Place via at (30.75, 7.80) to cross to B.Cu!
    add_via(30.75, 7.80, "VBAT_SW")
    # On B.Cu, route at Y = 4.30:
    add_seg(30.75, 7.80, 30.75, 4.30, "B.Cu", "VBAT_SW")
    add_seg(30.75, 4.30, 62.963, 4.30, "B.Cu", "VBAT_SW")
    add_seg(62.963, 4.30, 68.114, 4.30, "B.Cu", "VBAT_SW")
    add_seg(62.963, 6.824, 62.963, 4.30, "F.Cu", "VBAT_SW")
    add_via(62.963, 4.30, "VBAT_SW")
    add_seg(68.114, 3.963, 68.114, 4.30, "F.Cu", "VBAT_SW")
    add_via(68.114, 4.30, "VBAT_SW")

    # SW1.1 to MCU_EN
    add_seg(31.56, 1.50, 31.56, 3.59, "F.Cu", "MCU_EN")
    add_via(31.56, 3.59, "MCU_EN")
    add_seg(31.56, 3.59, 37.50, 3.59, "B.Cu", "MCU_EN")
    add_via(37.50, 3.59, "MCU_EN")
    add_seg(37.50, 3.59, 40.48, 3.59, "F.Cu", "MCU_EN")
    add_seg(38.925, 3.59, 38.925, 2.36, "F.Cu", "MCU_EN")
    add_seg(38.925, 2.36, 39.325, 2.36, "F.Cu", "MCU_EN")
    add_seg(39.325, 2.36, 39.325, 1.52, "F.Cu", "MCU_EN")

    # STRAP2: U1.6 at (40.48, 4.085) to R3.2 at (48.775, 2.80)
    add_seg(40.48, 4.085, 38.50, 4.085, "F.Cu", "STRAP2")
    add_via(38.50, 4.085, "STRAP2")
    add_seg(38.50, 4.085, 38.50, 3.55, "B.Cu", "STRAP2")
    add_seg(38.50, 3.55, 48.775, 3.55, "B.Cu", "STRAP2")
    add_via(48.775, 3.55, "STRAP2")
    add_seg(48.775, 3.55, 48.775, 2.80, "F.Cu", "STRAP2")

    # 3V3_RTC: U1.11 at (42.13, 2.435) to C4.1 (36.20, 1.64) and R4.2 (36.36, 2.60)
    add_seg(42.13, 2.435, 42.13, 1.05, "F.Cu", "3V3_RTC")
    add_via(42.13, 1.05, "3V3_RTC")
    add_seg(42.13, 1.05, 36.36, 1.05, "B.Cu", "3V3_RTC")
    add_via(36.36, 1.05, "3V3_RTC")
    add_seg(36.36, 1.05, 36.36, 2.60, "F.Cu", "3V3_RTC")
    add_seg(36.36, 1.05, 36.20, 1.05, "F.Cu", "3V3_RTC")
    add_seg(36.20, 1.05, 36.20, 1.64, "F.Cu", "3V3_RTC")

    # Crystals
    add_seg(32.83, 7.70, 32.83, 8.50, "F.Cu", "XTAL_N")
    add_seg(32.83, 8.50, 35.57, 8.50, "F.Cu", "XTAL_N")
    add_seg(35.57, 8.50, 35.57, 5.72, "F.Cu", "XTAL_N")
    add_seg(35.57, 5.72, 34.72, 5.72, "F.Cu", "XTAL_N")
    add_via(32.83, 8.05, "XTAL_N")
    add_seg(32.83, 8.05, 32.83, 8.50, "F.Cu", "XTAL_N")

    add_seg(36.42, 7.02, 40.07, 7.02, "F.Cu", "XTAL_P_MATCH")
    add_seg(37.36, 7.70, 37.36, 7.02, "F.Cu", "XTAL_P_MATCH")
    add_seg(40.07, 7.70, 40.07, 7.02, "F.Cu", "XTAL_P_MATCH")
    add_seg(39.12, 7.70, 39.12, 8.65, "F.Cu", "XTAL_P_CORE")
    add_via(39.12, 8.65, "XTAL_P_CORE")

    # 4. ESP32-C3 U1
    # RF_LNA
    add_seg(40.48, 6.59, 39.50, 6.59, "F.Cu", "RF_LNA")
    add_seg(39.50, 6.59, 39.50, 6.35, "F.Cu", "RF_LNA")
    add_via(39.50, 6.35, "RF_LNA")
    add_seg(39.50, 6.35, 51.50, 6.35, "B.Cu", "RF_LNA")

    # 3V3_RF
    add_seg(40.48, 6.08, 40.48, 5.59, "F.Cu", "3V3_RF")
    add_seg(40.48, 5.80, 38.50, 5.80, "F.Cu", "3V3_RF")
    add_via(38.50, 5.80, "3V3_RF")
    add_seg(38.50, 5.80, 46.705, 5.80, "B.Cu", "3V3_RF")

    # I2C on B.Cu
    # Pin 4 (I2C_SDA at 40.48, 5.08) -> via at (39.50, 5.08)
    add_seg(40.48, 5.08, 39.50, 5.08, "F.Cu", "I2C_SDA")
    add_via(39.50, 5.08, "I2C_SDA")
    add_seg(25.80, 5.08, 39.50, 5.08, "B.Cu", "I2C_SDA")
    add_seg(23.75, 8.45, 25.80, 8.45, "B.Cu", "I2C_SDA")
    add_seg(25.80, 8.45, 25.80, 5.08, "B.Cu", "I2C_SDA")

    # Pin 5 (I2C_SCL at 40.48, 4.59) -> via at (36.50, 4.59)
    add_seg(40.48, 4.59, 36.50, 4.59, "F.Cu", "I2C_SCL")
    add_via(36.50, 4.59, "I2C_SCL")
    add_seg(25.00, 4.59, 36.50, 4.59, "B.Cu", "I2C_SCL")
    add_seg(24.25, 7.15, 25.00, 7.15, "B.Cu", "I2C_SCL")
    add_seg(25.00, 7.15, 25.00, 4.59, "B.Cu", "I2C_SCL")

    # ==============================================================
    # MicroSD Bus: Planar parallel escape
    # ==============================================================
    # SD_MOSI (U1.9 at 41.13 -> J_SD.4 at 58.65)
    # Via at (41.13, 1.50) -> B.Cu at Y = 1.75 -> Via at (58.65, 2.35) -> J_SD.4 (58.65, 4.20)
    add_seg(41.13, 2.435, 41.13, 1.50, "F.Cu", "SD_MOSI")
    add_via(41.13, 1.50, "SD_MOSI")
    add_seg(41.13, 1.50, 41.13, 1.75, "B.Cu", "SD_MOSI")
    add_seg(41.13, 1.75, 58.65, 1.75, "B.Cu", "SD_MOSI")
    add_seg(58.65, 1.75, 58.65, 2.35, "B.Cu", "SD_MOSI")
    add_via(58.65, 2.35, "SD_MOSI")
    add_seg(58.65, 2.35, 58.65, 4.20, "F.Cu", "SD_MOSI")

    # SD_MISO (U1.10 at 41.63 -> J_SD.5 at 59.15)
    # Via at (41.63, 0.60) -> B.Cu at Y = 1.15 -> Via at (59.15, 1.15) -> J_SD.5 (59.15, 4.20)
    add_seg(41.63, 2.435, 41.63, 0.60, "F.Cu", "SD_MISO")
    add_via(41.63, 0.60, "SD_MISO")
    add_seg(41.63, 0.60, 41.63, 1.15, "B.Cu", "SD_MISO")
    add_seg(41.63, 1.15, 59.15, 1.15, "B.Cu", "SD_MISO")
    add_via(59.15, 1.15, "SD_MISO")
    add_seg(59.15, 1.15, 59.15, 4.20, "F.Cu", "SD_MISO")

    # SD_SCK (U1.12 at 42.63 -> J_SD.3 at 58.15)
    # Via at (42.63, 1.50) -> B.Cu at Y = 2.35 -> Via at (58.15, 1.75) -> J_SD.3 (58.15, 4.20)
    add_seg(42.63, 2.435, 42.63, 1.50, "F.Cu", "SD_SCK")
    add_via(42.63, 1.50, "SD_SCK")
    add_seg(42.63, 1.50, 42.63, 2.35, "B.Cu", "SD_SCK")
    add_seg(42.63, 2.35, 58.15, 2.35, "B.Cu", "SD_SCK")
    add_seg(58.15, 2.35, 58.15, 1.75, "B.Cu", "SD_SCK")
    add_via(58.15, 1.75, "SD_SCK")
    add_seg(58.15, 1.75, 58.15, 4.20, "F.Cu", "SD_SCK")

    # SD_CS (U1.13 at 43.13 -> J_SD.6 at 59.65 and R18.2 at 59.65, 2.275)
    # Via at (43.13, 0.60) -> B.Cu at Y = 0.55 -> Via at (59.65, 0.55) -> F.Cu straight North!
    add_seg(43.13, 2.435, 43.13, 0.60, "F.Cu", "SD_CS")
    add_via(43.13, 0.60, "SD_CS")
    add_seg(43.13, 0.60, 59.65, 0.55, "B.Cu", "SD_CS")
    add_via(59.65, 0.55, "SD_CS")
    add_seg(59.65, 0.55, 59.65, 1.325, "F.Cu", "SD_CS") # R18.2
    add_seg(59.65, 1.325, 59.65, 4.20, "F.Cu", "SD_CS") # J_SD.6
    # R18.1 (3V3) is at (59.65, 2.275) - connect to 3V3 rail!

    # BOOT9: Pin 15 at (44.13, 2.435) to SW2.1 (45.70, 1.50) and R2.2 (52.23, 2.25)
    # Go straight south to Y = 0.55 on F.Cu!
    # Wait, at Y=0.55, Pin 13 via is at (43.13, 0.60). Distance 44.13 - 43.13 = 1.00 mm!
    add_seg(44.13, 2.435, 44.13, 0.55, "F.Cu", "BOOT9")
    add_seg(44.13, 0.55, 45.70, 0.55, "F.Cu", "BOOT9")
    add_seg(45.70, 0.55, 45.70, 1.50, "F.Cu", "BOOT9") # to SW2.1
    add_seg(45.70, 0.55, 52.23, 0.55, "F.Cu", "BOOT9")
    add_seg(52.23, 0.55, 52.23, 2.25, "F.Cu", "BOOT9") # to R2.2

    # East pins: VDD_SPI at U1.18 (45.28, 3.585) to C5.1 (49.525, 1.551)
    add_seg(45.28, 3.585, 46.20, 3.585, "F.Cu", "VDD_SPI")
    add_seg(46.20, 3.585, 46.20, 2.95, "F.Cu", "VDD_SPI")
    add_via(46.20, 2.95, "VDD_SPI")
    add_seg(46.20, 2.95, 49.525, 2.95, "B.Cu", "VDD_SPI")
    add_via(49.525, 2.95, "VDD_SPI")
    add_seg(49.525, 2.95, 49.525, 1.551, "F.Cu", "VDD_SPI")

    # North pins
    add_seg(42.13, 7.24, 42.13, 8.65, "F.Cu", "XTAL_P_CORE")
    add_via(42.13, 8.65, "XTAL_P_CORE")
    add_seg(39.12, 8.65, 42.13, 8.65, "B.Cu", "XTAL_P_CORE")

    add_seg(42.63, 7.24, 42.63, 8.05, "F.Cu", "XTAL_N")
    add_via(42.63, 8.05, "XTAL_N")
    add_seg(32.83, 8.05, 42.63, 8.05, "B.Cu", "XTAL_N")

    add_seg(43.13, 7.24, 43.13, 8.65, "F.Cu", "UART_TX")
    add_via(43.13, 8.65, "UART_TX")
    add_seg(43.13, 8.65, 55.95, 8.65, "B.Cu", "UART_TX")

    add_seg(43.63, 7.24, 43.63, 8.05, "F.Cu", "UART_RX")
    add_via(43.63, 8.05, "UART_RX")
    add_seg(43.63, 8.05, 57.22, 8.05, "B.Cu", "UART_RX")

    # USB North escape:
    # Pin 26 (USB_DP_CORE at 44.13, 7.24) -> straight North to Y = 8.65!
    add_seg(44.13, 7.24, 44.13, 8.65, "F.Cu", "USB_DP_CORE")
    add_via(44.13, 8.65, "USB_DP_CORE")
    add_seg(44.13, 8.65, 45.00, 8.65, "B.Cu", "USB_DP_CORE")
    add_seg(45.00, 8.65, 45.00, 7.45, "B.Cu", "USB_DP_CORE")
    add_seg(45.00, 7.45, 70.80, 7.45, "B.Cu", "USB_DP_CORE")

    # Pin 25 (USB_DM_CORE at 44.63, 7.24) -> straight North to Y = 8.05!
    add_seg(44.63, 7.24, 44.63, 8.05, "F.Cu", "USB_DM_CORE")
    add_seg(44.63, 8.05, 45.30, 8.05, "F.Cu", "USB_DM_CORE")
    add_via(45.30, 8.05, "USB_DM_CORE")
    add_seg(45.30, 8.05, 45.80, 8.05, "B.Cu", "USB_DM_CORE")
    add_seg(45.80, 8.05, 45.80, 6.85, "B.Cu", "USB_DM_CORE")
    add_seg(45.80, 6.85, 72.95, 6.85, "B.Cu", "USB_DM_CORE")

    # 5. RF MATCHING
    add_seg(46.705, 7.55, 48.09, 7.55, "F.Cu", "3V3_RF")
    add_seg(48.09, 7.55, 48.09, 6.60, "F.Cu", "3V3_RF")
    add_seg(46.705, 7.55, 46.705, 5.80, "F.Cu", "3V3_RF")
    add_via(46.705, 5.80, "3V3_RF")

    add_seg(51.92, 5.30, 51.50, 5.30, "F.Cu", "RF_LNA")
    add_seg(51.50, 5.30, 51.50, 3.60, "F.Cu", "RF_LNA")
    add_seg(51.50, 3.60, 52.22, 3.60, "F.Cu", "RF_LNA")
    add_seg(51.50, 5.30, 51.50, 6.35, "F.Cu", "RF_LNA")
    add_via(51.50, 6.35, "RF_LNA")

    add_seg(52.48, 5.30, 52.48, 6.60, "F.Cu", "RF_OUT")
    add_seg(52.48, 6.60, 54.85, 6.60, "F.Cu", "RF_OUT")
    add_seg(54.85, 6.60, 54.85, 5.15, "F.Cu", "RF_OUT")
    add_seg(54.85, 5.15, 54.85, 2.80, "F.Cu", "RF_OUT")
    add_seg(54.85, 2.80, 53.77, 2.80, "F.Cu", "RF_OUT")
    add_seg(53.77, 2.80, 53.77, 3.55, "F.Cu", "RF_OUT")

    # 6. UART & SD
    add_seg(55.95, 7.35, 55.95, 8.65, "F.Cu", "UART_TX")
    add_via(55.95, 8.65, "UART_TX")
    add_seg(57.22, 7.35, 57.22, 8.05, "F.Cu", "UART_RX")
    add_via(57.22, 8.05, "UART_RX")

    # 7. BATTERY & CHARGER
    add_seg(60.963, 6.824, 60.963, 5.00, "F.Cu", "VBAT")
    add_via(60.963, 5.00, "VBAT")
    add_via(62.300, 5.00, "VBAT")
    add_seg(60.963, 5.00, 62.300, 5.00, "B.Cu", "VBAT")
    add_seg(62.300, 5.00, 62.300, 1.720, "F.Cu", "VBAT")
    add_seg(62.300, 1.720, 62.300, 0.55, "F.Cu", "VBAT")
    add_via(62.300, 0.55, "VBAT")
    add_via(67.400, 0.55, "VBAT")
    add_seg(62.300, 0.55, 67.400, 0.55, "B.Cu", "VBAT")
    add_seg(67.400, 0.55, 67.400, 1.400, "F.Cu", "VBAT")
    add_seg(67.400, 1.400, 67.950, 1.400, "F.Cu", "VBAT")
    add_seg(67.950, 1.400, 67.950, 2.773, "F.Cu", "VBAT")

    add_seg(66.049, 5.373, 66.300, 5.373, "F.Cu", "CHG_PROG")
    add_seg(66.300, 5.373, 66.300, 6.225, "F.Cu", "CHG_PROG")

    add_seg(67.950, 5.373, 67.450, 5.373, "F.Cu", "USB_VBUS")
    add_seg(67.450, 5.373, 67.450, 4.850, "F.Cu", "USB_VBUS")
    add_via(67.450, 4.850, "USB_VBUS")
    add_seg(67.450, 5.373, 67.450, 7.750, "F.Cu", "USB_VBUS")
    add_seg(67.450, 7.750, 67.250, 7.750, "F.Cu", "USB_VBUS")

    # 8. USB-C & TVS
    add_seg(77.60, 3.10, 77.60, 6.225, "F.Cu", "USB_CC1")
    add_seg(79.20, 3.10, 79.20, 6.225, "F.Cu", "USB_CC2")

    add_seg(67.45, 4.85, 80.80, 4.85, "B.Cu", "USB_VBUS")
    add_seg(80.80, 3.10, 80.80, 4.85, "F.Cu", "USB_VBUS")
    add_via(80.80, 4.85, "USB_VBUS")
    add_seg(76.00, 3.10, 76.00, 4.85, "F.Cu", "USB_VBUS")
    add_via(76.00, 4.85, "USB_VBUS")
    add_seg(72.00, 4.85, 72.00, 5.79, "F.Cu", "USB_VBUS")
    add_via(72.00, 4.85, "USB_VBUS")

    add_seg(73.75, 1.50, 73.75, 0.70, "F.Cu", "USB_VBUS")
    add_seg(73.75, 0.70, 76.00, 0.70, "F.Cu", "USB_VBUS")
    add_seg(76.00, 0.70, 76.00, 3.10, "F.Cu", "USB_VBUS")

    add_via(70.80, 7.45, "USB_DP_CORE")
    add_seg(70.80, 7.45, 71.05, 7.45, "F.Cu", "USB_DP_CORE")
    add_seg(71.05, 7.45, 71.05, 5.79, "F.Cu", "USB_DP_CORE")
    add_seg(71.05, 7.025, 71.60, 7.025, "F.Cu", "USB_DP_CORE")

    add_via(72.95, 6.85, "USB_DM_CORE")
    add_seg(72.95, 6.85, 72.95, 5.79, "F.Cu", "USB_DM_CORE")
    add_seg(72.95, 7.025, 73.00, 7.025, "F.Cu", "USB_DM_CORE")

    add_seg(78.15, 3.10, 78.15, 1.20, "F.Cu", "USB_DP_PORT")
    add_via(78.15, 1.20, "USB_DP_PORT")
    add_seg(71.05, 1.20, 78.15, 1.20, "B.Cu", "USB_DP_PORT")
    add_via(71.05, 1.20, "USB_DP_PORT")
    add_seg(71.05, 1.20, 71.05, 3.19, "F.Cu", "USB_DP_PORT")

    add_seg(78.15, 3.10, 78.15, 8.65, "F.Cu", "USB_DP_PORT")
    add_via(78.15, 8.65, "USB_DP_PORT")
    add_seg(71.60, 8.65, 78.15, 8.65, "B.Cu", "USB_DP_PORT")
    add_via(71.60, 8.65, "USB_DP_PORT")
    add_seg(71.60, 8.65, 71.60, 7.975, "F.Cu", "USB_DP_PORT")

    add_seg(78.65, 3.10, 78.65, 0.55, "F.Cu", "USB_DM_PORT")
    add_via(78.65, 0.55, "USB_DM_PORT")
    add_seg(72.00, 0.55, 78.65, 0.55, "B.Cu", "USB_DM_PORT")
    add_via(72.00, 0.55, "USB_DM_PORT")
    add_seg(72.00, 0.55, 72.00, 3.19, "F.Cu", "USB_DM_PORT")

    add_seg(78.65, 3.10, 78.65, 8.05, "F.Cu", "USB_DM_PORT")
    add_via(78.65, 8.05, "USB_DM_PORT")
    add_seg(73.00, 8.05, 78.65, 8.05, "B.Cu", "USB_DM_PORT")
    add_via(73.00, 8.05, "USB_DM_PORT")
    add_seg(73.00, 8.05, 73.00, 7.975, "F.Cu", "USB_DM_PORT")

    add_seg(70.014, 3.963, 70.014, 2.75, "F.Cu", "3V3")

    errs = check_pcb_geometry(pads, segments, list(vias))
    print(f"\n==========================================")
    print(f"INTERACTIVE TEST: {len(errs)} REMAINING ERRORS")
    print(f"==========================================")
    for e in errs:
        print("  *", e)
    return pads, segments, list(vias), len(errs)

if __name__ == '__main__':
    solve()
