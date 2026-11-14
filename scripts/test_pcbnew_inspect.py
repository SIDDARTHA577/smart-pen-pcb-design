import pcbnew

board = pcbnew.LoadBoard("output/RevG/SmartPen.kicad_pcb")

tracks = list(board.GetTracks())
print(f"Total track elements in board: {len(tracks)}")
segments = [t for t in tracks if not t.Type() == pcbnew.PCB_VIA_T]
vias = [t for t in tracks if t.Type() == pcbnew.PCB_VIA_T]
print(f"  Line segments: {len(segments)}")
print(f"  Vias: {len(vias)}")

zones = list(board.Zones())
print(f"Total zones in board: {len(zones)}")

footprints = list(board.GetFootprints())
print(f"Total footprints in board: {len(footprints)}")

