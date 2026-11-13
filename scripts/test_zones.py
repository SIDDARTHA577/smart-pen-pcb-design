import uuid

with open('output/RevF_Working/test_solved_bare.kicad_pcb', 'r') as f:
    text = f.read()

u1 = uuid.uuid4()
u2 = uuid.uuid4()

zones = f'''  (zone (net 1) (net_name "GND") (layers "F.Cu") (tstamp "{u1}")
    (hatch full 0.5)
    (priority 0)
    (connect_pads (clearance 0.15))
    (min_thickness 0.15)
    (filled_areas_thickness no)
    (fill yes (thermal_gap 0.18) (thermal_bridge_width 0.20))
    (polygon
      (pts
        (xy 0.25 0.25)
        (xy 83.75 0.25)
        (xy 83.75 8.95)
        (xy 0.25 8.95)
      )
    )
  )
  (zone (net 1) (net_name "GND") (layers "B.Cu") (tstamp "{u2}")
    (hatch full 0.5)
    (priority 0)
    (connect_pads (clearance 0.15))
    (min_thickness 0.15)
    (filled_areas_thickness no)
    (fill yes (thermal_gap 0.18) (thermal_bridge_width 0.20))
    (polygon
      (pts
        (xy 0.25 0.25)
        (xy 83.75 0.25)
        (xy 83.75 8.95)
        (xy 0.25 8.95)
      )
    )
  )
)'''

new_text = text[:-2] + '\n' + zones
with open('output/RevF_Working/test_solved_zones.kicad_pcb', 'w') as f:
    f.write(new_text)

print("Created test_solved_zones.kicad_pcb")

