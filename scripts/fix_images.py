#!/usr/bin/env python3
import glob, os, re

root = os.path.abspath(os.path.dirname(__file__) + os.sep + '..')
patterns = [os.path.join(root, '*.html'), os.path.join(root, '*.htm'), os.path.join(root, '*.txt')]

fixed = []
for pattern in patterns:
    for path in glob.glob(pattern, recursive=False):  # not recursive since root level
        try:
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                data = f.read()
        except Exception as e:
            print(f'ERROR reading {path}: {e}')
            continue

        new = data.replace('https://roadassistancesofia.bg/images/', '/images/')
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
print(f'Files fixed: {len(fixed)}')
for p in fixed:
    print(' -', p)