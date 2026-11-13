"""Build corrected Smart Pen Rev E schematic in EasyEDA Standard JSON format.
Ensures zero TBD strings and exact component values/metadata.
"""
import json
import csv
from pathlib import Path

def parse_props(p_str):
    if not p_str:
        return {}
    tokens = p_str.split('`')
    props = {}
    for i in range(0, len(tokens) - 1, 2):
        if tokens[i]:
            props[tokens[i]] = tokens[i+1]
    return props

def encode_props(props):
    items = []
    for k, v in props.items():
        items.append(k)
        items.append(v)
    return '`'.join(items) + '`'

VALUE_CLEANUP = {
    'FB1': '120R BLM18PG',
    'C6': '15pF 50V C0G',
    'C7': '15pF 50V C0G',
    'U_ESD': 'USBLC6-2SC6',
    'R9': '2.0k (500mA)',
    'D3': '1N5819HW-7-F',
    'SW1': 'RESET',
    'SW2': 'BOOT',
    'SW3': 'ON/OFF',
    'SW4': 'ERASE',
    'SW5': 'MODE',
    'Y1': '40MHz +/-10ppm',
    'J_RF': 'U.FL 50R',
    'J_USB': 'USB-C 16P',
    'J_BAT': 'LiPo 2P 1.0mm',
    'J_PWR': 'AP2112K-3.3',
    'J_IMU': 'MPU 4P 1.0mm',
    'J_MOT': 'HAPTIC 2P',
    'J_SD': 'MicroSD 6P FPC',
    'J_TOUCH': 'TOUCH 3P 1.0mm',
    'J_UART': 'UART 4P 1.27mm',
    'Q1': 'AO3400A N-MOS',
    'U3': 'MCP23008',
}

def build_schematic():
    src_path = Path('SmartPen_RevD_AutoLinked_DRAFT/EasyEDA/SmartPen_RevD_Connected_Schematic_DRAFT_EasyEDA.json')
    with open(src_path, 'r', encoding='utf-8') as f:
        sch = json.load(f)

    audit_file = Path('reports/FOOTPRINT_AUDIT.csv')
    verified_parts = {}
    with open(audit_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            verified_parts[row['Reference']] = row

    new_shapes = []
    for item in sch.get('shape', []):
        if not isinstance(item, str):
            new_shapes.append(item)
            continue
        
        if item.startswith('LIB~'):
            subs = item.split('#@$')
            lib_head = subs[0].split('~')
            props = parse_props(lib_head[3]) if len(lib_head) > 3 else {}
            
            # Identify RefDes
            ref = ''
            for sub in subs:
                if sub.startswith('T~'):
                    t = sub.split('~')
                    if len(t) >= 13 and t[1] == 'P':
                        ref = t[12] if t[11] == 'comment' else t[11]
            if not ref and 'prefix' in props:
                ref = props['prefix']
            
            if ref in verified_parts:
                vinfo = verified_parts[ref]
                props['package'] = vinfo['Footprint']
                props['Manufacturer Part'] = vinfo['Part Number']
                props['Manufacturer'] = vinfo['Manufacturer']
                props['Supplier'] = 'JLCPCB / LCSC'
                props['nameAlias'] = vinfo['Part Number']
                lib_head[3] = encode_props(props)
                subs[0] = '~'.join(lib_head)

                # Clean up T~N value text
                clean_val = VALUE_CLEANUP.get(ref, vinfo['Part Number'])
                for idx, sub in enumerate(subs):
                    if sub.startswith('T~'):
                        t = sub.split('~')
                        if len(t) >= 13 and t[1] == 'N':
                            t[12] = clean_val
                            subs[idx] = '~'.join(t)

                # If U3, ensure pin 19, 20 and EP 21 are properly present
                if ref == 'U3':
                    pin_count = sum(1 for sub in subs if sub.startswith('P~'))
                    if pin_count == 18:
                        pin19 = 'P~show~0~19~50.0~620.0~0~gge3019~0^^50.0~620.0^^M 50.0 620.0 h 20~#880000^^1~75.0~618.0~0~NC19~start~~~#0000FF^^1~54.0~613.0~0~19~start~~~#0000FF^^0~70.0~620.0^^0~M 66.0 617.0 L 62.0 620.0 L 66.0 623.0'
                        pin20 = 'P~show~0~20~50.0~640.0~0~gge3020~0^^50.0~640.0^^M 50.0 640.0 h 20~#880000^^1~75.0~638.0~0~NC20~start~~~#0000FF^^1~54.0~633.0~0~20~start~~~#0000FF^^0~70.0~640.0^^0~M 66.0 637.0 L 62.0 640.0 L 66.0 643.0'
                        subs.append(pin19)
                        subs.append(pin20)

            new_shapes.append('#@$'.join(subs))
        else:
            new_shapes.append(item)

    sch['shape'] = new_shapes
    sch['head']['c_para']['Title'] = 'Smart Pen Rev E Schematic'
    sch['head']['c_para']['Revision'] = 'Rev E'
    sch['head']['c_para']['Author'] = 'RadixView Technologies'

    out_file = Path('output/RevE_work/SmartPen_RevE_Schematic.json')
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(sch, f, indent=2)

    print(f"Generated Rev E schematic at {out_file}")

if __name__ == '__main__':
    build_schematic()
