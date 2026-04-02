from pathlib import Path
import os
import stat

docs = Path.home() / 'Documents'
print(f'Checking: {docs}\n')

items = os.listdir(docs)
for item in items:
    item_path = docs / item
    try:
        st = os.stat(item_path)
        is_file = stat.S_ISREG(st.st_mode)
        is_dir = stat.S_ISDIR(st.st_mode)
        print(f'{item}:')
        print(f'  os.path.isdir: {os.path.isdir(item_path)}')
        print(f'  Path.is_dir: {item_path.is_dir()}')
        print(f'  stat.S_ISDIR: {is_dir}')
        print(f'  stat.S_ISREG: {is_file}')
        
        # Try to list contents
        try:
            contents = os.listdir(item_path)
            print(f'  List contents: {len(contents)} items')
        except Exception as e:
            print(f'  Cannot list: {e}')
        print()
    except Exception as e:
        print(f'{item}: Error - {e}\n')
