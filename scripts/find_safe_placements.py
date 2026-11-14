import pcbnew

board = pcbnew.LoadBoard("output/RevG/SmartPen.kicad_pcb")

# Footprints to optimize:
# R27 -> target (43.20, 1.50)
# Q2  -> test
# D4  -> test
# R26 -> test

fixed_refs = [fp.GetReference() for fp in board.GetFootprints() if fp.GetReference() not in ["Q2", "D4", "R26", "R27"]]

def get_pad_boxes(fp, at_x=None, at_y=None):
    boxes = []
    base_pos = fp.GetPosition()
    dx = (at_x * 1e6 - base_pos.x) if at_x is not None else 0
    dy = (at_y * 1e6 - base_pos.y) if at_y is not None else 0
    for pad in fp.Pads():
        p = pad.GetPosition()
        px = (p.x + dx) / 1e6
        py = (p.y + dy) / 1e6
        sz = pad.GetSize()
        sx = sz.x / 1e6
        sy = sz.y / 1e6
        boxes.append((px - sx/2.0, px + sx/2.0, py - sy/2.0, py + sy/2.0))
    return boxes

fixed_boxes = []
for r in fixed_refs:
    fp = board.FindFootprintByReference(r)
    fixed_boxes.extend([(r, b) for b in get_pad_boxes(fp)])

def check_collision(fp, at_x, at_y, min_clear=0.25):
    boxes = get_pad_boxes(fp, at_x, at_y)
    for b in boxes:
        # Check against board edges: [0.0, 84.0], [0.0, 9.20]
        if b[0] < min_clear or b[1] > (84.0 - min_clear): return False
        if b[2] < min_clear or b[3] > (9.20 - min_clear): return False
        for ref, fb in fixed_boxes:
            # Overlap with clearance
            if not (b[1] + min_clear < fb[0] or b[0] - min_clear > fb[1] or
                    b[3] + min_clear < fb[2] or b[2] - min_clear > fb[3]):
                return False
    return True

print("Testing R27 at (43.20, 1.50):", check_collision(board.FindFootprintByReference("R27"), 43.20, 1.50))

# Search for Q2, D4, R26
fp_q2 = board.FindFootprintByReference("Q2")
fp_d4 = board.FindFootprintByReference("D4")
fp_r26 = board.FindFootprintByReference("R26")

valid_q2 = []
for x in [60.5, 61.0, 61.5, 62.0, 62.5, 63.0, 63.5, 64.0]:
    for y in [3.5, 3.8, 4.0, 4.2, 4.5, 4.8, 5.0]:
        if check_collision(fp_q2, x, y):
            valid_q2.append((x, y))

print(f"Valid Q2 positions: {len(valid_q2)}")
for p in valid_q2[:5]:
    print("  Q2 candidate:", p)

