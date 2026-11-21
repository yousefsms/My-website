with open('css/style.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the start of the block to remove
start_idx = -1
for i, line in enumerate(lines):
    if '/* Data Stream Content Wrapper - Unified Width & Alignment */' in line:
        start_idx = i
        break

if start_idx != -1:
    # Remove from start_idx to the end since it's the last block
    new_lines = lines[:start_idx]
    with open('css/style.css', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("CSS cleaned successfully.")
else:
    print("Block not found.")
