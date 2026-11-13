import sys
sys.path.insert(0, '.')
from scripts.solve_zero_drc_perfect import run_check

pads, segments, vias, n_err = run_check()

def inspect_net(net_name):
    print(f"=== NET: {net_name} ===")
    net_pads = [p for p in pads if p['net'] == net_name]
    for p in net_pads:
        print(f"  Pad {p['ref']}.{p['pin']} at ({p['x']:.3f}, {p['y']:.3f}) w={p['w']} h={p['h']}")
    net_vias = [v for v in vias if v[2] == net_name]
    for v in net_vias:
        print(f"  Via at ({v[0]:.3f}, {v[1]:.3f})")
    net_segs = [s for s in segments if s[5] == net_name]
    for s in net_segs:
        print(f"  Seg {s[4]}: ({s[0]:.3f}, {s[1]:.3f}) -> ({s[2]:.3f}, {s[3]:.3f})")

if __name__ == '__main__':
    for n in sys.argv[1:]:
        inspect_net(n)
