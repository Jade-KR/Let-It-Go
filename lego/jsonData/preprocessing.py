import json

LegoSort = {}
LegoSort["parts"] = {}
LegoSort["colors"] = {}

with open('LegoParts.json', 'r', encoding='UTF8') as partsRaw:
    partList = json.load(partsRaw)["rows"]
    for part in partList:
        # print(part)
        LegoSort["parts"][part[0]] = [
            part[0], part[2], part[1]
        ]

with open('LegoColors.json', 'r', encoding='UTF8') as colorsRaw:
    colorList = json.load(colorsRaw)["rows"]
    for color in colorList:
        # print(part)
        LegoSort["colors"][color[0]] = color[2]

# print(LegoSort)

with open('LegoSort.json', 'w', encoding='UTF8') as makeJson:
    json.dump(LegoSort, makeJson, ensure_ascii=False, indent="\t")