with open('output/RevF_Working/SmartPen.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('(setup')
end = text.find('(net 0', pos)
print(text[pos:end])
