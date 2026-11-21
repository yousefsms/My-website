import sys

with open('/Users/yoyo/01_Code/My-website/DataStream.html', 'r') as f:
    content = f.read()

# 1. Replace CSS
css_old = """
        /* Constrain the heated jet figure as it is too large */
        .analysis-figures-container figure.blog-image:first-child {
            max-width: 800px;
        }"""
css_new = """
        .analysis-media-wide {
            width: 100%;
            margin: 0 auto;
        }

        .analysis-media-compact {
            max-width: 600px !important;
            width: 100%;
            height: auto;
            margin: 0 auto;
            display: block;
            text-align: center;
        }"""
content = content.replace(css_old, css_new)

# 2. Replace the target section
# We target from <section class="blog-detail pt-100 pb-100"> (the last one) 
# to </footer>
# Since there are multiple blog-detail sections, we need to be precise.
# The one we want starts with <div class="blog-heading mt-50" style="border-top: 1px solid #eee; padding-top: 30px;">

start_marker = '<section class="blog-detail pt-100 pb-100">\n    <div class="container"><div class="row"><div class="col-lg-8 offset-lg-2">\n                        <div class="blog-content">\n                            <div class="blog-heading mt-50" style="border-top: 1px solid #eee; padding-top: 30px;">'
end_marker = '</div></section>\n\n        <!--Footer Start-->'

# Because the HTML formatting might be slightly different (indentation), 
# I'll use a more robust search for the start of that section.
# I'll look for the "Additional 2D Analyses" heading.

import re
pattern = r'<section class="blog-detail pt-100 pb-100">\s*<div class="container"><div class="row"><div class="col-lg-8 offset-lg-2">\s*<div class="blog-content">\s*<div class="blog-heading mt-50" style="border-top: 1px solid #eee; padding-top: 30px;">\s*<h2>Additional 2D Analyses</h2>.*?<!--Footer Start-->'
# This is too broad. Let's just replace the specific section content.

# Let's find the start of the section and the start of the footer.
section_start = content.find('<h2 class="blog-heading mt-50"') # Wait, it's <h2>Additional 2D Analyses</h2>
# Let's use a simpler approach: find the last section before the footer.
footer_index = content.find('<!--Footer Start-->')
# Find the start of the section that contains "Additional 2D Analyses"
search_text = 'Additional 2D Analyses'
search_index = content.find(search_text)
# The section starts before that.
section_start_index = content.rfind('<section class="blog-detail pt-100 pb-100">', 0, search_index)

# We want to replace everything from section_start_index to just before the footer_index.
# But we must make sure we don't accidentally remove other things.
# The block we want to replace ends at </div></section> just before footer.

# Let's just replace the specific block of HTML using a string replacement for the whole section.
# I will read the file and use a carefully crafted replacement.
