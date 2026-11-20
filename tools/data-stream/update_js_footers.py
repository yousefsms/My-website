import os

files = ['js/dm02-explorer.js', 'js/dm04-spectra.js']
old_text = 'U<sub>j</sub> = fully expanded jet velocity [m/s], D<sub>eq</sub> = equivalent nozzle-exit diameter (diameter of a circle with same exit area) [m]'
new_text = 'U<sub>j</sub> = calculated from selected nominal NPR using MATLAB cold jet model [m/s], D<sub>eq</sub> ≈ 29mm (approximate equivalent diameter)'

for file_path in files:
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        
        if old_text in content:
            updated_content = content.replace(old_text, new_text)
            with open(file_path, 'w') as f:
                f.write(updated_content)
            print(f"Updated {file_path}")
        else:
            print(f"Old text not found in {file_path}")
