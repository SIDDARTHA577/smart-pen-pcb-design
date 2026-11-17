#!/usr/bin/env python3
"""
Continuous Integration Native CAD Kernel Ingestion & BRep Topology Validator.
Executes on Linux CI runner (Ubuntu 22.04/24.04) or local workstation with official FreeCAD / OpenCASCADE.
Validates all 29 STEP files (27 components + 2 assemblies) in output/RevG/Mechanical_Phase04C/.

STRICT REQUIREMENT: Must execute a genuine native CAD kernel (FreeCAD or OpenCASCADE).
Silent fallback to text parsing is strictly forbidden; missing CAD tooling causes a test FAILURE/BLOCKED result.
"""

import os
import sys
import glob
from pathlib import Path

# Add potential FreeCAD library paths on Linux/macOS/Windows
potential_fc_paths = [
    "/usr/lib/freecad/lib",
    "/usr/lib/freecad-python3/lib",
    "/usr/lib/freecad-daily/lib",
    "/usr/share/freecad/lib",
    "C:/Program Files/FreeCAD 0.21/bin",
    "C:/Program Files/FreeCAD 0.20/bin",
    "C:/Program Files/FreeCAD/bin",
]
for p in potential_fc_paths:
    if os.path.exists(p) and p not in sys.path:
        sys.path.append(p)

def validate_step_files():
    base_dir = Path(__file__).resolve().parent.parent
    step_dir = base_dir / "output" / "RevG" / "Mechanical_Phase04C" / "STEP"
    assembly_dir = base_dir / "output" / "RevG" / "Mechanical_Phase04C" / "Assemblies"
    
    files = sorted(list(step_dir.glob("*.step")) + list(assembly_dir.glob("*.step")))
    if not files:
        print("ERROR: No STEP files found in target directories!")
        print(f"Looked in: {step_dir} and {assembly_dir}")
        sys.exit(1)
        
    print(f"Found {len(files)} STEP files for native CAD kernel validation.")
    
    # Try importing FreeCAD Part module first, then OpenCASCADE (pythonocc)
    cad_engine = None
    try:
        import FreeCAD
        import Part
        cad_engine = "FreeCAD"
        print(f"Using FreeCAD Native CAD Engine (Version: {FreeCAD.Version()}).")
    except ImportError:
        try:
            from OCC.Core.STEPControl import STEPControl_Reader
            from OCC.Core.IFSelect import IFSelect_RetDone
            from OCC.Core.BRepCheck import BRepCheck_Analyzer
            from OCC.Core.GProp import GProp_GProps
            from OCC.Core.BRepGProp import brepgprop
            from OCC.Core.TopExp import TopExp_Explorer
            from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_SOLID
            cad_engine = "OpenCASCADE"
            print("Using OpenCASCADE (pythonocc) Native CAD Engine.")
        except (ImportError, Exception) as e:
            print("=" * 100)
            print("CRITICAL FAILURE / TEST BLOCKED:")
            print("Neither FreeCAD nor OpenCASCADE native CAD kernel is importable in this environment.")
            print(f"Error details: {e}")
            print("PER SPECIFICATION: Silent text-parsing fallback is STRICTLY DISALLOWED.")
            print("A native CAD geometry kernel is required to validate ISO-10303-21 STEP BRep topology.")
            print("Status: BLOCKED — MISSING NATIVE CAD KERNEL (FreeCAD / OpenCASCADE)")
            print("=" * 100)
            return False, "NO_NATIVE_KERNEL"

    results = []
    all_passed = True
    
    print("-" * 105)
    print(f"{'File Name':<44} | {'Solids':<6} | {'Faces':<7} | {'Volume (mm³)':<14} | {'Status':<10}")
    print("-" * 105)
    
    for f in files:
        fname = f.name
        status = "FAIL"
        num_solids = 0
        num_faces = 0
        volume = 0.0
        
        if cad_engine == "FreeCAD":
            try:
                shape = Part.read(str(f))
                is_valid = shape.isValid()
                num_solids = len(shape.Solids) if shape.Solids else (1 if shape.Volume > 0 else 0)
                num_faces = len(shape.Faces)
                volume = shape.Volume
                if is_valid and num_faces > 0 and volume > 0:
                    status = "PASS"
                else:
                    status = "INVALID"
                    all_passed = False
            except Exception as e:
                status = f"ERR: {str(e)[:15]}"
                all_passed = False
                
        elif cad_engine == "OpenCASCADE":
            try:
                reader = STEPControl_Reader()
                status_code = reader.ReadFile(str(f))
                if status_code == IFSelect_RetDone:
                    reader.TransferRoots()
                    shape = reader.OneShape()
                    analyzer = BRepCheck_Analyzer(shape)
                    is_valid = analyzer.IsValid()
                    
                    props = GProp_GProps()
                    brepgprop.VolumeProperties(shape, props)
                    volume = props.Mass()
                    
                    face_exp = TopExp_Explorer(shape, TopAbs_FACE)
                    while face_exp.More():
                        num_faces += 1
                        face_exp.Next()
                        
                    solid_exp = TopExp_Explorer(shape, TopAbs_SOLID)
                    while solid_exp.More():
                        num_solids += 1
                        solid_exp.Next()
                        
                    if is_valid and num_faces > 0 and volume > 0:
                        status = "PASS"
                    else:
                        status = "INVALID"
                        all_passed = False
                else:
                    status = "READ_ERR"
                    all_passed = False
            except Exception as e:
                status = f"ERR: {str(e)[:15]}"
                all_passed = False
                
        vol_str = f"{volume:.2f}"
        print(f"{fname:<44} | {num_solids:<6} | {num_faces:<7} | {vol_str:<14} | {status:<10}")
        results.append((fname, num_solids, num_faces, volume, status))
        
    print("-" * 105)
    print(f"Total Evaluated: {len(results)} | Native Engine: {cad_engine} | All Passed: {all_passed}")
    return all_passed, cad_engine

if __name__ == "__main__":
    success, engine = validate_step_files()
    if not success:
        sys.stdout.flush()
        os._exit(1)
    sys.stdout.flush()
    os._exit(0)
