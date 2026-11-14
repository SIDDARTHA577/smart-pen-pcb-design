with open('output/RevG/SmartPen.pretty/J_USB.kicad_mod', 'r') as f:
    text = f.read()

for line in text.splitlines():
    if any(k in line for k in ['fp_line', 'fp_arc', 'fp_rect', 'pad', 'model']):
        print(line)

