import csv

with open('output/RevG/Phase05_Manufacturing/03_BOM/SmartPen_MainBoard_BOM.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Total rows in Main Board BOM: {len(rows)}")
for r in rows:
    mpn = r['Value / MPN']
    mfr = r['Manufacturer']
    pkg = r['Package']
    des = r['Designator']
    desc = r['Description']
    if 'Generic' in mfr or pkg in ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 'R11', 'R12', 'R13', 'R14', 'R15', 'R16', 'R17', 'R18', 'R19', 'R20', 'R26', 'R27']:
        print(f"{des:<6} | MPN: {mpn:<24} | Mfr: {mfr:<26} | Pkg: {pkg:<8} | Desc: {desc}")
