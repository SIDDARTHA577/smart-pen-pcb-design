with open('reports/RevF/SmartPen.net', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('(net (code "1")')
print(text[pos:pos+1500])
