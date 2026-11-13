"""Categorize all DRC violations from the raw DRC reports of all four boards.
Analyzes exact error descriptions, affected coordinates, nets, layers, and footprint references.
Groups violations by root cause.
"""
import re
from pathlib import Path
from collections import defaultdict, Counter

reports = {
    "SmartPen (Main PCB)": "reports/RevF/audit_reports/SmartPen_drc.rpt",
    "Front_MPU": "reports/RevF/audit_reports/Front_MPU_drc.rpt",
    "MicroSD_Carrier": "reports/RevF/audit_reports/MicroSD_Carrier_drc.rpt",
    "Touch_Sensor": "reports/RevF/audit_reports/Touch_Sensor_drc.rpt"
}

for board_name, rpt_path in reports.items():
    p = Path(rpt_path)
    if not p.exists():
        print(f"Report not found: {rpt_path}")
        continue
    
    text = p.read_text(encoding='utf-8')
    print(f"\n=======================================================")
    print(f"BOARD: {board_name}")
    print(f"Report: {rpt_path} ({p.stat().st_size:,} bytes)")
    print(f"=======================================================")

    # Find total violations summary from report
    violations_summary = re.findall(r'Found (\d+) DRC violations', text)
    unconnected_summary = re.findall(r'Found (\d+) unconnected items', text)
    ignored_summary = re.findall(r'Found (\d+) ignored DRC violations', text)

    print(f"Summary in header/footer: Violations={violations_summary}, Unconnected={unconnected_summary}, Ignored={ignored_summary}")

    # Parse individual violations
    # Format typically:
    # [rule_type]: Description
    #     Rule: ...
    #     @(x, y): item 1
    #     @(x, y): item 2
    
    # Split by violation entries: lines starting with [rule_name]:
    entries = re.split(r'\n(?=\[[a-zA-Z0-9_]+\]:)', text)
    header = entries[0]
    items = entries[1:]

    print(f"Total parsed violation blocks: {len(items)}")

    by_type = Counter()
    by_layer = Counter()
    by_rule = Counter()
    sample_by_type = defaultdict(list)

    for item in items:
        m = re.match(r'\[(.*?)\]: (.*)', item)
        if not m:
            continue
        v_type = m.group(1)
        v_desc = m.group(2)
        by_type[v_type] += 1
        
        # Layer
        layers = re.findall(r'on ([A-Za-z0-9_.]+)', item)
        for l in layers:
            by_layer[l] += 1

        if len(sample_by_type[v_type]) < 3:
            # get coordinates
            coords = re.findall(r'@\(([0-9.-]+)\s*mm,\s*([0-9.-]+)\s*mm\)', item)
            sample_by_type[v_type].append({
                "desc": v_desc,
                "coords": coords,
                "text": item.strip()[:300]
            })

    print(f"\nBreakdown by Violation Type:")
    for v_type, count in by_type.most_common():
        print(f"  - [{v_type}]: {count}")

    print(f"\nSamples by Violation Type:")
    for v_type, samples in sample_by_type.items():
        print(f"\n--- Type: [{v_type}] ({by_type[v_type]} total) ---")
        for i, s in enumerate(samples):
            print(f"  Sample {i+1}: {s['desc']}")
            print(f"    Coords: {s['coords']}")
            # print indented snippet
            for line in s['text'].split('\n')[:4]:
                print(f"      {line}")

