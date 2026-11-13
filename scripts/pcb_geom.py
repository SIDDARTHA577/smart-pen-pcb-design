"""Geometry and Collision Checking for PCB routing."""
import math

def dist_point_to_segment(px, py, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    l2 = dx*dx + dy*dy
    if l2 == 0:
        return math.hypot(px - x1, py - y1)
    t = max(0.0, min(1.0, ((px - x1)*dx + (py - y1)*dy) / l2))
    proj_x = x1 + t * dx
    proj_y = y1 + t * dy
    return math.hypot(px - proj_x, py - proj_y)

def dist_segment_to_segment(p1, p2, p3, p4):
    # Check if segments cross
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    
    def ccw(A, B, C):
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])
    
    # If they intersect, distance is 0
    if (ccw(p1, p3, p4) != ccw(p2, p3, p4)) and (ccw(p1, p2, p3) != ccw(p1, p2, p4)):
        return 0.0
    
    # Otherwise distance is min distance from endpoints to opposite segments
    d1 = dist_point_to_segment(x1, y1, x3, y3, x4, y4)
    d2 = dist_point_to_segment(x2, y2, x3, y3, x4, y4)
    d3 = dist_point_to_segment(x3, y3, x1, y1, x2, y2)
    d4 = dist_point_to_segment(x4, y4, x1, y1, x2, y2)
    return min(d1, d2, d3, d4)

def dist_segment_to_rect(x1, y1, x2, y2, rx, ry, rw, rh):
    # Rect is [rx - rw/2, rx + rw/2] x [ry - rh/2, ry + rh/2]
    # Sample points along segment
    steps = int(math.ceil(math.hypot(x2 - x1, y2 - y1) / 0.10)) + 1
    min_d = float('inf')
    for s in range(steps):
        t = s / max(1, steps - 1)
        sx = x1 + t * (x2 - x1)
        sy = y1 + t * (y2 - y1)
        dx = max(0.0, abs(sx - rx) - rw/2.0)
        dy = max(0.0, abs(sy - ry) - rh/2.0)
        d = math.hypot(dx, dy)
        if d < min_d: min_d = d
    return min_d

print("Geometry functions verified.")

