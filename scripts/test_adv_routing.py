import pcbnew

def test_routing_advancements():
    board = pcbnew.LoadBoard('output/RevG/SmartPen.kicad_pcb')
    
    # 1. Remove dangling vias and stubs at J_USB
    tracks_to_remove = []
    for t in board.GetTracks():
        if t.GetNetname() == '/USB_VBUS':
            pos = t.GetPosition()
            sp = t.GetStart()
            ep = t.GetEnd()
            # Vias at 76.0 and 80.8
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
                    
    print(f"Removing {len(tracks_to_remove)} J_USB VBUS stubs/vias")
    for t in tracks_to_remove:
        board.Remove(t)
        
    board.Save('output/test_adv_routing.kicad_pcb')
    print("Saved output/test_adv_routing.kicad_pcb")

test_routing_advancements()
