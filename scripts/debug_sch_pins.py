import re

with open('output/RevF_Working/SmartPen.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

symbols = ['J_BAT', 'J_MOT', 'J_PWR', 'J_RF', 'J_USB', 'SW3', 'U3', 'U_ESD']

for sym in symbols:
    pos = text.find(f'"{sym}"')
    if pos != -1:
        start = max(0, pos - 200)
        end = min(len(text), pos + 1200)
        print(f"=== {sym} context ===")
        print(text[start:end])
        print("="*40)
