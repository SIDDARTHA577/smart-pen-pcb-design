with open("reports/drc_test_zero_shorts3.rpt", "r") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "[shorting_items]" in l:
        print("".join(lines[i:i+6]))

