import pcbnew
import json

board = pcbnew.LoadBoard("output/test_clean_shorts.kicad_pcb")

# Run DRC on test board or parse the remaining 5 shorts from rpt
with open("reports/drc_test_after_remove.rpt", "r") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "[shorting_items]" in l:
        print(l.strip())
        for j in range(1, 4):
            if i+j < len(lines):
                print("  ", lines[i+j].strip())

