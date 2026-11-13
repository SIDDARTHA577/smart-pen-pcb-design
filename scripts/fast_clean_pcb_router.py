"""Fast Bytearray-based 2-Layer A* Router for Smart Pen Rev F PCB."""
import json, math, heapq, time, uuid, csv
from pathlib import Path

class FastPCBRouter:
    def __init__(self, width=84.0, height=9.2, res=0.10):
        self.width = width
        self.height = height
        self.res = res
        self.nx = int(math.ceil(width / res)) + 1
        self.ny = int(math.ceil(height / res)) + 1
        self.size = self.nx * self.ny
        
        # Copper maps: 0 = free, >0 = net_id
        self.copper_f = [0] * self.size
        self.copper_b = [0] * self.size
        
        # Clearance ownership: idx -> set of net_ids
        self.clr_f = {}
        self.clr_b = {}
        
        # Placed vias: list of (gx, gy, net_id)
        self.vias = []
        
        # Board edge border (0.35 mm = 4 cells)
        self.bx = 4
        self.by = 4

    def to_grid(self, x, y):
        gx = int(round(x / self.res))
        gy = int(round(y / self.res))
        gx = max(self.bx, min(self.nx - 1 - self.bx, gx))
        gy = max(self.by, min(self.ny - 1 - self.by, gy))
        return gx, gy

    def to_mm(self, gx, gy):
        return round(gx * self.res, 3), round(gy * self.res, 3)

    def add_pad(self, x, y, w, h, net_id):
        gx_c, gy_c = self.to_grid(x, y)
        rx = int(math.ceil((w / 2.0) / self.res))
        ry = int(math.ceil((h / 2.0) / self.res))
        clr_cells = 2 # 0.20 mm clearance

        # Pad copper
        for dx in range(-rx, rx + 1):
            for dy in range(-ry, ry + 1):
                gx = gx_c + dx
                gy = gy_c + dy
                if 0 <= gx < self.nx and 0 <= gy < self.ny:
                    self.copper_f[gx + gy * self.nx] = net_id

        # Pad clearance
        for dx in range(-rx - clr_cells, rx + clr_cells + 1):
            for dy in range(-ry - clr_cells, ry + clr_cells + 1):
                gx = gx_c + dx
                gy = gy_c + dy
                if 0 <= gx < self.nx and 0 <= gy < self.ny:
                    idx = gx + gy * self.nx
                    if self.copper_f[idx] == 0:
                        if idx not in self.clr_f:
                            self.clr_f[idx] = set()
                        self.clr_f[idx].add(net_id)

    def is_free(self, layer, gx, gy, net_id):
        if gx < self.bx or gx >= self.nx - self.bx or gy < self.by or gy >= self.ny - self.by:
            return False
        idx = gx + gy * self.nx
        copper = self.copper_f if layer == 0 else self.copper_b
        c = copper[idx]
        if c != 0 and c != net_id:
            return False
        
        clr_map = self.clr_f if layer == 0 else self.clr_b
        clrs = clr_map.get(idx)
        if clrs:
            for owner in clrs:
                if owner != net_id:
                    return False
        return True

    def is_via_legal(self, gx, gy, net_id):
        # Via total radius 4 cells (0.40 mm), hole clearance 6 cells (0.60 mm)
        if gx - 4 < self.bx or gx + 4 >= self.nx - self.bx or gy - 4 < self.by or gy + 4 >= self.ny - self.by:
            return False

        # Hole-to-hole check
        for vx, vy, vn in self.vias:
            if (gx - vx)**2 + (gy - vy)**2 < 36: # 6 cells squared
                return False

        # Check copper & clearance on both layers
        for dx in range(-4, 5):
            for dy in range(-4, 5):
                if dx*dx + dy*dy <= 16:
                    idx = (gx + dx) + (gy + dy) * self.nx
                    # F.Cu
                    cf = self.copper_f[idx]
                    if cf != 0 and cf != net_id: return False
                    clrs_f = self.clr_f.get(idx)
                    if clrs_f:
                        for o in clrs_f:
                            if o != net_id: return False
                    # B.Cu
                    cb = self.copper_b[idx]
                    if cb != 0 and cb != net_id: return False
                    clrs_b = self.clr_b.get(idx)
                    if clrs_b:
                        for o in clrs_b:
                            if o != net_id: return False
        return True

    def commit_path(self, path, net_id):
        clr_cells = 2
        for i, (l, gx, gy) in enumerate(path):
            copper = self.copper_f if l == 0 else self.copper_b
            clr_map = self.clr_f if l == 0 else self.clr_b
            copper[gx + gy * self.nx] = net_id
            for dx in range(-clr_cells, clr_cells + 1):
                for dy in range(-clr_cells, clr_cells + 1):
                    if dx*dx + dy*dy <= 4:
                        px = gx + dx
                        py = gy + dy
                        if 0 <= px < self.nx and 0 <= py < self.ny:
                            idx = px + py * self.nx
                            if copper[idx] == 0:
                                if idx not in clr_map: clr_map[idx] = set()
                                clr_map[idx].add(net_id)

        # Check vias
        for i in range(len(path) - 1):
            l1, x1, y1 = path[i]
            l2, x2, y2 = path[i+1]
            if l1 != l2:
                self.vias.append((x1, y1, net_id))
                for dx in range(-4, 5):
                    for dy in range(-4, 5):
                        if dx*dx + dy*dy <= 16:
                            px = x1 + dx
                            py = y1 + dy
                            if 0 <= px < self.nx and 0 <= py < self.ny:
                                idx = px + py * self.nx
                                self.copper_f[idx] = net_id
                                self.copper_b[idx] = net_id

    def route_connection(self, start_pt, target_pt, net_id):
        sx, sy = self.to_grid(start_pt[0], start_pt[1])
        tx, ty = self.to_grid(target_pt[0], target_pt[1])

        # Priority queue: (f_score, cost, (layer, gx, gy, cdx, cdy))
        pq = []
        start_state = (0, sx, sy, 0, 0)
        h0 = abs(sx - tx) + abs(sy - ty)
        heapq.heappush(pq, (h0, 0, start_state))
        
        visited = set()
        came_from = {}
        found_state = None
        max_iter = 40000
        iters = 0

        while pq and iters < max_iter:
            iters += 1
            f, cost, (l, cx, cy, cdx, cdy) = heapq.heappop(pq)

            if cx == tx and cy == ty:
                found_state = (l, cx, cy, cdx, cdy)
                break

            state_key = (l, cx, cy, cdx, cdy)
            if state_key in visited:
                continue
            visited.add(state_key)

            # 1. Neighbor moves on same layer
            for ndx, ndy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = cx + ndx, cy + ndy
                if self.is_free(l, nx, ny, net_id):
                    turn_penalty = 0.5 if (cdx != 0 or cdy != 0) and (ndx != cdx or ndy != cdy) else 0.0
                    step_cost = 1.0 if l == 1 else 1.5
                    new_cost = cost + step_cost + turn_penalty
                    h = (abs(nx - tx) + abs(ny - ty)) * 1.1
                    nxt = (l, nx, ny, ndx, ndy)
                    if nxt not in visited:
                        heapq.heappush(pq, (new_cost + h, new_cost, nxt))
                        if nxt not in came_from:
                            came_from[nxt] = (l, cx, cy, cdx, cdy)

            # 2. Via transition (only check if distance to target > 5 cells or at target)
            other_layer = 1 - l
            if (cx != sx or cy != sy) and self.is_via_legal(cx, cy, net_id):
                via_cost = cost + 8.0
                h = (abs(cx - tx) + abs(cy - ty)) * 1.1
                nxt = (other_layer, cx, cy, 0, 0)
                if nxt not in visited:
                    heapq.heappush(pq, (via_cost + h, via_cost, nxt))
                    if nxt not in came_from:
                        came_from[nxt] = (l, cx, cy, cdx, cdy)

        if not found_state:
            print(f"DEBUG: iters={iters}, pq_len={len(pq)}, visited={len(visited)}")
            return None

        # Reconstruct path
        path = []
        curr = found_state
        while curr in came_from:
            path.append((curr[0], curr[1], curr[2]))
            curr = came_from[curr]
        path.append((0, sx, sy))
        path.reverse()
        return path

print("FastPCBRouter defined.")
