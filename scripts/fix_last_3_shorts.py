import pcbnew

board = pcbnew.LoadBoard("output/test_zero_shorts.kicad_pcb")

# Remove legacy VBAT stubs at (60.96, 5.00) and (62.30, 5.00)
to_remove = []
for t in board.GetTracks():
    p = t.GetPosition()
    px, py = p.x / 1e6, p.y / 1e6
    if 60.5 <= px <= 62.5 and 4.8 <= py <= 5.2:
        to_remove.append(t)
    elif t.Type() == pcbnew.PCB_VIA_T and t.GetNetname() == "/VBAT":
        to_remove.append(t)

print(f"Removing {len(to_remove)} legacy VBAT items...")
for t in to_remove:
    board.Remove(t)

# Adjust D4: Rotate 270 deg so Pad 1 (/VSYS_RAW) is at Y=2.40 and Pad 2 (/USB_VBUS) is at Y=5.60
d4 = board.FindFootprintByReference("D4")
d4.SetOrientationDegrees(270.0)

# Move R26 to (60.50, 6.20)
r26 = board.FindFootprintByReference("R26")
r26.SetPosition(pcbnew.VECTOR2I(int(60.50 * 1e6), int(6.20 * 1e6)))

# Refill zones
filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())

out_pcb = "output/test_zero_shorts2.kicad_pcb"
board.Save(out_pcb)
print("Saved", out_pcb)

