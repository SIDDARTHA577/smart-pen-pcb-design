import pcbnew

board = pcbnew.LoadBoard("output/RevG/SmartPen.kicad_pcb")

refs = ['R9', 'U3', 'R5', 'R15', 'R14', 'R7', 'C14', 'R8', 'R6', 'D2', 'D1']

for r in refs:
    fp = board.FindFootprintByReference(r)
    if not fp:
        continue
    pos = fp.GetPosition()
    rot = fp.GetOrientationDegrees()
    print(f"\nRef: {r:<5} Pos: ({pos.x/1e6:6.2f}, {pos.y/1e6:6.2f}), Rot: {rot:5.1f} deg, FPID: {fp.GetFPIDAsString()}")
    for pad in fp.Pads():
        p_pos = pad.GetFPRelativePosition()
        p_sz = pad.GetSize()
        print(f"   Pad {pad.GetName():<3} at ({p_pos.x/1e6:6.3f}, {p_pos.y/1e6:6.3f}), size: ({p_sz.x/1e6:.3f}, {p_sz.y/1e6:.3f}), net: {pad.GetNetname()}")
