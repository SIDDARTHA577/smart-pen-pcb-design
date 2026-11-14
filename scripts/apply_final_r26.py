import pcbnew

board = pcbnew.LoadBoard("output/test_zero_shorts3.kicad_pcb")

r26 = board.FindFootprintByReference("R26")
r26.SetPosition(pcbnew.VECTOR2I(int(60.50 * 1e6), int(4.40 * 1e6)))
r26.SetOrientationDegrees(90.0)

# Refill zones
filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())

out_pcb = "output/test_zero_shorts4.kicad_pcb"
board.Save(out_pcb)
print("Saved", out_pcb)

