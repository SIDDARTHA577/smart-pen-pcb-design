"""Route only 3V3 around locked 40 nets using A*."""
import sys, json, math
sys.path.insert(0, '.')
from scripts.solve_zero_drc import run_check
from scripts.astar_pcb_router import AStarPCBRouter
from scripts.export_final_pcb import compress_orthogonal_path
from scripts.verify_smartpen_geometry import check_pcb_geometry

pads, locked_segs, locked_vias, errs = run_check()

print(f"Locked baseline: {len(locked_segs)} segments, {len(locked_vias)} vias, 0 errors.")

# Set up router with 0.05 mm grid resolution
router = AStarPCBRouter(width_mm=84.0, height_mm=9.2, grid_res=0.05)

# Add all non-3V3 pads as obstacles
# net_id 1 is 3V3, all others are obstacles (net_id 2)
for p in pads:
    nid = 1 if p['net'] == '3V3' else 2
    router.add_pad_obstacle(p['x'], p['y'], p['w'], p['h'], nid)

# Add all locked segments as obstacles (net_id 2)
# With clearance of 0.15 mm
for s in locked_segs:
    layer_id = 0 if s[4] == "F.Cu" else 1
    # Trace obstacle along segment
    x1, y1, x2, y2 = s[0], s[1], s[2], s[3]
    steps = int(math.hypot(x2 - x1, y2 - y1) / 0.05) + 1
    for step in range(steps + 1):
        t = step / max(steps, 1)
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        gx, gy = router.to_grid(x, y)
        occ = router.occ_f if layer_id == 0 else router.occ_b
        # Mark with clearance radius (0.15 mm = 3 grid cells)
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                if dx*dx + dy*dy <= 9:
                    occ[(gx + dx, gy + dy)] = 2

# Add all locked vias as obstacles on both layers
for v in locked_vias:
    vx, vy = v[0], v[1]
    gx, gy = router.to_grid(vx, vy)
    # Via radius (0.25 mm) + clearance (0.15 mm) = 0.40 mm = 8 grid cells
    for dx in range(-8, 9):
        for dy in range(-8, 9):
            if dx*dx + dy*dy <= 64:
                router.occ_f[(gx + dx, gy + dy)] = 2
                router.occ_b[(gx + dx, gy + dy)] = 2

# List all 3V3 pads
p_3v3 = [p for p in pads if p['net'] == '3V3']
p_3v3_sorted = sorted(p_3v3, key=lambda p: p['x'])
print(f"Routing 3V3 across {len(p_3v3_sorted)} pads from X={p_3v3_sorted[0]['x']} to X={p_3v3_sorted[-1]['x']}...")

# Route sequential MST / chain of 3V3 pads
all_3v3_segs = []
all_3v3_vias = set()
failed = 0

for i in range(len(p_3v3_sorted) - 1):
    p1 = p_3v3_sorted[i]
    p2 = p_3v3_sorted[i+1]
    pt1 = (p1['x'], p1['y'])
    pt2 = (p2['x'], p2['y'])
    path = router.route_net(pt1, pt2, 1)
    if path:
        segs, v_list = compress_orthogonal_path(path)
        for s in segs:
            layer = "F.Cu" if s[4] == 0 else "B.Cu"
            all_3v3_segs.append((round(s[0], 3), round(s[1], 3), round(s[2], 3), round(s[3], 3), layer, "3V3", 0.20))
        for v in v_list:
            all_3v3_vias.add((round(v[0], 3), round(v[1], 3), "3V3"))
        print(f"  [OK] {p1['ref']}.{p1['pin']} -> {p2['ref']}.{p2['pin']} (len={len(path)})")
    else:
        print(f"  [FAIL] {p1['ref']}.{p1['pin']} -> {p2['ref']}.{p2['pin']}")
        failed += 1

print(f"\n3V3 Routing completed: {len(p_3v3_sorted) - 1 - failed} connected, {failed} failed.")
