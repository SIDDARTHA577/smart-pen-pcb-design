from pathlib import Path

fp_dir = Path('output/RevG/variants/FourLayer_ECR_R9_50mA/SmartPen.pretty')
q1_mod = (fp_dir / 'Q1.kicad_mod').read_text(encoding='utf-8')
jpwr_mod = (fp_dir / 'J_PWR.kicad_mod').read_text(encoding='utf-8')

print("=== Q1.kicad_mod ===")
print(q1_mod)

print("=== J_PWR.kicad_mod ===")
print(jpwr_mod)
