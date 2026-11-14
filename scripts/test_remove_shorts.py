import pcbnew
import json

board = pcbnew.LoadBoard("output/RevG/SmartPen.kicad_pcb")

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

print(f"Removing {len(shorting_uuids)} offending copper items...")
to_remove = [t for t in board.GetTracks() if t.m_Uuid.AsString() in shorting_uuids]
for t in to_remove:
    board.Remove(t)

# Refill zones
filler = pcbnew.ZONE_FILLER(board)
zones = board.Zones()
filler.Fill(zones)

test_pcb_path = "output/test_clean_shorts.kicad_pcb"
board.Save(test_pcb_path)
print(f"Saved test board to {test_pcb_path}")

