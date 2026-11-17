#!/usr/bin/env python3
"""
Complete 27-Body Pairwise Collision Matrix Audit for Phase 4C (351 Pairwise Intersections).
Validates 0.0000 mm³ collision across all parts in State A.
"""
import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from output.RevG.Mechanical_Phase04C.CAD_Source.SmartPen_Parametric_CAD_RevG_Phase4C import (
    SmartPenParameters,
    build_01_outer_barrel, build_02_front_grip, build_03_front_nose_cone,
    build_04_removable_electronics_rail, build_05_battery_cradle,
    build_06_front_mpu_carrier, build_07_microsd_carrier_mount,
    build_08_usb_c_access_feature, build_09_button_actuators,
    build_10a_click_plunger_button, build_10b_click_rotor_cam,
    build_10c_click_guide_stator, build_11_rear_bayonet_collar,
    build_12_pocket_clip, build_13_vibration_motor_mount,
    build_14_antenna_mount, build_reference_parts
)

def run_collision_audit():
    p = SmartPenParameters()
    custom_parts = {
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
    ref_parts = build_reference_parts(p)
    all_parts = {}
    all_parts.update(custom_parts)
    all_parts.update(ref_parts)

    part_names = sorted(list(all_parts.keys()))
    n_parts = len(part_names)
    total_pairs = n_parts * (n_parts - 1) // 2

    print("=" * 85)
    print(f"PHASE 4C 27-BODY COMPLETE 3D COLLISION AUDIT — {total_pairs} PAIRWISE INTERSECTIONS")
    print("=" * 85)

    collisions = []
    zero_collisions = 0
    non_zero_collisions = []

    for i in range(n_parts):
        for j in range(i + 1, n_parts):
            p1 = part_names[i]
            p2 = part_names[j]
            s1 = all_parts[p1]
            s2 = all_parts[p2]

            # Fast bounding box pre-filter
            bb1 = s1.bounding_box() # min_x, min_y, min_z, max_x, max_y, max_z
            bb2 = s2.bounding_box()

            # Check overlap in X, Y, Z
            overlap_x = (bb1[0] <= bb2[3]) and (bb1[3] >= bb2[0])
            overlap_y = (bb1[1] <= bb2[4]) and (bb1[4] >= bb2[1])
            overlap_z = (bb1[2] <= bb2[5]) and (bb1[5] >= bb2[2])

            if overlap_x and overlap_y and overlap_z:
                inter = s1 ^ s2
                vol = inter.volume()
                if vol > 1e-4:
                    non_zero_collisions.append((p1, p2, vol))
                else:
                    zero_collisions += 1
            else:
                vol = 0.0
                zero_collisions += 1
            collisions.append((p1, p2, vol))

    print(f"Total Pairwise Intersections Evaluated: {total_pairs}")
    print(f"Pairs with 0.0000 mm³ Collision:        {zero_collisions} / {total_pairs} ({zero_collisions/total_pairs*100:.1f}%)")
    if non_zero_collisions:
        print(f"CRITICAL WARNING: Found {len(non_zero_collisions)} colliding pairs:")
        for p1, p2, v in non_zero_collisions:
            print(f"  - {p1} vs {p2}: {v:.4f} mm^3")
    else:
        print("PERFECT CLEARANCE CONFIRMED: 0.0000 mm³ Collision Across Entire Assembly!")

    # Write detailed markdown report
    rep_dir = Path("output/RevG/Mechanical_Phase04C/Validation")
    rep_dir.mkdir(parents=True, exist_ok=True)
    out_file = rep_dir / "COMPLETE_27_BODY_COLLISION_MATRIX.txt"
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("SMART PEN REV G — PHASE 4C COMPLETE 27-BODY COLLISION MATRIX\n")
        f.write("=" * 85 + "\n\n")
        f.write(f"Total Pairs: {total_pairs}\n")
        f.write(f"Zero Collision Pairs: {zero_collisions}\n")
        f.write(f"Non-Zero Collision Pairs: {len(non_zero_collisions)}\n\n")
        f.write(f"{'Part 1':<34} {'Part 2':<34} {'Overlap (mm^3)':<15} {'Status'}\n")
        f.write("-" * 88 + "\n")
        for p1, p2, v in collisions:
            status = "CLEAR" if v < 1e-4 else "CLASH"
            f.write(f"{p1:<34} {p2:<34} {v:<15.4f} {status}\n")

    print(f"Saved complete collision audit log to: {out_file}")
    return len(non_zero_collisions) == 0

if __name__ == '__main__':
    run_collision_audit()
