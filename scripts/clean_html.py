#!/usr/bin/env python3
import glob, os, re

root = os.path.abspath(os.path.dirname(__file__) + os.sep + '..')
patterns = [os.path.join(root, '*.html'), os.path.join(root, '**', '*.html')]

def should_skip(path):
    low = path.replace('\\','/').lower()
    return ('/docs/' in low) or ('/images/' in low) or low.endswith('.py') or low.endswith('clean_html.py')

fixed = []
for pattern in patterns:
    for path in glob.glob(pattern, recursive=True):
        if should_skip(path):
            continue
        try:
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                data = f.read()
        except Exception as e:
            print(f'ERROR reading {path}: {e}')
            continue

        m_start = re.search(r'<!doctype', data, re.IGNORECASE)
        start = m_start.start() if m_start else 0
        m_end = re.search(r'</html>', data, re.IGNORECASE)
        end = m_end.end() if m_end else len(data)
        new = data[start:end]
        # remove unicode replacement char and stray nulls
        new = new.replace('\uFFFD', '')
        new = new.replace('\x00', '')
        # collapse accidental repeated DOCTYPEs at top
        # keep only the first <!doctype ...>... </html>
        if new != data:
            try:
                with open(path, 'w', encoding='utf-8', newline='\n') as f:
                    f.write(new)
                fixed.append(path)
                print(f'Fixed: {path}')
            except Exception as e:
                print(f'ERROR writing {path}: {e}')
        else:
            print(f'NoChange: {path}')

print('\nSummary:')
print(f'Total files scanned patterns: {len(patterns)}')
print(f'Files fixed: {len(fixed)}')
for p in fixed:
    print(' -', p)
