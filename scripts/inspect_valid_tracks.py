import pcbnew
from collections import Counter

board = pcbnew.LoadBoard("output/RevG/SmartPen.kicad_pcb")

# Import the shorting uuids
import json
with open("reports/RevG/Phase03B/raw/before/Main_SmartPen_drc.json", "r") as f:
    drc = json.load(f)
shorts = [v for v in drc["violations"] if v.get("type") == "shorting_items"]
shorting_uuids = set()
for s in shorts:
    for it in s.get("items", []):
        p = it.get("pos", {})
        x, y = p.get("x"), p.get("y")
        if x is None or y is None: continue
        pt = pcbnew.VECTOR2I(int(x * 1e6), int(y * 1e6))
        for t in board.GetTracks():
            if t.HitTest(pt):
                shorting_uuids.add(t.m_Uuid.AsString())

valid_tracks = [t for t in board.GetTracks() if t.m_Uuid.AsString() not in shorting_uuids]
print(f"Total non-shorting tracks: {len(valid_tracks)}")
valid_nets = Counter(t.GetNetname() for t in valid_tracks)
for net, count in valid_nets.most_common():
    print(f"  {net:<20}: {count} tracks/vias")

