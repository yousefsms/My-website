import re

with open('DataStream.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Restore id="dm04-container"
html = html.replace('<div class="dm04-explorer">', '<div class="dm04-explorer" id="dm04-container">')

# 2. Clean up remaining Bootstrap col-lg-8 offset-lg-2 in the last section
# Looking for <div class="col-lg-8 offset-lg-2"> and replacing it with <div>
# and its corresponding closing </div>.
# In the last section, it looks like:
# <div class="col-lg-8 offset-lg-2">
#     <figure class="blog-image"> ... </figure>
#     <figure class="blog-image"> ... </figure>
# </div>

html = html.replace('<div class="col-lg-8 offset-lg-2">', '<div>')

with open('DataStream.html', 'w', encoding='utf-8') as f:
    f.write(html)
