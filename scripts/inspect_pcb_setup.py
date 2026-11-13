with open('output/RevF_Working/SmartPen.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('(setup')
end = text.find('(net ', pos)
print(text[pos:end])
