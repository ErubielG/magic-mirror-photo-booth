#!/usr/bin/env python3
"""Read-only photo file inventory; cannot prove completed physical prints."""
from pathlib import Path
from collections import Counter
import argparse

p = argparse.ArgumentParser(description=__doc__)
p.add_argument("--photos-dir", default=str(Path.home() / "fotos"))
a = p.parse_args()
folder = Path(a.photos_dir)
if not folder.is_dir():
    raise SystemExit(f"Directory not found: {folder}")
files = sorted(folder.glob("*.jpg"))
print(f"Folder: {folder}")
print(f"All top-level JPG files: {len(files)}")
print(f"Possible print sheets (hoja-*): {sum(x.name.startswith('hoja-') for x in files)}")
print(f"Other top-level JPG files (candidate captures): {sum(not x.name.startswith('hoja-') for x in files)}")
print(f"Originals (not added to total): {len(list((folder / 'originales').glob('*.jpg')))}")
by_day = Counter(__import__('datetime').datetime.fromtimestamp(x.stat().st_mtime).strftime("%Y-%m-%d") for x in files if not x.name.startswith("hoja-"))
for date, count in sorted(by_day.items()):
    print(f"{date}: {count} candidate captures (by file modification date)")
