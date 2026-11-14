import pcbnew

board = pcbnew.LoadBoard("output/RevG/SmartPen.kicad_pcb")
fp = board.FindFootprintByReference("R9")
pad = list(fp.Pads())[0]
for m in dir(pad):
    if "pos" in m.lower():
        print(m)

