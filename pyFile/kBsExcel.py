#!/usr/local/bin/python3
import os, xlwt, re

style_wrap = xlwt.XFStyle()
style_wrap.alignment.wrap = 1

dataFileRoot = '~/Desktop/PicturesT'

items = os.listdir(dataFileRoot)

bNs = [] #bookNames
bOD = [] #bookOriginalData
aBD = {} #aBD

for item in items:
    if os.path.isdir(os.path.join(dataFileRoot, item)):
        bNs.append(item)

print(bNs)
for book in bNs:

  oFP = os.path.join(dataFileRoot, book, "original.txt") #originalFilePath
  print(oFP)
  if os.path.exists(oFP):
    with open(oFP,"r") as read:
      oFD = read.readlines()[::2] #originalFileData
    for line in oFD:
      bOD.append([" ".join(line.split(" ")[1:])[:-1]])
    
    aBD[book] = bOD
    aBD[book].insert(0,["original"])
    bOD = []


  tBsLs = ["zh-CN", "zh-TW", "ru", "ko", "ja", "es", "de", "fr"] #translateBooksLanguages
  tDTFs = [] #translateDataTxtFiles
  for language in tBsLs:
    tFP = os.path.join(dataFileRoot, book, f"tanslate.txt-{language}.txt") #translateFilePath
    print(tFP)
    if os.path.exists(tFP):
      with open(tFP,"r") as read:
        tFD = read.readlines() #translateFileData
      
      aBD[book][0].append(language)
      for i in range(1, len(tFD)):
        aBD[book][i].append(tFD[i - 1][:-1])
      aBD[book][-1].append(tFD[-1][:-1])

workbook = xlwt.Workbook()

for sheet_key in aBD.keys():
  print(re.sub(r'[^\w\s]', '', sheet_key))
  worksheet = workbook.add_sheet(re.sub(r'[^\w\s\']', '', sheet_key).replace(" ","")[:31])
  for row_index, row_data in enumerate(aBD[sheet_key]):
      for col_index, col_data in enumerate(row_data):
          worksheet.write(row_index, col_index, col_data, style=style_wrap)

workbook.save('~/Desktop/TranslateXLS.xls')
print(aBD)