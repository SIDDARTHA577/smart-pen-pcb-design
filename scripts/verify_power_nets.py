import os, sys
os.environ["WXSUPPRESS_SIZER_FLAGS_CHECK"] = "1"
import pcbnew
from strict_clearance_checker import BoardGeometry

b = pcbnew.LoadBoard('output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb')
geom = BoardGeometry(b)

# 1. /VBAT_SW
# Existing track: B.Cu (62.963, 4.400) -> (68.114, 4.400)
# East connection: via at (68.114, 4.400), track F.Cu to U4.1 (68.114, 3.963) and U4.3 (70.014, 3.963)
# West connection: via at (62.963, 4.400), track F.Cu (62.963, 4.400) -> (62.963, 6.824) [SW3.2]
# And B.Cu (28.090, 4.400) -> (62.963, 4.400), via at (28.090, 4.400), F.Cu to D3.1 (28.086, 4.704) and J_MOT.1 (30.753, 6.285)

print("Checking /VBAT_SW:")
v_east_ok, r1 = geom.is_via_legal(68.114, 4.400, '/VBAT_SW')
v_mid_ok, r2 = geom.is_via_legal(62.963, 4.400, '/VBAT_SW')
v_west_ok, r3 = geom.is_via_legal(28.090, 4.400, '/VBAT_SW')
print(f"  Vias: east={v_east_ok}({r1}), mid={v_mid_ok}({r2}), west={v_west_ok}({r3})")

s_bcu_west, rw = geom.is_segment_legal(28.090, 4.400, 62.963, 4.400, 'B.Cu', '/VBAT_SW')
print(f"  B.Cu run west: {s_bcu_west} ({rw})")

# 2. /VBAT
# J_BAT.1 (62.300, 1.720) -> via at (62.300, 1.000) -> B.Cu to (67.400, 1.000) -> via to F.Cu -> C12.1 (67.400, 1.400) -> U2.3 (67.950, 2.770)
# And Q2.3 (63.900, 4.400) to J_BAT.1
print("\nChecking /VBAT:")
v_bat1, rb1 = geom.is_via_legal(62.300, 1.000, '/VBAT')
v_bat2, rb2 = geom.is_via_legal(67.400, 1.000, '/VBAT')
print(f"  Vias: v1={v_bat1}({rb1}), v2={v_bat2}({rb2})")
s_bat_bcu, r_bat_bcu = geom.is_segment_legal(62.300, 1.000, 67.400, 1.000, 'B.Cu', '/VBAT')
print(f"  B.Cu run: {s_bat_bcu} ({r_bat_bcu})")

sys.exit(0)
