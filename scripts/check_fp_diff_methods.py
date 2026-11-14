import pcbnew

board = pcbnew.LoadBoard("output/RevG/SmartPen.kicad_pcb")
fp = board.FindFootprintByReference("R9")
lib_fp = pcbnew.FootprintLoad("output/RevG/SmartPen.pretty", "R9")

# Check if there is a comparison function in pcbnew
for m in dir(fp):
    if "match" in m.lower() or "diff" in m.lower() or "compare" in m.lower():
        print(m)

