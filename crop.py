import xml.etree.ElementTree as ET
import cv2
import os
import csv

if __name__ == "__main__":

    xml_files = [f"./dataset/{filename}" for filename in os.listdir('./dataset') if filename.endswith('.xml')]
    png_files = []
    for y in xml_files:
        png_files.append(y[:-3] + 'png')

    j = 19491
    rows = []
    # header = ['file', 'type', 'extra']
    # rows.append(header)

    for x, p in zip(xml_files, png_files):
        tree = ET.parse(x)
        root = tree.getroot()
        objects = root.findall('object')
        image = cv2.imread(p)
        for o in objects:
            # if p == "./dataset/Town01_003120.png":
            #     print("Hello")
            row = []

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
            if (ymax - ymin < 13 or xmax - xmin < 13):
                continue

            x_left = xmin + int(width / 2) - int(length / 2)
            x_right = xmin + int(width / 2) + int(length / 2)
            if (x_left < 0):
                x_right = x_right - x_left
                x_left = 0
            if (x_right > image.shape[1]):
                x_left = x_left - (x_right - image.shape[1])
                x_right = image.shape[1]

            roi = image[ymin:ymax, x_left:x_right]

            dim = (69, 69)
            # resize image
            resized = cv2.resize(roi, dim, interpolation=cv2.INTER_AREA)
            s = "%06d" % (j,)
            z = f"./output/object_{str(j).zfill(6)}.jpg"
            j = j + 1
            # print(f"{p},{s},{o[0].text},")
            # cv2.imshow('image', resized)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            cv2.imwrite(z, resized)

            row.append(s)
            row.append(o[0].text)
            row.append('')
            rows.append(row)

    with open('labels.csv', 'w', newline='') as csvfile:
        writeCSV = csv.writer(csvfile, delimiter=',')
        writeCSV.writerows(rows)
