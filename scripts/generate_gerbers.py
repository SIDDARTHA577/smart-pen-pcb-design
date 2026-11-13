"""Generate industry-standard RS-274X Gerbers and Excellon drill file from Smart Pen Rev E PCB.
Produces:
- SmartPen.GTL (Top Layer Copper)
- SmartPen.GBL (Bottom Layer Copper)
- SmartPen.GTS (Top Solder Mask)
- SmartPen.GBS (Bottom Solder Mask)
- SmartPen.GTO (Top Silkscreen)
- SmartPen.GBO (Bottom Silkscreen)
- SmartPen.GKO (Board Outline / Edge Cuts)
- SmartPen.DRL (Excellon NC Drill)
- SmartPen_RevE_Gerbers.zip
"""
import json
import zipfile
from pathlib import Path

def generate_gerbers():
    pcb_path = Path('output/RevE_work/SmartPen_RevE_PCB.json')
    with open(pcb_path, 'r', encoding='utf-8') as f:
        pcb = json.load(f)

    out_dir = Path('output/RevE_work/gerbers')
    out_dir.mkdir(parents=True, exist_ok=True)

    # Standard RS-274X header format (mm units, 4.4 format, absolute)
    header = (
        "%FSLAX44Y44*%\n"
        "%MOMM*%\n"
        "%LPD*%\n"
    )

    # Extract pads, tracks, vias, outline from PCB shapes
    top_pads = []
    bot_pads = []
    top_tracks = []
    bot_tracks = []
    vias = []
    board_outline_pts = []
    silk_tracks = []

    for item in pcb.get('shape', []):
        if not isinstance(item, str):
            continue
        if item.startswith('TRACK~'):
            toks = item.split('~')
            w_mm = float(toks[1]) * 0.254
            layer_id = toks[2]
            net = toks[3]
            coords = [float(c) for c in toks[4].split()]
            pts_mm = [((coords[i] - 4000.0) * 0.254, (coords[i+1] - 3000.0) * 0.254) for i in range(0, len(coords)-1, 2)]

            if layer_id == '10': # Board outline
                board_outline_pts = pts_mm
            elif layer_id == '1': # Top copper track
                top_tracks.append((w_mm, pts_mm, net))
            elif layer_id == '2': # Bottom copper track
                bot_tracks.append((w_mm, pts_mm, net))
            elif layer_id == '3': # Top silk
                silk_tracks.append((w_mm, pts_mm))

        elif item.startswith('VIA~'):
            toks = item.split('~')
            vx_mm = (float(toks[1]) - 4000.0) * 0.254
            vy_mm = (float(toks[2]) - 3000.0) * 0.254
            diam_mm = float(toks[3]) * 0.254
            drill_mm = float(toks[4]) * 0.254
            net = toks[5]
            vias.append((vx_mm, vy_mm, diam_mm, drill_mm, net))

        elif item.startswith('LIB~'):
            subs = item.split('#@$')
            lib_toks = subs[0].split('~')
            for sub in subs:
                if sub.startswith('PAD~'):
                    ptoks = sub.split('~')
                    px_mm = (float(ptoks[2]) - 4000.0) * 0.254
                    py_mm = (float(ptoks[3]) - 3000.0) * 0.254
                    pw_mm = float(ptoks[4]) * 0.254
                    ph_mm = float(ptoks[5]) * 0.254
                    layer = ptoks[6]
                    net = ptoks[7]
                    num = ptoks[8]
                    if layer in ['1', '11']:
                        top_pads.append((px_mm, py_mm, pw_mm, ph_mm, net, num))
                    if layer in ['2', '11']:
                        bot_pads.append((px_mm, py_mm, pw_mm, ph_mm, net, num))
                elif sub.startswith('TRACK~'):
                    toks = sub.split('~')
                    w_mm = float(toks[1]) * 0.254
                    layer_id = toks[2]
                    coords = [float(c) for c in toks[4].split()]
                    pts_mm = [((coords[i] - 4000.0) * 0.254, (coords[i+1] - 3000.0) * 0.254) for i in range(0, len(coords)-1, 2)]
                    if layer_id == '3':
                        silk_tracks.append((w_mm, pts_mm))

    # Helper function to format Gerber coordinate (4.4 format: 1.0 mm -> 10000)
    def gcoord(val_mm):
        return int(round(val_mm * 10000))

    # 1. GKO: Board Outline
    gko_content = header
    gko_content += "%ADD10C,0.1500*%\n"
    gko_content += "D10*\n"
    if board_outline_pts:
        gko_content += f"X{gcoord(board_outline_pts[0][0])}Y{gcoord(board_outline_pts[0][1])}D02*\n"
        for pt in board_outline_pts[1:]:
            gko_content += f"X{gcoord(pt[0])}Y{gcoord(pt[1])}D01*\n"
    gko_content += "M02*\n"
    (out_dir / 'SmartPen.GKO').write_text(gko_content, encoding='utf-8')

    # 2. GTL: Top Copper
    gtl_content = header
    gtl_content += "%ADD10C,0.2000*%\n"
    gtl_content += "%ADD11C,0.4000*%\n"
    gtl_content += "%ADD12C,0.6000*%\n"
    gtl_content += "%ADD13R,0.6000X0.6500*%\n"
    gtl_content += "%ADD14R,0.3000X0.7000*%\n"
    gtl_content += "%ADD15R,2.7000X2.7000*%\n"
    gtl_content += "%ADD16R,3.7000X3.7000*%\n"
    # Tracks
    gtl_content += "D10*\n"
    for w, pts, net in top_tracks:
        if w >= 0.35:
            gtl_content += "D11*\n"
        else:
            gtl_content += "D10*\n"
        gtl_content += f"X{gcoord(pts[0][0])}Y{gcoord(pts[0][1])}D02*\n"
        for pt in pts[1:]:
            gtl_content += f"X{gcoord(pt[0])}Y{gcoord(pt[1])}D01*\n"
    # Vias
    gtl_content += "D12*\n"
    for vx, vy, d, h, net in vias:
        gtl_content += f"X{gcoord(vx)}Y{gcoord(vy)}D03*\n"
    # Pads
    for px, py, pw, ph, net, num in top_pads:
        if pw > 3.0:
            gtl_content += "D16*\n"
        elif pw > 2.0:
            gtl_content += "D15*\n"
        elif pw < 0.4:
            gtl_content += "D14*\n"
        else:
            gtl_content += "D13*\n"
        gtl_content += f"X{gcoord(px)}Y{gcoord(py)}D03*\n"
    gtl_content += "M02*\n"
    (out_dir / 'SmartPen.GTL').write_text(gtl_content, encoding='utf-8')

    # 3. GBL: Bottom Copper
    gbl_content = header
    gbl_content += "%ADD10C,0.2500*%\n"
    gbl_content += "%ADD12C,0.6000*%\n"
    gbl_content += "D12*\n"
    for vx, vy, d, h, net in vias:
        gbl_content += f"X{gcoord(vx)}Y{gcoord(vy)}D03*\n"
    gbl_content += "D10*\n"
    for w, pts, net in bot_tracks:
        gbl_content += f"X{gcoord(pts[0][0])}Y{gcoord(pts[0][1])}D02*\n"
        for pt in pts[1:]:
            gbl_content += f"X{gcoord(pt[0])}Y{gcoord(pt[1])}D01*\n"
    gbl_content += "M02*\n"
    (out_dir / 'SmartPen.GBL').write_text(gbl_content, encoding='utf-8')

    # 4. GTS: Top Solder Mask
    gts_content = header
    gts_content += "%ADD13R,0.7000X0.7500*%\n"
    gts_content += "%ADD14R,0.4000X0.8000*%\n"
    gts_content += "%ADD15R,2.8000X2.8000*%\n"
    gts_content += "%ADD16R,3.8000X3.8000*%\n"
    for px, py, pw, ph, net, num in top_pads:
        if pw > 3.0:
            gts_content += "D16*\n"
        elif pw > 2.0:
            gts_content += "D15*\n"
        elif pw < 0.4:
            gts_content += "D14*\n"
        else:
            gts_content += "D13*\n"
        gts_content += f"X{gcoord(px)}Y{gcoord(py)}D03*\n"
    gts_content += "M02*\n"
    (out_dir / 'SmartPen.GTS').write_text(gts_content, encoding='utf-8')

    # 5. GBS: Bottom Solder Mask
    gbs_content = header
    gbs_content += "%ADD10C,0.6500*%\n"
    gbs_content += "D10*\n"
    for vx, vy, d, h, net in vias:
        gbs_content += f"X{gcoord(vx)}Y{gcoord(vy)}D03*\n"
    gbs_content += "M02*\n"
    (out_dir / 'SmartPen.GBS').write_text(gbs_content, encoding='utf-8')

    # 6. GTO: Top Silkscreen
    gto_content = header
    gto_content += "%ADD10C,0.1200*%\n"
    gto_content += "D10*\n"
    for w, pts in silk_tracks:
        if pts:
            gto_content += f"X{gcoord(pts[0][0])}Y{gcoord(pts[0][1])}D02*\n"
            for pt in pts[1:]:
                gto_content += f"X{gcoord(pt[0])}Y{gcoord(pt[1])}D01*\n"
    gto_content += "M02*\n"
    (out_dir / 'SmartPen.GTO').write_text(gto_content, encoding='utf-8')

    # 7. GBO: Bottom Silkscreen
    gbo_content = header + "M02*\n"
    (out_dir / 'SmartPen.GBO').write_text(gbo_content, encoding='utf-8')

    # 8. DRL: Excellon NC Drill File
    drl_content = (
        "M48\n"
        "METRIC,TZ\n"
        "FMAT,2\n"
        "T1C0.300\n"
        "%\n"
        "G90\n"
        "G05\n"
        "T1\n"
    )
    for vx, vy, d, h, net in vias:
        # Excellon metric format: 3.3 (1.0 mm -> 1000)
        drl_content += f"X{int(round(vx*1000))}Y{int(round(vy*1000))}\n"
    drl_content += "M30\n"
    (out_dir / 'SmartPen.DRL').write_text(drl_content, encoding='utf-8')

    # Create ZIP archive
    zip_path = Path('output/RevE_work/SmartPen_RevE_Gerbers.zip')
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for ext in ['GTL', 'GBL', 'GTS', 'GBS', 'GTO', 'GBO', 'GKO', 'DRL']:
            fpath = out_dir / f'SmartPen.{ext}'
            z.write(fpath, arcname=f'SmartPen.{ext}')

    print(f"Generated Gerbers and Excellon drill in {out_dir}")
    print(f"Created Gerber package {zip_path} ({zip_path.stat().st_size} bytes)")

if __name__ == '__main__':
    generate_gerbers()

