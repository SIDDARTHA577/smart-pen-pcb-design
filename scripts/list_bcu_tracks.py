import pcbnew

board = pcbnew.LoadBoard("output/RevG/SmartPen.kicad_pcb")

print("All tracks on B.Cu:")
bcu_tracks = [t for t in board.GetTracks() if t.GetLayer() == pcbnew.B_Cu and t.Type() != pcbnew.PCB_VIA_T]
for t in bcu_tracks:
    print(f"  Net: {t.GetNetname():<16} ({t.GetStart().x/1e6:6.2f}, {t.GetStart().y/1e6:6.2f}) -> ({t.GetEnd().x/1e6:6.2f}, {t.GetEnd().y/1e6:6.2f}), width={t.GetWidth()/1e6:.2f}")

