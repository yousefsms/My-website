import re

path = '/Users/yoyo/Library/CloudStorage/GoogleDrive-koukousaleh@gmail.com/My Drive/Website/Kalvin - Portfolio Template/html/My-website/js/dm04-spectra.js'
with open(path, 'r') as f:
    content = f.read()

# Fix 1: closing </div> in loadSpectrum
content = content.replace('</div>', '</div>')

# Fix 2: template literal in updateFallback
# Find the line with updateFallback and replace the single quotes with backticks
content = re.sub(
    r'fallback\.innerHTML = \'<div class="text-center"><p>\${msg}</p></div>\';',
    r'fallback.innerHTML = `<div class="text-center"><p>${msg}</p></div>`;',
    content
)

with open(path, 'w') as f:
    f.write(content)
