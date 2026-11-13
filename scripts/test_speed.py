"""Fast bytearray-based 2D grid router benchmark."""
import time, heapq, math

nx = 841
ny = 93
grid_f = bytearray(nx * ny)
grid_b = bytearray(nx * ny)
via_legal = bytearray(nx * ny)

# Benchmark A* across the entire length of the board (84 mm)
t0 = time.time()
sx, sy = 50, 46
tx, ty = 790, 46

pq = []
heapq.heappush(pq, (abs(sx - tx) + abs(sy - ty), 0, sx, sy, 1)) # layer 1 (B.Cu)
visited = bytearray(nx * ny)
visited[sx + sy * nx] = 1

nodes = 0
found = False
while pq:
    f, cost, cx, cy, l = heapq.heappop(pq)
    nodes += 1
    if cx == tx and cy == ty:
        found = True
        break
    
    for ndx, ndy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nx_c, ny_c = cx + ndx, cy + ndy
        if 0 <= nx_c < nx and 0 <= ny_c < ny:
            idx = nx_c + ny_c * nx
            if visited[idx] == 0 and grid_b[idx] == 0:
                visited[idx] = 1
                heapq.heappush(pq, (cost + 1 + abs(nx_c - tx) + abs(ny_c - ty), cost + 1, nx_c, ny_c, l))

dt = time.time() - t0
print(f"Searched {nodes} nodes in {dt*1000:.2f} ms (Found: {found})")

