import pcbnew

board = pcbnew.LoadBoard("output/RevG/SmartPen.kicad_pcb")
fp = board.FindFootprintByReference("R9")
for m in dir(fp):
    if any(k in m.lower() for k in ["prop", "graph", "zone"]):
        print(m)

