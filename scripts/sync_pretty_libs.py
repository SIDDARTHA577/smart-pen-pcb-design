import pcbnew
import re

board = pcbnew.LoadBoard("output/RevG/SmartPen.kicad_pcb")
refs = ['R9', 'U3', 'R5', 'R15', 'R14', 'R7', 'C14', 'R8', 'R6', 'D2', 'D1']

for r in refs:
    fp = board.FindFootprintByReference(r)
    if not fp:
        continue
    # Save footprint to library file
    mod_path = f"output/RevG/SmartPen.pretty/{r}.kicad_mod"
    
    # We can create a temporary board with just this footprint and export, or use SaveFootprint
    # Or format as s-expression
    # Let's extract from SmartPen.kicad_pcb text directly:
    with open("output/RevG/SmartPen.kicad_pcb", "r") as f:
        pcb_text = f.read()
    
    marker = f'(property "Reference" "{r}"'
    idx = pcb_text.find(marker)
    start = pcb_text.rfind('(footprint "', 0, idx)
    
    # find closing paren
    depth = 0
    end = start
    for i in range(start, len(pcb_text)):
        if pcb_text[i] == '(':
            depth += 1
        elif pcb_text[i] == ')':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    fp_text = pcb_text[start:end]
    
    # In .kicad_mod, the header is (footprint "Ref" ... instead of (footprint "SmartPen:Ref"
    mod_content = re.sub(r'\(footprint "SmartPen:([^"]+)"', r'(footprint "\1"', fp_text, count=1)
    # Strip (at X Y [rot]) from the footprint itself since library footprints are at (0 0)
    mod_content = re.sub(r'\n\s*\(at\s+[-\d\.]+\s+[-\d\.]+(\s+[-\d\.]+)?\)', '', mod_content, count=1)
    # Strip net info from pads in library
    mod_content = re.sub(r'\s*\(net\s+"?[^"\)]+"?\)', '', mod_content)
    
    with open(mod_path, "w", encoding="utf-8") as mf:
        mf.write(mod_content)
    print(f"Updated {mod_path}")

