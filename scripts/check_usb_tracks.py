import pcbnew

board = pcbnew.LoadBoard('output/RevG/SmartPen.kicad_pcb')
for t in board.GetTracks():
    if t.GetNetname() in ('/USB_DP_CORE', '/USB_DM_CORE', '/USB_DP_PORT', '/USB_DM_PORT'):
        sp = t.GetStart()
        ep = t.GetEnd()
        print(f"{t.GetClass()} {t.GetNetname()} on {board.GetLayerName(t.GetLayer())}: ({sp.x/1e6:.2f}, {sp.y/1e6:.2f}) -> ({ep.x/1e6:.2f}, {ep.y/1e6:.2f})")
