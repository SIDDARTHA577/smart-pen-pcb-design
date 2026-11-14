with open('output/RevG/SmartPen.kicad_pcb', 'r') as f:
    text = f.read()

def get_fp_text(ref):
    m = f'(property "Reference" "{ref}"'
    idx = text.find(m)
    start = text.rfind('(footprint "', 0, idx)
    depth = 0
    end = start
    for i in range(start, len(text)):
        if text[i] == '(': depth += 1
        elif text[i] == ')':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    return text[start:end]

print("=== PCB R1 (NO MISMATCH) ===")
print(get_fp_text("R1"))

print("\n=== PCB R9 (HAS MISMATCH) ===")
print(get_fp_text("R9"))

print("\n=== LIB R1 ===")
with open('output/RevG/SmartPen.pretty/R1.kicad_mod', 'r') as f:
    print(f.read())

