import json
import h5py
import os

# Paths
CONFIG_PATH = '/Users/yoyo/03_Dissertation_Work/figure_recreation/scripts/cases_config.json'
MANIFEST_PATH = '/Users/yoyo/03_Dissertation_Work/figure_recreation/figures_spectra/dm_04_manifest.json'
OUTPUT_PATH = '/Users/yoyo/Library/CloudStorage/GoogleDrive-koukousaleh@gmail.com/My Drive/Website/Kalvin - Portfolio Template/html/My-website/media/figures/dm04/catalog.json'

def main():
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
    
    with open(MANIFEST_PATH, 'r') as f:
        manifest = json.load(f)
    
    # Create a lookup for source paths based on nozzle and npr
    case_lookup = {}
    for c in config:
        # Use a key like "diamond:4.3" to match manifest
        key = f"{c['nozzle']}:{c['npr']}"
        case_lookup[key] = c['source_path']
    
    catalog = []
    
    for item in manifest['results']:
        if item['status'] != 'success':
            continue
            
        case_key = item['case']
        mic_idx = item['mic'] # 1-based
        
        source_path = case_lookup.get(case_key)
        if not source_path:
            print(f"Warning: No source path for {case_key}")
            continue
            
        try:
            with h5py.File(source_path, 'r') as f:
                theta_all = f['theta'][()].flatten()
                # theta_all should have 9 elements
                phi = float(theta_all[mic_idx - 1])
        except Exception as e:
            print(f"Error reading theta for {case_key} mic {mic_idx}: {e}")
            phi = None
            
        # Parse case_key for metadata
        nozzle, npr_str = case_key.split(':')
        
        # Determine filename
        # The files are named like dm_04_diamond_NPR4p3_mic01.html
        # We need to convert npr_str (e.g. "4.3") to "4p3"
        npr_filename = npr_str.replace('.', 'p')
        filename = f"dm_04_{nozzle}_NPR{npr_filename}_mic{mic_idx:02d}.html"
        
        catalog.append({
            "nozzle": nozzle,
            "npr": npr_str,
            "mic": mic_idx,
            "phi": phi,
            "file": f"media/figures/dm04/{filename}"
        })

    # Sort catalog by nozzle, then npr, then mic
    catalog.sort(key=lambda x: (x['nozzle'], x['npr'], x['mic']))
    
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(catalog, f, indent=4)
    
    print(f"Successfully wrote {len(catalog)} entries to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
