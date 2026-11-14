import sys
import pcbnew

def sync_board(pcb_path, out_path=None):
    if out_path is None:
        out_path = pcb_path
    board = pcbnew.LoadBoard(pcb_path)
    print(f"Loaded board '{pcb_path}', initial footprints: {len(board.GetFootprints())}")

    # Helper to get or create net
    def get_or_create_net(name):
        if not name:
            return None
        net = board.FindNet(name)
        if net is None:
            net = pcbnew.NETINFO_ITEM(board, name)
            board.Add(net)
            net = board.FindNet(name)
        return net

    # Pre-create all required nets
    net_3v3 = get_or_create_net('/3V3')
    net_gnd = get_or_create_net('/GND')
    net_vbat = get_or_create_net('/VBAT')
    net_vbat_sw = get_or_create_net('/VBAT_SW')
    net_vbus = get_or_create_net('/USB_VBUS')
    net_vsys_raw = get_or_create_net('/VSYS_RAW')
    net_gpio8 = get_or_create_net('/GPIO8_STRAP')
    net_cc1 = get_or_create_net('/USB_CC1')
    net_cc2 = get_or_create_net('/USB_CC2')
    net_dm_port = get_or_create_net('/USB_DM_PORT')
    net_dp_port = get_or_create_net('/USB_DP_PORT')

    def set_pad_net(pad, net):
        if net is None:
            # Net 0
            net0 = board.FindNet(0)
            if net0:
                pad.SetNet(net0)
        else:
            pad.SetNet(net)

    # 1. Update U4 (formerly J_PWR)
    fp_pwr = board.FindFootprintByReference('J_PWR')
    if fp_pwr:
        fp_pwr.SetReference('U4')
        fp_pwr.SetValue('AP2112K-3.3TRG1')
        fp_pwr.SetFPID(pcbnew.LIB_ID('SmartPen', 'J_PWR'))
        fp_pwr.SetPath(pcbnew.KIID_PATH('/0f9de0f5-e8c4-4282-a8a4-9acd96cf456d'))
        for pad in fp_pwr.Pads():
            num = pad.GetNumber()
            if num == '1': set_pad_net(pad, net_vbat_sw)
            elif num == '2': set_pad_net(pad, net_gnd)
            elif num == '3': set_pad_net(pad, net_vbat_sw)
            elif num == '4': set_pad_net(pad, None)
            elif num == '5': set_pad_net(pad, net_3v3)
        print("Updated U4 (AP2112K)")

    # 2. Add Q2 (DMG2305UX)
    fp_q2_existing = board.FindFootprintByReference('Q2')
    if fp_q2_existing:
        board.Remove(fp_q2_existing)
    fp_q2 = pcbnew.FootprintLoad('output/RevG/SmartPen.pretty', 'Q1')
    fp_q2.SetReference('Q2')
    fp_q2.SetValue('DMG2305UX')
    fp_q2.SetFPID(pcbnew.LIB_ID('SmartPen', 'Q1'))
    fp_q2.SetPosition(pcbnew.VECTOR2I(int(64.50 * 1e6), int(4.30 * 1e6)))
    fp_q2.SetPath(pcbnew.KIID_PATH('/11223344-5566-4778-8899-aabbccddeeff'))
    for pad in fp_q2.Pads():
        num = pad.GetNumber()
        if num == '1': set_pad_net(pad, net_vbus)
        elif num == '2': set_pad_net(pad, net_vsys_raw)
        elif num == '3': set_pad_net(pad, net_vbat)
    board.Add(fp_q2)
    print("Added Q2 (DMG2305UX)")

    # 3. Add D4 (1N5819HW-7-F)
    fp_d4_existing = board.FindFootprintByReference('D4')
    if fp_d4_existing:
        board.Remove(fp_d4_existing)
    fp_d4 = pcbnew.FootprintLoad('output/RevG/SmartPen.pretty', 'D3')
    fp_d4.SetReference('D4')
    fp_d4.SetValue('1N5819HW-7-F')
    fp_d4.SetFPID(pcbnew.LIB_ID('SmartPen', 'D3'))
    fp_d4.SetPosition(pcbnew.VECTOR2I(int(66.50 * 1e6), int(5.60 * 1e6)))
    fp_d4.SetPath(pcbnew.KIID_PATH('/bbccddee-ff00-4112-2233-445566778899'))
    for pad in fp_d4.Pads():
        num = pad.GetNumber()
        if num == '1': set_pad_net(pad, net_vsys_raw)
        elif num == '2': set_pad_net(pad, net_vbus)
    board.Add(fp_d4)
    print("Added D4 (1N5819HW-7-F)")

    # 4. Add R26 (RC0402FR-07100KL)
    fp_r26_existing = board.FindFootprintByReference('R26')
    if fp_r26_existing:
        board.Remove(fp_r26_existing)
    fp_r26 = pcbnew.FootprintLoad('output/RevG/SmartPen.pretty', 'R1')
    fp_r26.SetReference('R26')
    fp_r26.SetValue('RC0402FR-07100KL')
    fp_r26.SetFPID(pcbnew.LIB_ID('SmartPen', 'R1'))
    fp_r26.SetPosition(pcbnew.VECTOR2I(int(64.50 * 1e6), int(2.80 * 1e6)))
    fp_r26.SetPath(pcbnew.KIID_PATH('/22334455-6677-4889-99aa-bbccddeeff01'))
    for pad in fp_r26.Pads():
        num = pad.GetNumber()
        if num == '1': set_pad_net(pad, net_vbus)
        elif num == '2': set_pad_net(pad, net_gnd)
    board.Add(fp_r26)
    print("Added R26 (RC0402FR-07100KL)")

    # 5. Add R27 (RC0402FR-0710KL)
    fp_r27_existing = board.FindFootprintByReference('R27')
    if fp_r27_existing:
        board.Remove(fp_r27_existing)
    fp_r27 = pcbnew.FootprintLoad('output/RevG/SmartPen.pretty', 'R27')
    fp_r27.SetReference('R27')
    fp_r27.SetValue('RC0402FR-0710KL')
    fp_r27.SetFPID(pcbnew.LIB_ID('SmartPen', 'R27'))
    fp_r27.SetPosition(pcbnew.VECTOR2I(int(44.80 * 1e6), int(1.50 * 1e6)))
    fp_r27.SetPath(pcbnew.KIID_PATH('/33445566-7788-4990-aabb-ccddeeff0112'))
    for pad in fp_r27.Pads():
        num = pad.GetNumber()
        if num == '1': set_pad_net(pad, net_3v3)
        elif num == '2': set_pad_net(pad, net_gpio8)
    board.Add(fp_r27)
    print("Added R27 (RC0402FR-0710KL)")

    # 6. Rebuild J_USB footprint from SmartPen.pretty
    fp_usb_old = board.FindFootprintByReference('J_USB')
    usb_pos = fp_usb_old.GetPosition() if fp_usb_old else pcbnew.VECTOR2I(int(78.40 * 1e6), int(4.60 * 1e6))
    if fp_usb_old:
        board.Remove(fp_usb_old)
    fp_usb = pcbnew.FootprintLoad('output/RevG/SmartPen.pretty', 'J_USB')
    fp_usb.SetReference('J_USB')
    fp_usb.SetValue('TYPE-C-31-M-12')
    fp_usb.SetFPID(pcbnew.LIB_ID('SmartPen', 'J_USB'))
    fp_usb.SetPosition(usb_pos)
    fp_usb.SetPath(pcbnew.KIID_PATH('/be1de1d9-5f04-41c4-a4d9-a2f87eb6a924'))
    for pad in fp_usb.Pads():
        num = pad.GetNumber()
        if num in ['1', '12', '13', '14', '15', '16']: set_pad_net(pad, net_gnd)
        elif num in ['2', '11']: set_pad_net(pad, net_vbus)
        elif num == '4': set_pad_net(pad, net_cc1)
        elif num in ['5', '7']: set_pad_net(pad, net_dm_port)
        elif num in ['6', '8']: set_pad_net(pad, net_dp_port)
        elif num == '9': set_pad_net(pad, net_cc2)
        else: set_pad_net(pad, None)
    board.Add(fp_usb)
    print("Rebuilt J_USB (TYPE-C-31-M-12)")

    # 7. Update SW3
    fp_sw3 = board.FindFootprintByReference('SW3')
    if fp_sw3:
        fp_sw3.SetPath(pcbnew.KIID_PATH('/3c5ca43d-822f-4990-9eaf-aed6ab014eb5'))
        for pad in fp_sw3.Pads():
            num = pad.GetNumber()
            if num == '1': set_pad_net(pad, net_vsys_raw)
            elif num == '2': set_pad_net(pad, net_vbat_sw)
            elif num == '3': set_pad_net(pad, None)
        print("Updated SW3 (net_vsys_raw)")

    # 8. Update R9
    fp_r9 = board.FindFootprintByReference('R9')
    if fp_r9:
        fp_r9.SetValue('RC0402FR-0710KL')
        fp_r9.SetPath(pcbnew.KIID_PATH('/9037a657-97bd-4d44-87da-92a3e4007ba9'))
        print("Updated R9 value to RC0402FR-0710KL")

    # 9. Update U1 (ESP32-C3FH4X)
    fp_u1 = board.FindFootprintByReference('U1')
    if fp_u1:
        fp_u1.SetPath(pcbnew.KIID_PATH('/142de3ff-3fd7-4263-b422-60ebe0c56118'))
        for pad in fp_u1.Pads():
            num = pad.GetNumber()
            if num == '14': set_pad_net(pad, net_gpio8)
            elif num in ['16', '19', '20', '21', '22', '23', '24']: set_pad_net(pad, None)
        print("Updated U1 (GPIO8 & NC pins)")

    # 10. Update mechanical pads on J_BAT, J_MOT, J_RF, U3
    for ref, pad_nums in [('J_BAT', ['3', '4']), ('J_MOT', ['3', '4']), ('J_RF', ['3']), ('U3', ['21'])]:
        fp = board.FindFootprintByReference(ref)
        if fp:
            for pad in fp.Pads():
                if pad.GetNumber() in pad_nums:
                    set_pad_net(pad, None)
    print("Cleaned mechanical tab nets on J_BAT, J_MOT, J_RF, U3")

    # Build connectivity and save
    board.BuildConnectivity()
    pcbnew.SaveBoard(out_path, board)
    print(f"Successfully saved synchronized board to '{out_path}'. Total footprints: {len(board.GetFootprints())}")

if __name__ == '__main__':
    sync_board('output/RevG/SmartPen.kicad_pcb', 'output/RevG/SmartPen.kicad_pcb')

