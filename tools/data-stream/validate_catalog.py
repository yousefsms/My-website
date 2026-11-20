import json
from collections import defaultdict

with open('media/figures/dm04/catalog.json', 'r') as f:
    catalog = json.load(f)

# Check total count
print(f"Total entries: {len(catalog)}")

# Group by (nozzle, npr)
groups = defaultdict(list)
for entry in catalog:
    groups[(entry['nozzle'], entry['npr'])].append(entry)

print(f"Number of (nozzle, npr) groups: {len(groups)}")

valid_groups = 0
for (nozzle, npr), entries in groups.items():
    # Check if group has exactly 8 mics
    mics = sorted([int(e['mic']) for e in entries])
    if mics == list(range(1, 9)):
        # Check if phi_deg are unique within the group
        phis = [e['phi_deg'] for e in entries]
        if len(set(phis)) == 8:
            valid_groups += 1
        else:
            print(f"Duplicate phis in group {nozzle}, {npr}: {phis}")
    else:
        print(f"Invalid mic set in group {nozzle}, {npr}: {mics}")

print(f"Valid groups (8 mics 1-8, unique phis): {valid_groups}")
