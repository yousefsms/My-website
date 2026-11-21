import re

with open('DataStream.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace <div class="ds-content-wrapper"> with the bootstrap structure
content = content.replace('<div class="ds-content-wrapper">', '<div class="container"><div class="row"><div class="col-lg-8 offset-lg-2">')

# Now we need to close these 3 new divs.
# The ds-content-wrapper was a single div.
# We need to find where those wrappers end.
# This is tricky because there are multiple and they might have nested divs.

# Let's try a more robust approach.
# We search for <div class="ds-content-wrapper"> and find its matching </div>.

def replace_wrapper(text):
    start_marker = '<div class="ds-content-wrapper">'
    end_marker = '</div>'
    
    while True:
        start_idx = text.find(start_marker)
        if start_idx == -1:
            break
        
        # Find the matching </div>
        depth = 1
        current_pos = start_idx + len(start_marker)
        while depth > 0:
            next_div_start = text.find('<div', current_pos)
            next_div_end = text.find('</div>', current_pos)
            
            if next_div_end == -1:
                break # Should not happen in valid HTML
                
            if next_div_start != -1 and next_div_start < next_div_end:
                depth += 1
                current_pos = next_div_start + 4
            else:
                depth -= 1
                current_pos = next_div_end + 6
        
        # Now we have the full block from start_idx to current_pos
        block = text[start_idx:current_pos]
        # Replace start and end of the block
        new_block = '<div class="container"><div class="row"><div class="col-lg-8 offset-lg-2">' + block[len(start_marker):-6] + '</div></div></div>'
        text = text[:start_idx] + new_block + text[current_pos:]
        
    return text

final_content = replace_wrapper(content)

with open('DataStream.html', 'w', encoding='utf-8') as f:
    f.write(final_content)
