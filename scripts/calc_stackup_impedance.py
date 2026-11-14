import math

def calc_single_ended_microstrip(w, h, t, er):
    # IPC-2141 formula
    # Zo = (87 / sqrt(er + 1.41)) * ln(5.98 * h / (0.8 * w + t))
    ratio = (5.98 * h) / (0.8 * w + t)
    if ratio <= 0: return 0.0
    zo = (87.0 / math.sqrt(er + 1.41)) * math.log(ratio)
    return zo

def calc_diff_microstrip(w, s, h, t, er):
    # IPC-2141 edge-coupled differential pair
    zo = calc_single_ended_microstrip(w, h, t, er)
    zdiff = 2.0 * zo * (1.0 - 0.48 * math.exp(-0.96 * (s / h)))
    return zdiff

print("=== STACKUP IMPEDANCE CALCULATIONS ===")

# 1. 2-Layer 1.6 mm
er_2l = 4.5
h_2l = 1.51 # mm
t_cu = 0.035 # mm (1 oz)

# Target 50 ohm single-ended
# solve for w
for w in [0.2, 0.5, 1.0, 1.5, 2.0, 2.5, 2.8, 3.0]:
    zo = calc_single_ended_microstrip(w, h_2l, t_cu, er_2l)
    print(f"2-Layer 1.6mm: w={w:.2f}mm -> Zo={zo:.1f} ohm")

# USB 90 ohm on 2-Layer
for w, s in [(0.2, 0.2), (0.3, 0.2), (0.5, 0.2), (1.0, 0.2), (1.2, 0.2)]:
    zd = calc_diff_microstrip(w, s, h_2l, t_cu, er_2l)
    print(f"2-Layer 1.6mm Diff USB: w={w:.2f}mm, s={s:.2f}mm -> Zdiff={zd:.1f} ohm")

# 2. 4-Layer JLC7628 1.6 mm
er_4l_7628 = 4.6
h_4l_7628 = 0.21 # mm (Prepreg 7628)
print("\n4-Layer JLC7628 (1.6mm, h1=0.21mm, er=4.6):")
for w in [0.2, 0.3, 0.35, 0.38, 0.4, 0.5]:
    zo = calc_single_ended_microstrip(w, h_4l_7628, t_cu, er_4l_7628)
    print(f"  Single RF 50 ohm: w={w:.2f}mm -> Zo={zo:.1f} ohm")

for w, s in [(0.15, 0.15), (0.2, 0.15), (0.2, 0.2), (0.25, 0.2)]:
    zd = calc_diff_microstrip(w, s, h_4l_7628, t_cu, er_4l_7628)
    print(f"  Diff USB 90 ohm: w={w:.2f}mm, s={s:.2f}mm -> Zdiff={zd:.1f} ohm")

# 3. 4-Layer JLC2313 1.0 mm
er_4l_2313 = 4.05
h_4l_2313 = 0.10 # mm (Prepreg 2313)
print("\n4-Layer JLC2313 (1.0mm, h1=0.10mm, er=4.05):")
for w in [0.15, 0.18, 0.20, 0.22]:
    zo = calc_single_ended_microstrip(w, h_4l_2313, t_cu, er_4l_2313)
    print(f"  Single RF 50 ohm: w={w:.2f}mm -> Zo={zo:.1f} ohm")

for w, s in [(0.12, 0.15), (0.15, 0.15), (0.15, 0.20)]:
    zd = calc_diff_microstrip(w, s, h_4l_2313, t_cu, er_4l_2313)
    print(f"  Diff USB 90 ohm: w={w:.2f}mm, s={s:.2f}mm -> Zdiff={zd:.1f} ohm")

