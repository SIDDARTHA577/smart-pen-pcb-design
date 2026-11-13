import json, math

with open('output/RevF_Working/solved_coords.json') as f:
    coords = json.load(f)
with open('output/RevF_Working/SmartPen_RevE_PCB.json') as f:
    pcb_json = json.load(f)

nets = set(['GND'])
for item in pcb_json['shape']:
    if isinstance(item, str) and item.startswith('LIB~'):
        for sub in item.split('#@$'):
            if sub.startswith('PAD~'):
                ptoks = sub.split('~')
                if len(ptoks) > 7 and ptoks[7]:
                    nets.add(ptoks[7])
sorted_nets = [''] + sorted(list(nets))

fp_defs = {}
for item in pcb_json['shape']:
    if isinstance(item, str) and item.startswith('LIB~'):
        subs = item.split('#@$')
        ref = ''
        for sub in subs:
            if sub.startswith('TEXT~P~'):
                ref = sub.split('~')[10]
        if not ref: continue
        lib_toks = subs[0].split('~')
        orig_x, orig_y = float(lib_toks[1]), float(lib_toks[2])
        pads = []
        for sub in subs:
            if sub.startswith('PAD~'):
                ptoks = sub.split('~')
                dx = (float(ptoks[2]) - orig_x) * 0.254
                dy = (float(ptoks[3]) - orig_y) * 0.254
                pw = float(ptoks[4]) * 0.254
                ph = float(ptoks[5]) * 0.254
                pads.append({'num': ptoks[8], 'net': ptoks[7], 'dx': round(dx, 4), 'dy': round(dy, 4), 'w': round(pw, 4), 'h': round(ph, 4)})
        fp_defs[ref] = pads

all_pads = []
for ref, (cx, cy) in coords.items():
    if ref in fp_defs:
        for p in fp_defs[ref]:
            pnet = p['net']
            all_pads.append({
                'ref': ref, 'pin': p['num'], 'net': pnet,
                'x': round(cx + p['dx'], 4), 'y': round(cy + p['dy'], 4),
                'w': p['w'], 'h': p['h']
            })

def is_via_legal_at(vx, vy, net_name):
    if vx - 0.25 < 0.35 or vx + 0.25 > 83.65: return False
    if vy - 0.25 < 0.35 or vy + 0.25 > 8.85: return False
    for pad in all_pads:
        if pad['net'] == net_name: continue
        px, py, pw, ph = pad['x'], pad['y'], pad['w'], pad['h']
        dx = max(0.0, abs(vx - px) - pw/2.0)
        dy = max(0.0, abs(vy - py) - ph/2.0)
        if math.hypot(dx, dy) < 0.25 + 0.15:
            return False
    return True

# Test highway lanes for long nets
highways = {
    '3V3': 1.0,
    '3V3_RTC': 1.4,
    'MCU_EN': 1.8,
    'SD_CS': 2.2,
    'SD_SCK': 2.6,
    'SD_MOSI': 3.0,
    'SD_MISO': 3.4,
    'TOUCH_OUT': 3.8,
    'I2C_SDA': 4.2,
    'I2C_SCL': 4.6,
    'CHG_STAT': 5.0,
    'VBAT_SW': 5.4,
    'UART_TX': 5.8,
    'UART_RX': 6.2,
    'USB_DM_CORE': 6.6,
    'USB_DP_CORE': 7.0,
    '3V3_RF': 7.4,
    'USB_VBUS': 7.8,
    'VBAT': 8.2
}

print("Checking highway via placement...")
for net, y_hw in highways.items():
    plist = [p for p in all_pads if p['net'] == net]
    for p in plist:
        px, py = p['x'], p['y']
        # Try finding vx near px on y_hw
        found_vx = None
        for dx in [0.0, 0.2, -0.2, 0.4, -0.4, 0.6, -0.6, 0.8, -0.8, 1.0, -1.0, 1.2, -1.2, 1.5, -1.5, 2.0, -2.0]:
            vx = round(px + dx, 3)
            if is_via_legal_at(vx, y_hw, net):
                found_vx = vx
                break
        if not found_vx:
            print(f"Could not place via for {net} at {p['ref']}.{p['pin']} ({px}, {py}) on y={y_hw}")

print("Highway via placement test complete.")

