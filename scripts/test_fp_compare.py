import pcbnew

board = pcbnew.LoadBoard("output/RevG/SmartPen.kicad_pcb")
fp = board.FindFootprintByReference("R9")

lib_path = "output/RevG/SmartPen.pretty"
lib_fp = pcbnew.FootprintLoad(lib_path, "R9")

if not lib_fp:
    print("Could not load from library!")
else:
    print("Loaded from library successfully!")
    # Check pads comparison
    fp_pads = list(fp.Pads())
    lib_pads = list(lib_fp.Pads())
    print(f"FP pads: {len(fp_pads)}, Lib pads: {len(lib_pads)}")
    for p1, p2 in zip(fp_pads, lib_pads):
        print(f"FP pad {p1.GetName()}: pos={p1.GetFPRelativePosition()}, sz={p1.GetSize()}, shape={p1.GetShape()}")
        print(f"Lib pad {p2.GetName()}: pos={p2.GetFPRelativePosition()}, sz={p2.GetSize()}, shape={p2.GetShape()}")

