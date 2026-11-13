"""Test staggered fanout for U1, U3, and J_USB."""
import math

u1_bottom_pins = [
    (9, "SD_MOSI", 41.13, 2.44),
    (10, "SD_MISO", 41.63, 2.44),
    (11, "3V3_RTC", 42.13, 2.44),
    (12, "SD_SCK", 42.63, 2.44),
    (13, "SD_CS", 43.13, 2.44),
    (15, "BOOT9", 44.13, 2.44)
]

vias_staggered = []
for i, (pin, net, px, py) in enumerate(u1_bottom_pins):
    # Stagger: even indices go to Y = 1.60, odd indices go to Y = 0.90
    vy = 1.60 if (i % 2 == 0) else 0.90
    vx = px
    vias_staggered.append((vx, vy, net))

print("U1 Bottom Vias:")
for v in vias_staggered:
    print(f"  {v[2]:12s} at ({v[0]:.2f}, {v[1]:.2f})")

# Check distances between all pairs
min_dist = float('inf')
for i in range(len(vias_staggered)):
    for j in range(i + 1, len(vias_staggered)):
        v1 = vias_staggered[i]
        v2 = vias_staggered[j]
        d = math.hypot(v1[0] - v2[0], v1[1] - v2[1])
        if d < min_dist: min_dist = d

print(f"\nMinimum distance between any two U1 bottom vias: {min_dist:.3f} mm (required >= 0.55 mm)")

