"""Hybrid Highway + A* Router to achieve 100% (41/41) routed nets."""
import json
import uuid
import sys
sys.path.insert(0, '.')
from scripts.astar_pcb_router import AStarPCBRouter

def run_hybrid_routing():
    with open('output/RevF_Working/solved_coords.json') as f:
        coords = json.load(f)
    with open('output/RevF_Working/SmartPen_RevE_PCB.json') as f:
        pcb_json = json.load(f)
    import csv
    with open('reports/RevF/FOOTPRINT_AUDIT.csv') as f:
        parts_audit = {r['Reference']: r for r in csv.DictReader(f)}

    nets = set(['GND'])
    for item in pcb_json['shape']:
        if isinstance(item, str) and item.startswith('LIB~'):
            subs = item.split('#@$')
            for sub in subs:
                if sub.startswith('PAD~'):
                    ptoks = sub.split('~')
                    if len(ptoks) > 7 and ptoks[7]:
                        nets.add(ptoks[7])
    sorted_nets = [''] + sorted(list(nets))
    net_id_map = {n: i for i, n in enumerate(sorted_nets)}

    # Extract pad offsets
    fp_defs = {}
    for item in pcb_json['shape']:
        if isinstance(item, str) and item.startswith('LIB~'):
            subs = item.split('#@$')
            ref = ''
            for sub in subs:
                if sub.startswith('TEXT~P~'):
                    ref = sub.split('~')[10]
            if not ref:
                continue
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
                    pnet = ptoks[7]
                    pnum = ptoks[8]
                    pads.append({
                        'num': pnum, 'net': pnet,
                        'dx': round(dx, 4), 'dy': round(dy, 4),
                        'w': round(pw, 4), 'h': round(ph, 4)
                    })
            fp_defs[ref] = pads

    # Compute absolute pad locations
    net_pads = {net: [] for net in sorted_nets if net}
    all_pads = []
    for ref, pos in coords.items():
        if ref not in fp_defs:
            continue
        cx, cy = pos
        for p in fp_defs[ref]:
            p_abs_x = round(cx + p['dx'], 4)
            p_abs_y = round(cy + p['dy'], 4)
            pnet = p['net']
            all_pads.append((p_abs_x, p_abs_y, p['w'], p['h'], net_id_map.get(pnet, 0)))
            if pnet:
                net_pads[pnet].append({
                    'ref': ref, 'pin': p['num'],
                    'x': p_abs_x, 'y': p_abs_y,
                    'w': p['w'], 'h': p['h']
                })

    router = AStarPCBRouter(width_mm=84.0, height_mm=9.2, grid_res=0.10)
    for pad in all_pads:
        router.add_pad_obstacle(pad[0], pad[1], pad[2], pad[3], pad[4])

    non_gnd_nets = [n for n in sorted_nets if n and n != 'GND']

    # Custom highway assignments on B.Cu
    highways = {
        '3V3': 1.0,
        'USB_DM_CORE': 1.6,
        'USB_DP_CORE': 2.2,
        'SD_MISO': 2.8,
        'I2C_SDA': 3.4,
        'I2C_SCL': 4.0,
        'TOUCH_OUT': 4.6,
        'CHG_STAT': 5.2,
        'VBAT_SW': 5.8,
        'SD_CS': 6.4,
        'UART_RX': 7.0,
        'RF_LNA': 8.0,
    }

    # Pre-reserve highways in router
    for net, y_hw in highways.items():
        nid = net_id_map[net]
        plist = net_pads[net]
        if not plist: continue
        xs = [p['x'] for p in plist]
        gx1, gy = router.to_grid(min(xs), y_hw)
        gx2, _  = router.to_grid(max(xs), y_hw)
        for gx in range(gx1, gx2 + 1):
            router.occ_b[(gx, gy)] = nid

    # Route all nets
    def net_priority(n):
        if n in highways: return 0 # Route highways first
        plist = net_pads[n]
        if not plist: return 999
        xs = [p['x'] for p in plist]
        return max(xs) - min(xs)

    sorted_nets_by_pri = sorted(non_gnd_nets, key=net_priority)

    routed_paths = {}
    success_count = 0
    fail_count = 0

    print(f"Routing {len(sorted_nets_by_pri)} nets with hybrid highways...")
    for net in sorted_nets_by_pri:
        plist = net_pads[net]
        nid = net_id_map[net]
        if len(plist) < 2:
            continue
        
        plist_sorted = sorted(plist, key=lambda p: p['x'])
        net_paths = []
        net_ok = True

        for i in range(len(plist_sorted) - 1):
            p1 = (plist_sorted[i]['x'], plist_sorted[i]['y'])
            p2 = (plist_sorted[i+1]['x'], plist_sorted[i+1]['y'])
            path = router.route_net(p1, p2, nid)
            if path:
                net_paths.append(path)
            else:
                net_ok = False
                break
        
        if net_ok:
            routed_paths[net] = net_paths
            success_count += 1
        else:
            fail_count += 1
            print(f"  FAILED net: {net}")

    print(f"\nFinal Hybrid Routing Result: {success_count} succeeded, {fail_count} failed.")

    # Save routed paths to JSON for KiCad export
    if fail_count == 0:
        with open('output/RevF_Working/routed_paths.json', 'w') as f:
            json.dump({k: [[[round(pt[0]*0.1, 3), round(pt[1]*0.1, 3), pt[2]] for pt in seg] for seg in v] for k, v in routed_paths.items()}, f)
        print("Saved routed_paths.json successfully!")

if __name__ == '__main__':
    run_hybrid_routing()
