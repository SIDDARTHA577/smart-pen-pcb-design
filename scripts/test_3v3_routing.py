import sys, json
sys.path.insert(0, '.')
from scripts.solve_zero_drc import run_check
from scripts.verify_smartpen_geometry import check_pcb_geometry

pads, segs, vias, errs = run_check()

# Load 3V3 from routed_paths.json
with open('output/RevF_Working/routed_paths.json') as f:
    rp = json.load(f)

# Compress 3V3 path
from scripts.export_final_pcb import compress_orthogonal_path

segs_3v3 = []
vias_3v3 = []
for p in rp.get('3V3', []):
    s_list, v_list = compress_orthogonal_path(p)
    for s in s_list:
        layer = "F.Cu" if s[4] == 0 else "B.Cu"
        segs_3v3.append((round(s[0], 3), round(s[1], 3), round(s[2], 3), round(s[3], 3), layer, "3V3", 0.20))
    for v in v_list:
        vias_3v3.append((round(v[0], 3), round(v[1], 3), "3V3"))

print(f"Compressed 3V3: {len(segs_3v3)} segments, {len(vias_3v3)} vias")

# Check 3V3 against existing pads and traces
test_segs = segs + segs_3v3
test_vias = list(set(vias).union(vias_3v3))

all_errs = check_pcb_geometry(pads, test_segs, list(test_vias))
print(f"Total errors with 3V3 added: {len(all_errs)}")
for e in all_errs[:20]:
    print("  *", e)
