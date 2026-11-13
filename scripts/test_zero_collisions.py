"""Refined floorplan for 0 collisions."""
import json
import sys
sys.path.insert(0, '.')
from scripts.relax_placement import count_collisions

coords = {
    # Stage 1: Front Tip & Controls (0 - 20 mm)
    'J_IMU': [3.0, 4.6],
    'C15': [6.0, 2.0],
    'R10': [6.0, 4.6],
    'R11': [6.0, 7.2],
    'J_TOUCH': [9.0, 2.0],
    'SW4': [9.5, 7.0],
    'R19': [12.5, 2.0],
    'R12': [13.2, 7.0],
    'D1': [15.5, 2.0],
    'D2': [15.5, 4.4],
    'SW5': [16.8, 7.0],
    'R14': [18.5, 2.0],
    'R15': [18.5, 4.4],
    'R13': [20.2, 7.0],

    # Stage 2: Front Logic & Haptics (20 - 32 mm)
    'U3': [23.0, 4.6],
    'C13': [23.0, 8.0],
    'R16': [26.5, 2.0],
    'R17': [26.5, 4.6],
    'Q1': [29.0, 2.2],
    'J_MOT': [29.0, 7.0],
    'D3': [32.0, 4.6],

    # Stage 3: MCU, Crystal, RF (32 - 48 mm)
    'SW1': [35.0, 1.8],
    'R4': [38.0, 2.0],
    'C4': [40.0, 2.0],
    'C6': [35.0, 7.5],
    'Y1': [37.8, 7.5],
    'C7': [40.5, 7.5],
    'U1': [44.0, 4.6],
    'L1': [47.5, 7.5],
    'FB1': [50.0, 7.5],
    'C2': [52.0, 7.5],
    'C3': [54.5, 7.5],
    'R1': [47.5, 2.0],
    'C1': [49.5, 2.0],
    'SW2': [53.0, 1.8],

    # Stage 4: RF & Peripherals (48 - 63 mm)
    'L2': [47.5, 4.6],
    'C8': [50.0, 3.6],
    'C9': [51.5, 3.6],
    'J_RF': [53.0, 4.6],
    'J_SD': [57.0, 4.6],
    'R18': [56.0, 2.0],
    'R3': [58.0, 2.0],
    'C5': [60.0, 2.0],
    'R2': [61.5, 2.0],
    'J_UART': [57.0, 7.2],
    'SW3': [63.0, 7.5],
    'J_BAT': [65.0, 2.5],

    # Stage 5: Power Management (63 - 73 mm)
    'C11': [68.0, 7.2],
    'C12': [70.5, 7.2],
    'U2': [69.5, 2.8],
    'R9': [72.2, 2.0],
    'J_PWR': [73.0, 4.6],
    'C14': [71.5, 4.6],

    # Stage 6: USB Subsystem (73 - 84 mm)
    'U_ESD': [75.5, 4.6],
    'C10': [75.5, 7.2],
    'R5': [75.5, 2.0],
    'R6': [75.5, 0.8],
    'R7': [77.0, 6.0],
    'R8': [77.0, 7.4],
    'J_USB': [81.5, 4.6]
}

print(f"Total components placed: {len(coords)}")
cols = count_collisions(coords, clearance=0.15)
print("Collisions (< 0.15 mm):", len(cols))
for c in cols:
    print(f"  {c[0]} vs {c[1]}: dx={c[2]:.3f}, dy={c[3]:.3f}")

if not cols:
    with open('output/RevF_Working/solved_coords.json', 'w') as f:
        json.dump(coords, f, indent=2)
    print("SUCCESS: EXACTLY ZERO COLLISIONS!")

