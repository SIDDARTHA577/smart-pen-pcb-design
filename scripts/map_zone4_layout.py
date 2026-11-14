import pcbnew

board = pcbnew.LoadBoard("output/RevG/SmartPen.kicad_pcb")

print("Zone 4/5 Components (X = 58.0 to 74.0 mm):")
for fp in board.GetFootprints():
    pos = fp.GetPosition()
    x = pos.x / 1e6
    y = pos.y / 1e6
    if 58.0 <= x <= 74.0:
        bb = fp.GetBoundingBox()
        x1 = bb.GetX() / 1e6
        x2 = (bb.GetX() + bb.GetWidth()) / 1e6
        y1 = bb.GetY() / 1e6
        y2 = (bb.GetY() + bb.GetHeight()) / 1e6
        print(f"  {fp.GetReference():<6} at ({x:5.2f}, {y:5.2f})  BBox: X=[{x1:5.2f}, {x2:5.2f}], Y=[{y1:5.2f}, {y2:5.2f}] - {fp.GetValue()}")

