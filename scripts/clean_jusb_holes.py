import pcbnew

def clean_jusb_hole_violations():
    board = pcbnew.LoadBoard('output/RevG/SmartPen.kicad_pcb')
    
    tracks_to_remove = []
    for t in board.GetTracks():
        if t.GetNetname() == '/USB_VBUS':
            pos = t.GetPosition()
            sp = t.GetStart()
            ep = t.GetEnd()
            if t.GetClass() == 'PCB_VIA':
                x, y = pos.x / 1e6, pos.y / 1e6
                if abs(x - 76.0) < 0.1 and abs(y - 4.85) < 0.1:
                    tracks_to_remove.append(t)
                elif abs(x - 80.8) < 0.1 and abs(y - 4.85) < 0.1:
                    tracks_to_remove.append(t)
            elif t.GetClass() == 'PCB_TRACK':
                x1, y1 = sp.x / 1e6, sp.y / 1e6
                x2, y2 = ep.x / 1e6, ep.y / 1e6
                if abs(x1 - 76.0) < 0.1 and abs(x2 - 76.0) < 0.1 and y1 > 3.0 and y2 > 3.0:
                    tracks_to_remove.append(t)
                elif abs(x1 - 80.8) < 0.1 and abs(x2 - 80.8) < 0.1 and y1 > 3.0 and y2 > 3.0:
                    tracks_to_remove.append(t)
                    
    print(f"Found {len(tracks_to_remove)} offending J_USB stubs/vias")
    for t in tracks_to_remove:
        board.Remove(t)
        
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())
    board.Save('output/RevG/SmartPen.kicad_pcb')
    print("Saved output/RevG/SmartPen.kicad_pcb")

clean_jusb_hole_violations()
