import pcbnew

board = pcbnew.LoadBoard("output/RevG/SmartPen.kicad_pcb")

r27 = board.FindFootprintByReference("R27")
sw2 = board.FindFootprintByReference("SW2")

print(f"R27 pos: ({r27.GetPosition().x/1e6:.3f}, {r27.GetPosition().y/1e6:.3f})")
for p in r27.Pads():
    print(f"  R27 Pad {p.GetName()} ({p.GetNetname()}) at ({p.GetPosition().x/1e6:.3f}, {p.GetPosition().y/1e6:.3f}) size ({p.GetSize().x/1e6:.3f}, {p.GetSize().y/1e6:.3f})")

print(f"SW2 pos: ({sw2.GetPosition().x/1e6:.3f}, {sw2.GetPosition().y/1e6:.3f})")
for p in sw2.Pads():
    print(f"  SW2 Pad {p.GetName()} ({p.GetNetname()}) at ({p.GetPosition().x/1e6:.3f}, {p.GetPosition().y/1e6:.3f}) size ({p.GetSize().x/1e6:.3f}, {p.GetSize().y/1e6:.3f})")

