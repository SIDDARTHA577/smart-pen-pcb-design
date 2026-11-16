import pcbnew, shutil, subprocess, json, os

src_pcb = 'scratch_test_mosi_flawless.kicad_pcb'
dst_dir = 'output/RevG/variants/FourLayer_Candidate'
dst_pcb = os.path.join(dst_dir, 'SmartPen.kicad_pcb')
dst_pro = os.path.join(dst_dir, 'SmartPen.kicad_pro')
dst_prl = os.path.join(dst_dir, 'SmartPen.kicad_prl')

shutil.copyfile('scratch_test_mosi_flawless.kicad_pro', dst_pro)
shutil.copyfile('scratch_test_mosi_flawless.kicad_prl', dst_prl)

b = pcbnew.LoadBoard(src_pcb)
fcu = b.GetLayerID('F.Cu')
in1 = b.GetLayerID('In1.Cu')
in2 = b.GetLayerID('In2.Cu')
bcu = b.GetLayerID('B.Cu')

# 1. Update D4 footprint to standard SOD-123 pad size (0.800, 0.900) on board
# and set D4 position to (59.000, 4.050)
d4 = b.FindFootprintByReference('D4')
d4.SetPosition(pcbnew.VECTOR2I_MM(59.000, 4.050))
p1 = d4.FindPadByNumber('1')
p2 = d4.FindPadByNumber('2')
p1.SetSize(pcbnew.VECTOR2I_MM(0.800, 0.900))
p2.SetSize(pcbnew.VECTOR2I_MM(0.800, 0.900))

# D4.1 is at (59.000, 2.450)
# Update VSYS_RAW via on Pad 1 to (59.000, 2.450)
for t in b.GetTracks():
    if isinstance(t, pcbnew.PCB_VIA) and t.GetNetname() == '/VSYS_RAW':
        pos = t.GetPosition()
        if abs(pcbnew.ToMM(pos.x) - 59.0) < 0.05 and abs(pcbnew.ToMM(pos.y) - 2.4) < 0.05:
            t.SetPosition(pcbnew.VECTOR2I_MM(59.000, 2.450))
    elif not isinstance(t, pcbnew.PCB_VIA) and t.GetNetname() == '/VSYS_RAW':
        p1_t, p2_t = t.GetStart(), t.GetEnd()
        x1, y1 = pcbnew.ToMM(p1_t.x), pcbnew.ToMM(p1_t.y)
        x2, y2 = pcbnew.ToMM(p2_t.x), pcbnew.ToMM(p2_t.y)
        if abs(y1 - 2.4) < 0.05 and abs(y2 - 2.4) < 0.05:
            t.SetStart(pcbnew.VECTOR2I_MM(59.500, 2.450))
            t.SetEnd(pcbnew.VECTOR2I_MM(59.000, 2.450))
        if abs(x1 - 59.5) < 0.05 and abs(x2 - 59.5) < 0.05 and abs(y2 - 2.4) < 0.05:
            t.SetEnd(pcbnew.VECTOR2I_MM(59.500, 2.450))

# Update USB_VBUS track to Pad 2 at (59.000, 5.650)
for t in b.GetTracks():
    if not isinstance(t, pcbnew.PCB_VIA) and t.GetNetname() == '/USB_VBUS' and t.GetLayer() == fcu:
        p1_t, p2_t = t.GetStart(), t.GetEnd()
        x2, y2 = pcbnew.ToMM(p2_t.x), pcbnew.ToMM(p2_t.y)
        if abs(x2 - 59.0) < 0.05 and abs(y2 - 5.6) < 0.05:
            t.SetEnd(pcbnew.VECTOR2I_MM(59.000, 5.650))

def add_tr(netname, lid, x1, y1, x2, y2, w=0.150):
    t = pcbnew.PCB_TRACK(b)
    t.SetStart(pcbnew.VECTOR2I_MM(x1, y1))
    t.SetEnd(pcbnew.VECTOR2I_MM(x2, y2))
    t.SetWidth(pcbnew.FromMM(w))
    t.SetLayer(lid)
    t.SetNet(b.FindNet(netname))
    b.Add(t)
    return t

def add_via(netname, x, y, drill=0.300, dia=0.500):
    v = pcbnew.PCB_VIA(b)
    v.SetPosition(pcbnew.VECTOR2I_MM(x, y))
    v.SetDrill(pcbnew.FromMM(drill))
    v.SetWidth(pcbnew.FromMM(dia))
    v.SetNet(b.FindNet(netname))
    v.SetViaType(pcbnew.VIATYPE_THROUGH)
    b.Add(v)
    return v

# 2. J_SD North Escape:
# Pad 5 (59.150, 4.200) -> (59.150, 5.025) -> (57.300, 5.025) -> (57.300, 5.500)
add_tr('/SD_MISO', fcu, 59.150, 4.200, 59.150, 5.025)
add_tr('/SD_MISO', fcu, 59.150, 5.025, 57.300, 5.025)
add_tr('/SD_MISO', fcu, 57.300, 5.025, 57.300, 5.500)
add_via('/SD_MISO', 57.300, 5.500)

# 3. U1 South Escape: Pad 10 (41.630, 2.435) -> (41.630, 1.200)
add_tr('/SD_MISO', fcu, 41.630, 2.435, 41.630, 1.200)
add_via('/SD_MISO', 41.630, 1.200)

# 4. In1.Cu transit path for /SD_MISO:
pts = [
  (41.630, 1.200),
  (41.400, 1.200),
  (41.350, 1.150),
  (40.900, 1.150),
  (40.700, 1.350),
  (40.700, 1.400),
  (40.650, 1.450),
  (40.650, 1.550),
  (40.600, 1.600),
  (40.600, 1.700),
  (40.650, 1.750),
  (40.650, 1.850),
  (40.700, 1.900),
  (40.700, 1.950),
  (41.150, 2.400),
  (41.150, 2.450),
  (41.300, 2.600),
  (41.350, 2.600),
  (41.400, 2.650),
  (44.550, 2.650),
  (45.950, 4.050),
  (46.000, 4.050),
  (46.050, 4.100),
  (54.250, 4.100),
  (54.300, 4.150),
  (54.350, 4.150),
  (54.400, 4.200),
  (54.450, 4.200),
  (54.500, 4.250),
  (54.600, 4.250),
  (54.650, 4.300),
  (54.700, 4.300),
  (54.750, 4.350),
  (54.800, 4.350),
  (54.850, 4.400),
  (54.900, 4.400),
  (54.950, 4.450),
  (55.000, 4.450),
  (55.050, 4.500),
  (55.150, 4.500),
  (55.200, 4.550),
  (55.250, 4.550),
  (55.300, 4.600),
  (55.350, 4.600),
  (55.400, 4.650),
  (55.450, 4.650),
  (55.500, 4.700),
  (55.550, 4.700),
  (55.600, 4.750),
  (55.700, 4.750),
  (55.750, 4.800),
  (55.800, 4.800),
  (55.850, 4.850),
  (55.900, 4.850),
  (55.950, 4.900),
  (56.000, 4.900),
  (56.050, 4.950),
  (56.100, 4.950),
  (56.150, 5.000),
  (56.250, 5.000),
  (56.300, 5.050),
  (56.350, 5.050),
  (56.400, 5.100),
  (56.450, 5.100),
  (56.500, 5.150),
  (56.550, 5.150),
  (56.600, 5.200),
  (56.650, 5.200),
  (56.700, 5.250),
  (56.800, 5.250),
  (56.850, 5.300),
  (56.900, 5.300),
  (56.950, 5.350),
  (57.000, 5.350),
  (57.050, 5.400),
  (57.100, 5.400),
  (57.150, 5.450),
  (57.300, 5.500)
]

for i in range(len(pts) - 1):
    add_tr('/SD_MISO', in1, pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1])

# 5. Route /3V3_RTC on In2.Cu jogging north around MISO via:
to_del = []
for t in b.GetTracks():
    if not isinstance(t, pcbnew.PCB_VIA) and t.GetNetname() == '/3V3_RTC' and t.GetLayer() == in2:
        to_del.append(t)
for t in to_del:
    b.Delete(t)

add_tr('/3V3_RTC', in2, 42.130, 1.800, 42.130, 2.150)
add_tr('/3V3_RTC', in2, 42.130, 2.150, 40.500, 2.150)
add_tr('/3V3_RTC', in2, 40.500, 2.150, 40.500, 1.100)
add_tr('/3V3_RTC', in2, 40.500, 1.100, 36.000, 1.100)
add_tr('/3V3_RTC', in2, 36.000, 1.100, 36.000, 1.600)

# 6. Bridge 3V3 on B.Cu to connect R27.1 via at (44.475, 0.500) to main 3V3 plane
add_via('/3V3', 40.500, 0.500)
add_tr('/3V3', bcu, 40.500, 0.500, 44.475, 0.500)

# 7. Bridge 3V3 on In2.Cu to merge West and East planes:
add_tr('/3V3', in2, 38.900, 4.350, 39.600, 4.350, w=0.250)

# Refill all zones
filler = pcbnew.ZONE_FILLER(b)
filler.Fill(b.Zones())

b.Save(dst_pcb)
print(f"Successfully saved {dst_pcb}!")
