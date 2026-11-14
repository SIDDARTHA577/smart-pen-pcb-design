import pcbnew

board = pcbnew.LoadBoard("output/RevG/SmartPen.kicad_pcb")

# Find tracks touching (41.63, 1.15)
pt1 = pcbnew.VECTOR2I(int(41.63 * 1e6), int(1.15 * 1e6))
pt2 = pcbnew.VECTOR2I(int(24.25 * 1e6), int(1.45 * 1e6))

print("Tracks at pt1 (41.63, 1.15):")
for t in board.GetTracks():
    if t.HitTest(pt1):
        print(f"  {t.GetClass()} on {board.GetLayerName(t.GetLayer())}, net: {t.GetNetname()}, start: ({t.GetStart().x/1e6}, {t.GetStart().y/1e6}), end: ({t.GetEnd().x/1e6}, {t.GetEnd().y/1e6})")

print("Tracks at pt2 (24.25, 1.45):")
for t in board.GetTracks():
    if t.HitTest(pt2):
        print(f"  {t.GetClass()} on {board.GetLayerName(t.GetLayer())}, net: {t.GetNetname()}, start: ({t.GetStart().x/1e6}, {t.GetStart().y/1e6}), end: ({t.GetEnd().x/1e6}, {t.GetEnd().y/1e6})")

