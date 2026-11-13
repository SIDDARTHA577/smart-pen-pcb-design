import sys
sys.path.insert(0, '.')
from scripts.solve_zero_drc import run_check

pads, segs, vias, errs = run_check()

def check_via_clear(vx, vy, net_name="3V3"):
    # Check against all pads of other nets
    for p in pads:
        if p['net'] == net_name: continue
        px, py, pw, ph = p['x'], p['y'], p['w'], p['h']
        dx = max(0, abs(vx - px) - pw/2)
        dy = max(0, abs(vy - py) - ph/2)
        dist = (dx**2 + dy**2)**0.5
        if dist < 0.25 + 0.127: # via radius (0.25) + min clearance (0.127)
            return False, f"pad {p['ref']}.{p['pin']} ({p['net']}) dist={dist:.3f}"
    
    # Check against all existing vias
    for v in vias:
        if (v[0] - vx)**2 + (v[1] - vy)**2 < 0.58**2:
            return False, f"via {v[2]} at ({v[0]}, {v[1]}) pitch={( (v[0]-vx)**2 + (v[1]-vy)**2 )**0.5:.3f}"
            
    # Check against all F.Cu segments of other nets
    for s in segs:
        if s[5] == net_name: continue
        # Distance from point (vx, vy) to segment (s[0], s[1])-(s[2], s[3])
        x1, y1, x2, y2 = s[0], s[1], s[2], s[3]
        l2 = (x2 - x1)**2 + (y2 - y1)**2
        if l2 == 0:
            dist = ((vx - x1)**2 + (vy - y1)**2)**0.5
        else:
            t = max(0, min(1, ((vx - x1)*(x2 - x1) + (vy - y1)*(y2 - y1)) / l2))
            proj_x = x1 + t * (x2 - x1)
            proj_y = y1 + t * (y2 - y1)
            dist = ((vx - proj_x)**2 + (vy - proj_y)**2)**0.5
        if dist < 0.25 + s[6]/2 + 0.127:
            return False, f"seg {s[5]} on {s[4]} ({x1},{y1})->({x2},{y2}) dist={dist:.3f}"
    return True, "OK"

# Test candidate X positions for 3V3 vias at Y = 2.25
candidates = [7.5, 8.0, 13.5, 18.0, 19.475, 20.0, 25.5, 26.0, 31.0, 35.0, 37.0, 44.5, 45.0, 47.0, 50.0, 55.0, 57.0, 60.0, 66.0, 68.0, 69.5]
for x in candidates:
    ok, reason = check_via_clear(x, 2.25)
    print(f"X = {x:6.3f}, Y = 2.25: {ok} -> {reason}")
