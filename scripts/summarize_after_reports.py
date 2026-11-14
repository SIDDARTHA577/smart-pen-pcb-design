import json
import glob

print("--- PCB DRC RESULTS (AFTER) ---")
for pcb_json in sorted(glob.glob('reports/RevG/Phase03B/raw/after/*_drc.json')):
    with open(pcb_json, 'r') as f:
        data = json.load(f)
    print(pcb_json)
    print(f"  Violations: {len(data.get('violations', []))}")
    print(f"  Unconnected: {len(data.get('unconnected_items', []))}")
    print(f"  Schematic parity issues: {len(data.get('schematic_parity_issues', []))}")

print("\n--- SCHEMATIC ERC RESULTS (AFTER) ---")
for sch_json in sorted(glob.glob('reports/RevG/Phase03B/raw/after/*_erc.json')):
    with open(sch_json, 'r') as f:
        data = json.load(f)
    print(sch_json)
    print(f"  Violations: {len(data.get('violations', []))}")
