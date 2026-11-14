import pcbnew

board = pcbnew.LoadBoard("output/test_zero_shorts2.kicad_pcb")

r26 = board.FindFootprintByReference("R26")
r26.SetPosition(pcbnew.VECTOR2I(int(58.50 * 1e6), int(2.50 * 1e6)))

# Refill zones
filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())

out_pcb = "output/test_zero_shorts3.kicad_pcb"
board.Save(out_pcb)
print("Saved", out_pcb)

