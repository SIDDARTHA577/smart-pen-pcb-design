import os, sys
os.environ["WXSUPPRESS_SIZER_FLAGS_CHECK"] = "1"
import pcbnew
from strict_clearance_checker import BoardGeometry

b = pcbnew.LoadBoard('output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb')
geom = BoardGeometry(b)

# Test DP:
# U1.26 at (44.130, 7.235)
# F.Cu: (44.130, 7.235) -> (44.130, 8.750) -> (54.000, 8.750) -> (54.000, 7.200)
# Via at (54.000, 7.200)
# In2.Cu: (54.000, 7.200) -> (70.500, 7.200) -> (70.500, 7.800)
# Via at (70.500, 7.800)
# F.Cu: (70.500, 7.800) -> (71.600, 7.025)

print("Checking DP:")
print("v_w:", geom.is_via_legal(54.0, 7.2, '/USB_DP_CORE'))
print("v_e:", geom.is_via_legal(70.5, 7.8, '/USB_DP_CORE'))
print("s1 F.Cu:", geom.is_segment_legal(44.13, 7.235, 44.13, 8.75, 'F.Cu', '/USB_DP_CORE'))
print("s2 F.Cu:", geom.is_segment_legal(44.13, 8.75, 54.0, 8.75, 'F.Cu', '/USB_DP_CORE'))
print("s3 F.Cu:", geom.is_segment_legal(54.0, 8.75, 54.0, 7.2, 'F.Cu', '/USB_DP_CORE'))
print("s4 In2:", geom.is_segment_legal(54.0, 7.2, 70.5, 7.2, 'In2.Cu', '/USB_DP_CORE'))
print("s5 In2:", geom.is_segment_legal(70.5, 7.2, 70.5, 7.8, 'In2.Cu', '/USB_DP_CORE'))
print("s6 F.Cu:", geom.is_segment_legal(70.5, 7.8, 71.6, 7.025, 'F.Cu', '/USB_DP_CORE'))

# Test DM:
# U1.25 at (44.630, 7.235)
# F.Cu: (44.630, 7.235) -> (44.630, 8.350) -> (52.000, 8.350) -> (52.000, 6.600)
# Via at (52.000, 6.600) -- wait let's check if (52.0, 6.6) is legal via
print("\nChecking DM via at (52.0, 6.6):", geom.is_via_legal(52.0, 6.6, '/USB_DM_CORE'))
print("Checking DM via at (52.0, 7.0):", geom.is_via_legal(52.0, 7.0, '/USB_DM_CORE'))
print("Checking DM via at (73.0, 7.0):", geom.is_via_legal(73.0, 7.0, '/USB_DM_CORE'))
print("s1 F.Cu DM:", geom.is_segment_legal(44.63, 7.235, 44.63, 8.35, 'F.Cu', '/USB_DM_CORE'))
print("s2 F.Cu DM:", geom.is_segment_legal(44.63, 8.35, 52.0, 8.35, 'F.Cu', '/USB_DM_CORE'))
print("s3 F.Cu DM:", geom.is_segment_legal(52.0, 8.35, 52.0, 7.0, 'F.Cu', '/USB_DM_CORE'))
print("s4 F.Cu DM (73.0, 7.0)->(72.5, 7.025):", geom.is_segment_legal(73.0, 7.0, 72.5, 7.025, 'F.Cu', '/USB_DM_CORE'))

sys.exit(0)
