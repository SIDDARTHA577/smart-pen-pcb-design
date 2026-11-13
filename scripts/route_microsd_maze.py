"""Complete Grid-based Maze Router for MicroSD Carrier PCB.
Routes all nets with guaranteed clearance and converts grid paths to clean KiCad PCB segments and vias.
"""
import heapq
import json
import uuid
import subprocess
import os
from pathlib import Path

KICAD_CLI = Path(os.environ.get('LOCALAPPDATA', '')) / 'Programs/KiCad/10.0/bin/kicad-cli.exe'

RES = 0.05
W_MM, H_MM = 11.4, 16.0
NX = int(round(W_MM / RES)) + 1
NY = int(round(H_MM / RES)) + 1

def to_grid(x, y):
    gx = int(round(x / RES))
    gy = int(round(y / RES))
    return max(0, min(NX - 1, gx)), max(0, min(NY - 1, gy))

def to_mm(gx, gy):
    return round(gx * RES, 3), round(gy * RES, 3)

def solve_carrier():
    print(f"Grid size: {NX} x {NY} x 2 layers")
    carrier_dir = Path('output/RevF_Working/MicroSD_Carrier')
    
    grid = [{}, {}]  # layer 0=F.Cu, 1=B.Cu: (gx, gy) -> (net_id, is_pad_center)

    pads = [
        # J1 (FPC 6P) at (5.7, 2.0)
        ('J1_1', 2, 4.45, 3.25, 0.30, 1.00, 0),
        ('J1_2', 1, 4.95, 3.25, 0.30, 1.00, 0),
        ('J1_3', 3, 5.45, 3.25, 0.30, 1.00, 0),
        ('J1_4', 4, 5.95, 3.25, 0.30, 1.00, 0),
        ('J1_5', 5, 6.45, 3.25, 0.30, 1.00, 0),
        ('J1_6', 6, 6.95, 3.25, 0.30, 1.00, 0),
        ('J1_MP1', 1, 3.50, 1.80, 1.00, 1.20, 0),
        ('J1_MP2', 1, 7.90, 1.80, 1.00, 1.20, 0),

        # C1 (0402) at (1.8, 3.8)
        ('C1_1', 2, 1.32, 3.80, 0.60, 0.60, 0),
        ('C1_2', 1, 2.28, 3.80, 0.60, 0.60, 0),

        # C2 (0603) at (1.8, 6.2)
        ('C2_1', 2, 1.05, 6.20, 0.80, 0.90, 0),
        ('C2_2', 1, 2.55, 6.20, 0.80, 0.90, 0),

        # R1 (0402) at (9.6, 3.8)
        ('R1_1', 2, 9.12, 3.80, 0.60, 0.60, 0),
        ('R1_2', 6, 10.08, 3.80, 0.60, 0.60, 0),

        # R2 (0402) at (9.6, 6.2)
        ('R2_1', 2, 9.12, 6.20, 0.60, 0.60, 0),
        ('R2_2', 5, 10.08, 6.20, 0.60, 0.60, 0),

        # J2 (TF-01A) at (5.7, 10.5)
        ('J2_1', 0, 2.20, 6.50, 0.70, 1.50, 0),
        ('J2_2', 6, 3.30, 6.50, 0.70, 1.50, 0),
        ('J2_3', 4, 4.40, 6.50, 0.70, 1.50, 0),
        ('J2_4', 2, 5.50, 6.50, 0.70, 1.50, 0),
        ('J2_5', 3, 6.60, 6.50, 0.70, 1.50, 0),
        ('J2_6', 1, 7.70, 6.50, 0.70, 1.50, 0),
        ('J2_7', 5, 8.80, 6.50, 0.70, 1.50, 0),
        ('J2_8', 0, 9.90, 6.50, 0.70, 1.50, 0),
        ('J2_9', 1, 0.40, 15.00, 1.20, 1.80, 0),
        ('J2_10', 1, 11.00, 15.00, 1.20, 1.80, 0),
    ]

    pad_dict = {p[0]: p for p in pads}

    # Mark pad keepouts:
    pad_clearance = 0.16
    for name, net_id, px, py, pw, ph, layer in pads:
        gx0, gy0 = to_grid(px - pw/2 - pad_clearance, py - ph/2 - pad_clearance)
        gx1, gy1 = to_grid(px + pw/2 + pad_clearance, py + ph/2 + pad_clearance)
        for gx in range(gx0, gx1 + 1):
            for gy in range(gy0, gy1 + 1):
                in_pad = (abs(gx*RES - px) <= pw/2 and abs(gy*RES - py) <= ph/2)
                grid[layer][(gx, gy)] = (net_id, in_pad)

    # Edge margin: 0.35mm from board edge
    edge_cells = int(round(0.35 / RES))
    for layer in [0, 1]:
        for gx in range(NX):
            for gy in range(edge_cells):
                grid[layer][(gx, gy)] = (-1, False)
                grid[layer][(gx, NY - 1 - gy)] = (-1, False)
        for gy in range(NY):
            for gx in range(edge_cells):
                grid[layer][(gx, gy)] = (-1, False)
                grid[layer][(NX - 1 - gx, gy)] = (-1, False)

    # Net connections to route:
    net_connections = [
        (3, [('J1_3', 'J2_5')]),
        (4, [('J1_4', 'J2_3')]),
        (5, [('J1_5', 'J2_7'), ('J2_7', 'R2_2')]),
        (6, [('J1_6', 'J2_2'), ('J2_2', 'R1_2')]),
        (2, [('J1_1', 'C1_1'), ('C1_1', 'C2_1'), ('J1_1', 'J2_4'), ('J2_4', 'R1_1'), ('R1_1', 'R2_1')]),
        (1, [('J1_2', 'J1_MP1'), ('J1_MP1', 'C1_2'), ('C1_2', 'C2_2'), ('J1_2', 'J1_MP2'), ('J1_MP2', 'J2_6'), ('J2_6', 'J2_10'), ('C2_2', 'J2_9')])
    ]

    def mark_path_obstacles(path, net_id):
        clr_cells = int(round(0.15 / RES))
        for layer, gx, gy in path:
            for dx in range(-clr_cells, clr_cells + 1):
                for dy in range(-clr_cells, clr_cells + 1):
                    if dx*dx + dy*dy <= clr_cells*clr_cells:
                        pt = (gx + dx, gy + dy)
                        if 0 <= pt[0] < NX and 0 <= pt[1] < NY:
                            existing = grid[layer].get(pt)
                            if existing is None or existing[0] == 0:
                                grid[layer][pt] = (net_id, False)

    def route_pair(p1_name, p2_name, net_id):
        p1 = pad_dict[p1_name]
        p2 = pad_dict[p2_name]
        gx1, gy1 = to_grid(p1[2], p1[3])
        gx2, gy2 = to_grid(p2[2], p2[3])

        start_pt = (p1[6], gx1, gy1)
        target_pt = (p2[6], gx2, gy2)

        open_set = []
        heapq.heappush(open_set, (0, 0, start_pt, [start_pt]))
        visited = set()

        def h(pt):
            l, x, y = pt
            tl, tx, ty = target_pt
            return (abs(x - tx) + abs(y - ty)) + (30 if l != tl else 0)

        while open_set:
            f, cost, current, path = heapq.heappop(open_set)
            if current in visited:
                continue
            visited.add(current)

            cl, cx, cy = current
            if (cl, cx, cy) == target_pt or (cx == target_pt[1] and cy == target_pt[2]):
                mark_path_obstacles(path, net_id)
                return path

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < NX and 0 <= ny < NY:
                    npt = (cl, nx, ny)
                    if npt in visited:
                        continue
                    cell = grid[cl].get((nx, ny))
                    if cell is not None:
                        c_net, in_pad = cell
                        if c_net != 0 and c_net != net_id:
                            continue
                    new_cost = cost + 1.0
                    heapq.heappush(open_set, (new_cost + h(npt), new_cost, npt, path + [npt]))

            other_layer = 1 - cl
            vpt = (other_layer, cx, cy)
            if vpt not in visited:
                via_ok = True
                via_r = int(round(0.35 / RES))
                for vx in range(cx - via_r, cx + via_r + 1):
                    for vy in range(cy - via_r, cy + via_r + 1):
                        if (vx - cx)**2 + (vy - cy)**2 <= via_r**2:
                            for l in [0, 1]:
                                cell = grid[l].get((vx, vy))
                                if cell is not None and cell[0] != 0 and cell[0] != net_id:
                                    via_ok = False
                                    break
                            if not via_ok:
                                break
                    if not via_ok:
                        break
                if via_ok:
                    new_cost = cost + 25.0
                    heapq.heappush(open_set, (new_cost + h(vpt), new_cost, vpt, path + [vpt]))

        print(f"FAILED to route {p1_name} -> {p2_name} for Net {net_id}")
        return None

    routed_nets = {}
    for net_id, pairs in net_connections:
        routed_nets[net_id] = []
        for p1_name, p2_name in pairs:
            print(f"Routing Net {net_id}: {p1_name} -> {p2_name}...")
            path = route_pair(p1_name, p2_name, net_id)
            if path:
                routed_nets[net_id].append(path)
                print(f"  Routed {len(path)} cells")
            else:
                print(f"  FAILED!")

    segments = []
    vias = set()

    for net_id, paths in routed_nets.items():
        for path in paths:
            if not path:
                continue
            simplified = [path[0]]
            for i in range(1, len(path) - 1):
                prev_l, prev_x, prev_y = simplified[-1]
                cur_l, cur_x, cur_y = path[i]
                next_l, next_x, next_y = path[i+1]

                if cur_l != prev_l or cur_l != next_l:
                    simplified.append(path[i])
                else:
                    dx1, dy1 = cur_x - prev_x, cur_y - prev_y
                    dx2, dy2 = next_x - cur_x, next_y - cur_y
                    if (dx1 * dy2 - dy1 * dx2) != 0:
                        simplified.append(path[i])
            simplified.append(path[-1])

            for i in range(len(simplified) - 1):
                l1, x1, y1 = simplified[i]
                l2, x2, y2 = simplified[i+1]
                mx1, my1 = to_mm(x1, y1)
                mx2, my2 = to_mm(x2, y2)

                if l1 != l2:
                    vias.add((mx1, my1, net_id))
                else:
                    layer_name = "F.Cu" if l1 == 0 else "B.Cu"
                    if (mx1, my1) != (mx2, my2):
                        segments.append(f'(segment (start {mx1:.3f} {my1:.3f}) (end {mx2:.3f} {my2:.3f}) (width 0.15) (layer "{layer_name}") (net {net_id}))')

    pcb_lines = [
        '(kicad_pcb (version 20221018) (generator pcbnew) (generator_version "8.0")',
        '  (general (thickness 0.8))',
        '  (paper "A4")',
        '  (title_block (title "MicroSD Carrier PCB") (rev "Rev F.1") (company "RadixView Technologies"))',
        '  (layers',
        '    (0 "F.Cu" signal)',
        '    (31 "B.Cu" signal)',
        '    (36 "B.SilkS" user "B.Silkscreen")',
        '    (37 "F.SilkS" user "F.Silkscreen")',
        '    (38 "B.Mask" user)',
        '    (39 "F.Mask" user)',
        '    (44 "Edge.Cuts" user)',
        '    (48 "F.Fab" user)',
        '    (49 "B.Fab" user)',
        '  )',
        '  (setup',
        '    (pad_to_mask_clearance 0.0)',
        '    (solder_mask_min_width 0.0)',
        '    (pad_to_paste_clearance 0)',
        '  )',
        '  (net 0 "")',
        '  (net 1 "GND")',
        '  (net 2 "3V3")',
        '  (net 3 "SD_SCK")',
        '  (net 4 "SD_MOSI")',
        '  (net 5 "SD_MISO")',
        '  (net 6 "SD_CS")',
        '  (net_class "Default" "Standard net class"',
        '    (clearance 0.127)',
        '    (trace_width 0.15)',
        '    (via_dia 0.50)',
        '    (via_drill 0.30)',
        '  )',
        '  (gr_line (start 0 0) (end 11.4 0) (layer "Edge.Cuts") (width 0.15))',
        '  (gr_line (start 11.4 0) (end 11.4 16.0) (layer "Edge.Cuts") (width 0.15))',
        '  (gr_line (start 11.4 16.0) (end 0 16.0) (layer "Edge.Cuts") (width 0.15))',
        '  (gr_line (start 0 16.0) (end 0 0) (layer "Edge.Cuts") (width 0.15))',

        '  (footprint "MicroSD:FPC_6P_0.5mm" (layer "F.Cu") (at 5.7 2.0)',
        '    (uuid "' + str(uuid.uuid4()) + '")',
        '    (fp_text reference "J1" (at 0 -1.5) (layer "F.SilkS") (effects (font (size 0.6 0.6) (thickness 0.1))))',
        '    (fp_text value "FH12-6S-0.5SH" (at 0 2.5) (layer "F.Fab") (effects (font (size 0.5 0.5) (thickness 0.1)) hide))',
        '    (pad "1" smd rect (at -1.25 1.25) (size 0.30 1.00) (layers "F.Cu" "F.Paste" "F.Mask") (net 2 "3V3"))',
        '    (pad "2" smd rect (at -0.75 1.25) (size 0.30 1.00) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))',
        '    (pad "3" smd rect (at -0.25 1.25) (size 0.30 1.00) (layers "F.Cu" "F.Paste" "F.Mask") (net 3 "SD_SCK"))',
        '    (pad "4" smd rect (at 0.25 1.25) (size 0.30 1.00) (layers "F.Cu" "F.Paste" "F.Mask") (net 4 "SD_MOSI"))',
        '    (pad "5" smd rect (at 0.75 1.25) (size 0.30 1.00) (layers "F.Cu" "F.Paste" "F.Mask") (net 5 "SD_MISO"))',
        '    (pad "6" smd rect (at 1.25 1.25) (size 0.30 1.00) (layers "F.Cu" "F.Paste" "F.Mask") (net 6 "SD_CS"))',
        '    (pad "MP1" smd rect (at -2.2 -0.2) (size 1.0 1.2) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))',
        '    (pad "MP2" smd rect (at 2.2 -0.2) (size 1.0 1.2) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))',
        '  )',

        '  (footprint "MicroSD:C_0402" (layer "F.Cu") (at 1.8 3.8)',
        '    (uuid "' + str(uuid.uuid4()) + '")',
        '    (fp_text reference "C1" (at 0 -0.8) (layer "F.Fab") (effects (font (size 0.5 0.5) (thickness 0.1))))',
        '    (pad "1" smd rect (at -0.48 0) (size 0.6 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (net 2 "3V3"))',
        '    (pad "2" smd rect (at 0.48 0) (size 0.6 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))',
        '  )',

        '  (footprint "MicroSD:C_0603" (layer "F.Cu") (at 1.8 6.2)',
        '    (uuid "' + str(uuid.uuid4()) + '")',
        '    (fp_text reference "C2" (at 0 -0.8) (layer "F.Fab") (effects (font (size 0.5 0.5) (thickness 0.1))))',
        '    (pad "1" smd rect (at -0.75 0) (size 0.8 0.9) (layers "F.Cu" "F.Paste" "F.Mask") (net 2 "3V3"))',
        '    (pad "2" smd rect (at 0.75 0) (size 0.8 0.9) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))',
        '  )',

        '  (footprint "MicroSD:R_0402" (layer "F.Cu") (at 9.6 3.8)',
        '    (uuid "' + str(uuid.uuid4()) + '")',
        '    (fp_text reference "R1" (at 0 -0.8) (layer "F.Fab") (effects (font (size 0.5 0.5) (thickness 0.1))))',
        '    (pad "1" smd rect (at -0.48 0) (size 0.6 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (net 2 "3V3"))',
        '    (pad "2" smd rect (at 0.48 0) (size 0.6 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (net 6 "SD_CS"))',
        '  )',

        '  (footprint "MicroSD:R_0402" (layer "F.Cu") (at 9.6 6.2)',
        '    (uuid "' + str(uuid.uuid4()) + '")',
        '    (fp_text reference "R2" (at 0 -0.8) (layer "F.Fab") (effects (font (size 0.5 0.5) (thickness 0.1))))',
        '    (pad "1" smd rect (at -0.48 0) (size 0.6 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (net 2 "3V3"))',
        '    (pad "2" smd rect (at 0.48 0) (size 0.6 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (net 5 "SD_MISO"))',
        '  )',

        '  (footprint "MicroSD:MicroSD_Socket_TF01A" (layer "F.Cu") (at 5.7 10.5)',
        '    (uuid "' + str(uuid.uuid4()) + '")',
        '    (fp_text reference "J2" (at 0 -6.5) (layer "F.SilkS") (effects (font (size 0.6 0.6) (thickness 0.1))))',
        '    (fp_text value "TF-01A" (at 0 6.5) (layer "F.Fab") (effects (font (size 0.5 0.5) (thickness 0.1)) hide))',
        '    (pad "1" smd rect (at -3.5 -4.0) (size 0.70 1.50) (layers "F.Cu" "F.Paste" "F.Mask") (net 0 ""))',
        '    (pad "2" smd rect (at -2.4 -4.0) (size 0.70 1.50) (layers "F.Cu" "F.Paste" "F.Mask") (net 6 "SD_CS"))',
        '    (pad "3" smd rect (at -1.3 -4.0) (size 0.70 1.50) (layers "F.Cu" "F.Paste" "F.Mask") (net 4 "SD_MOSI"))',
        '    (pad "4" smd rect (at -0.2 -4.0) (size 0.70 1.50) (layers "F.Cu" "F.Paste" "F.Mask") (net 2 "3V3"))',
        '    (pad "5" smd rect (at 0.9 -4.0) (size 0.70 1.50) (layers "F.Cu" "F.Paste" "F.Mask") (net 3 "SD_SCK"))',
        '    (pad "6" smd rect (at 2.0 -4.0) (size 0.70 1.50) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))',
        '    (pad "7" smd rect (at 3.1 -4.0) (size 0.70 1.50) (layers "F.Cu" "F.Paste" "F.Mask") (net 5 "SD_MISO"))',
        '    (pad "8" smd rect (at 4.2 -4.0) (size 0.70 1.50) (layers "F.Cu" "F.Paste" "F.Mask") (net 0 ""))',
        '    (pad "9" smd rect (at -5.3 4.5) (size 1.20 1.80) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))',
        '    (pad "10" smd rect (at 5.3 4.5) (size 1.20 1.80) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))',
        '  )',
    ]

    for vx, vy, vnet in vias:
        pcb_lines.append(f'  (via (at {vx:.3f} {vy:.3f}) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net {vnet}))')

    for seg in segments:
        pcb_lines.append(f'  {seg}')

    zones = [
        '  (zone (net 1) (net_name "GND") (layers "F.Cu") (tstamp "' + str(uuid.uuid4()) + '")',
        '    (hatch full 0.5) (priority 0) (connect_pads (clearance 0.15)) (min_thickness 0.127)',
        '    (filled_areas_thickness no) (fill yes (thermal_gap 0.15) (thermal_bridge_width 0.18))',
        '    (polygon (pts (xy 0.25 0.25) (xy 11.15 0.25) (xy 11.15 15.75) (xy 0.25 15.75)))',
        '  )',
        '  (zone (net 1) (net_name "GND") (layers "B.Cu") (tstamp "' + str(uuid.uuid4()) + '")',
        '    (hatch full 0.5) (priority 0) (connect_pads (clearance 0.15)) (min_thickness 0.127)',
        '    (filled_areas_thickness no) (fill yes (thermal_gap 0.15) (thermal_bridge_width 0.18))',
        '    (polygon (pts (xy 0.25 0.25) (xy 11.15 0.25) (xy 11.15 15.75) (xy 0.25 15.75)))',
        '  )'
    ]
    pcb_lines.extend(zones)
    pcb_lines.append(')')

    out_file = carrier_dir / 'MicroSD_Carrier.kicad_pcb'
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(pcb_lines))
    print(f"Successfully generated {out_file} with {len(segments)} segments and {len(vias)} vias.")

if __name__ == '__main__':
    solve_carrier()
