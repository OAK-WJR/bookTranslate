#!/usr/local/bin/python3
import os
from zipfile import ZipFile

bigFile = '~/Desktop/AllBooks'
unzipRoot = '~/Desktop/PicturesT'
pptsPath = []
pptsNames = []
for root, dirs, files in os.walk(bigFile):
    for file in files:
        if file.startswith(".") == False and file.endswith(".pptx"):
          pptsPath.append(os.path.join(root, file))
          pptsNames.append(file.replace(".pptx", ""))
          
for i in range(0, len(pptsPath)):
  with ZipFile(pptsPath[i]) as f:
    for file in f.namelist():
      if file.startswith("ppt/media/"):
        f.extract(file, path = unzipRoot)
    if os.path.exists(unzipRoot + "/" + pptsNames[i]):
      os.rename(unzipRoot + "/ppt/media", unzipRoot + "/" + pptsNames[i] + "2")
    else:
      os.rename(unzipRoot + "/ppt/media", unzipRoot + "/" + pptsNames[i])

print(pptsNames)
print(len(pptsNames))


        


'''
txt = ""
txt = txt.split("\n")
for i in txt:
  if len(i) > 5:
    print(i)
text = filter(str.isalpha, txt)
print("".join(list(text)))
'''

'''
import ntpath
images = ['~/Desktop/PictureBooksT/2/picture3.png', '~/Desktop/PictureBooksT/2/picture2.png', '~/Desktop/PictureBooksT/2/picture1.png', '~/Desktop/PictureBooksT/2/picture5.png', '~/Desktop/PictureBooksT/2/picture4.png', '~/Desktop/PictureBooksT/2/picture6.png', '~/Desktop/PictureBooksT/2/picture7.png', '~/Desktop/PictureBooksT/2/picture19.png', '~/Desktop/PictureBooksT/2/picture18.png', '~/Desktop/PictureBooksT/2/picture16.png', '~/Desktop/PictureBooksT/2/picture17.png', '~/Desktop/PictureBooksT/2/picture15.png', '~/Desktop/PictureBooksT/2/picture14.png', '~/Desktop/PictureBooksT/2/picture10.png', '~/Desktop/PictureBooksT/2/picture11.png', '~/Desktop/PictureBooksT/2/picture13.png', '~/Desktop/PictureBooksT/2/picture12.png', '~/Desktop/PictureBooksT/2/picture9.png', '~/Desktop/PictureBooksT/2/picture8.png']
imagesSort = {}
for image in images:
  imagesSort[int("".join(list(filter(str.isdigit, ntpath.basename(image)))))] = image
imagesSort = sorted(imagesSort.items(), key = lambda k: k[0])
images = []
for i in range(0, len(imagesSort)):
  images.append(imagesSort[i][1])
print(images[2:])
'''