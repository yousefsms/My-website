import re

with open('DataStream.html', 'r') as f:
    content = f.read()

# 1. Remove the load button
content = content.replace('<button id="dm04-load-btn" class="btn-dm04 btn-dm04-primary" disabled>Load selected spectrum</button>', '')

# 2. Merge metadata and actions into a details panel
# Find the metadata and actions divs
# They are:
# <div class="dm04-metadata" id="dm04-metadata">...</div>
# <div class="dm04-actions">...</div>

# We'll wrap them.
# Using regex to find the block from dm04-metadata to dm04-actions
pattern = r'(<div class="dm04-metadata" id="dm04-metadata">.*?</div>\s*<div class="dm04-actions">.*?</div>)'
content = re.sub(pattern, r'<div class="dm04-details-panel">\1</div>', content, flags=re.DOTALL)

# 3. Move dm04-explorer to full width
# We find the start and end of <div class=dm04-explorer id=dm04-container> ... </div>
# And we'll wrap it in <div class="row"><div class="col-12"><div class="blog-content"> ... </div></div></div>
# But we need to be careful not to break the existing layout.

# First, let's find the dm04-explorer block
explorer_pattern = r'(<div class=dm04-explorer id=dm04-container>.*?</div>\s*</div>\s*</div>)'
# Wait, the closing divs might be tricky.
# Let's find the exactly matching <div> for dm04-explorer.

def extract_block(text, start_tag):
    start_idx = text.find(start_tag)
    if start_idx == -1:
        return None, None
    
    depth = 0
    for i in range(start_idx, len(text)):
        if text[i:i+2] == '<div': # simplified
            depth += 1
        elif text[i:i+3] == '</div>':
            depth -= 1
            if depth == 0:
                return start_idx, i + 6
    return None, None

# Let's just use a simpler approach for the layout change: 
# replace the dm04-explorer block with a wrapped version.
# The dm04-explorer is inside <div class="blog-content"> which is inside <div class="col-lg-8 offset-lg-2">.

# I'll just replace the dm04-explorer block.
# I'll search for the block that starts with <div class=dm04-explorer and ends with the matching </div>.

# Since the HTML is a bit messy (missing quotes on some classes), I'll use a more flexible search.
# Looking at the file: <div class=dm04-explorer id=dm04-container>
# It ends before <div class="blog-heading mt-50"

# Let's just use the current content and do the wrap.
# I will find the index of '<div class=dm04-explorer id=dm04-container>'
# and the index of '<div class="blog-heading mt-50"'

start_marker = '<div class=dm04-explorer id=dm04-container>'
end_marker = '<div class="blog-heading mt-50"'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    explorer_block = content[start_idx:end_idx].strip()
    # The explorer_block probably contains the closing div of dm04-explorer
    # and maybe some other closing divs.
    
    # Let's ensure we only take the explorer and not the parent.
    # We can count divs.
    
    div_count = 0
    actual_end = -1
    for i in range(len(explorer_block)):
        if explorer_block[i:i+4] == '<div':
            div_count += 1
        elif explorer_block[i:i+6] == '</div>':
            div_count -= 1
            if div_count == 0:
                actual_end = i + 6
                break
    
    if actual_end != -1:
        real_explorer = explorer_block[:actual_end]
        rest_of_block = explorer_block[actual_end:]
        
        # Now we replace the whole segment from start_idx to end_idx
        # with a new structure.
        
        # We need to close the previous col-lg-8 and blog-content
        # and start a new row for DM04.
        
        # Looking at the original:
        # <div class="col-lg-8 offset-lg-2">
        #     <div class="blog-content">
        #         ...
        #         <div class=dm04-explorer ...>...</div>
        #         <div class="blog-heading ...">...</div>
        #     </div>
        # </div>
        
        # We want:
        # <div class="col-lg-8 offset-lg-2">
        #     <div class="blog-content">
        #         ...
        #     </div>
        # </div>
        # <div class="row">
        #     <div class="col-12">
        #         <div class="blog-content">
        #             <div class=dm04-explorer ...>...</div>
        #         </div>
        #     </div>
        # </div>
        # <div class="col-lg-8 offset-lg-2">
        #     <div class="blog-content">
        #         <div class="blog-heading ...">...</div>
        #     </div>
        # </div>
        
        # This is complex because of the nested structure.
        # A simpler way: just make dm04-explorer use CSS to be full width.
        # .dm04-explorer { width: 100vw; position: relative; left: 50%; right: 50%; margin-left: -50vw; margin-right: -50vw; }
        # But that's a hack.
        
        # Let's just do the wrap and hope the closing divs align or fix them.
        
        # Actually, let's just do the HTML content replacement and the CSS will handle the width.
        # User said "override Bootstrap 1/3 constraints".
        # If I keep it in col-lg-8, I can't easily make it full width without CSS hacks.
        
        # Let's try to just wrap the explorer block in a way that doesn't break.
        
        # Better: I'll replace the segment:
        # [DM04 start] ... [DM04 end]
        # with:
        # </div></div><div class="row"><div class="col-12"><div class="blog-content">[DM04 block]</div></div></div><div class="col-lg-8 offset-lg-2"><div class="blog-content">
        
        new_segment = '</div></div><div class="row"><div class="col-12"><div class="blog-content">' + real_explorer + '</div></div></div><div class="col-lg-8 offset-lg-2"><div class="blog-content">' + rest_of_block
        content = content[:start_idx] + new_segment + content[end_idx:]

with open('DataStream.html', 'w') as f:
    f.write(content)
