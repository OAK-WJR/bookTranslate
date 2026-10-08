#!/usr/bin/env python3
"""Put each book's original text and its translations side by side, one Excel sheet per book.

Translations are powered by Google Translate (https://cloud.google.com/translate), so every sheet
starts with the "powered by Google Translate" badge and Google's disclaimer.
"""
import argparse, os, re, unicodedata
import xlwt

LANGUAGES = ["zh-CN", "zh-TW", "ru", "ko", "ja", "es", "de", "fr"]
BADGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "powered-by-google-translate.bmp")
DISCLAIMER = ("THIS SERVICE MAY CONTAIN TRANSLATIONS POWERED BY GOOGLE. GOOGLE DISCLAIMS ALL WARRANTIES RELATED TO THE "
              "TRANSLATIONS, EXPRESS OR IMPLIED, INCLUDING ANY WARRANTIES OF ACCURACY, RELIABILITY, AND ANY IMPLIED "
              "WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.")
WIDTH = 24   # column width in characters

def fit(sheetRow, cells, width):
  """Make a row tall enough for its longest wrapped cell; Chinese, Japanese and Korean characters count twice."""
  chars = max(sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in cell) for cell in cells)
  sheetRow.height_mismatch, sheetRow.height = True, min(8180, 300 * max(1, -(-chars // (width - 4))))   # Excel's limit is 409 pt

parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("pictures", help="folder with one folder per book (after translateTest.py)")
parser.add_argument("output", help="the .xls file to write")
args = parser.parse_args()

wrap = xlwt.easyxf("align: wrap on, vert top")
workbook = xlwt.Workbook()
sheetNames = set()

for book in sorted(os.listdir(args.pictures)):
  bookDir = os.path.join(args.pictures, book)
  originalPath = os.path.join(bookDir, "original.txt")
  if not os.path.exists(originalPath):
    continue

  # original.txt has "<page> <text>" followed by a blank line for every page
  with open(originalPath) as file:
    rows = [[line.split(" ", 1)[1].strip() if " " in line else ""] for line in file.readlines()[::2]]
  header = ["original"]

  for language in LANGUAGES:
    translationPath = os.path.join(bookDir, f"translation-{language}.txt")
    if not os.path.exists(translationPath):
      continue
    header.append(language)
    with open(translationPath) as file:
      translations = file.read().split("\n")
    for n, row in enumerate(rows):
      row.append(translations[n] if n < len(translations) else "")

  # Sheet names: at most 31 characters, no symbols, no repeats (Excel ignores case)
  baseName = re.sub(r"\W", "", book) or "Book"
  sheetName, n = baseName[:31], 2
  while sheetName.lower() in sheetNames:
    sheetName, n = baseName[:31 - len(str(n))] + str(n), n + 1
  sheetNames.add(sheetName.lower())

  sheet = workbook.add_sheet(sheetName)
  columns = max(len(header), 9)
  for c in range(columns):
    sheet.col(c).width = 256 * WIDTH
  # Google's attribution rules: the badge next to the translations, then the disclaimer.
  # The 32 px badge fills the first two rows, which keep their default height so it is not stretched.
  sheet.insert_bitmap(BADGE, 0, 0)
  sheet.write_merge(2, 2, 0, 3, DISCLAIMER, wrap)
  fit(sheet.row(2), [DISCLAIMER], WIDTH * 4)
  for r, row in enumerate([header] + rows, start=3):
    for c, cell in enumerate(row):
      sheet.write(r, c, cell, wrap)
    fit(sheet.row(r), row, WIDTH)
  print(book, "->", sheetName)

workbook.save(args.output)
print("saved", args.output)
