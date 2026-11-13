import re

with open('output/RevF_Working/SmartPen.kicad_pcb', 'r', encoding='utf-8') as f:
    pcb = f.read()

# Replace all (net X "NAME") where NAME does not start with / and is not empty
def repl_net_def(m):
    nid = m.group(1)
    name = m.group(2)
    if name == "" or name.startswith("/"):
        return m.group(0)
    return f'(net {nid} "/{name}")'

pcb_patched = re.sub(r'\(net\s+(\d+)\s+"([^"]*)"\)', repl_net_def, pcb)

# Also in pads: (net X "NAME")
# Also in zones: (net_name "NAME") -> (net_name "/NAME")
def repl_zone_net(m):
    name = m.group(1)
    if name == "" or name.startswith("/"):
        return m.group(0)
    return f'(net_name "/{name}")'

pcb_patched = re.sub(r'\(net_name\s+"([^"]*)"\)', repl_zone_net, pcb_patched)

with open('output/RevF_Working/SmartPen_test_parity.kicad_pcb', 'w', encoding='utf-8') as f:
    f.write(pcb_patched)

print("Saved SmartPen_test_parity.kicad_pcb")
