with open('output/RevF_Working/Front_MPU/Front_MPU.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('(setup')
end = text.find('(net ', pos)
print(text[pos:end])
