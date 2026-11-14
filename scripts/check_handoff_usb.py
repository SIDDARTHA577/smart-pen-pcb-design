with open('reports/Smart_Pen_PCB_Handoff_extracted.txt', 'r', errors='ignore') as f:
    text = f.read()

for i, line in enumerate(text.splitlines()):
    if any(k in line.lower() for k in ['usb', 'connector', 'port', 'receptacle', 'charging', 'aperture', 'barrel', 'click']):
        print(f'{i}: {line}')

