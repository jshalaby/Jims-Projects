from pathlib import Path
import os

docs = Path.home() / 'Documents'
print(f'Checking: {docs}')
items = list(docs.iterdir())
for item in items:
    is_dir = item.is_dir()
    print(f"{'DIR ' if is_dir else 'FILE'}: {item.name}")

print("\nUsing os.path.isdir:")
items2 = os.listdir(docs)
for item in items2:
    item_path = docs / item
    is_dir = os.path.isdir(item_path)
    print(f"{'DIR ' if is_dir else 'FILE'}: {item}")
