#!/usr/local/bin/python3
print("Importing libraries...")
import io, os, ntpath

from google.cloud import vision

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

print("Getting the Google API key...")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "~/Desktop/bookTranslate/google-cloud-key.json"

def pic_to_text(infile):

    client = vision.ImageAnnotatorClient()

    with io.open(infile, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content = content)
    response = client.document_text_detection(image = image)
    text = response.full_text_annotation.text
    print("Detected text: {}".format(text))

    return text

bigFile = "~/Desktop/PictureBooksT"
images = {}

print("Checking which files to translate...")
for root, dirs, files in os.walk(bigFile):
    for file in files:
        if file.startswith(".") == False and file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
            if root not in images:
                images[root] = []
            images[root].append(os.path.join(root, file))

for key in images.keys():
  imagesSort = {}
  for image in images[key]:
    imagesSort[int("".join(list(filter(str.isdigit, ntpath.basename(image)))))] = image
  imagesSort = sorted(imagesSort.items(), key = lambda k: k[0])
  images[key] = []

  for i in range(0, len(imagesSort)):
    images[key].append(imagesSort[i][1])
  images[key] = images[key][1:]

for key in images.keys():
    if len(images[key]) != 0:
        
        print("Files found, getting ready...")

        original = ""
        translate = ""
        oTAll = ""
        allText = ""

        txtO = key + "/original"
        txtT = key + "/tanslate.txt"
        txtOT = key + "/original-Tanslate"

        texts = []
        languages = ["zh-CN", "zh-TW", "ru", "ko", "ja", "es", "de", "fr"]

        for o in range(0, len(images[key])):
            print(images[key][o] + "\n")
            lines = pic_to_text(images[key][o]).split("\n")
            text = ""
            for line in lines:
                if len(line) > 3:
                    text += line+" "
            texts.append(text)
            original += str(o+1) + " " + text + "\n\n"
        print(original)
        with open(txtO + ".txt", "a") as O:
            O.write(original)

        for language in languages:
            for o in range(0, len(images[key])):

                translated = ""   # not included in this public copy
                translate += translated + "\n"
                print(translated)

                oTAll += "page" + str(o+1) + ": \n" + texts[o] + "\n" + translated + "\n\n"

                allText += oTAll

                with open(txtT + "-" + language + ".txt", "a") as T:
                    T.write(translate)
                with open(txtOT + "-" + language + ".txt", "a") as OT:
                    OT.write(oTAll)
                
                translate = ""
                oTAll = "" 
    
    print("——————————————————————————————————————————————")
    print(allText)

'''
    for language in languages:
        original += text
        translated = ""   # not included in this public copy
        translate += translated
        print(translated)
        oTAll += image + text + "\n" + translated + "\n\n"

        openImage = Image.open(image)
        draw = ImageDraw.Draw(openImage)

        fontPath = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
        textFont = ImageFont.truetype(fontPath, 15)

        textPosition = (0,0)

        if translated != "" and translated != " ":
            left, top, right, bottom = draw.textbbox(textPosition, translated, font = textFont)
            draw.rectangle((left, top, right, bottom), "white")
        draw.text(textPosition, 
                translated, 
                font = textFont, 
                fill = "black")
        openImage.save(image)

    print("——————————————————————————————————————————————")
    print(original,"\n",translate,"\n",oTAll)

    with open(txtO, "a") as O:
        O.write(original)
    with open(txtT, "a") as T:
        T.write(translate)
    with open(txtOT, "a") as OT:
        OT.write(oTAll)
'''