import pcbnew

board = pcbnew.LoadBoard("output/RevG/SmartPen.kicad_pcb")
fp_q2 = board.FindFootprintByReference("Q2")
fp_q2.SetOrientationDegrees(90.0)

# Check clearance at (62.80, 4.40)
base_pos = fp_q2.GetPosition()
dx = int(62.80 * 1e6 - base_pos.x)
dy = int(4.40 * 1e6 - base_pos.y)

collides = False
for pad in fp_q2.Pads():
    p = pad.GetPosition()
    px = (p.x + dx) / 1e6
    py = (p.y + dy) / 1e6
    sz = pad.GetSize()
    b = (px - sz.x/2e6, px + sz.x/2e6, py - sz.y/2e6, py + sz.y/2e6)
    print(f"Q2 (rot 90) pad {pad.GetName()} box: {b}")
    for ofp in board.GetFootprints():
        if ofp.GetReference() in ["Q2", "D4", "R26", "R27"]: continue
        for opad in ofp.Pads():
            op = opad.GetPosition()
            opx = op.x / 1e6
            opy = op.y / 1e6
            osz = opad.GetSize()
            ob = (opx - osz.x/2e6, opx + osz.x/2e6, opy - osz.y/2e6, opy + osz.y/2e6)
            if not (b[1] + 0.20 < ob[0] or b[0] - 0.20 > ob[1] or
                    b[3] + 0.20 < ob[2] or b[2] - 0.20 > ob[3]):
                print(f"  Collides with {ofp.GetReference()} Pad {opad.GetName()} box {ob}")
                collides = True

if not collides:
    print(">>> Q2 (rot 90) at (62.80, 4.40) has ZERO COLLISIONS! <<<")

