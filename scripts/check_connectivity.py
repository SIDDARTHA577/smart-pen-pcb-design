import sys
sys.path.insert(0, '.')
from scripts.solve_zero_drc import run_check
import math

pads, segs, vias, errs = run_check()

# Check connectivity for each non-GND net
non_gnd_nets = sorted(set(p['net'] for p in pads if p['net'] and p['net'] != 'GND'))

print(f"Checking connectivity for {len(non_gnd_nets)} non-GND nets:")
unconnected_nets = []

for net in non_gnd_nets:
    net_pads = [p for p in pads if p['net'] == net]
    net_segs = [s for s in segs if s[5] == net]
    net_vias = [v for v in vias if v[2] == net]

    # Build graph of points
    adj = {}
    def add_node(pt):
        if pt not in adj: adj[pt] = []

    def add_edge(pt1, pt2):
        add_node(pt1)
        add_node(pt2)
        adj[pt1].append(pt2)
        adj[pt2].append(pt1)

    # Add segments
    for s in net_segs:
        pt1 = (s[0], s[1])
        pt2 = (s[2], s[3])
        add_edge(pt1, pt2)

    # Connect pads to nearby segment endpoints / vias (within 0.05 mm or inside pad rectangle)
    pad_nodes = []
    for p in net_pads:
        px, py, pw, ph = p['x'], p['y'], p['w'], p['h']
        matched_node = None
        # Check if any segment endpoint or via is within the pad
        for node in adj:
            if abs(node[0] - px) <= pw/2 + 0.05 and abs(node[1] - py) <= ph/2 + 0.05:
                matched_node = node
                break
        pad_nodes.append((p, matched_node))

    # Check connected components of pad_nodes
    # Find which components are connected
    unmatched = [p for p, m in pad_nodes if m is None]
    if unmatched:
        print(f"  * {net}: {len(unmatched)}/{len(net_pads)} pads not connected to any segment!")
        for u in unmatched:
            print(f"      unmatched pad: {u['ref']}.{u['pin']} at ({u['x']}, {u['y']})")
        unconnected_nets.append(net)
        continue

    # BFS from first pad node
    visited = set()
    start_node = pad_nodes[0][1]
    queue = [start_node]
    visited.add(start_node)
    while queue:
        curr = queue.pop(0)
        for neighbor in adj.get(curr, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    # Check if all pad nodes are visited
    missing = [p for p, m in pad_nodes if m not in visited]
    if missing:
        print(f"  * {net}: disconnected components! {len(missing)} pads unreachable from first pad.")
        for m in missing:
            print(f"      unreachable pad: {m['ref']}.{m['pin']} at ({m['x']}, {m['y']})")
        unconnected_nets.append(net)
    else:
        # All pads connected
        pass

if not unconnected_nets:
    print("\nALL 41 NON-GND NETS ARE 100% FULLY CONNECTED!")
else:
    print(f"\n{len(unconnected_nets)} nets need connection adjustments.")
