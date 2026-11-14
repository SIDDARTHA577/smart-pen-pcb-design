import json
import pcbnew

board = pcbnew.LoadBoard("output/RevG/SmartPen.kicad_pcb")

with open("reports/RevG/Phase03B/raw/before/Main_SmartPen_drc.json", "r") as f:
    drc = json.load(f)

shorts = [v for v in drc["violations"] if v.get("type") == "shorting_items"]

shorting_tracks = set()
shorting_vias = set()

for s in shorts:
    for it in s.get("items", []):
        p = it.get("pos", {})
        x, y = p.get("x"), p.get("y")
        if x is None or y is None: continue
        pt = pcbnew.VECTOR2I(int(x * 1e6), int(y * 1e6))
        for t in board.GetTracks():
            if t.HitTest(pt):
                if t.Type() == pcbnew.PCB_VIA_T:
                    shorting_vias.add(t.m_Uuid.AsString())
                else:
                    shorting_tracks.add(t.m_Uuid.AsString())

print(f"Total track segments directly involved in shorts: {len(shorting_tracks)}")
print(f"Total vias directly involved in shorts: {len(shorting_vias)}")

