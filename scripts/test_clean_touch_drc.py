"""Solve Touch Sensor layout with 0 DRC violations and 0 unconnected items.
"""
import uuid
from pathlib import Path

prj_dir = Path('output/RevF_Working/Touch_Sensor')

pcb = f"""(kicad_pcb (version 20221018) (generator pcbnew) (generator_version "8.0")
  (general (thickness 0.8))
  (paper "A4")
  (title_block (title "Touch Sensor Daughterboard") (rev "Rev F.1") (company "RadixView Technologies"))
  (layers
    (0 "F.Cu" signal)
    (31 "B.Cu" signal)
    (36 "B.SilkS" user "B.Silkscreen")
    (37 "F.SilkS" user "F.Silkscreen")
    (38 "B.Mask" user)
    (39 "F.Mask" user)
    (44 "Edge.Cuts" user)
    (48 "F.Fab" user)
    (49 "B.Fab" user)
  )
  (setup
    (pad_to_mask_clearance 0.0)
    (solder_mask_min_width 0.0)
    (pad_to_paste_clearance 0)
  )
  (net 0 "")
  (net 1 "GND")
  (net 2 "3V3")
  (net 3 "TOUCH_OUT")
  (net 4 "TOUCH_IN")
  (net_class "Default" "Standard net class"
    (clearance 0.127)
    (trace_width 0.20)
    (via_dia 0.50)
    (via_drill 0.30)
  )
  (gr_line (start 0 0) (end 6.0 0) (layer "Edge.Cuts") (width 0.15))
  (gr_line (start 6.0 0) (end 6.0 18.0) (layer "Edge.Cuts") (width 0.15))
  (gr_line (start 6.0 18.0) (end 0 18.0) (layer "Edge.Cuts") (width 0.15))
  (gr_line (start 0 18.0) (end 0 0) (layer "Edge.Cuts") (width 0.15))

  (footprint "Touch:JST_SH_3P" (layer "F.Cu") (at 3.0 2.2)
    (uuid "{uuid.uuid4()}")
    (fp_text reference "J1" (at 0 -1.5) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_text value "SM03B-SRSS-TB" (at 0 2.2) (layer "F.Fab") hide (effects (font (size 0.8 0.8) (thickness 0.12))))
    (pad "1" smd rect (at -1.0 0) (size 0.6 1.2) (layers "F.Cu" "F.Paste" "F.Mask") (net 2 "3V3"))
    (pad "2" smd rect (at 0.0 0) (size 0.6 1.2) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))
    (pad "3" smd rect (at 1.0 0) (size 0.6 1.2) (layers "F.Cu" "F.Paste" "F.Mask") (net 3 "TOUCH_OUT"))
    (pad "4" smd rect (at -2.2 0) (size 0.6 1.2) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))
    (pad "4" smd rect (at 2.2 0) (size 0.6 1.2) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))
  )

  (footprint "Touch:SOT-23-6" (layer "F.Cu") (at 3.0 6.5)
    (uuid "{uuid.uuid4()}")
    (fp_text reference "U1" (at 0 0) (layer "F.SilkS") hide (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_text value "TTP223-BA6" (at 0 0) (layer "F.Fab") hide (effects (font (size 0.8 0.8) (thickness 0.12))))
    (pad "1" smd rect (at -0.95 -1.25) (size 0.55 1.0) (layers "F.Cu" "F.Paste" "F.Mask") (net 3 "TOUCH_OUT"))
    (pad "2" smd rect (at 0.0 -1.25) (size 0.55 1.0) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))
    (pad "3" smd rect (at 0.95 -1.25) (size 0.55 1.0) (layers "F.Cu" "F.Paste" "F.Mask") (net 4 "TOUCH_IN"))
    (pad "4" smd rect (at 0.95 1.25) (size 0.55 1.0) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))
    (pad "5" smd rect (at 0.0 1.25) (size 0.55 1.0) (layers "F.Cu" "F.Paste" "F.Mask") (net 2 "3V3"))
    (pad "6" smd rect (at -0.95 1.25) (size 0.55 1.0) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))
  )

  (footprint "Touch:C_0402" (layer "F.Cu") (at 1.0 7.8 90)
    (uuid "{uuid.uuid4()}")
    (fp_text reference "C1" (at 0 0) (layer "F.SilkS") hide (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_text value "0.1uF" (at 0 0) (layer "F.Fab") hide (effects (font (size 0.8 0.8) (thickness 0.12))))
    (pad "1" smd rect (at -0.48 0 90) (size 0.6 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (net 2 "3V3"))
    (pad "2" smd rect (at 0.48 0 90) (size 0.6 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))
  )

  (footprint "Touch:C_0402" (layer "F.Cu") (at 5.0 7.8 90)
    (uuid "{uuid.uuid4()}")
    (fp_text reference "C2" (at 0 0) (layer "F.SilkS") hide (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_text value "10pF" (at 0 0) (layer "F.Fab") hide (effects (font (size 0.8 0.8) (thickness 0.12))))
    (pad "1" smd rect (at -0.48 0 90) (size 0.6 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (net 4 "TOUCH_IN"))
    (pad "2" smd rect (at 0.48 0 90) (size 0.6 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))
  )

  (footprint "Touch:Touch_Pad_5x10mm" (layer "F.Cu") (at 3.0 13.5)
    (uuid "{uuid.uuid4()}")
    (fp_text reference "E1" (at 0 -4.5) (layer "F.SilkS") hide (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_text value "TOUCH_PAD" (at 0 0) (layer "F.Fab") hide (effects (font (size 0.8 0.8) (thickness 0.12))))
    (pad "1" smd rect (at 0 0) (size 4.6 7.5) (layers "F.Cu" "F.Paste" "F.Mask") (net 4 "TOUCH_IN"))
  )

  ;; --- NET 2: 3V3 ---
  ;; J1.1 is at (2.0, 2.2). Via at (2.0, 3.0).
  (segment (start 2.0 2.2) (end 2.0 3.0) (width 0.20) (layer "F.Cu") (net 2))
  (via (at 2.0 3.0) (size 0.5) (drill 0.3) (layers "F.Cu" "B.Cu") (net 2))
  (segment (start 2.0 3.0) (end 1.0 3.0) (width 0.20) (layer "B.Cu") (net 2))
  (segment (start 1.0 3.0) (end 1.0 9.0) (width 0.20) (layer "B.Cu") (net 2))
  (via (at 1.0 9.0) (size 0.5) (drill 0.3) (layers "F.Cu" "B.Cu") (net 2))
  (segment (start 1.0 9.0) (end 1.0 8.28) (width 0.20) (layer "F.Cu") (net 2))
  (segment (start 1.0 9.0) (end 3.0 9.0) (width 0.20) (layer "B.Cu") (net 2))
  (via (at 3.0 9.0) (size 0.5) (drill 0.3) (layers "F.Cu" "B.Cu") (net 2))
  (segment (start 3.0 9.0) (end 3.0 7.75) (width 0.20) (layer "F.Cu") (net 2))

  ;; --- NET 3: TOUCH_OUT ---
  ;; J1.3 is at (4.0, 2.2). Via at (4.0, 3.0).
  (segment (start 4.0 2.2) (end 4.0 3.0) (width 0.20) (layer "F.Cu") (net 3))
  (via (at 4.0 3.0) (size 0.5) (drill 0.3) (layers "F.Cu" "B.Cu") (net 3))
  (segment (start 4.0 3.0) (end 2.05 4.4) (width 0.20) (layer "B.Cu") (net 3))
  (via (at 2.05 4.4) (size 0.5) (drill 0.3) (layers "F.Cu" "B.Cu") (net 3))
  (segment (start 2.05 4.4) (end 2.05 5.25) (width 0.20) (layer "F.Cu") (net 3))

  ;; --- NET 4: TOUCH_IN ---
  ;; U1.3 is at (3.95, 5.25). C2.1 is at (5.0, 8.28). E1 is at (3.0, 9.75).
  (segment (start 3.95 5.25) (end 4.2 5.5) (width 0.20) (layer "F.Cu") (net 4))
  (via (at 4.2 5.5) (size 0.5) (drill 0.3) (layers "F.Cu" "B.Cu") (net 4))
  (segment (start 4.2 5.5) (end 5.0 5.5) (width 0.20) (layer "B.Cu") (net 4))
  (segment (start 5.0 5.5) (end 5.0 8.28) (width 0.20) (layer "B.Cu") (net 4))
  (via (at 5.0 8.28) (size 0.5) (drill 0.3) (layers "F.Cu" "B.Cu") (net 4))
  (segment (start 5.0 8.28) (end 4.2 9.0) (width 0.25) (layer "F.Cu") (net 4))
  (segment (start 4.2 9.0) (end 3.0 9.75) (width 0.25) (layer "F.Cu") (net 4))

  ;; --- NET 1: GND ---
  ;; J1.2 is at (3.0, 2.2).
  ;; Shields at (0.8, 2.2) and (5.2, 2.2).
  ;; U1.2 is at (3.0, 5.25).
  ;; U1.6 is at (2.05, 7.75).
  ;; C1.2 is at (1.0, 7.32).
  ;; U1.4 is at (3.95, 7.75).
  ;; C2.2 is at (5.0, 7.32).
  (segment (start 3.0 2.2) (end 3.0 5.25) (width 0.20) (layer "F.Cu") (net 1))
  (segment (start 0.8 2.2) (end 0.8 1.2) (width 0.20) (layer "F.Cu") (net 1))
  (segment (start 0.8 1.2) (end 3.0 1.2) (width 0.20) (layer "F.Cu") (net 1))
  (segment (start 3.0 1.2) (end 3.0 2.2) (width 0.20) (layer "F.Cu") (net 1))
  (segment (start 5.2 2.2) (end 5.2 1.2) (width 0.20) (layer "F.Cu") (net 1))
  (segment (start 5.2 1.2) (end 3.0 1.2) (width 0.20) (layer "F.Cu") (net 1))

  ;; F.Cu connections for GND on lower U1:
  (segment (start 2.05 7.75) (end 1.5 7.75) (width 0.20) (layer "F.Cu") (net 1))
  (segment (start 1.5 7.75) (end 1.0 7.32) (width 0.20) (layer "F.Cu") (net 1))

  (segment (start 3.95 7.75) (end 4.5 7.75) (width 0.20) (layer "F.Cu") (net 1))
  (segment (start 4.5 7.75) (end 5.0 7.32) (width 0.20) (layer "F.Cu") (net 1))

  ;; Connect U1.2 (3.0, 5.25) to U1.6/U1.4 via B.Cu:
  (via (at 3.0 4.6) (size 0.5) (drill 0.3) (layers "F.Cu" "B.Cu") (net 1))
  (segment (start 3.0 5.25) (end 3.0 4.6) (width 0.20) (layer "F.Cu") (net 1))
  (segment (start 3.0 4.6) (end 3.0 7.0) (width 0.20) (layer "B.Cu") (net 1))
  (segment (start 3.0 7.0) (end 2.05 7.0) (width 0.20) (layer "B.Cu") (net 1))
  (via (at 2.05 7.0) (size 0.5) (drill 0.3) (layers "F.Cu" "B.Cu") (net 1))
  (segment (start 2.05 7.0) (end 2.05 7.75) (width 0.20) (layer "F.Cu") (net 1))
  (segment (start 3.0 7.0) (end 3.95 7.0) (width 0.20) (layer "B.Cu") (net 1))
  (via (at 3.95 7.0) (size 0.5) (drill 0.3) (layers "F.Cu" "B.Cu") (net 1))
  (segment (start 3.95 7.0) (end 3.95 7.75) (width 0.20) (layer "F.Cu") (net 1))
)"""

lines = [l for l in pcb.splitlines() if not l.strip().startswith(';')]
clean_pcb = '\n'.join(lines) + '\n'

with open(prj_dir / 'Touch_Sensor.kicad_pcb', 'w', encoding='utf-8') as f:
    f.write(clean_pcb)

print("Saved cleanly routed Touch_Sensor.kicad_pcb with Pad 1 net assigned.")
