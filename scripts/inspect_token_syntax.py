with open('output/RevG/SmartPen.kicad_pcb', 'r') as f:
    text = f.read()

# Look for (segment or (via or (net
for token in ['(segment', '(via', '(net ']:
    idx = text.find(token)
    if idx != -1:
        print(f'=== {token} ===')
        print(text[idx:idx+250])
    else:
        print(f'{token} not found')

