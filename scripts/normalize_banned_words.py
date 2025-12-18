#!/usr/bin/env python3
import re
from pathlib import Path
p = Path('banned-words.js')
s = p.read_text(encoding='utf-8')
# Find all single- or double-quoted strings inside the file
# Use a simpler pattern because the list entries do not contain embedded escaped quotes
items = re.findall(r'"([^\"]*)"|\'([^\']*)\'', s)
words = [a or b for (a, b) in items]
words = [w for w in words if w.strip()]
# Build normalized content
out = ['window.BANNED_WORDS = [']
for i, w in enumerate(words):
    escaped = w.replace('\\', '\\\\').replace('"', '\\"')
    comma = ',' if i < len(words) - 1 else ''
    out.append(f'  "{escaped}"{comma}')
out.append('];')
out_text = '\n'.join(out) + '\n'
# Backup original
bak = p.with_suffix('.js.bak')
bak.write_text(s, encoding='utf-8')
# Write normalized file
p.write_text(out_text, encoding='utf-8')
print(f'Wrote {p} with {len(words)} entries; backup at {bak}')
