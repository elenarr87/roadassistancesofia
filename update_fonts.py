#!/usr/bin/env python3
# update_fonts.py — replace Google Fonts with local assets/inter-font.css,
# fix font paths in assets/inter-font.css and fix kalkulator typo.
import re
from pathlib import Path

repo_root = Path('.').resolve()

# 1) Find html files
html_files = list(repo_root.glob('*.html')) + list(repo_root.glob('**/*.html'))

# Regex to match the google fonts block (robust enough for current patterns)
google_block_re = re.compile(
    r'(?s)(?:\s*<link rel=["\']preconnect["\'] href=["\']https://fonts.googleapis.com["\'].*?>\s*\n)?'
    r'(?:\s*<link rel=["\']preconnect["\'] href=["\']https://fonts.gstatic.com["\'].*?>\s*\n)?'
    r'(?:\s*<link [^>]*href=["\']https://fonts.googleapis.com/[^>]+>)+',
    flags=re.IGNORECASE
)

replacement = '<link rel="stylesheet" href="assets/inter-font.css">\n'

updated = []

for f in html_files:
    try:
        text = f.read_text(encoding='utf-8')
    except Exception:
        continue
    orig = text
    if 'fonts.googleapis.com' in text or 'fonts.gstatic.com' in text:
        text = google_block_re.sub(replacement, text)
    # Ensure inter-font.css link is present
    if 'assets/inter-font.css' not in text:
        title_end_re = re.compile(r'(</title>)', re.IGNORECASE)
        text = title_end_re.sub(r'\1\n' + replacement, text, count=1)
    # Fix typo in all files
    if 'roadasistancesofia' in text:
        text = text.replace('roadasistancesofia', 'roadassistancesofia')
    if text != orig:
        f.write_text(text, encoding='utf-8')
        updated.append(str(f))
        print('Updated:', f)
# 2) Fix inter-font.css paths if needed
inter_css = repo_root / 'assets' / 'inter-font.css'
if inter_css.exists():
    txt = inter_css.read_text(encoding='utf-8')
    new_txt = re.sub(r"url\(['\"]?assets/fonts/([^'\")]+)['\"]?\)", r"url('fonts/\\1')", txt)
    new_txt = re.sub(r"url\(['\"]?\.\./assets/fonts/([^'\")]+)['\"]?\)", r"url('fonts/\\1')", new_txt)
    # Also handle url("assets/fonts/..") with double quotes etc.
    if new_txt != txt:
        inter_css.write_text(new_txt, encoding='utf-8')
        updated.append(str(inter_css))
        print('Fixed paths in:', inter_css)

print('Total files changed:', len(updated))
if updated:
    for u in updated:
        print(' -', u)
else:
    print('No changes made.')