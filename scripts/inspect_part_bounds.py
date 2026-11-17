import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

from output.RevG.Mechanical_Phase04C.CAD_Source.SmartPen_Parametric_CAD_RevG_Phase4C import (
    SmartPenParameters, build_01_outer_barrel, build_02_front_grip, build_03_front_nose_cone,
    build_04_removable_electronics_rail, build_05_battery_cradle, build_06_front_mpu_carrier,
    build_07_microsd_carrier_mount, build_08_usb_c_access_feature, build_09_button_actuators,
    build_10a_click_plunger_button, build_10b_click_rotor_cam, build_10c_click_guide_stator,
    build_11_rear_bayonet_collar, build_12_pocket_clip, build_13_vibration_motor_mount,
    build_14_antenna_mount, build_reference_parts
)

p = SmartPenParameters()
parts = {
    '01_Outer_Barrel': build_01_outer_barrel(p),
    '02_Front_Grip': build_02_front_grip(p),
    '03_Front_Nose_Cone': build_03_front_nose_cone(p),
    '04_Removable_Electronics_Rail': build_04_removable_electronics_rail(p),
    '05_Battery_Cradle': build_05_battery_cradle(p),
    '06_Front_MPU_Carrier': build_06_front_mpu_carrier(p),
    '07_MicroSD_Carrier_Mount': build_07_microsd_carrier_mount(p),
    '08_USB_C_Access_Feature': build_08_usb_c_access_feature(p),
    '09_Button_Actuators': build_09_button_actuators(p),
    '10A_Click_Plunger_Button': build_10a_click_plunger_button(p),
    '10B_Click_Rotor_Cam': build_10b_click_rotor_cam(p),
    '10C_Click_Guide_Stator': build_10c_click_guide_stator(p),
    '11_Rear_Bayonet_Collar': build_11_rear_bayonet_collar(p),
    '12_Pocket_Clip': build_12_pocket_clip(p),
    '13_Vibration_Motor_Mount': build_13_vibration_motor_mount(p),
    '14_Antenna_Mount': build_14_antenna_mount(p),
}
parts.update(build_reference_parts(p))

print(f"{'Part Name':<35} | {'X Span':<18} | {'Y Span':<18} | {'Z Span':<18}")
print("-" * 95)
for name, s in sorted(parts.items()):
    bb = s.bounding_box()
    x_str = f"[{bb[0]:.2f}, {bb[3]:.2f}]"
    y_str = f"[{bb[1]:.2f}, {bb[4]:.2f}]"
    z_str = f"[{bb[2]:.2f}, {bb[5]:.2f}]"
    print(f"{name:<35} | {x_str:<18} | {y_str:<18} | {z_str:<18}")
