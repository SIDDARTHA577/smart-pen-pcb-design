import pcbnew
import json

pcb_path = "output/RevG/SmartPen.kicad_pcb"
board = pcbnew.LoadBoard(pcb_path)

# 1. Update R27 position to (43.50, 1.00)
r27 = board.FindFootprintByReference("R27")
r27.SetPosition(pcbnew.VECTOR2I(int(43.50 * 1e6), int(1.00 * 1e6)))
r27.SetOrientationDegrees(0.0)

# 2. Update Q2 position to (62.80, 4.40), rotation 90 deg
q2 = board.FindFootprintByReference("Q2")
q2.SetPosition(pcbnew.VECTOR2I(int(62.80 * 1e6), int(4.40 * 1e6)))
q2.SetOrientationDegrees(90.0)

# 3. Update D4 position to (59.00, 4.00), rotation 270 deg
d4 = board.FindFootprintByReference("D4")
d4.SetPosition(pcbnew.VECTOR2I(int(59.00 * 1e6), int(4.00 * 1e6)))
d4.SetOrientationDegrees(270.0)

# 4. Update R26 position to (60.50, 4.40), rotation 90 deg
r26 = board.FindFootprintByReference("R26")
r26.SetPosition(pcbnew.VECTOR2I(int(60.50 * 1e6), int(4.40 * 1e6)))
r26.SetOrientationDegrees(90.0)

# 5. Remove the shorting tracks and legacy stubs
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

# Also remove legacy VBAT stubs at (60.96, 5.00) and (62.30, 5.00)
for t in board.GetTracks():
    p = t.GetPosition()
    px, py = p.x / 1e6, p.y / 1e6
    if 60.5 <= px <= 62.5 and 4.8 <= py <= 5.2 and t.GetNetname() == "/VBAT":
        shorting_uuids.add(t.m_Uuid.AsString())
    elif t.Type() == pcbnew.PCB_VIA_T and t.GetNetname() == "/VBAT" and 60.5 <= px <= 63.0:
        shorting_uuids.add(t.m_Uuid.AsString())

print(f"Purging {len(shorting_uuids)} offending copper items from SmartPen.kicad_pcb...")
to_remove = [t for t in board.GetTracks() if t.m_Uuid.AsString() in shorting_uuids]
for t in to_remove:
    board.Remove(t)

# Refill zones natively
filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())

board.Save(pcb_path)
print(f"Successfully saved updated and short-free {pcb_path}")

