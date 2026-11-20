path = '/Users/yoyo/Library/CloudStorage/GoogleDrive-koukousaleh@gmail.com/My Drive/Website/Kalvin - Portfolio Template/html/My-website/js/dm04-spectra.js'
with open(path, 'r') as f:
    content = f.read()

content = content.replace('</div>', '</div>')

with open(path, 'w') as f:
    f.write(content)
