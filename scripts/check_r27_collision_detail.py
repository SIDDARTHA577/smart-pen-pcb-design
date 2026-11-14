import pcbnew

board = pcbnew.LoadBoard("output/RevG/SmartPen.kicad_pcb")

fp = board.FindFootprintByReference("R27")
boxes = []
base_pos = fp.GetPosition()
dx = int(43.20 * 1e6 - base_pos.x)
dy = int(1.50 * 1e6 - base_pos.y)

for pad in fp.Pads():
    p = pad.GetPosition()
    px = (p.x + dx) / 1e6
    py = (p.y + dy) / 1e6
    sz = pad.GetSize()
    sx = sz.x / 1e6
    sy = sz.y / 1e6
    b = (px - sx/2.0, px + sx/2.0, py - sy/2.0, py + sy/2.0)
    print(f"R27 pad box: {b}")
    for ofp in board.GetFootprints():
        if ofp.GetReference() in ["R27", "Q2", "D4", "R26"]: continue
        for opad in ofp.Pads():
            op = opad.GetPosition()
            opx = op.x / 1e6
            opy = op.y / 1e6
            osz = opad.GetSize()
            ob = (opx - osz.x/2e6, opx + osz.x/2e6, opy - osz.y/2e6, opy + osz.y/2e6)
            # check overlap with 0.25 margin
            if not (b[1] + 0.25 < ob[0] or b[0] - 0.25 > ob[1] or
                    b[3] + 0.25 < ob[2] or b[2] - 0.25 > ob[3]):
                print(f"  Collides with {ofp.GetReference()} Pad {opad.GetName()} box {ob}")

