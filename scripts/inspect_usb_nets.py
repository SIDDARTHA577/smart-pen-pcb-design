import re

with open('output/RevF_Working/SmartPen.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect wires and labels near U_ESD, R7, R8
# Or better, let's look at the PCB nets in SmartPen_RevE_PCB.json because that defines the net for each pad!
import json
with open('output/RevF_Working/SmartPen_RevE_PCB.json') as f:
    pcb = json.load(f)

for s in pcb['shape']:
    if isinstance(s, str) and s.startswith('LIB~'):
        subs = s.split('#@$')
        ref = ''
        for sub in subs:
            if sub.startswith('TEXT~P~'): ref = sub.split('~')[10]
        if ref in ['U_ESD', 'R7', 'R8', 'J_USB', 'R5', 'R6', 'C10', 'C14']:
            print(f'=== {ref} ===')
            for sub in subs:
                if sub.startswith('PAD~'):
                    toks = sub.split('~')
                    print(f'  Pin {toks[8]}: net={toks[7]}')

