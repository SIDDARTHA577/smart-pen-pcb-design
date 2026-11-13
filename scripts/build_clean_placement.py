"""Authoritative 60-component collision-free placement dictionary."""
import json
import sys
sys.path.insert(0, '.')
from scripts.relax_placement import count_collisions

coords = {
    # Block 1: Front Tip (0 - 4 mm)
    'J_IMU': [3.0, 4.6],

    # Block 2: Front User Interface & Pull-ups (4 - 21 mm)
    'C15': [5.8, 2.0],
    'R10': [5.8, 4.6],
    'R11': [5.8, 7.2],

    'J_TOUCH': [8.8, 2.0],
    'SW4': [9.5, 7.0],

    'R19': [12.0, 2.0],
    'R12': [13.2, 7.0],

    'D1': [15.2, 2.0],
    'D2': [15.2, 4.4],
    'SW5': [16.8, 7.0],

    'R14': [18.2, 2.0],
    'R15': [18.2, 4.4],
    'R13': [20.2, 7.0],

    # Block 3: Front Logic & Capacitive Sensor (21 - 25 mm)
    'U3': [23.2, 4.6],
    'C13': [23.2, 8.0],

    # Block 4: Haptic Feedback Motor Driver (25 - 33 mm)
    'R16': [26.5, 2.0],
    'R17': [26.5, 4.6],
    'Q1': [29.0, 2.2],
    'J_MOT': [29.0, 7.0],
    'D3': [32.0, 4.6],

    # Block 5: MCU Input Controls & Crystal Resonator (33 - 42 mm)
    'SW1': [35.0, 1.8],
    'R4': [38.0, 2.0],
    'C4': [40.0, 2.0],

    'C6': [35.0, 7.5],
    'Y1': [37.8, 7.5],
    'C7': [40.5, 7.5],

    # Block 6: ESP32-C3 Main Controller (42 - 47 mm)
    'U1': [44.0, 4.6],

    # Block 7: MCU Decoupling & Strapping (47 - 52 mm)
    'L1': [47.5, 7.5],
    'FB1': [49.8, 7.5],
    'C2': [52.0, 7.5],

    'R1': [47.5, 2.0],
    'C1': [49.5, 2.0],
    'SW2': [52.8, 1.8],

    # Block 8: RF Matching Network (51 - 55 mm)
    'L2': [47.5, 4.6],
    'C8': [49.2, 3.6],
    'C9': [51.0, 3.6],
    'J_RF': [53.2, 4.6],

    # Block 9: Storage, UART & Battery (54 - 64 mm)
    'C3': [54.2, 7.5],
    'J_UART': [56.8, 7.2],

    'J_SD': [56.5, 4.6],
    'R18': [54.5, 2.0],
    'R3': [56.8, 2.0],
    'R2': [58.8, 2.0],
    'C5': [58.8, 4.6],

    'SW3': [61.5, 7.5],
    'J_BAT': [62.8, 2.5],

    # Block 10: Power Subsystem (MCP73831 & AP2112K) (64 - 73 mm)
    'C11': [65.5, 7.2],
    'C12': [67.8, 7.2],
    'U2': [66.8, 2.8],
    'R9': [69.2, 2.0],

    'J_PWR': [70.0, 4.6],
    'C14': [71.5, 2.0],
    'U_ESD': [72.8, 4.6],

    # Block 11: USB Type-C Receptacle & Termination (73 - 84 mm)
    'R5': [73.5, 2.0],
    'R6': [75.3, 2.0],
    'C10': [75.2, 4.6],
    'R7': [73.5, 7.4],
    'R8': [75.3, 7.4],
    'J_USB': [81.5, 4.6]
}

print(f"Total parts in dictionary: {len(coords)}")
cols = count_collisions(coords, clearance=0.15)
print(f"Collisions (< 0.15 mm): {len(cols)}")
for c in cols:
    print(f"  {c[0]} vs {c[1]}: dx={c[2]:.3f}, dy={c[3]:.3f}")

if not cols:
    with open('output/RevF_Working/solved_coords.json', 'w') as f:
        json.dump(coords, f, indent=2)
    print("SUCCESS: EXACTLY ZERO COLLISIONS!")

