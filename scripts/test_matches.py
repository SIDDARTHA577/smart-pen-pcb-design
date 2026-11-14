import pcbnew

board = pcbnew.LoadBoard("output/RevG/SmartPen.kicad_pcb")
fp = board.FindFootprintByReference("R9")
lib_fp = pcbnew.FootprintLoad("output/RevG/SmartPen.pretty", "R9")

try:
    print("fp.Matches(lib_fp):", fp.Matches(lib_fp))
except Exception as e:
    print("Matches error:", e)

