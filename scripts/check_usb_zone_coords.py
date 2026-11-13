import json

with open('output/RevF_Working/solved_coords.json') as f:
    coords = json.load(f)

print("Existing coordinates near X >= 60:")
for k, v in sorted(coords.items(), key=lambda item: item[1][0]):
    if v[0] >= 60:
        print(f"  {k:8s}: ({v[0]:6.2f}, {v[1]:6.2f})")

