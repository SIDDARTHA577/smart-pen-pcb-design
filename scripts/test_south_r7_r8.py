import json, sys
sys.path.insert(0, '.')
from scripts.verify_smartpen_geometry import check_pcb_geometry

with open('output/RevF_Working/solved_coords.json') as f:
    coords = json.load(f)

# Coordinates
coords['C1'] = [39.80, 1.52]
coords['R18'] = [55.00, 2.35]
coords['FB1'] = [46.23, 7.55]
coords['J_BAT'] = [62.80, 1.72]
coords['U2'] = [67.00, 4.07]
coords['R9'] = [66.30, 6.70]
coords['C11'] = [68.00, 7.75]
coords['C12'] = [68.30, 1.40]
coords['C14'] = [71.05, 1.40]

# Let's test R7 and R8 in the South Zone:
# J_USB.7 (DP_PORT) at (78.15, 3.10)
# J_USB.9 (DM_PORT) at (78.65, 3.10)
# If R8 is at (76.00, 1.20): Pin 1 (DP_PORT) at 76.475, Pin 2 (DP_CORE) at 75.525
# If R7 is at (76.00, 0.60): Pin 1 (DM_PORT) at 76.475, Pin 2 (DM_CORE) at 75.525
# And where is C10? C10 at (73.90, 1.50)
# And where is R6? R6 at (79.70, 1.80) (CC2 pull-down)
# And where is R5? R5 at (70.20, 7.70) (CC1 pull-down)
print("Testing South placement for R7 and R8...")

