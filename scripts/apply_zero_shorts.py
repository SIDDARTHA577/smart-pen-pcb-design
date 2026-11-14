import pcbnew

board = pcbnew.LoadBoard("output/RevG/SmartPen.kicad_pcb")

# Update R27 position
r27 = board.FindFootprintByReference("R27")
r27.SetPosition(pcbnew.VECTOR2I(int(43.50 * 1e6), int(1.00 * 1e6)))
r27.SetOrientationDegrees(0.0)

# Update Q2 position
q2 = board.FindFootprintByReference("Q2")
q2.SetPosition(pcbnew.VECTOR2I(int(62.80 * 1e6), int(4.40 * 1e6)))
q2.SetOrientationDegrees(90.0)

# Update D4 position
d4 = board.FindFootprintByReference("D4")
d4.SetPosition(pcbnew.VECTOR2I(int(59.00 * 1e6), int(4.00 * 1e6)))
d4.SetOrientationDegrees(90.0)

# Update R26 position
r26 = board.FindFootprintByReference("R26")
r26.SetPosition(pcbnew.VECTOR2I(int(60.00 * 1e6), int(5.50 * 1e6)))
r26.SetOrientationDegrees(0.0)

# Remove the 84 shorting tracks/vias
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

print(f"Purging {len(shorting_uuids)} shorting tracks/vias...")
to_remove = [t for t in board.GetTracks() if t.m_Uuid.AsString() in shorting_uuids]
for t in to_remove:
    board.Remove(t)

# Refill zones
filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())

out_pcb = "output/test_zero_shorts.kicad_pcb"
board.Save(out_pcb)
print(f"Saved {out_pcb}")

