import pcbnew

board = pcbnew.LoadBoard("output/test_zero_shorts3.kicad_pcb")

# Check empty spot for R26
fp_r26 = board.FindFootprintByReference("R26")

for x in [59.5, 60.0, 60.5, 61.0, 61.5]:
    for y in [3.8, 4.0, 4.2, 4.4, 4.6, 4.8]:
        for rot in [0.0, 90.0]:
            fp_r26.SetPosition(pcbnew.VECTOR2I(int(x * 1e6), int(y * 1e6)))
            fp_r26.SetOrientationDegrees(rot)
            
            # Check overlap with all other pads
            collides = False
            for pad in fp_r26.Pads():
                pos = pad.GetPosition()
                px, py = pos.x / 1e6, pos.y / 1e6
                sz = pad.GetSize()
                sx, sy = sz.x / 1e6, sz.y / 1e6
                b = (px - sx/2, px + sx/2, py - sy/2, py + sy/2)
                for ofp in board.GetFootprints():
                    if ofp.GetReference() == "R26": continue
                    for opad in ofp.Pads():
                        opos = opad.GetPosition()
                        opx, opy = opos.x / 1e6, opos.y / 1e6
                        osz = opad.GetSize()
                        osx, osy = osz.x / 1e6, osz.y / 1e6
                        ob = (opx - osx/2, opx + osx/2, opy - osy/2, opy + osy/2)
                        if not (b[1] + 0.25 < ob[0] or b[0] - 0.25 > ob[1] or
                                b[3] + 0.25 < ob[2] or b[2] - 0.25 > ob[3]):
                            collides = True
                            break
                    if collides: break
                if collides: break
            if not collides:
                print(f"R26 Clean at ({x:.2f}, {y:.2f}) rot {rot}")

