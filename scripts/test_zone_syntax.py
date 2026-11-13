"""Test modern KiCad 8/10 zone syntax."""
import json
import uuid
from pathlib import Path

# Load test bare PCB and replace zone with modern syntax
with open('output/RevF_Working/test_bare.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

# Add modern zone
gnd_nid = 1 # GND
zone_str = f'''  (zone (net {gnd_nid}) (net_name "GND") (layers "F.Cu") (tstamp "{uuid.uuid4()}")
    (hatch full 0.5)
    (priority 0)
    (connect_pads (clearance 0.2))
    (min_thickness 0.2)
    (filled_areas_thickness no)
    (fill yes (thermal_gap 0.25) (thermal_bridge_width 0.25))
    (polygon
      (pts
        (xy 0.35 0.35)
        (xy 83.65 0.35)
        (xy 83.65 8.85)
        (xy 0.35 8.85)
      )
    )
  )
  (zone (net {gnd_nid}) (net_name "GND") (layers "B.Cu") (tstamp "{uuid.uuid4()}")
    (hatch full 0.5)
    (priority 0)
    (connect_pads (clearance 0.2))
    (min_thickness 0.2)
    (filled_areas_thickness no)
    (fill yes (thermal_gap 0.25) (thermal_bridge_width 0.25))
    (polygon
      (pts
        (xy 0.35 0.35)
        (xy 83.65 0.35)
        (xy 83.65 8.85)
        (xy 0.35 8.85)
      )
    )
  )
)'''

new_text = text[:-2] + '\n' + zone_str

with open('output/RevF_Working/test_zone.kicad_pcb', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Created test_zone.kicad_pcb with modern zone syntax.")

