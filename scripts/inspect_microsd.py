import re

with open('output/RevF_Working/MicroSD_Carrier/MicroSD_Carrier.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

symbols = re.findall(r'\(symbol\s+\(lib_id.*?\n\s+\(uuid.*?\n\s+\(property "Reference" "(.*?)".*?\n\s+\(property "Value" "(.*?)"', text)
print('Symbols in sch:', symbols)

labels = re.findall(r'\(label "(.*?)"', text)
print('Labels in sch:', sorted(list(set(labels))))

# check pin numbers of symbols
pins = re.findall(r'\(symbol "MicroSD_Lib:(.*?)".*?\n(.*?)\n  \)', text, re.DOTALL)
for name, body in pins:
    print(f'Symbol definition: {name}')
    sym_pins = re.findall(r'\(pin \w+ \w+ .*?\(name "(.*?)" .*?\(number "(.*?)"', body)
    for pname, pnum in sym_pins:
        print(f'  Pin {pnum}: {pname}')

