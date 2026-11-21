import re

with open('DataStream.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Replace the Bootstrap container/row/col-8 pattern
# This matches <div class="container">\n<div class="row">\n<div class="col-lg-8 offset-lg-2">
# and we want to replace it with <div class="ds-content-wrapper">
# We need to be careful about indentation and the closing tags.

# We'll use a regex to find the pattern and then manually handle closing tags for each section.
# But a simpler way: find all <section class="blog-detail ..."> and update their contents.

def update_blog_section(match):
    content = match.group(0)
    # Replace the opening structure
    content = re.sub(
        r'\s*<div class="container">\s*<div class="row">\s*<div class="col-lg-8 offset-lg-2">',
        '\n    <div class="ds-content-wrapper">',
        content
    )
    # Remove the 3 closing divs at the end of the section
    # The pattern is usually: </div>\n</div>\n</div>\n</section>
    content = re.sub(
        r'</div>\s*</div>\s*</div>\s*(?=\s*</section>)',
        '</div>',
        content
    )
    return content

html = re.sub(r'<section class="blog-detail[^>]*>.*?</section>', update_blog_section, html, flags=re.DOTALL)

# 2. Update the DM04 section
# <section class="dm04-wrapper pt-100 pb-100">
#     <div class="container">
#         <div class="dm04-explorer" id="dm04-container">
#     ...
#     </div>
#     </div>
# </section>

def update_dm04_section(match):
    content = match.group(0)
    # Replace the opening
    content = content.replace(
        '<div class="container">\n                <div class="dm04-explorer" id="dm04-container">',
        '    <div class="ds-content-wrapper">\n        <div class="dm04-explorer">'
    )
    # Replace the closing
    content = content.replace(
        '                </div>\n            </div>\n        </section>',
        '        </div>\n    </div>\n</section>'
    )
    return content

html = re.sub(r'<section class="dm04-wrapper[^>]*>.*?</section>', update_dm04_section, html, flags=re.DOTALL)

with open('DataStream.html', 'w', encoding='utf-8') as f:
    f.write(html)
