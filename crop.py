import xml.etree.ElementTree as ET
import cv2
import os
import csv

xml_files = [f for f in os.listdir('.') if f.endswith('.xml')]
png_files = []
for y in xml_files:
    png_files.append(y[:-3] + 'png')

j = 0
rows = []
header = ['file', 'type', 'extra']
rows.append(header)

for x, p in zip(xml_files, png_files):
    tree = ET.parse(x)
    root = tree.getroot()
    objects = root.findall('object')
    image = cv2.imread(p)
    for o in objects:

        row = []
        s = "%04d" % (j,)
        z = "img" + s + ".png"
        j = j + 1
        box = []
        for a in o:
            if (a.tag == 'bndbox'):
                for t in a:
                    box.append(t.text)
        xmin = int(box[0])
        ymin = int(box[1])
        xmax = int(box[2])
        ymax = int(box[3])
        width = xmax - xmin
        length = max(ymax - ymin, xmax - xmin)
        # black magix
        x_left = xmin + int(width / 2) - int(length / 2)
        x_right = xmin + int(width / 2) + int(length / 2)
        if (x_left < 0):
            x_right = x_right - x_left
            x_left = 0
        if (x_right > image.shape[1]):
            x_left = x_left - (x_right - image.shape[0])
            x_right = image.shape[0]
        if (ymax - ymin < 15 or x_right - x_left < 15):
            continue
        roi = image[ymin:ymax, x_left:x_right]

        dim = (64, 64)
        # resize image
        resized = cv2.resize(roi, dim, interpolation=cv2.INTER_AREA)
        cv2.imwrite(z, resized)

        row.append(z)
        row.append(o[0].text)
        row.append('')
        rows.append(row)

with open('labels.csv', 'w', newline='') as csvfile:
    writeCSV = csv.writer(csvfile, delimiter=',')
    writeCSV.writerows(rows)
