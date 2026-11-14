import re

refs = ['R9', 'U3', 'R5', 'R15', 'R14', 'R7', 'C14', 'R8', 'R6', 'D2', 'D1']

with open('output/RevG/SmartPen.kicad_pcb', 'r') as f:
    pcb_text = f.read()

for ref in refs:
    marker = f'(property "Reference" "{ref}"'
    idx = pcb_text.find(marker)
    start = pcb_text.rfind('(footprint "', 0, idx)
    # find closing paren of this footprint
    # count parens
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
    pcb_fp = pcb_text[start:end]
    
    with open(f'output/RevG/SmartPen.pretty/{ref}.kicad_mod', 'r') as mf:
        lib_fp = mf.read()
    
    # Extract pads from pcb_fp and lib_fp
    pcb_pads = re.findall(r'\(pad\s+"?([^"\s]+)"?\s+([^\)]+)\)', pcb_fp)
    lib_pads = re.findall(r'\(pad\s+"?([^"\s]+)"?\s+([^\)]+)\)', lib_fp)
    
    print(f'=== {ref} ===')
    print(f'  PCB pads count: {len(pcb_pads)}, LIB pads count: {len(lib_pads)}')
    # compare pad details
    for p_num, p_body in pcb_pads:
        # strip net info from p_body for comparison
        clean_pcb_body = re.sub(r'\(net\s+[^\)]+\)', '', p_body).strip()
        matching_lib = [lb for ln, lb in lib_pads if ln == p_num]
        if not matching_lib:
            print(f'    Pad {p_num} missing in LIB!')
        else:
            clean_lib_body = re.sub(r'\(net\s+[^\)]+\)', '', matching_lib[0]).strip()
            if clean_pcb_body != clean_lib_body:
                print(f'    Pad {p_num} mismatch:')
                print(f'      PCB: {clean_pcb_body[:80]}')
                print(f'      LIB: {clean_lib_body[:80]}')

