import json
import pcbnew

board = pcbnew.LoadBoard("output/RevG/SmartPen.kicad_pcb")

with open("reports/RevG/Phase03B/raw/before/Main_SmartPen_drc.json", "r") as f:
    drc = json.load(f)

shorts = [v for v in drc["violations"] if v.get("type") == "shorting_items"]
print(f"Analyzing {len(shorts)} shorting violations:")

# Build spatial index or find what items touch at the coordinates
for i, s in enumerate(shorts, 1):
    desc = s.get("description")
    items = s.get("items", [])
    coords = []
    for it in items:
        p = it.get("pos", {})
        coords.append((p.get("x"), p.get("y")))
    print(f"\n--- Violation #{i}: {desc} ---")
    for (x, y) in coords:
        if x is None or y is None:
            continue
        # Convert mm to nm
        pt = pcbnew.VECTOR2I(int(x * 1e6), int(y * 1e6))
        # Find pads at pt
        matching_pads = []
        for fp in board.GetFootprints():
            for pad in fp.Pads():
                # check bounding box or hit test
                if pad.HitTest(pt):
                    matching_pads.append(f"{fp.GetReference()} Pad {pad.GetName()} (Net: {pad.GetNetname()})")
        
        # Find tracks / vias at pt
        matching_tracks = []
        for t in board.GetTracks():
            if t.HitTest(pt):
                t_type = "Via" if t.Type() == pcbnew.PCB_VIA_T else "Segment"
                matching_tracks.append(f"{t_type} on {board.GetLayerName(t.GetLayer())} (Net: {t.GetNetname()})")
        
        print(f"  At ({x:.3f}, {y:.3f}):")
        if matching_pads:
            print(f"    Pads: {', '.join(matching_pads)}")
        if matching_tracks:
            print(f"    Tracks: {', '.join(matching_tracks)}")
        if not matching_pads and not matching_tracks:
            print("    No direct hit on pad/track (zone or near-miss)")

