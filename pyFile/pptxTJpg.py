#!/usr/bin/env python3
"""Copy the pictures out of every .pptx slideshow in a folder, one folder per book."""
import argparse, os
from zipfile import ZipFile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("slides", help="folder with the .pptx slideshows (subfolders are searched too)")
parser.add_argument("pictures", help="folder to create one picture folder per book in")
args = parser.parse_args()

usedNames = set()
for root, dirs, files in os.walk(args.slides):
  for file in sorted(files):
    if file.startswith(".") or not file.endswith(".pptx"):
      continue

    # Two slideshows with the same name go to "Name" and "Name2"
    name = file[:-len(".pptx")]
    bookName, n = name, 2
    while bookName in usedNames:
      bookName, n = f"{name}{n}", n + 1
    usedNames.add(bookName)

    bookDir = os.path.join(args.pictures, bookName)
    os.makedirs(bookDir, exist_ok=True)
    with ZipFile(os.path.join(root, file)) as pptx:
      for member in pptx.namelist():
        if member.startswith("ppt/media/") and not member.endswith("/"):
          with open(os.path.join(bookDir, os.path.basename(member)), "wb") as picture:
            picture.write(pptx.read(member))
    print(bookDir)

print(len(usedNames), "books")
