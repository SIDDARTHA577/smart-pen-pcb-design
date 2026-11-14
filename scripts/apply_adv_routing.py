import pcbnew
import shutil

shutil.copy('output/RevG/SmartPen.kicad_pro', 'output/test_adv_routing.kicad_pro')
board = pcbnew.LoadBoard('output/test_adv_routing.kicad_pcb')

# Helper to find net by name
def get_net(net_name):
    netinfo = board.GetNetInfo()
    net = netinfo.GetNetItem(net_name)
    return net

def add_track(layer_name, start_x, start_y, end_x, end_y, width, net_name):
    net = get_net(net_name)
    if not net:
        print(f"Net {net_name} not found!")
        return None
    layer_id = board.GetLayerID(layer_name)
    track = pcbnew.PCB_TRACK(board)
    track.SetStart(pcbnew.VECTOR2I(int(start_x * 1e6), int(start_y * 1e6)))
    track.SetEnd(pcbnew.VECTOR2I(int(end_x * 1e6), int(end_y * 1e6)))
    track.SetWidth(int(width * 1e6))
    track.SetLayer(layer_id)
    track.SetNet(net)
    board.Add(track)
    return track

# 1. Connect R27-2 to U1-14 (GPIO8_STRAP)
# R27-2 is at (43.975, 1.0), U1-14 is at (43.63, 2.435)
add_track("F.Cu", 43.975, 1.0, 43.63, 1.35, 0.20, "/GPIO8_STRAP")
add_track("F.Cu", 43.63, 1.35, 43.63, 2.435, 0.20, "/GPIO8_STRAP")

# 2. Connect R27-1 to 3V3 rail
# R27-1 is at (43.025, 1.0). Nearby 3V3 track is at (41.5, 1.0) or (43.0, 1.0)
add_track("F.Cu", 43.025, 1.0, 42.0, 1.0, 0.25, "/3V3")

# 3. Connect SW2-1 to U1-15 (BOOT9)
# SW2-1 is at (45.704, 1.5), U1-15 is at (44.13, 2.435)
add_track("F.Cu", 45.704, 1.5, 44.13, 1.5, 0.20, "/BOOT9")
add_track("F.Cu", 44.13, 1.5, 44.13, 2.435, 0.20, "/BOOT9")

# 4. Connect Zone 4 Power nets:
# USB_VBUS: Q2-1 (61.7, 5.35) -> R26-1 (60.5, 4.88) -> D4-2 (59.0, 5.60)
add_track("F.Cu", 61.7, 5.35, 60.5, 4.88, 0.35, "/USB_VBUS")
add_track("F.Cu", 60.5, 4.88, 59.0, 5.60, 0.35, "/USB_VBUS")
# Also connect to U2-4 / existing VBUS track at (67.45, 5.37) via clean F.Cu path
add_track("F.Cu", 61.7, 5.35, 66.0, 5.35, 0.35, "/USB_VBUS")
add_track("F.Cu", 66.0, 5.35, 67.45, 5.37, 0.35, "/USB_VBUS")

# VSYS_RAW: D4-1 (59.0, 2.40) -> Q2-2 (61.7, 3.45) -> SW3-1 (60.963, 6.824)
add_track("F.Cu", 59.0, 2.40, 61.7, 3.45, 0.35, "/VSYS_RAW")
# From Q2-2 (61.7, 3.45) to SW3-1 (60.963, 6.824):
# Avoid Q2 body: go west to X=60.963, then south to Y=6.824
add_track("F.Cu", 61.7, 3.45, 60.963, 3.45, 0.35, "/VSYS_RAW")
add_track("F.Cu", 60.963, 3.45, 60.963, 6.824, 0.35, "/VSYS_RAW")

# VBAT: Q2-3 (63.9, 4.4) to VBAT track/pad
# J_BAT-1 is at (62.3, 1.72), with existing track to (62.3, 1.0).
# Route Q2-3 (63.9, 4.4) -> (63.9, 1.72) -> (62.3, 1.72)
add_track("F.Cu", 63.9, 4.4, 63.9, 1.72, 0.35, "/VBAT")
add_track("F.Cu", 63.9, 1.72, 62.3, 1.72, 0.35, "/VBAT")

# VBAT_SW: U4-1 (68.114, 3.963) to U4-3 (70.014, 3.963)
add_track("F.Cu", 68.114, 3.963, 70.014, 3.963, 0.30, "/VBAT_SW")

# Refill zones
filler = pcbnew.ZONE_FILLER(board)
zones = board.Zones()
filler.Fill(zones)

board.Save('output/test_adv_routing.kicad_pcb')
print("Successfully routed test tracks and saved.")
