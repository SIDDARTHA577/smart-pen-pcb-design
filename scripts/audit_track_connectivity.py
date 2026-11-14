import pcbnew

board = pcbnew.LoadBoard("output/RevG/SmartPen.kicad_pcb")

# Check connectivity of tracks to actual footprint pads of the same net
tracks = list(board.GetTracks())
print(f"Total tracks and vias: {len(tracks)}")

# Map pads by net
pads_by_net = {}
for fp in board.GetFootprints():
    for pad in fp.Pads():
        netname = pad.GetNetname()
        if netname not in pads_by_net:
            pads_by_net[netname] = []
        pads_by_net[netname].append((fp.GetReference(), pad.GetName(), pad.GetPosition()))

# For each track, check if its start or end connects to any pad or track of the same net
print("\nChecking track endpoints against net pad coordinates...")
for t in tracks:
    netname = t.GetNetname()
    if not netname:
        print(f"Track with NO NET: {t.GetClass()} on {board.GetLayerName(t.GetLayer())} ({t.GetStart().x/1e6}, {t.GetStart().y/1e6})")

