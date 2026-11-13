"""Test fixing the clearance owner in AStarPCBRouter."""
import math

class TestRouter:
    def __init__(self, width_mm=84.0, height_mm=9.2, res=0.10):
        self.res = res
        self.nx = int(math.ceil(width_mm / res)) + 1
        self.ny = int(math.ceil(height_mm / res)) + 1
        # Maps (gx, gy) -> net_id of pad/track
        # Maps (gx, gy) -> set of net_ids that claim this as clearance
        self.pad_layer = [{}, {}] # 0 = F.Cu, 1 = B.Cu
        self.clr_layer = [{}, {}]

    def to_grid(self, x, y):
        gx = int(round(x / self.res))
        gy = int(round(y / self.res))
        return max(3, min(self.nx - 4, gx)), max(3, min(self.ny - 4, gy))

    def add_pad(self, x, y, w, h, net_id):
        clr = 0.15
        gx_c, gy_c = self.to_grid(x, y)
        rx = int(math.ceil((w / 2.0) / self.res))
        ry = int(math.ceil((h / 2.0) / self.res))
        rx_clr = int(math.ceil((w / 2.0 + clr) / self.res))
        ry_clr = int(math.ceil((h / 2.0 + clr) / self.res))

        for dx in range(-rx_clr, rx_clr + 1):
            for dy in range(-ry_clr, ry_clr + 1):
                gx, gy = gx_c + dx, gy_c + dy
                if 0 <= gx < self.nx and 0 <= gy < self.ny:
                    if abs(dx) <= rx and abs(dy) <= ry:
                        self.pad_layer[0][(gx, gy)] = net_id
                    else:
                        if (gx, gy) not in self.clr_layer[0]:
                            self.clr_layer[0][(gx, gy)] = set()
                        self.clr_layer[0][(gx, gy)].add(net_id)

    def is_free(self, gx, gy, layer, net_id):
        if gx < 3 or gx >= self.nx - 3 or gy < 3 or gy >= self.ny - 3:
            return False
        # Check pad collision
        p = self.pad_layer[layer].get((gx, gy), 0)
        if p != 0 and p != net_id:
            return False
        # Check clearance collision: if another net claims this clearance
        clr_owners = self.clr_layer[layer].get((gx, gy))
        if clr_owners:
            for owner in clr_owners:
                if owner != net_id:
                    return False
        return True

print("TestRouter structure defined.")

