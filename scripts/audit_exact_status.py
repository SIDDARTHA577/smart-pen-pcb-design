import json
with open("drc_current.json") as f:
    d = json.load(f)

unconn_by_net = {}
for u in d.get('unconnected_items', []):
    desc = u.get('description', '')
    # extract net name in brackets
    items = u.get('items', [])
    for it in items:
        idesc = it.get('description', '')
        if '[' in idesc and ']' in idesc:
            net = idesc.split('[')[1].split(']')[0]
            unconn_by_net[net] = unconn_by_net.get(net, 0) + 1

print(f"Total violations: {len(d.get('violations', []))}")
print(f"Total unconnected items: {len(d.get('unconnected_items', []))}")
print("\nUnconnected by net:")
for net, count in sorted(unconn_by_net.items(), key=lambda x: -x[1]):
    print(f"  {net:20s}: {count} references")
