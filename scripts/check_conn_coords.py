import pcbnew

board = pcbnew.LoadBoard('output/RevG/SmartPen.kicad_pcb')

def pad_pos(ref, pad_num):
    fp = board.FindFootprintByReference(ref)
    if not fp:
        return None
    for pad in fp.Pads():
        if pad.GetNumber() == str(pad_num):
            p = pad.GetPosition()
            return (p.x / 1e6, p.y / 1e6)
    return None

print("Key connection coordinates:")
print("Q2-1 (VBUS):", pad_pos('Q2', 1))
print("D4-2 (VBUS):", pad_pos('D4', 2))
print("R26-1 (VBUS):", pad_pos('R26', 1))
print("U2-4 (VBUS):", pad_pos('U2', 4))

print("Q2-2 (VSYS_RAW):", pad_pos('Q2', 2))
print("D4-1 (VSYS_RAW):", pad_pos('D4', 1))
print("SW3-1 (VSYS_RAW):", pad_pos('SW3', 1))

print("Q2-3 (VBAT):", pad_pos('Q2', 3))
print("J_BAT-1 (VBAT):", pad_pos('J_BAT', 1))
print("U2-3 (VBAT):", pad_pos('U2', 3))

print("SW3-2 (VBAT_SW):", pad_pos('SW3', 2))
print("U4-1 (VBAT_SW):", pad_pos('U4', 1))
print("U4-3 (VBAT_SW):", pad_pos('U4', 3))

print("U4-5 (3V3):", pad_pos('U4', 5))
print("C14-1 (3V3):", pad_pos('C14', 1))

print("R27-2 (GPIO8_STRAP):", pad_pos('R27', 2))
print("U1-14 (GPIO8_STRAP):", pad_pos('U1', 14))
print("R27-1 (3V3):", pad_pos('R27', 1))
print("U1-17 (3V3):", pad_pos('U1', 17))

print("SW2-1 (BOOT9):", pad_pos('SW2', 1))
print("U1-15 (BOOT9):", pad_pos('U1', 15))

print("J_USB-4 (CC1):", pad_pos('J_USB', 4))
print("R5-1 (CC1):", pad_pos('R5', 1))
print("J_USB-9 (CC2):", pad_pos('J_USB', 9))
print("R6-1 (CC2):", pad_pos('R6', 1))
