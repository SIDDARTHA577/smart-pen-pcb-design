import subprocess, os, re

# Let's use kicad-cli sch export netlist or inspect the schematic directly
kicad_cli = r'C:\Users\goran\AppData\Local\Programs\KiCad\10.0\bin\kicad-cli.exe'
res = subprocess.run([kicad_cli, 'sch', 'export', 'netlist', '-o', 'reports/RevF/SmartPen.net', 'output/RevF_Working/SmartPen.kicad_sch'], capture_output=True, text=True)
print("Netlist export result:", res.returncode)

if os.path.exists('reports/RevF/SmartPen.net'):
    with open('reports/RevF/SmartPen.net', 'r', encoding='utf-8') as f:
        netlist = f.read()
    # parse nets
    nets = re.findall(r'\(net\s+\(code\s+"?\d+"?\)\s+\(name\s+"([^"]+)"\)(.*?)\n\s*\)', netlist, re.DOTALL)
    print(f"Total nets in netlist: {len(nets)}")
    for name, nodes_str in sorted(nets, key=lambda x: x[0]):
        nodes = re.findall(r'\(node\s+\(ref\s+"([^"]+)"\)\s+\(pin\s+"([^"]+)"\)', nodes_str)
        node_list = [f"{ref}.{pin}" for ref, pin in nodes]
        print(f"Net {name:<20} ({len(node_list)} pins): {', '.join(node_list)}")
