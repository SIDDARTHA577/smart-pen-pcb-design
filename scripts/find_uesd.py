with open('output/RevF_Working/SmartPen.kicad_sch', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'SmartPen_Lib:U_ESD' in line and '(symbol ' in line and '(lib_symbols' not in lines[i-5:i+5]:
        print("Found U_ESD instance at line", i)
        for j in range(max(0, i-2), min(len(lines), i+30)):
            print(lines[j], end='')
