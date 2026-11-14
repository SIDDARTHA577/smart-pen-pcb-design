import pcbnew

board = pcbnew.LoadBoard("output/RevG/SmartPen.kicad_pcb")

fp_r27 = board.FindFootprintByReference("R27")
fp_q2 = board.FindFootprintByReference("Q2")
fp_d4 = board.FindFootprintByReference("D4")
fp_r26 = board.FindFootprintByReference("R26")

def get_pad_boxes(fp, at_x, at_y):
    boxes = []
    base_pos = fp.GetPosition()
    dx = int(at_x * 1e6 - base_pos.x)
    dy = int(at_y * 1e6 - base_pos.y)
    for pad in fp.Pads():
        p = pad.GetPosition()
        px = (p.x + dx) / 1e6
        py = (p.y + dy) / 1e6
        sz = pad.GetSize()
        sx = sz.x / 1e6
        sy = sz.y / 1e6
        boxes.append((px - sx/2.0, px + sx/2.0, py - sy/2.0, py + sy/2.0))
    return boxes

all_other_boxes = []
for fp in board.GetFootprints():
    if fp.GetReference() in ["R27", "Q2", "D4", "R26"]: continue
    for pad in fp.Pads():
        p = pad.GetPosition()
        px = p.x / 1e6
        py = p.y / 1e6
        sz = pad.GetSize()
        all_other_boxes.append((fp.GetReference(), (px - sz.x/2e6, px + sz.x/2e6, py - sz.y/2e6, py + sz.y/2e6)))

def check_pos(fp, x, y, min_c=0.20):
    boxes = get_pad_boxes(fp, x, y)
    for b in boxes:
        if b[0] < min_c or b[1] > (84.0 - min_c): return False
        if b[2] < min_c or b[3] > (9.20 - min_c): return False
        for ref, ob in all_other_boxes:
            if not (b[1] + min_c < ob[0] or b[0] - min_c > ob[1] or
                    b[3] + min_c < ob[2] or b[2] - min_c > ob[3]):
                return False
    return True

print("R27 at (43.50, 1.00):", check_pos(fp_r27, 43.50, 1.00))

# Find Q2 positions
q2_positions = []
for x in [x*0.1 for x in range(600, 650)]:
    for y in [y*0.1 for y in range(25, 60)]:
        if check_pos(fp_q2, x, y):
            q2_positions.append((round(x, 2), round(y, 2)))

print(f"Valid Q2 positions: {len(q2_positions)}")
if q2_positions:
    print("Sample Q2:", q2_positions[:5])

