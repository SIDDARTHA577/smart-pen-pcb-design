"""Test exact 3V3 routing with 0 collisions and full connectivity."""
import sys, json
sys.path.insert(0, '.')
from scripts.solve_zero_drc import run_check
from scripts.verify_smartpen_geometry import check_pcb_geometry

pads, segs, vias, errs = run_check()

segs_3v3 = []
vias_3v3 = set()

def add_s3(x1, y1, x2, y2, layer):
    if abs(x1 - x2) > 0.0005 or abs(y1 - y2) > 0.0005:
        segs_3v3.append((round(x1, 3), round(y1, 3), round(x2, 3), round(y2, 3), layer, "3V3", 0.20))

def add_v3(vx, vy):
    vias_3v3.add((round(vx, 3), round(vy, 3), "3V3"))

# ==============================================================
# 3V3 ROUTING
# ==============================================================
# 1. Front cluster (X = 1.7 to 8.0)
# J_IMU.1 (1.70, 4.60) to R10.1 (5.725, 4.60)
add_s3(1.70, 4.60, 5.725, 4.60, "F.Cu")
# R11.1 (5.725, 7.20) -> R10.1 (5.725, 4.60) -> C15.1 (5.725, 2.00)
add_s3(5.725, 7.20, 5.725, 2.00, "F.Cu")
# C15.1 (5.725, 2.00) -> J_TOUCH.1 (8.00, 2.40)
add_s3(5.725, 2.00, 8.00, 2.00, "F.Cu")
add_s3(8.00, 2.00, 8.00, 2.40, "F.Cu")

# Via to B.Cu at (8.00, 2.20)
add_v3(8.00, 2.20)
add_s3(8.00, 2.40, 8.00, 2.20, "F.Cu")

# 2. B.Cu 3V3 highway segments:
# Main highway on B.Cu at Y = 2.20:
# From (8.00, 2.20) to (19.475, 2.20)
add_s3(8.00, 2.20, 19.475, 2.20, "B.Cu")
add_v3(19.475, 2.20)

# At X = 19.475: R14.1 is at (19.475, 2.20), R15.1 is at (19.475, 4.40)
add_s3(19.475, 2.20, 19.475, 4.40, "F.Cu")

# R12.1 (14.025, 7.00) and R13.1 (20.025, 7.00)
# Connect R12.1 to 3V3:
add_s3(14.025, 7.00, 14.025, 7.80, "F.Cu")
add_s3(14.025, 7.80, 20.025, 7.80, "F.Cu")
add_s3(20.025, 7.80, 20.025, 7.00, "F.Cu")
# Connect R13.1 (20.025, 7.00) to U3.6 (21.35, 5.65)
add_s3(20.025, 7.00, 20.025, 5.65, "F.Cu")
add_s3(20.025, 5.65, 21.35, 5.65, "F.Cu")

# Connect U3.6 to highway via X = 19.475 on F.Cu:
add_s3(20.025, 5.65, 19.475, 5.65, "F.Cu")
add_s3(19.475, 5.65, 19.475, 4.40, "F.Cu")

# U3.18 (25.15, 4.65) and C13.1 (25.525, 7.50):
add_s3(25.15, 4.65, 25.525, 4.65, "F.Cu")
add_s3(25.525, 4.65, 25.525, 7.50, "F.Cu")
# Drop U3.18 to highway at Y = 2.20:
add_s3(25.525, 4.65, 25.525, 2.20, "F.Cu")
add_v3(25.525, 2.20)
add_s3(19.475, 2.20, 25.525, 2.20, "B.Cu")

# Continue B.Cu highway to East:
# (25.525, 2.20) to (35.407, 2.20)
add_s3(25.525, 2.20, 35.407, 2.20, "B.Cu")
add_v3(35.407, 2.20)
# R4.1 (35.407, 2.601)
add_s3(35.407, 2.20, 35.407, 2.601, "F.Cu")
# R1.1 (37.975, 2.36)
add_s3(35.407, 2.20, 37.975, 2.20, "B.Cu")
add_v3(37.975, 2.20)
add_s3(37.975, 2.20, 37.975, 2.36, "F.Cu")

# Continue to U1.17 (45.28, 3.085), R3.1 (47.825, 2.80), R2.1 (51.275, 2.25):
add_s3(37.975, 2.20, 45.28, 2.20, "B.Cu")
add_v3(45.28, 2.20)
add_s3(45.28, 2.20, 45.28, 3.085, "F.Cu")

add_s3(45.28, 2.20, 47.825, 2.20, "B.Cu")
add_v3(47.825, 2.20)
add_s3(47.825, 2.20, 47.825, 2.80, "F.Cu")

add_s3(47.825, 2.20, 51.275, 2.20, "B.Cu")
add_v3(51.275, 2.20)
add_s3(51.275, 2.20, 51.275, 2.25, "F.Cu")

# Continue to R18.1 (56.025, 2.00) & J_SD.1 (57.15, 4.20):
add_s3(51.275, 2.20, 56.025, 2.20, "B.Cu")
add_v3(56.025, 2.20)
add_s3(56.025, 2.20, 56.025, 2.00, "F.Cu")

add_s3(56.025, 2.20, 57.15, 2.20, "B.Cu")
add_v3(57.15, 2.20)
add_s3(57.15, 2.20, 57.15, 4.20, "F.Cu")

# Continue to C14.1 (70.014, 2.75) & J_PWR.3 (70.014, 3.963):
add_s3(57.15, 2.20, 69.20, 2.20, "B.Cu")
add_v3(69.20, 2.20)
add_s3(69.20, 2.20, 69.20, 2.75, "F.Cu")
add_s3(69.20, 2.75, 70.014, 2.75, "F.Cu")

# J_UART.4 (59.76, 7.347), C3.1 (50.253, 7.70), FB1.1 (45.48, 7.55):
# At East: via from J_UART.4 (59.76, 7.347)
add_s3(59.76, 7.347, 59.76, 8.45, "F.Cu")
add_v3(59.76, 8.45)
# On B.Cu at Y = 8.45 (open East of X = 43.13):
# Wait, at Y = 8.45:
# UART_TX is at 8.65, UART_RX is at 8.05.
# At Y = 8.35:
add_s3(59.76, 8.45, 60.50, 8.45, "B.Cu")
# Connect to highway:
add_s3(57.15, 2.20, 59.76, 2.20, "B.Cu")
add_v3(59.76, 2.20)
add_s3(59.76, 2.20, 59.76, 3.50, "F.Cu")

# Check FB1.1 (45.48, 7.55) & C3.1 (50.253, 7.70):
add_s3(45.48, 7.55, 50.253, 7.55, "F.Cu")
add_s3(50.253, 7.55, 50.253, 7.70, "F.Cu")
# Connect FB1.1 down to U1.17 via B.Cu or F.Cu:
add_v3(45.48, 7.55)
add_v3(45.48, 3.085)
add_s3(45.48, 7.55, 45.48, 3.085, "B.Cu")
add_s3(45.48, 3.085, 45.28, 3.085, "F.Cu")

print(f"Generated 3V3 routing: {len(segs_3v3)} segments, {len(vias_3v3)} vias")

test_segs = segs + segs_3v3
test_vias = list(set(vias).union(vias_3v3))

all_errs = check_pcb_geometry(pads, test_segs, test_vias)
print(f"\n==========================================")
print(f"GEOMETRY CHECK WITH 3V3: {len(all_errs)} ERRORS")
print(f"==========================================")
for e in all_errs:
    print("  *", e)
