import sys
target = sys.argv[1] if len(sys.argv) > 1 else 'J_USB'
lines = open('output/RevF_Working/SmartPen.kicad_pcb').read().splitlines()
matches = [i for i, l in enumerate(lines) if target in l]
print(f"Found {len(matches)} matches for {target}")
for m in matches[:5]:
    start = max(0, m - 2)
    end = min(len(lines), m + 15)
    print(f"--- Match at line {m} ---")
    print('\n'.join(lines[start:end]))
