import json

with open("reports/RevG/Phase03B/raw/before/Main_SmartPen_drc.json", "r") as f:
    drc = json.load(f)

for v in drc["violations"]:
    if v.get("type") == "lib_footprint_mismatch":
        print(json.dumps(v, indent=2))
        break

