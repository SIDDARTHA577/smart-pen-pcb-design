"""Robust 2-Layer Grid Router for Smart Pen Rev F PCB.
Tests routing all 41 non-GND nets with exact physical clearances.
"""
import heapq
import json
import math
import time
import csv

class CleanPCBRouter:
    def __init__(self, width=84.0, height=9.2, res=0.10):
        self.width = width
        self.height = height
        self.res = res
        self.nx = int(math.ceil(width / res)) + 1
        self.ny = int(math.ceil(height / res)) + 1
        
        # Grid layers: 0 = F.Cu, 1 = B.Cu
        # Maps (layer, gx, gy) -> net_id of copper item (pad, track, via)
        self.copper = {}
        # Maps (layer, gx, gy) -> set of net_ids claiming clearance
        self.clearance = {}
        # Via centers: set of (gx, gy, net_id)
        self.vias = set()
        
        # Edge clearance: 0.35 mm from board edges
        self.bx = int(math.ceil(0.35 / res))
        self.by = int(math.ceil(0.35 / res))

    def to_grid(self, x, y):
        gx = int(round(x / self.res))
        gy = int(round(y / self.res))
        gx = max(self.bx, min(self.nx - 1 - self.bx, gx))
        gy = max(self.by, min(self.ny - 1 - self.by, gy))
        return gx, gy

    def to_mm(self, gx, gy):
        return round(gx * self.res, 3), round(gy * self.res, 3)

    def add_pad(self, x, y, w, h, net_id):
        """Register a rectangular pad on F.Cu with 0.15 mm clearance."""
        gx_c, gy_c = self.to_grid(x, y)
        clr = 0.15
        rx = int(math.ceil((w / 2.0) / self.res))
        ry = int(math.ceil((h / 2.0) / self.res))
        rx_clr = int(math.ceil((w / 2.0 + clr) / self.res))
        ry_clr = int(math.ceil((h / 2.0 + clr) / self.res))

        for dx in range(-rx_clr, rx_clr + 1):
            for dy in range(-ry_clr, ry_clr + 1):
                gx = gx_c + dx
                gy = gy_c + dy
                if 0 <= gx < self.nx and 0 <= gy < self.ny:
                    if abs(dx) <= rx and abs(dy) <= ry:
                        self.copper[(0, gx, gy)] = net_id
                    else:
                        key = (0, gx, gy)
                        if key not in self.clearance:
                            self.clearance[key] = set()
                        self.clearance[key].add(net_id)

    def is_cell_free(self, layer, gx, gy, net_id):
        """Check if cell is walkable for net_id."""
        if gx < self.bx or gx >= self.nx - self.bx:
            return False
        if gy < self.by or gy >= self.ny - self.by:
            return False
        
        # Check copper
        c = self.copper.get((layer, gx, gy), 0)
        if c != 0 and c != net_id:
            return False
        
        # Check clearance claimed by foreign nets
        clrs = self.clearance.get((layer, gx, gy))
        if clrs:
            for owner in clrs:
                if owner != net_id:
                    return False
        return True

    def is_via_legal(self, gx, gy, net_id):
        """Check if a via (dia 0.50 mm, drill 0.30 mm, clearance 0.15 mm -> radius 0.40 mm) can be placed at (gx, gy)."""
        # Board edge clearance: via edge must be >= 0.35 mm from outline
        r_via_copper = int(math.ceil(0.25 / self.res))
        r_via_total = int(math.ceil(0.40 / self.res)) # 4 cells
        r_via_hole = int(math.ceil(0.55 / self.res))  # 6 cells for hole-to-hole

        if gx - r_via_total < self.bx or gx + r_via_total >= self.nx - self.bx:
            return False
        if gy - r_via_total < self.by or gy + r_via_total >= self.ny - self.by:
            return False

        # Hole-to-hole check with existing vias
        for vx, vy, vn in self.vias:
            if (gx - vx)**2 + (gy - vy)**2 < r_via_hole**2:
                return False

        # Clearance check on both layers
        for dx in range(-r_via_total, r_via_total + 1):
            for dy in range(-r_via_total, r_via_total + 1):
                if dx*dx + dy*dy <= r_via_total**2:
                    for l in (0, 1):
                        c = self.copper.get((l, gx + dx, gy + dy), 0)
                        if c != 0 and c != net_id:
                            return False
                        clrs = self.clearance.get((l, gx + dx, gy + dy))
                        if clrs:
                            for owner in clrs:
                                if owner != net_id:
                                    return False
        return True

    def commit_path(self, path, net_id):
        """Mark path copper and clearance into grid."""
        r_tr_clr = int(math.ceil((0.10 + 0.15) / self.res)) # 3 cells
        for i, (l, gx, gy) in enumerate(path):
            self.copper[(l, gx, gy)] = net_id
            for dx in range(-r_tr_clr, r_tr_clr + 1):
                for dy in range(-r_tr_clr, r_tr_clr + 1):
                    if dx*dx + dy*dy <= r_tr_clr**2:
                        key = (l, gx + dx, gy + dy)
                        if key not in self.copper:
                            if key not in self.clearance:
                                self.clearance[key] = set()
                            self.clearance[key].add(net_id)

        # Check vias
        for i in range(len(path) - 1):
            l1, x1, y1 = path[i]
            l2, x2, y2 = path[i+1]
            if l1 != l2:
                # Via at (x1, y1)
                self.vias.add((x1, y1, net_id))
                r_via = int(math.ceil(0.40 / self.res))
                for dx in range(-r_via, r_via + 1):
                    for dy in range(-r_via, r_via + 1):
                        if dx*dx + dy*dy <= r_via**2:
                            for l in (0, 1):
                                self.copper[(l, x1 + dx, y1 + dy)] = net_id

    def route_segment(self, start_pt, target_pt, net_id):
        """A* search from start_pt to target_pt."""
        sx, sy = self.to_grid(start_pt[0], start_pt[1])
        tx, ty = self.to_grid(target_pt[0], target_pt[1])

        # State: (layer, gx, gy)
        # Priority queue: (f_score, cost, layer, gx, gy, dir_x, dir_y)
        pq = []
        start_state = (0, sx, sy, 0, 0)
        heapq.heappush(pq, (abs(sx - tx) + abs(sy - ty), 0, start_state))
        
        came_from = {}
        cost_so_far = {start_state: 0}
        found_state = None
        max_iter = 60000
        iterations = 0

        while pq and iterations < max_iter:
            iterations += 1
            f, cost, (l, cx, cy, cdx, cdy) = heapq.heappop(pq)

            if cx == tx and cy == ty:
                found_state = (l, cx, cy, cdx, cdy)
                break

            if cost > cost_so_far.get((l, cx, cy, cdx, cdy), float('inf')):
                continue

            # 1. Moves on same layer
            for ndx, ndy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = cx + ndx, cy + ndy
                if self.is_cell_free(l, nx, ny, net_id):
                    # Cost: layer 1 (B.Cu) preferred for long routes
                    step_cost = 1.0 if l == 1 else 1.2
                    turn_penalty = 0.4 if (cdx != 0 or cdy != 0) and (ndx != cdx or ndy != cdy) else 0.0
                    new_cost = cost + step_cost + turn_penalty
                    nxt = (l, nx, ny, ndx, ndy)
                    if new_cost < cost_so_far.get(nxt, float('inf')):
                        cost_so_far[nxt] = new_cost
                        h = (abs(nx - tx) + abs(ny - ty)) * 1.05
                        heapq.heappush(pq, (new_cost + h, new_cost, nxt))
                        came_from[nxt] = (l, cx, cy, cdx, cdy)

            # 2. Via transition
            other_layer = 1 - l
            if self.is_via_legal(cx, cy, net_id):
                via_cost = cost + 6.0
                nxt = (other_layer, cx, cy, 0, 0)
                if via_cost < cost_so_far.get(nxt, float('inf')):
                    cost_so_far[nxt] = via_cost
                    h = (abs(cx - tx) + abs(cy - ty)) * 1.05
                    heapq.heappush(pq, (via_cost + h, via_cost, nxt))
                    came_from[nxt] = (l, cx, cy, cdx, cdy)

        if not found_state:
            return None

        # Reconstruct path: list of (layer, gx, gy)
        path = []
        curr = found_state
        while curr in came_from:
            path.append((curr[0], curr[1], curr[2]))
            curr = came_from[curr]
        path.append((0, sx, sy))
        path.reverse()
        return path

print("CleanPCBRouter defined.")

