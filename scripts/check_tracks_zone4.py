import pcbnew

board = pcbnew.LoadBoard('output/RevG/SmartPen.kicad_pcb')

print("Tracks in X: 58.0 to 71.0, Y: 1.0 to 8.0:")
for t in board.GetTracks():
    sp = t.GetStart()
    ep = t.GetEnd()
    x1, y1 = sp.x/1e6, sp.y/1e6
    x2, y2 = ep.x/1e6, ep.y/1e6
    if (58.0 <= x1 <= 71.0 or 58.0 <= x2 <= 71.0) and (1.0 <= y1 <= 8.0 or 1.0 <= y2 <= 8.0):
        print(f"{t.GetClass()} {t.GetNetname()} on {board.GetLayerName(t.GetLayer())}: ({x1:.2f}, {y1:.2f}) -> ({x2:.2f}, {y2:.2f})")
