import json
import h5py
import numpy as np
import os
import base64
import struct

# Paths
CONFIG_PATH = '/Users/yoyo/03_Dissertation_Work/figure_recreation/scripts/cases_config.json'
HTML_DIR = '/Users/yoyo/Library/CloudStorage/GoogleDrive-koukousaleh@gmail.com/My Drive/Website/Kalvin - Portfolio Template/html/My-website/media/figures/dm04'

def decode_plotly_bdata(bdata_str):
    """Decodes Plotly's base64 encoded binary data (float64)."""
    try:
        binary_data = base64.b64decode(bdata_str)
        # Plotly bdata for 'f8' is typically a sequence of IEEE 754 double precision floats
        # Use numpy to interpret the bytes
        return np.frombuffer(binary_data, dtype='<f8')
    except Exception as e:
        print(f"Error decoding bdata: {e}")
        return None

def extract_plotly_z_from_bdata(html_path):
    """Extracts Z data from Plotly HTML using bdata decoding."""
    with open(html_path, 'r') as f:
        content = f.read()
    
    # Look for "z":{"dtype":"f8","bdata":"..."}
    # This is a bit fragile but follows the pattern seen in the file
    import re
    match = re.search(r'"z":\s*\{"dtype":"f8","bdata":"([^"]+)"\}', content)
    if not match:
        return None
    
    bdata_str = match.group(1)
    return decode_plotly_bdata(bdata_str)

def main():
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
    
    # Select 6 representative cases
    test_cases = [
        {"nozzle": "diamond", "npr": 4.3, "mic": 1},
        {"nozzle": "diamond", "npr": 15, "mic": 8},
        {"nozzle": "rectangular", "npr": 4.3, "mic": 2},
        {"nozzle": "rectangular", "npr": 12.5, "mic": 5},
        {"nozzle": "elliptic", "npr": 5.2, "mic": 3},
        {"nozzle": "elliptic", "npr": 15, "mic": 9},
    ]
    
    results = []
    for tc in test_cases:
        source_path = next((c['source_path'] for c in config if c['nozzle'] == tc['nozzle'] and c['npr'] == tc['npr']), None)
        if not source_path:
            continue
            
        npr_filename = str(tc['npr']).replace('.', 'p')
        html_filename = f"dm_04_{tc['nozzle']}_NPR{npr_filename}_mic{tc['mic']:02d}.html"
        html_path = os.path.join(HTML_DIR, html_filename)
        
        if not os.path.exists(html_path):
            continue
            
        z_html = extract_plotly_z_from_bdata(html_path)
        if z_html is None:
            print(f"Failed to extract Z from {html_filename}")
            continue
        
        try:
            with h5py.File(source_path, 'r') as f:
                pxx_full = f['Pxx'][()]
                if pxx_full.ndim == 3:
                    pxx_source = pxx_full[tc['mic']-1, :, :]
                else:
                    pxx_source = pxx_full
        except Exception as e:
            print(f"Error reading HDF5: {e}")
            continue
            
        # Since z_html is now a flattened array (bdata), we should compare with flattened pxx_source
        z_html_flat = np.nan_to_num(z_html)
        pxx_source_flat = np.nan_to_num(pxx_source).flatten()
        
        # Check if sizes match or if one is a subset
        min_len = min(len(z_html_flat), len(pxx_source_flat))
        correlation = np.corrcoef(z_html_flat[:min_len], pxx_source_flat[:min_len])[0, 1]
        
        results.append({
            "case": f"{tc['nozzle']} {tc['npr']}",
            "mic": tc['mic'],
            "correlation": correlation,
            "status": "PASS" if correlation > 0.999 else "FAIL"
        })

    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
