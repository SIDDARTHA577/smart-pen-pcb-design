import json
import csv
import pcbnew

board = pcbnew.LoadBoard("output/RevG/SmartPen.kicad_pcb")

with open("reports/RevG/Phase03B/raw/before/Main_SmartPen_drc.json", "r") as f:
    drc = json.load(f)

violations = drc.get("violations", [])

csv_path = "reports/RevG/Phase03B/02_DRC_ISSUE_REGISTER.csv"

fieldnames = [
    "Issue_ID",
    "DRC_Category",
    "Severity",
    "Affected_Nets",
    "Coordinates_mm",
    "Item_Identifiers",
    "Root_Cause",
    "Proposed_Repair",
    "Repair_Status",
    "Verification_Result"
]

rows = []
for i, v in enumerate(violations, 1):
    cat = v.get("type", "unknown")
    sev = v.get("severity", "error")
    desc = v.get("description", "")
    
    items = v.get("items", [])
    coords_list = []
    item_ids = []
    nets = set()
    
    for it in items:
        p = it.get("pos", {})
        x = p.get("x")
        y = p.get("y")
        if x is not None and y is not None:
            coords_list.append(f"({x:.3f}, {y:.3f})")
            pt = pcbnew.VECTOR2I(int(x * 1e6), int(y * 1e6))
            
            # Hit test pads
            for fp in board.GetFootprints():
                for pad in fp.Pads():
                    if pad.HitTest(pt):
                        item_ids.append(f"{fp.GetReference()}.{pad.GetName()}")
                        if pad.GetNetname():
                            nets.add(pad.GetNetname())
            
            # Hit test tracks
            for t in board.GetTracks():
                if t.HitTest(pt):
                    t_type = "Via" if t.Type() == pcbnew.PCB_VIA_T else "Track"
                    layer = board.GetLayerName(t.GetLayer())
                    item_ids.append(f"{t_type}[{layer}]({t.GetNetname()})")
                    if t.GetNetname():
                        nets.add(t.GetNetname())
        
        uuid = it.get("uuid")
        if uuid:
            item_ids.append(f"UUID:{uuid[:8]}")

    # Fallback to description for nets if not detected
    if not nets and "nets" in desc:
        nets.add(desc)

    # Determine Root Cause and Proposed Repair based on category
    if cat == "shorting_items":
        root_cause = "Legacy bus highway tracks or overlapping collinear segments on B.Cu, or pad-track net mismatch from component placement"
        proposed = "Remove offending legacy track stubs/vias and reroute with proper net isolation and clearance"
    elif cat == "hole_clearance":
        root_cause = "Via-to-track or via-to-via hole edge clearance < 0.25 mm caused by tight 0.30 mm pitch parallel bus routing"
        proposed = "Remove redundant transition vias and stagger required vias with >= 0.50 mm hole-to-hole clearance"
    elif cat == "solder_mask_bridge":
        root_cause = "Solder mask dam < 0.08 mm between tightly placed 0402 pads or connector pins"
        proposed = "Increase pad spacing to >= 0.25 mm or apply 1:1 gang-mask opening in footprint definition"
    elif cat == "clearance":
        root_cause = "Track-to-track or track-to-pad copper spacing < 0.15 mm from unrouted stubs and legacy routes"
        proposed = "Rip up conflicting stubs and route using 0.20 mm standard design rules"
    elif cat == "lib_footprint_mismatch":
        root_cause = "Footprint pad orientation/rotation mismatch between PCB definition and SmartPen.pretty library"
        proposed = "Synchronize footprint definitions and update rotations to eliminate mismatch warnings"
    elif cat == "starved_thermal":
        root_cause = "Thermal relief spokes on ground pads constricted by adjacent cutouts or traces"
        proposed = "Relocate nearby signal traces to allow at least 2 full copper thermal relief spokes to GND zone"
    elif cat == "silk_over_copper":
        root_cause = "Component reference silkscreen overlapping exposed solder pad"
        proposed = "Move silkscreen text outside component courtyard and away from exposed copper"
    elif cat == "tracks_crossing":
        root_cause = "Two tracks crossing on the same layer without a net tie"
        proposed = "Separate crossing tracks onto orthogonal layers (F.Cu horizontal, B.Cu vertical) with vias"
    elif cat == "silk_edge_clearance":
        root_cause = "Silkscreen graphic or text within 0.20 mm of Edge.Cuts board outline"
        proposed = "Pull silkscreen back >= 0.30 mm from board edge"
    else:
        root_cause = "Geometric design rule constraint violation"
        proposed = "Adjust geometry to meet design rules"

    rows.append({
        "Issue_ID": f"DRC-{i:03d}",
        "DRC_Category": cat,
        "Severity": sev,
        "Affected_Nets": " / ".join(sorted(nets)) if nets else desc,
        "Coordinates_mm": " | ".join(coords_list[:2]),
        "Item_Identifiers": ", ".join(list(dict.fromkeys(item_ids))[:4]),
        "Root_Cause": root_cause,
        "Proposed_Repair": proposed,
        "Repair_Status": "IDENTIFIED",
        "Verification_Result": "PENDING_REPAIR"
    })

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Successfully generated {csv_path} with {len(rows)} entries.")

