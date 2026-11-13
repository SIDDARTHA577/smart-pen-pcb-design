with open('output/RevF_Working/Front_MPU/Front_MPU.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('(zone')
while pos != -1:
    print(text[pos:pos+400])
    pos = text.find('(zone', pos+1)
