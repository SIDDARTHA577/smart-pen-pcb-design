import pcbnew

board = pcbnew.LoadBoard("output/RevG/SmartPen.kicad_pcb")

print("Components between X = 63.0 and 75.0 mm:")
for fp in board.GetFootprints():
    x = fp.GetPosition().x / 1e6
    y = fp.GetPosition().y / 1e6
    if 63.0 <= x <= 75.0:
        print(f"  {fp.GetReference():<6}: at ({x:6.2f}, {y:6.2f}) - {fp.GetValue()}")

