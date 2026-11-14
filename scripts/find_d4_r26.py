import pcbnew

board = pcbnew.LoadBoard("output/RevG/SmartPen.kicad_pcb")
fp_q2 = board.FindFootprintByReference("Q2")
fp_q2.SetOrientationDegrees(90.0)
fp_q2.SetPosition(pcbnew.VECTOR2I(int(62.80 * 1e6), int(4.40 * 1e6)))

fp_d4 = board.FindFootprintByReference("D4")
fp_r26 = board.FindFootprintByReference("R26")

def get_boxes(fp, x, y, rot=0.0):
    fp.SetOrientationDegrees(rot)
    fp.SetPosition(pcbnew.VECTOR2I(int(x * 1e6), int(y * 1e6)))
    boxes = []
    for pad in fp.Pads():
        p = pad.GetPosition()
        sz = pad.GetSize()
        boxes.append((p.x/1e6 - sz.x/2e6, p.x/1e6 + sz.x/2e6, p.y/1e6 - sz.y/2e6, p.y/1e6 + sz.y/2e6))
    return boxes

all_fixed = []
for fp in board.GetFootprints():
    if fp.GetReference() in ["D4", "R26", "R27"]: continue
    for pad in fp.Pads():
        p = pad.GetPosition()
        sz = pad.GetSize()
        all_fixed.append((fp.GetReference(), (p.x/1e6 - sz.x/2e6, p.x/1e6 + sz.x/2e6, p.y/1e6 - sz.y/2e6, p.y/1e6 + sz.y/2e6)))

def check(fp, x, y, rot=0.0):
    boxes = get_boxes(fp, x, y, rot)
    for b in boxes:
        if b[0] < 0.25 or b[1] > 83.75: return False
        if b[2] < 0.25 or b[3] > 8.95: return False
        for ref, ob in all_fixed:
            if not (b[1] + 0.25 < ob[0] or b[0] - 0.25 > ob[1] or
                    b[3] + 0.25 < ob[2] or b[2] - 0.25 > ob[3]):
                return False
    return True

print("Testing D4 candidates...")
for x in [59.0, 59.5, 60.0, 60.5, 64.5, 65.0, 65.5]:
    for y in [3.0, 3.5, 4.0, 4.5, 5.0, 5.5]:
        for rot in [0.0, 90.0, 180.0, 270.0]:
            if check(fp_d4, x, y, rot):
                print(f"  D4 clean at ({x:.2f}, {y:.2f}) rot {rot}")
                break

print("Testing R26 candidates...")
for x in [59.0, 59.5, 60.0, 60.5, 61.0, 64.5, 65.0]:
    for y in [2.5, 3.0, 3.5, 5.5, 6.0]:
        for rot in [0.0, 90.0]:
            if check(fp_r26, x, y, rot):
                print(f"  R26 clean at ({x:.2f}, {y:.2f}) rot {rot}")
                break

