"""Inspect EasyEDA schematic and PCB files.
"""
import json
import re
from pathlib import Path

def parse_easyeda_props(prop_str):
    parts = prop_str.split('`')
    props = {}
    for i in range(0, len(parts)-1, 2):
        props[parts[i]] = parts[i+1]
    return props

def inspect_schematic(sch_path):
    with open(sch_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    shapes = data.get('shape', [])
    components = []

    for item in shapes:
        if not isinstance(item, str) or not item.startswith('LIB~'):
            continue
        
        # Sub-shapes separated by #@$
        subshapes = item.split('#@$')
        lib_header = subshapes[0].split('~')
        props = parse_easyeda_props(lib_header[3]) if len(lib_header) > 3 else {}
        
        # Find prefix/reference and name/value from T~ subshapes
        prefix = ''
        name_val = ''
        pins = []
        for sub in subshapes[1:]:
            tokens = sub.split('~')
            if sub.startswith('T~'):
                # In EasyEDA: T~L/C/R~x~y~...~type~text
                # Let's inspect tokens
                # Usually type is in tokens: e.g. 'P' for prefix, 'N' for name
                if len(tokens) >= 12:
                    tag = tokens[10]
                    txt = tokens[11]
                    if tag == 'P':
                        prefix = txt
                    elif tag == 'N':
                        name_val = txt
            elif sub.startswith('P~'):
                # Pin
                # P~show~order~name~num~x~y~rot~id...
                pin_name = tokens[3] if len(tokens) > 3 else ''
                pin_num = tokens[4] if len(tokens) > 4 else ''
                pins.append((pin_num, pin_name))

        components.append({
            'prefix': prefix,
            'name': name_val,
            'package': props.get('package', ''),
            'mpn': props.get('Manufacturer Part', ''),
            'supplier': props.get('Supplier', ''),
            'pin_count': len(pins),
            'pins': pins,
            'props': props
        })
    return components

if __name__ == '__main__':
    sch_file = Path('SmartPen_RevD_AutoLinked_DRAFT/EasyEDA/SmartPen_RevD_Connected_Schematic_DRAFT_EasyEDA.json')
    comps = inspect_schematic(sch_file)
    print(f'Total schematic components: {len(comps)}')
    for c in comps:
        print(f"Ref: {c['prefix']:<8} Name: {c['name']:<20} Pkg: {c['package']:<24} MPN: {c['mpn']:<18} Pins: {c['pin_count']}")

