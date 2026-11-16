import pcbnew
from collections import defaultdict
from pathlib import Path

pcb_path = Path("output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb")
board = pcbnew.LoadBoard(str(pcb_path))

net_pads = defaultdict(list)
for fp in board.GetFootprints():
    ref = fp.GetReference()
    for pad in fp.Pads():
        netname = pad.GetNetname()
        if netname and not netname.startswith("unconnected-"):
            pnum = pad.GetNumber()
            pos = pad.GetPosition()
            net_pads[netname].append({
                "ref": ref,
                "pad": pnum,
                "x": round(pos.x / 1e6, 4),
                "y": round(pos.y / 1e6, 4),
                "layer": "F.Cu" if pad.IsOnLayer(pcbnew.F_Cu) else "B.Cu"
            })

print(f"Total active routed nets: {len(net_pads)}")
for netname in sorted(net_pads.keys()):
    pads = net_pads[netname]
    pads.sort(key=lambda p: (p["x"], p["y"]))
    print(f"\nNet: {netname} ({len(pads)} pads)")
    for p in pads:
        print(f"  {p['ref']}.{p['pad']} @ ({p['x']}, {p['y']}) [{p['layer']}]")

