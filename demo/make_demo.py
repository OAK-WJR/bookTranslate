#!/usr/bin/env python3
"""Put the demo book and what the scripts made from it into docs/ for the demo web page.

usage: python demo/make_demo.py BOOK_FOLDER PICTURES_FOLDER XLS_FILE
BOOK_FOLDER is the folder used by make_pages.py, PICTURES_FOLDER the folder given to translateTest.py
and XLS_FILE the file written by kBsExcel.py. Writes docs/book.json, docs/pages/ and the two downloads.
Needs Pillow.
"""
import glob, json, os, shutil, sys
from PIL import Image

LANGUAGES = [("en", "English"), ("zh-CN", "简体中文"), ("zh-TW", "繁體中文"), ("ru", "Русский"), ("ko", "한국어"),
             ("ja", "日本語"), ("es", "Español"), ("de", "Deutsch"), ("fr", "Français")]
DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs")

bookFolder, picturesFolder, xls = sys.argv[1:4]
book = os.path.join(picturesFolder, "Denslows Three Bears")

# original.txt has "<page> <text>" and a blank line for every page; translation files have one line per page
original = [block.split(" ", 1)[1].strip() if " " in block else ""
            for block in open(os.path.join(book, "original.txt")).read().split("\n\n") if block.strip()]
texts = {"en": original}
for code, _ in LANGUAGES[1:]:
  lines = open(os.path.join(book, f"translation-{code}.txt")).read().split("\n")
  texts[code] = [lines[n] if n < len(lines) else "" for n in range(len(original))]

os.makedirs(os.path.join(DOCS, "pages"), exist_ok=True)
pages = []
for n, path in enumerate(sorted(glob.glob(os.path.join(bookFolder, "pages", "page*.jpg")))):
  name = os.path.basename(path)
  Image.open(path).save(os.path.join(DOCS, "pages", name), quality=82, optimize=True, progressive=True)
  # bookTranslate skips the first picture of a slideshow (the cover), so page n has text line n - 1
  pages.append({"image": f"pages/{name}",
                "text": {code: texts[code][n - 1] if n > 0 else "" for code, _ in LANGUAGES}})

json.dump({"title": "Denslow's Three Bears", "languages": LANGUAGES, "pages": pages},
          open(os.path.join(DOCS, "book.json"), "w"), ensure_ascii=False, indent=1)
shutil.copy(os.path.join(bookFolder, "slides", "Denslows Three Bears.pptx"), os.path.join(DOCS, "denslows-three-bears.pptx"))
shutil.copy(xls, os.path.join(DOCS, "denslows-three-bears-translations.xls"))
print(len(pages), "pages written to", os.path.normpath(DOCS))
