import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

from output.RevG.Mechanical_Phase04C.CAD_Source.SmartPen_Parametric_CAD_RevG_Phase4C import (
    SmartPenParameters, make_cylinder_z, make_box,
    build_01_outer_barrel, build_02_front_grip, build_03_front_nose_cone,
    build_04_removable_electronics_rail, build_06_front_mpu_carrier,
    build_07_microsd_carrier_mount, build_08_usb_c_access_feature,
    build_09_button_actuators, build_10a_click_plunger_button,
    build_10b_click_rotor_cam, build_10c_click_guide_stator,
    build_11_rear_bayonet_collar, build_12_pocket_clip,
    build_13_vibration_motor_mount, build_14_antenna_mount,
    build_reference_parts
)

p = SmartPenParameters()
# Update to LP300830-PCM verified maximum dimensions
p.BATT_LEN = 33.00
p.BATT_WIDTH = 8.20
p.BATT_THICK = 3.30
p.Z_BATT_START = 74.50
p.Z_BATT_END = 107.50
p.BATT_Y_TOP = -1.50
p.BATT_Y_BOT = -4.80

p.CRADLE_INSIDE_WIDTH = 8.40
p.CRADLE_INSIDE_DEPTH = 3.50
p.CRADLE_INSIDE_LEN = 34.00

def build_test_cradle(p):
    hull = make_cylinder_z(6.60, p.CRADLE_Z_START, p.CRADLE_Z_END, n_seg=48)
    upper_clip = make_box(-8.0, 8.0, -1.40, 8.0, p.CRADLE_Z_START - 0.5, p.CRADLE_Z_END + 0.5)
    cradle_base = hull - upper_clip
    
    cavity = make_box(
        -p.CRADLE_INSIDE_WIDTH/2.0, p.CRADLE_INSIDE_WIDTH/2.0,
        -4.95, -1.45,
        74.00, 108.00
    )
    cradle_solid = cradle_base - cavity
    clip_front = make_box(-3.5, 3.5, -1.50, 0.20, 73.50, 74.00)
    clip_rear = make_box(-3.5, 3.5, -1.50, 0.20, 108.00, 109.00)
    wire_chase = make_box(-1.50, 1.50, -3.50, 0.50, 107.00, 109.50)
    pushrod_tunnel = make_cylinder_z(1.20, 73.00, 110.00, n_seg=24)
    return (cradle_solid + clip_front + clip_rear) - wire_chase - pushrod_tunnel

cradle = build_test_cradle(p)
batt = make_box(-p.BATT_WIDTH/2.0, p.BATT_WIDTH/2.0, p.BATT_Y_BOT, p.BATT_Y_TOP, p.Z_BATT_START, p.Z_BATT_END)

# Check cradle vs batt
inter = cradle ^ batt
print("Cradle vs Battery overlap: %f mm^3" % inter.volume())

# Check cradle vs outer barrel
barrel = build_01_outer_barrel(p)
inter_barrel = cradle ^ barrel
print("Cradle vs Barrel overlap: %f mm^3" % inter_barrel.volume())

# Check battery vs outer barrel
inter_batt_barrel = batt ^ barrel
print("Battery vs Barrel overlap: %f mm^3" % inter_batt_barrel.volume())

# Check cradle vs rail
rail = build_04_removable_electronics_rail(p)
inter_rail = cradle ^ rail
print("Cradle vs Rail overlap: %f mm^3" % inter_rail.volume())

# Check pushrod vs cradle
pushrod = make_cylinder_z(p.PUSHROD_OD/2.0, 68.50, 140.00, n_seg=24)
inter_pushrod = cradle ^ pushrod
print("Cradle vs Pushrod overlap: %f mm^3" % inter_pushrod.volume())
