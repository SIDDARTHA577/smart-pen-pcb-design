import pcbnew

board = pcbnew.LoadBoard("output/RevG/SmartPen.kicad_pcb")

refs = ["U2", "U4", "Q2", "D4", "R26", "R9", "J_BAT", "SW3", "C13", "C14", "C15", "R27", "SW2"]
for r in refs:
    fp = board.FindFootprintByReference(r)
    if not fp: continue
    bb = fp.GetBoundingBox()
    pos = fp.GetPosition()
    print(f"Ref: {r:<6} Pos: ({pos.x/1e6:6.2f}, {pos.y/1e6:6.2f})  BBox: X=[{bb.GetX()/1e6:6.2f}, {(bb.GetX()+bb.GetWidth())/1e6:6.2f}], Y=[{bb.GetY()/1e6:6.2f}, {(bb.GetY()+bb.GetHeight())/1e6:6.2f}]")

