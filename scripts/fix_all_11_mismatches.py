import pcbnew

board = pcbnew.LoadBoard("output/RevG/SmartPen.kicad_pcb")
refs = ['U3', 'R5', 'R15', 'R14', 'R7', 'C14', 'R8', 'R6', 'D2', 'D1']

for r in refs:
    fp = board.FindFootprintByReference(r)
    if not fp:
        continue
    
    val = fp.GetValue()
    lines = [f'(footprint "{r}" (version 20221018) (generator pcbnew)']
    lines.append('  (layer "F.Cu")')
    lines.append(f'  (fp_text reference "{r}" (at 0 -1.5) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.15))))')
    lines.append(f'  (fp_text value "{val}" (at 0 1.5) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.15))))')
    
    # Pads
    for pad in fp.Pads():
        p_name = pad.GetName()
        pos = pad.GetFPRelativePosition()
        px = pos.x / 1e6
        py = pos.y / 1e6
        sz = pad.GetSize()
        sx = sz.x / 1e6
        sy = sz.y / 1e6
        
        # Pad shape
        shape_enum = pad.GetShape()
        if shape_enum == pcbnew.PAD_SHAPE_RECT:
            shape_str = "rect"
        elif shape_enum == pcbnew.PAD_SHAPE_ROUNDRECT:
            shape_str = "roundrect"
        elif shape_enum == pcbnew.PAD_SHAPE_OVAL:
            shape_str = "oval"
        elif shape_enum == pcbnew.PAD_SHAPE_CIRCLE:
            shape_str = "circle"
        else:
            shape_str = "rect"
            
        drill = pad.GetDrillSize()
        dx = drill.x / 1e6
        dy = drill.y / 1e6
        
        if dx > 0:
            pad_type = "thru_hole"
            drill_str = f" (drill {dx:.3f})" if dx == dy else f" (drill oval {dx:.3f} {dy:.3f})"
            layer_str = '"*.Cu" "*.Mask"'
        else:
            pad_type = "smd"
            drill_str = ""
            layer_str = '"F.Cu" "F.Paste" "F.Mask"'
            
        lines.append(f'  (pad "{p_name}" {pad_type} {shape_str} (at {px:.3f} {py:.3f}) (size {sx:.3f} {sy:.3f}){drill_str} (layers {layer_str}))')
        
    lines.append(')')
    
    mod_path = f"output/RevG/SmartPen.pretty/{r}.kicad_mod"
    with open(mod_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Generated clean {mod_path}")

