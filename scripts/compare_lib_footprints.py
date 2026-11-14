import sys

# Compare footprints in SmartPen.kicad_pcb vs SmartPen.pretty
refs = ['R9', 'U3', 'R5', 'R15', 'R14', 'R7', 'C14', 'R8', 'R6', 'D2', 'D1']

with open('output/RevG/SmartPen.kicad_pcb', 'r') as f:
    pcb_text = f.read()

for ref in refs:
    # Find footprint block in PCB
    marker = f'(property "Reference" "{ref}"'
    idx = pcb_text.find(marker)
    if idx == -1:
        print(f'{ref} not found in PCB')
        continue
    # find start of footprint
    start = pcb_text.rfind('(footprint "', 0, idx)
    end = pcb_text.find('(footprint "', idx)
    if end == -1:
        end = pcb_text.find('(zone', idx)
    pcb_fp = pcb_text[start:idx+300]
    
    # Read library footprint
    mod_path = f'output/RevG/SmartPen.pretty/{ref}.kicad_mod'
    with open(mod_path, 'r') as mf:
        mod_text = mf.read()
    
    # Extract library footprint header
    mod_header = mod_text[:200]
    
    print(f'=== {ref} ===')
    print('PCB:', pcb_fp.split('\n')[0], pcb_fp.split('\n')[1])
    print('LIB:', mod_text.split('\n')[0])

