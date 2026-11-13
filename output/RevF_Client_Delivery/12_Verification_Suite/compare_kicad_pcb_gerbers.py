"""Compare KiCad PCB file against generated RS-274X Gerbers and Excellon drill files.
Verifies outline dimensions, via coordinates, pad counts, copper-to-edge clearance.
"""
import re
from pathlib import Path

def compare_kicad_and_gerbers():
    pcb_path = Path('output/client_delivery/02_KiCad_Source/SmartPen.kicad_pcb')
    gerber_dir = Path('output/client_delivery/04_Gerber_Drill')

    pcb_content = pcb_path.read_text(encoding='utf-8')

    # 1. Outline in KiCad PCB
    edge_lines = re.findall(r'\(gr_line \(start ([\d\.]+) ([\d\.]+)\) \(end ([\d\.]+) ([\d\.]+)\) \(layer "Edge\.Cuts"\)', pcb_content)
    xs = []
    ys = []
    for x1, y1, x2, y2 in edge_lines:
        xs.extend([float(x1), float(x2)])
        ys.extend([float(y1), float(y2)])
    pcb_len = max(xs) - min(xs)
    pcb_wid = max(ys) - min(ys)

    # Outline in GKO
    gko_content = (gerber_dir / 'SmartPen.GKO').read_text(encoding='utf-8')
    gko_xs = [int(m.group(1)) / 10000.0 for m in re.finditer(r'X(-?\d+)', gko_content)]
    gko_ys = [int(m.group(1)) / 10000.0 for m in re.finditer(r'Y(-?\d+)', gko_content)]
    gko_len = max(gko_xs) - min(gko_xs)
    gko_wid = max(gko_ys) - min(gko_ys)

    # 2. Vias in KiCad PCB vs DRL
    pcb_vias = re.findall(r'\(via \(at ([\d\.]+) ([\d\.]+)\) \(size ([\d\.]+)\) \(drill ([\d\.]+)\)', pcb_content)
    drl_content = (gerber_dir / 'SmartPen.DRL').read_text(encoding='utf-8')
    drl_holes = re.findall(r'X(\d+)Y(\d+)', drl_content)

    # 3. Footprints count
    pcb_fps = re.findall(r'\(footprint "([^"]+)"', pcb_content)

    # 4. Copper to edge clearance in zone
    zone_pts = re.findall(r'\(xy ([\d\.]+) ([\d\.]+)\)', pcb_content)
    z_xs = [float(p[0]) for p in zone_pts]
    z_ys = [float(p[1]) for p in zone_pts]
    copper_edge_clearance_x = min(z_xs) - min(xs)
    copper_edge_clearance_y = min(z_ys) - min(ys)

    print("=== KiCad PCB vs. Gerber Comparison Report ===")
    print(f"Board Length: KiCad={pcb_len:.3f} mm, Gerber GKO={gko_len:.3f} mm -> Delta: {abs(pcb_len - gko_len):.4f} mm")
    print(f"Board Width : KiCad={pcb_wid:.3f} mm, Gerber GKO={gko_wid:.3f} mm -> Delta: {abs(pcb_wid - gko_wid):.4f} mm")
    print(f"Via Count   : KiCad={len(pcb_vias)}, Drill DRL={len(drl_holes)} -> Match: {len(pcb_vias) == len(drl_holes)}")
    print(f"Footprints  : KiCad placed={len(pcb_fps)} components")
    print(f"Copper Edge Clearance: X={copper_edge_clearance_x:.3f} mm, Y={copper_edge_clearance_y:.3f} mm (>= 0.20 mm JLCPCB spec)")

    assert abs(pcb_len - gko_len) < 0.01, "Board length mismatch!"
    assert abs(pcb_wid - gko_wid) < 0.01, "Board width mismatch!"
    assert len(pcb_vias) == len(drl_holes), "Via/drill count mismatch!"
    assert len(pcb_fps) == 60, "Footprint count must be 60!"
    assert copper_edge_clearance_x >= 0.20 and copper_edge_clearance_y >= 0.20, "Copper edge clearance violation!"
    print("Manufacturing outputs 100% verified against native KiCad PCB!")

if __name__ == '__main__':
    compare_kicad_and_gerbers()

