import math

# Barrel bore
r_bore = 6.75  # 13.5 mm diameter
r_cradle_hull = 6.60  # 0.15 mm clearance to bore

# Pushrod tunnel
r_pushrod_tunnel = 1.20 # Pushrod OD is 1.6 mm (R=0.8 mm), tunnel is R=1.2 mm

# Candidate: LP300830-PCM
batt_l = 33.00
batt_w = 8.20
batt_t = 3.30

# Battery placement:
y_batt_top = -1.50
y_batt_bot = y_batt_top - batt_t  # -4.80 mm
x_batt_min = -batt_w / 2.0  # -4.10 mm
x_batt_max = batt_w / 2.0   # +4.10 mm

# Cradle cavity dimensions (with clearances):
cav_l = 34.00  # +1.0 mm clearance
cav_w = 8.40   # +0.2 mm clearance (x: -4.20 to +4.20)
cav_t = 3.50   # +0.2 mm clearance (y: -1.45 to -4.95)
y_cav_top = -1.45
y_cav_bot = y_cav_top - cav_t  # -4.95 mm
x_cav_min = -cav_w / 2.0      # -4.20 mm
x_cav_max = cav_w / 2.0       # +4.20 mm

# 1. Check battery corners against barrel bore:
r_batt_corner = math.sqrt(x_batt_max**2 + y_batt_bot**2)
clr_batt_to_bore = r_bore - r_batt_corner

# 2. Check cradle cavity corners against cradle hull and barrel bore:
r_cav_corner = math.sqrt(x_cav_max**2 + y_cav_bot**2)
clr_cav_to_hull = r_cradle_hull - r_cav_corner
clr_cav_to_bore = r_bore - r_cav_corner

# 3. Check cradle bottom wall thickness at center (X=0):
y_hull_bot_center = -r_cradle_hull  # -6.60 mm
t_cradle_bot_wall = abs(y_hull_bot_center - y_cav_bot)

# 4. Check pushrod tunnel clearance:
clr_to_pushrod_tunnel = abs(y_cav_top) - r_pushrod_tunnel

print(f"Battery Finished Dimensions : {batt_t:.2f} x {batt_w:.2f} x {batt_l:.2f} mm")
print(f"Battery Y span              : [{y_batt_bot:.2f}, {y_batt_top:.2f}] mm")
print(f"Battery R_corner            : {r_batt_corner:.3f} mm")
print(f"Battery Clearance to Bore   : {clr_batt_to_bore:+.3f} mm (Safe: {clr_batt_to_bore > 0})")
print(f"Cradle Cavity Dimensions    : {cav_t:.2f} x {cav_w:.2f} x {cav_l:.2f} mm")
print(f"Cavity Y span               : [{y_cav_bot:.2f}, {y_cav_top:.2f}] mm")
print(f"Cavity R_corner             : {r_cav_corner:.3f} mm")
print(f"Cavity Wall at Corner       : {clr_cav_to_hull:+.3f} mm")
print(f"Cavity Clearance to Bore    : {clr_cav_to_bore:+.3f} mm")
print(f"Cradle Bottom Wall at X=0   : {t_cradle_bot_wall:.2f} mm")
print(f"Clearance to Pushrod Tunnel : {clr_to_pushrod_tunnel:.2f} mm")
