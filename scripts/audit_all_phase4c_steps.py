#!/usr/bin/env python3
"""
Comprehensive STEP Reader & Topological Validation Audit for Phase 4C deliverables.
Parses all 27 component STEP files and 2 Master Assembly STEP files.
Validates entity uniqueness, reference resolution, BRep topology, units, bounding boxes, and volume.
"""
import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import numpy as np

from scripts.step_reader_validator import parse_step_file

def audit_all_step_files():
    step_dir = Path("output/RevG/Mechanical_Phase04C/STEP")
    assy_dir = Path("output/RevG/Mechanical_Phase04C/Assemblies")
    
    step_files = sorted(list(step_dir.glob("*.step"))) + sorted(list(assy_dir.glob("*.step")))
    
    print("=" * 80)
    print(f"PHASE 4C COMPREHENSIVE STEP INDEPENDENT AUDIT — {len(step_files)} FILES")
    print("=" * 80)
    
    results = []
    total_duplicate_ids = 0
    total_unresolved_refs = 0
    all_valid = True
    
    header = f"{'File Name':<38} {'Size (B)':<10} {'Ents':<7} {'Dups':<6} {'Unres':<6} {'Solids':<7} {'Faces':<7} {'Status'}"
    print(header)
    print("-" * len(header))
    
    for f in step_files:
        sz = f.stat().st_size
        res = parse_step_file(f)
        results.append((f.name, sz, res))
        
        dups = len(res.duplicate_ids)
        unres = len(res.unresolved_refs)
        total_duplicate_ids += dups
        total_unresolved_refs += unres
        if not res.is_valid:
            all_valid = False
            
        status = "PASS" if res.is_valid else "FAIL"
        print(f"{f.name:<38} {sz:<10,d} {res.total_entities:<7,d} {dups:<6d} {unres:<6d} {len(res.solid_breps):<7d} {len(res.advanced_faces):<7d} {status}")
        
    print("-" * len(header))
    print(f"Summary: Total Files Tested: {len(step_files)}")
    print(f"         Total Duplicate Entity IDs: {total_duplicate_ids}")
    print(f"         Total Unresolved References: {total_unresolved_refs}")
    print(f"         Overall Compliance: {'100% PASS' if all_valid else 'FAIL'}")
    
    # Write full detailed audit log to Validation directory and reports directory
    log_path = Path("output/RevG/Mechanical_Phase04C/Validation/STEP_KERNEL_INDEPENDENT_AUDIT_LOG.txt")
    with open(log_path, 'w', encoding='utf-8') as out:
        out.write("SMART PEN REV G — PHASE 4C INDEPENDENT STEP AUDIT LOG\n")
        out.write("=" * 80 + "\n\n")
        out.write(header + "\n")
        out.write("-" * len(header) + "\n")
        for fname, sz, res in results:
            status = "PASS" if res.is_valid else "FAIL"
            out.write(f"{fname:<38} {sz:<10,d} {res.total_entities:<7,d} {len(res.duplicate_ids):<6d} {len(res.unresolved_refs):<6d} {len(res.solid_breps):<7d} {len(res.advanced_faces):<7d} {status}\n")
        out.write("\n" + "=" * 80 + "\n")
        out.write("INDIVIDUAL FILE TOPOLOGICAL EXTENTS & VOLUMES:\n")
        out.write("=" * 80 + "\n")
        for fname, sz, res in results:
            out.write(f"\nFile: {fname}\n")
            out.write(f"  Valid: {res.is_valid}\n")
            out.write(f"  Schema: {res.header_schema}\n")
            out.write(f"  Units: {res.unit_length}\n")
            out.write(f"  Total Entities: {res.total_entities:,d}\n")
            out.write(f"  Solids: {len(res.solid_breps)}, Shells: {len(res.closed_shells)}, Faces: {len(res.advanced_faces)}\n")
            out.write(f"  Euler Characteristic (V-E+F): {res.euler_characteristic}\n")
            out.write(f"  Bounding Box: {res.bounding_box}\n")
            out.write(f"  Computed Volume: {res.computed_volume:.4f} mm^3\n")
            if res.errors:
                out.write("  ERRORS:\n")
                for e in res.errors:
                    out.write(f"    - {e}\n")
                    
    print(f"\nWrote full audit log to: {log_path}")
    return all_valid

if __name__ == '__main__':
    audit_all_step_files()
