#!/usr/bin/env python3
"""Read the English text on each picture-book page and translate it into other languages.

Text is read with Google Cloud Vision. Translations are powered by Google Translate,
through the Cloud Translation API (https://cloud.google.com/translate).
Sign in once with "gcloud auth application-default login", or set
GOOGLE_APPLICATION_CREDENTIALS to the path of a key file.
"""
import argparse, io, os, re
import google.auth, google.auth.exceptions
import wordfreq
from google.cloud import translate_v2 as translate
from google.cloud import vision
from spellchecker import SpellChecker

LANGUAGES = ["zh-CN", "zh-TW", "ru", "ko", "ja", "es", "de", "fr"]
PICTURE_TYPES = (".png", ".jpg", ".jpeg")

spell = SpellChecker()

# pic_to_text is adapted, with changes, from the detect_document code sample in Google's Cloud Vision documentation
# (Copyright 2017 Google LLC, Apache License 2.0; see THIRD_PARTY_NOTICES.md).
def pic_to_text(path):
  client = vision.ImageAnnotatorClient()
  with io.open(path, "rb") as picture:
    response = client.document_text_detection(image=vision.Image(content=picture.read()))
  return response.full_text_annotation.text

def page_number(file):
  numbers = re.findall(r"\d+", file)
  return int(numbers[-1]) if numbers else 0

def keep_english(line):
  """Keep a line that reads like a sentence; from short lines keep only common, correctly spelled words."""
  text = re.sub(r"[^a-zA-Z\s:;'\".,!?~'`\-()/\\]+", "", line)
  if len(text) > 8:
    return text + " "
  words = re.sub(r"[^a-zA-Z\s']+", "", text).split(" ")
  return "".join(word + " " for word in words
                 if len(word) > 1 and spell.correction(word) == word and wordfreq.zipf_frequency(word, "en") > 3.5)

def translate_text(translator, text, language):
  if not text:
    return ""
  result = translator.translate(text, target_language=language, source_language="en", format_="text")
  return " ".join(result["translatedText"].split("\n"))   # one line per page in the output files

def translate_book(bookDir, pages, translator):
  done = lambda language: os.path.exists(os.path.join(bookDir, f"translation-{language}.txt"))
  if all(done(language) for language in LANGUAGES):
    return   # finished on an earlier run (e.g. before a daily quota ran out)
  texts = []
  original = ""
  for n, page in enumerate(pages, start=1):
    print(page)
    text = "".join(keep_english(line) for line in pic_to_text(page).split("\n"))
    if len(text) > 6:
      texts.append(text)
      original += f"{n} {text}\n\n"
    else:
      texts.append("")
      original += f"{n}\n\n"
  print(original)
  with open(os.path.join(bookDir, "original.txt"), "w") as file:
    file.write(original)

  for language in LANGUAGES:
    if done(language):
      continue
    translations = [translate_text(translator, text, language) for text in texts]
    with open(os.path.join(bookDir, f"translation-{language}.txt"), "w") as file:
      file.write("".join(translated + "\n" for translated in translations))
    with open(os.path.join(bookDir, f"original-translation-{language}.txt"), "w") as file:
      for n, (text, translated) in enumerate(zip(texts, translations), start=1):
        file.write(f"page{n}: \n{text}\n{translated}\n\n")
    print(language, "done")

def main():
  parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument("pictures", help="folder with one picture folder per book (made by pptxTJpg.py)")
  args = parser.parse_args()
  try:
    google.auth.default()
  except google.auth.exceptions.DefaultCredentialsError:
    parser.error("no Google Cloud credentials: run 'gcloud auth application-default login', "
                 "or set GOOGLE_APPLICATION_CREDENTIALS to the path of a key file")

  translator = translate.Client()
  for root, dirs, files in os.walk(args.pictures):
    pictures = sorted((file for file in files if not file.startswith(".") and file.lower().endswith(PICTURE_TYPES)),
                      key=lambda file: (page_number(file), file))
    pages = [os.path.join(root, file) for file in pictures[1:]]
    if pages:
      translate_book(root, pages, translator)

if __name__ == "__main__":
  main()
