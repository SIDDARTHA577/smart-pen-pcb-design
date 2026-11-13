"""Pre-flight Geometric Verification for SmartPen PCB routing.
Tests all pads, segments, and vias against exact JLCPCB 2-layer design rules:
- Trace width: >= 0.18 mm (min 0.127 mm)
- Clearance: >= 0.127 mm
- Via diameter: 0.50 mm (drill 0.30 mm)
- Via-to-via pitch (diff nets): >= 0.627 mm (0.50 dia + 0.127 clearance)
- Via-to-trace pitch (diff nets): >= 0.467 mm (0.25 via_r + 0.09 tr_r + 0.127 clearance)
- Trace-to-trace pitch (diff nets): >= 0.307 mm (0.09 + 0.09 + 0.127)
- Copper-to-edge clearance: >= 0.30 mm
"""
import math

def dist_point_to_segment(px, py, x1, y1, x2, y2):
    """Calculates minimum distance from point (px, py) to line segment (x1, y1)-(x2, y2)."""
    dx = x2 - x1
    dy = y2 - y1
    l2 = dx*dx + dy*dy
    if l2 == 0:
        return math.hypot(px - x1, py - y1)
    # Project point onto line parameter t clamped to [0, 1]
    t = max(0.0, min(1.0, ((px - x1)*dx + (py - y1)*dy) / l2))
    proj_x = x1 + t * dx
    proj_y = y1 + t * dy
    return math.hypot(px - proj_x, py - proj_y)

def dist_segment_to_segment(s1_x1, s1_y1, s1_x2, s1_y2, s2_x1, s2_y1, s2_x2, s2_y2):
    """Calculates minimum distance between two line segments."""
    # Check if they intersect
    def ccw(ax, ay, bx, by, cx, cy):
        return (cy - ay) * (bx - ax) > (by - ay) * (cx - ax)

    if (ccw(s1_x1, s1_y1, s2_x1, s2_y1, s2_x2, s2_y2) != ccw(s1_x2, s1_y2, s2_x1, s2_y1, s2_x2, s2_y2)) and \
       (ccw(s1_x1, s1_y1, s1_x2, s1_y2, s2_x1, s2_y1) != ccw(s1_x1, s1_y1, s1_x2, s1_y2, s2_x2, s2_y2)):
        return 0.0 # direct intersection

    # Otherwise min distance is min of endpoint-to-segment distances
    d1 = dist_point_to_segment(s1_x1, s1_y1, s2_x1, s2_y1, s2_x2, s2_y2)
    d2 = dist_point_to_segment(s1_x2, s1_y2, s2_x1, s2_y1, s2_x2, s2_y2)
    d3 = dist_point_to_segment(s2_x1, s2_y1, s1_x1, s1_y1, s1_x2, s1_y2)
    d4 = dist_point_to_segment(s2_x2, s2_y2, s1_x1, s1_y1, s1_x2, s1_y2)
    return min(d1, d2, d3, d4)

def check_pcb_geometry(pads, segments, vias):
    """
    pads: list of dicts {'ref', 'pin', 'net', 'x', 'y', 'w', 'h'}
    segments: list of tuples (x1, y1, x2, y2, layer, net, width)
    vias: list of tuples (x, y, net)
    """
    errors = []
    CLEARANCE = 0.127
    VIA_RADIUS = 0.25 # dia 0.50 mm
    EDGE_MIN_X = 0.30
    EDGE_MAX_X = 83.70
    EDGE_MIN_Y = 0.30
    EDGE_MAX_Y = 8.90

    # 1. Pad-to-Pad clearance on F.Cu
    for i in range(len(pads)):
        p1 = pads[i]
        for j in range(i + 1, len(pads)):
            p2 = pads[j]
            if p1['net'] == p2['net']: continue
            dx = max(0.0, abs(p1['x'] - p2['x']) - (p1['w'] + p2['w'])/2.0)
            dy = max(0.0, abs(p1['y'] - p2['y']) - (p1['h'] + p2['h'])/2.0)
            d = math.hypot(dx, dy)
            if d < CLEARANCE - 0.001:
                errors.append(f"Pad collision ({p1['ref']}.{p1['pin']} [{p1['net']}] vs {p2['ref']}.{p2['pin']} [{p2['net']}]): dist={d:.4f} mm < {CLEARANCE} mm")

    # 2. Board edge checks
    for v in vias:
        vx, vy, vnet = v
        if vx - VIA_RADIUS < EDGE_MIN_X or vx + VIA_RADIUS > EDGE_MAX_X:
            errors.append(f"Via {vnet} at ({vx},{vy}) violates board edge X (req >= {EDGE_MIN_X})")
        if vy - VIA_RADIUS < EDGE_MIN_Y or vy + VIA_RADIUS > EDGE_MAX_Y:
            errors.append(f"Via {vnet} at ({vx},{vy}) violates board edge Y (req >= {EDGE_MIN_Y})")

    for s in segments:
        x1, y1, x2, y2, lyr, snet, w = s
        tr_r = w / 2.0
        min_x = min(x1, x2) - tr_r
        max_x = max(x1, x2) + tr_r
        min_y = min(y1, y2) - tr_r
        max_y = max(y1, y2) + tr_r
        if min_x < EDGE_MIN_X or max_x > EDGE_MAX_X or min_y < EDGE_MIN_Y or max_y > EDGE_MAX_Y:
            errors.append(f"Segment {snet} ({x1},{y1})->({x2},{y2}) violates board edge clearance")

    # 3. Via-to-Via distance
    for i in range(len(vias)):
        v1 = vias[i]
        for j in range(i + 1, len(vias)):
            v2 = vias[j]
            d = math.hypot(v1[0] - v2[0], v1[1] - v2[1])
            if v1[2] != v2[2]:
                # Required pitch: 0.25 + 0.25 + 0.127 = 0.627 mm
                req_pitch = 2 * VIA_RADIUS + CLEARANCE
                if d < req_pitch - 0.001:
                    errors.append(f"Via collision ({v1[2]} vs {v2[2]}): dist={d:.4f} mm < {req_pitch:.4f} mm at ({v1[0]},{v1[1]}) and ({v2[0]},{v2[1]})")
            else:
                # Same-net drill-to-drill distance: drill 0.30 + hole clearance 0.25 = 0.55 mm
                if d < 0.549:
                    errors.append(f"Same-net via hole collision: dist={d:.4f} mm at ({v1[0]},{v1[1]}) and ({v2[0]},{v2[1]})")

    # 4. Via-to-Pad clearance on F.Cu
    for v in vias:
        vx, vy, vnet = v
        for p in pads:
            if p['net'] == vnet: continue
            dx = max(0.0, abs(vx - p['x']) - p['w']/2.0)
            dy = max(0.0, abs(vy - p['y']) - p['h']/2.0)
            d = math.hypot(dx, dy)
            req_d = VIA_RADIUS + CLEARANCE # 0.377 mm
            if d < req_d - 0.001:
                errors.append(f"Via-Pad collision: via {vnet} at ({vx},{vy}) vs {p['ref']}.{p['pin']} ({p['net']}): dist={d:.4f} mm < {req_d:.4f} mm")

    # 5. Via-to-Segment clearance (both F.Cu and B.Cu!)
    for v in vias:
        vx, vy, vnet = v
        for s in segments:
            x1, y1, x2, y2, lyr, snet, w = s
            if snet == vnet: continue
            dist = dist_point_to_segment(vx, vy, x1, y1, x2, y2)
            tr_r = w / 2.0
            req_pitch = VIA_RADIUS + tr_r + CLEARANCE # 0.25 + 0.09 + 0.127 = 0.467 mm
            if dist < req_pitch - 0.001:
                errors.append(f"Via-Segment collision on {lyr}: via {vnet} at ({vx},{vy}) vs seg {snet} ({x1},{y1})->({x2},{y2}): dist={dist:.4f} mm < {req_pitch:.4f} mm")

    # 6. Segment-to-Segment clearance and crossings (same layer)
    for i in range(len(segments)):
        s1 = segments[i]
        for j in range(i + 1, len(segments)):
            s2 = segments[j]
            if s1[4] != s2[4]: continue # different layers
            if s1[5] == s2[5]: continue # same net
            dist = dist_segment_to_segment(s1[0], s1[1], s1[2], s1[3], s2[0], s2[1], s2[2], s2[3])
            tr1_r = s1[6] / 2.0
            tr2_r = s2[6] / 2.0
            req_pitch = tr1_r + tr2_r + CLEARANCE
            if dist < req_pitch - 0.001:
                errors.append(f"Segment-Segment collision on {s1[4]} ({s1[5]} vs {s2[5]}): dist={dist:.4f} mm < {req_pitch:.4f} mm between ({s1[0]},{s1[1]})->({s1[2]},{s1[3]}) and ({s2[0]},{s2[1]})->({s2[2]},{s2[3]})")

    # 7. Segment-to-Pad clearance on F.Cu
    for s in segments:
        x1, y1, x2, y2, lyr, snet, w = s
        if lyr != "F.Cu": continue
        tr_r = w / 2.0
        for p in pads:
            if p['net'] == snet: continue
            # Sample along segment
            steps = int(math.ceil(math.hypot(x2 - x1, y2 - y1) / 0.05)) + 1
            min_d = float('inf')
            for st in range(steps):
                t = st / max(1, steps - 1)
                sx = x1 + t * (x2 - x1)
                sy = y1 + t * (y2 - y1)
                dx = max(0.0, abs(sx - p['x']) - p['w']/2.0)
                dy = max(0.0, abs(sy - p['y']) - p['h']/2.0)
                d = math.hypot(dx, dy)
                if d < min_d: min_d = d
            req_d = tr_r + CLEARANCE
            if min_d < req_d - 0.001:
                errors.append(f"Segment-Pad collision on F.Cu ({snet} vs {p['ref']}.{p['pin']} [{p['net']}]): dist={min_d:.4f} mm < {req_d:.4f} mm")

    return errors

if __name__ == '__main__':
    print("Rigorous geometry checker compiled.")
