import json
import math

def compute_uj(npr, gamma=1.4, R=287, T0=295):
    term1 = (2 * gamma * R * T0) / (gamma - 1)
    term2 = 1 - math.pow(float(npr), -(gamma - 1) / gamma)
    return round(math.sqrt(term1 * term2), 2)

files = [
    'media/figures/dm02/catalog.json',
    'media/figures/dm03/catalog.json',
    'media/figures/dm04/catalog.json'
]

for file_path in files:
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    for item in data:
        npr_val = item.get('npr')
        if npr_val is not None:
            item['uj_m_s'] = compute_uj(npr_val)
            item['uj_source'] = 'calculated_nominal_npr'
            item['uj_T0_K'] = 295
            item['deq_mm'] = 29
            item['deq_approx'] = True
    
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Updated {file_path}")
