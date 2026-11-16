import sys
sys.path.append('scripts')
import pcbnew
from strict_clearance_checker import BoardGeometry

b = pcbnew.LoadBoard('scratch_test_vip.kicad_pcb')
r27 = b.FindFootprintByReference('R27')
r27.SetPosition(pcbnew.VECTOR2I(int(44.0*1e6), int(1.0*1e6)))

# Remove old tracks
for t in list(b.GetTracks()):
    if t.GetNetname() == '/GPIO8_STRAP':
        b.Delete(t)
    elif t.GetNetname() == '/3V3' and (round(t.GetPosition().x/1e6, 1) == 42.0 or (t.GetClass() != 'PCB_VIA' and round(t.GetStart().x/1e6, 1) == 42.0)):
        b.Delete(t)

# Add 3V3 via for R27.1 at (43.525, 0.500)
net_3v3 = b.FindNet('/3V3')
v_3v3 = pcbnew.PCB_VIA(b)
v_3v3.SetPosition(pcbnew.VECTOR2I(int(43.525*1e6), int(0.500*1e6)))
v_3v3.SetWidth(int(0.5*1e6))
v_3v3.SetDrill(int(0.3*1e6))
v_3v3.SetTopLayer(b.GetLayerID('F.Cu'))
v_3v3.SetBottomLayer(b.GetLayerID('B.Cu'))
v_3v3.SetNet(net_3v3)
b.Add(v_3v3)

t_3v3 = pcbnew.PCB_TRACK(b)
t_3v3.SetStart(pcbnew.VECTOR2I(int(43.525*1e6), int(1.000*1e6)))
t_3v3.SetEnd(pcbnew.VECTOR2I(int(43.525*1e6), int(0.500*1e6)))
t_3v3.SetWidth(int(0.15*1e6))
t_3v3.SetLayer(b.GetLayerID('F.Cu'))
t_3v3.SetNet(net_3v3)
b.Add(t_3v3)

# Add GPIO8_STRAP
net_strap = b.FindNet('/GPIO8_STRAP')
def add_trk(layer, sx, sy, ex, ey, net):
    t = pcbnew.PCB_TRACK(b)
    t.SetStart(pcbnew.VECTOR2I(int(sx*1e6), int(sy*1e6)))
    t.SetEnd(pcbnew.VECTOR2I(int(ex*1e6), int(ey*1e6)))
    t.SetWidth(int(0.15*1e6))
    t.SetLayer(b.GetLayerID(layer))
    t.SetNet(net)
    b.Add(t)

add_trk('F.Cu', 43.630, 2.435, 43.630, 1.400, net_strap)
add_trk('F.Cu', 43.630, 1.400, 44.475, 1.400, net_strap)
add_trk('F.Cu', 44.475, 1.400, 44.475, 1.000, net_strap)

geom = BoardGeometry(b)
print("1. R27.1 3V3 via:", geom.is_via_legal(43.525, 0.500, '/3V3'))
print("2. GPIO8_STRAP s1:", geom.is_segment_legal(43.630, 2.435, 43.630, 1.400, 'F.Cu', '/GPIO8_STRAP'))
print("   GPIO8_STRAP s2:", geom.is_segment_legal(43.630, 1.400, 44.475, 1.400, 'F.Cu', '/GPIO8_STRAP'))
print("   GPIO8_STRAP s3:", geom.is_segment_legal(44.475, 1.400, 44.475, 1.000, 'F.Cu', '/GPIO8_STRAP'))

print("3. SD_CS s1:", geom.is_segment_legal(43.130, 2.435, 43.130, 1.750, 'F.Cu', '/SD_CS'))
print("   SD_CS via:", geom.is_via_legal(43.130, 1.750, '/SD_CS'))

print("4. SD_SCK s1:", geom.is_segment_legal(42.630, 2.435, 42.630, 0.500, 'F.Cu', '/SD_SCK'))
print("   SD_SCK via:", geom.is_via_legal(42.630, 0.500, '/SD_SCK'))

print("5. SD_MISO s1:", geom.is_segment_legal(41.630, 2.435, 41.400, 1.600, 'F.Cu', '/SD_MISO'))
print("   SD_MISO via:", geom.is_via_legal(41.400, 1.600, '/SD_MISO'))

print("6. SD_MOSI s1:", geom.is_segment_legal(41.130, 2.435, 39.680, 2.435, 'F.Cu', '/SD_MOSI'))
print("   SD_MOSI via:", geom.is_via_legal(39.680, 2.435, '/SD_MOSI'))
