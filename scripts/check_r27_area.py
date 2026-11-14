import pcbnew

board = pcbnew.LoadBoard("output/RevG/SmartPen.kicad_pcb")

print("Components around X = 40.0 to 46.0 mm:")
for fp in board.GetFootprints():
    x = fp.GetPosition().x / 1e6
    y = fp.GetPosition().y / 1e6
    if 40.0 <= x <= 46.0:
        print(f"  {fp.GetReference():<6}: at ({x:6.2f}, {y:6.2f}) - {fp.GetValue()}")

