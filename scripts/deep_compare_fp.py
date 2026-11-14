import pcbnew

board = pcbnew.LoadBoard("output/RevG/SmartPen.kicad_pcb")
fp = board.FindFootprintByReference("R9")
lib_fp = pcbnew.FootprintLoad("output/RevG/SmartPen.pretty", "R9")

# Compare graphical items
print("FP graphical items:", len(list(fp.GraphicalItems())))
print("Lib graphical items:", len(list(lib_fp.GraphicalItems())))

# Compare pads
print("FP pads count:", len(list(fp.Pads())))
print("Lib pads count:", len(list(lib_fp.Pads())))
for p1, p2 in zip(fp.Pads(), lib_fp.Pads()):
    print(f"P1: pos={p1.GetFPRelativePosition()}, sz={p1.GetSize()}, shape={p1.GetShape()}, drill={p1.GetDrillSize()}, offset={p1.GetOffset()}")
    print(f"P2: pos={p2.GetFPRelativePosition()}, sz={p2.GetSize()}, shape={p2.GetShape()}, drill={p2.GetDrillSize()}, offset={p2.GetOffset()}")

# Compare zones inside footprint
print("FP zones:", len(list(fp.Zones())))
print("Lib zones:", len(list(lib_fp.Zones())))
