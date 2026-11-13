"""Test evenly distributed 6-stage floorplan across 84mm board."""
import json
import sys
sys.path.insert(0, '.')
from scripts.relax_placement import count_collisions

coords = {
    # Stage 1: Front Tip & Controls (0 - 18 mm)
    'J_IMU': [3.0, 4.6],
    'C15': [5.8, 2.0],
    'R10': [5.8, 4.6],
    'R11': [5.8, 7.2],
    'J_TOUCH': [8.5, 2.0],
    'SW4': [8.5, 7.0],
    'R19': [11.2, 2.0],
    'R12': [11.2, 7.0],
    'D1': [14.0, 2.0],
    'D2': [14.0, 4.4],
    'SW5': [14.0, 7.0],
    'R14': [16.8, 2.0],
    'R15': [16.8, 4.4],
    'R13': [16.8, 7.0],

    # Stage 2: Front Logic & Haptics (18 - 30 mm)
    'U3': [21.0, 4.6],
    'C13': [21.0, 8.0],
    'R16': [24.5, 2.0],
    'R17': [24.5, 4.6],
    'Q1': [27.0, 2.2],
    'D3': [29.8, 4.6],
    'J_MOT': [27.0, 7.0],

    # Stage 3: MCU, Crystal, RF (30 - 46 mm)
    'SW1': [33.0, 1.8],
    'R4': [35.5, 2.0],
    'C4': [37.2, 2.0],
    'C6': [33.0, 7.5],
    'Y1': [35.5, 7.5],
    'C7': [38.0, 7.5],
    'U1': [41.5, 4.6],
    'R1': [45.5, 2.0],
    'C1': [47.0, 2.0],
    'SW2': [49.5, 1.8],
    'L1': [45.5, 7.5],
    'FB1': [47.0, 7.5],
    'C2': [48.5, 7.5],
    'C3': [50.0, 7.5],

    # Stage 4: RF, SD, UART, Battery (46 - 60 mm)
    'L2': [45.0, 4.6],
    'C8': [47.0, 3.6],
    'C9': [48.5, 3.6],
    'J_RF': [52.5, 4.6],
    'J_SD': [55.5, 4.6],
    'R18': [53.5, 2.0],
    'R3': [58.5, 2.0],
    'C5': [60.0, 2.0],
    'R2': [61.5, 2.0],
    'J_UART': [57.5, 7.2],
    'J_BAT': [63.5, 2.5],
    'SW3': [63.5, 7.5],

    # Stage 5: Power Management (60 - 73 mm)
    'C11': [67.5, 7.2],
    'U2': [67.5, 2.8],
    'R9': [70.0, 2.0],
    'C12': [70.0, 7.2],
    'J_PWR': [72.5, 4.6],
    'C14': [74.5, 4.6],

    # Stage 6: USB Subsystem (73 - 84 mm)
    'U_ESD': [76.0, 4.6],
    'R5': [77.5, 1.8],
    'R6': [77.5, 3.0],
    'C10': [77.5, 4.6],
    'R7': [77.5, 6.2],
    'R8': [77.5, 7.4],
    'J_USB': [81.5, 4.6]
}

print(f"Total components placed: {len(coords)}")
cols = count_collisions(coords, clearance=0.15)
print("Collisions (< 0.15 mm):", len(cols))
for c in cols:
    print(f"  {c[0]} vs {c[1]}: dx={c[2]:.3f}, dy={c[3]:.3f}")

