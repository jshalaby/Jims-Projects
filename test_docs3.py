from pathlib import Path
import os

docs = Path.home() / 'Documents'
print(f'Checking: {docs}\n')

# Get raw directory listing
items = os.listdir(docs)
for item in items:
    full_path = docs / item
    print(f'{item}:')
    print(f'  Full path: {full_path}')
    print(f'  Exists: {full_path.exists()}')
    
    # Check if .lnk extension
    if str(full_path).endswith('.lnk'):
        print(f'  Type: Shortcut file (.lnk)')
    
    # Check file attributes
    try:
        print(f'  Absolute path: {full_path.absolute()}')
    except:
        pass
    print()
