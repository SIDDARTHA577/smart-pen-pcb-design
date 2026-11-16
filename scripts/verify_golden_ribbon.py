import sys
sys.path.append('scripts')
import pcbnew
from strict_clearance_checker import BoardGeometry

b = pcbnew.LoadBoard('scratch_test_vip.kicad_pcb')
# Delete freestanding GND via at (55.00, 1.20)
for t in list(b.GetTracks()):
    if t.GetClass() == 'PCB_VIA' and round(t.GetPosition().x/1e6, 2) == 55.00 and round(t.GetPosition().y/1e6, 2) == 1.20:
        b.Delete(t)

geom = BoardGeometry(b)

print("Checking the Golden 4-Track Ribbon on In2.Cu from X=43.0 to 57.0:")
nets = [('/SD_CS', 1.150), ('/SD_SCK', 1.450), ('/SD_MOSI', 1.750), ('/SD_MISO', 2.050)]
for net, y in nets:
    s, r = geom.is_segment_legal(43.000, y, 57.000, y, 'In2.Cu', net)
    print(f"Track {net} at Y={y:.3f}: {s} ({r})")
