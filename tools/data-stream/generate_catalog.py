import json
import os
import hashlib

manifest_path = '/Users/yoyo/03_Dissertation_Work/figure_recreation/figures_spectra/dm_04_manifest.json'
target_dir = '/Users/yoyo/Library/CloudStorage/GoogleDrive-koukousaleh@gmail.com/My Drive/Website/Kalvin - Portfolio Template/html/My-website/media/figures/dm04'

with open(manifest_path, 'r') as f:
    manifest = json.load(f)

catalog = []
for item in manifest['results']:
    if item['status'] == 'success':
        case = item['case']
        mic = item['mic']
        
        # Parse nozzle and npr from case (e.g., "diamond:4.3")
        nozzle, npr = case.split(':')
        
        # Normalize nozzle name for JS (e.g., "diamond" -> "Diamond")
        nozzle_norm = nozzle.capitalize()
        
        # Normalize npr for filename (e.g., "4.3" -> "4p3")
        npr_filename = npr.replace('.', 'p')
        
        # Correct filename: dm_04_{nozzle}_NPR{npr_filename}_mic{mic}.html
        filename = f"dm_04_{nozzle}_NPR{npr_filename}_mic{mic:02d}.html"
        full_path = os.path.join(target_dir, filename)
        
        if not os.path.exists(full_path):
            print(f"Warning: File {full_path} not found")
            continue
            
        with open(full_path, 'rb') as f:
            file_bytes = os.path.getsize(full_path)
            content_hash = hashlib.sha256(f.read()).hexdigest()[:12]
            
        # Use phi_deg = 90 as per README_SPECTRA.md
        phi_deg = 90
            
        catalog.append({
            "nozzle": nozzle_norm,
            "npr": npr,
            "mic": mic,
            "phi_deg": phi_deg,
            "html": f"media/figures/dm04/{filename}?v={content_hash}",
            "file_bytes": file_bytes
        })

with open(os.path.join(target_dir, 'catalog.json'), 'w') as f:
    json.dump(catalog, f, indent=4)

print(f"Generated catalog with {len(catalog)} entries.")
