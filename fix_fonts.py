#!/usr/bin/env python3
from pathlib import Path

p = Path('assets/inter-font.css')
if not p.exists():
    print('assets/inter-font.css not found')
    raise SystemExit(1)

text = p.read_text(encoding='utf-8')

# ordered list of files to substitute in place of \1 (one-per-block)
files = [
 'inter-cyrillic-ext.woff2',
 'inter-cyrillic.woff2',
 'inter-greek-ext.woff2',
 'inter-greek.woff2',
 'inter-vietnamese.woff2',
 'inter-latin-ext.woff2',
 'inter-latin.woff2',
 # repeat pattern for other weights if file has many repeated blocks;
 # if number of placeholders differs adjust accordingly
]

# Replace the placeholder occurrences in order
count = 0
def repl(match):
    global count
    if count < len(files):
        s = f"url('fonts/{files[count]}')"
    else:
        s = "url('fonts/inter-latin.woff2')"  # fallback
    count += 1
    return s

# simple replacement of "url('fonts/\\1')" occurrences
new_text = text.replace("url('fonts/\\1')", "__PLACEHOLDER__")
for f in files:
    new_text = new_text.replace("__PLACEHOLDER__", f"url('fonts/{f}')", 1)

# In case other quoting styles exist:
new_text = new_text.replace('url("fonts/\\1")', "__PLACEHOLDER2__")
for f in files:
    new_text = new_text.replace("__PLACEHOLDER2__", f'url("fonts/{f}")', 1)

p.write_text(new_text, encoding='utf-8')
print('Updated', p)