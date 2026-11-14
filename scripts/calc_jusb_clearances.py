import pcbnew
import math

board = pcbnew.LoadBoard("output/RevG/SmartPen.kicad_pcb")

# Find J_USB
jusb = None
for fp in board.GetFootprints():
    if fp.GetReference() == "J_USB":
        jusb = fp
        break

print(f"J_USB Position: ({jusb.GetPosition().x/1e6:.3f}, {jusb.GetPosition().y/1e6:.3f}), Orientation: {jusb.GetOrientationDegrees()}")

# Board bounding box: X: 0 to 84.0 mm, Y: 0 to 9.20 mm
bb_xmin, bb_xmax = 0.0, 84.0
bb_ymin, bb_ymax = 0.0, 9.20

print("\n--- EXACT PAD AND HOLE CLEARANCES TO PCB EDGES (Current Orientation: 0 deg) ---")
min_clear_north = 999.0
min_clear_south = 999.0
min_clear_east = 999.0
min_clear_west = 999.0

min_hole_north = 999.0
min_hole_south = 999.0
min_hole_east = 999.0

for pad in jusb.Pads():
    pos = pad.GetPosition()
    px = pos.x / 1e6
    py = pos.y / 1e6
    sz = pad.GetSize()
    sx = sz.x / 1e6
    sy = sz.y / 1e6
    
    # Copper outer envelope for this pad
    pad_xmin = px - sx/2.0
    pad_xmax = px + sx/2.0
    pad_ymin = py - sy/2.0
    pad_ymax = py + sy/2.0
    
    c_north = bb_ymax - pad_ymax
    c_south = pad_ymin - bb_ymin
    c_east = bb_xmax - pad_xmax
    c_west = pad_xmin - bb_xmin
    
    min_clear_north = min(min_clear_north, c_north)
    min_clear_south = min(min_clear_south, c_south)
    min_clear_east = min(min_clear_east, c_east)
    min_clear_west = min(min_clear_west, c_west)
    
    # If pad has hole
    drill = pad.GetDrillSize()
    dx = drill.x / 1e6
    dy = drill.y / 1e6
    if dx > 0:
        h_xmin = px - dx/2.0
        h_xmax = px + dx/2.0
        h_ymin = py - dy/2.0
        h_ymax = py + dy/2.0
        min_hole_north = min(min_hole_north, bb_ymax - h_ymax)
        min_hole_south = min(min_hole_south, h_ymin - bb_ymin)
        min_hole_east = min(min_hole_east, bb_xmax - h_xmax)

print(f"Minimum Copper Edge Clearances (Side-mount 0 deg):")
print(f"  To North Edge (Y = 9.20 mm): {min_clear_north:.3f} mm")
print(f"  To South Edge (Y = 0.00 mm): {min_clear_south:.3f} mm")
print(f"  To East Edge  (X = 84.00 mm): {min_clear_east:.3f} mm")
print(f"  To West Edge  (X = 0.00 mm): {min_clear_west:.3f} mm")

print(f"\nMinimum Hole Edge Clearances (Side-mount 0 deg):")
print(f"  To North Edge (Y = 9.20 mm): {min_hole_north:.3f} mm")
print(f"  To South Edge (Y = 0.00 mm): {min_hole_south:.3f} mm")
print(f"  To East Edge  (X = 84.00 mm): {min_hole_east:.3f} mm")

# Now evaluate Rear-mount (90 deg rotation)
print("\n--- EVALUATION OF REAR-MOUNT (90 deg rotation at X = 78.4, Y = 4.6) ---")
# When rotated 90 deg, pad X offsets become Y offsets, pad Y offsets become X offsets!
# Shell stakes at X = +-4.30 mm, size 1.20 x 2.00 mm
# Width across Y becomes 2 * (4.30 + 1.20/2) = 9.80 mm!
rear_ymax = 4.60 + 4.90 # 9.50 mm
rear_ymin = 4.60 - 4.90 # -0.30 mm
print(f"  Outer Copper Y envelope: {rear_ymin:.3f} mm to {rear_ymax:.3f} mm")
print(f"  Overhang past North Edge (9.20 mm): {rear_ymax - 9.20:.3f} mm OVERHANG!")
print(f"  Overhang past South Edge (0.00 mm): {0.00 - rear_ymin:.3f} mm OVERHANG!")

