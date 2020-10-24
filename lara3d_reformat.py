import csv
import cv2 as cv
from math import floor, ceil


def crop2square(original_min, original_max, difference):
    new_min = original_min - floor(difference / 2)
    new_max = original_max + ceil(difference / 2)
    return new_min, new_max


def shift(y_down, y_up, x_left, x_right, shape):
    if y_down < 0:
        y_up += abs(y_down)
        y_down = 0
    if y_up > shape[0]:
        y_down -= y_up - shape[0]
        y_up = shape[0]
    if x_left < 0:
        x_right += abs(x_left)
        x_left = 0
    if x_right > shape[1]:
        x_left -= x_right - shape[1]
        x_right = shape[1]
    return y_down, y_up, x_left, x_right


if __name__ == "__main__":
    with open('./Lara3D/labels.txt') as label_file:
        labels = []
        for row in label_file:
            row_split = row.rstrip().split(' ')
            if row_split[10] == 'ambiguous':
                continue
            traffic_light = [''.join(row_split[8:10])]
            labels.append([row_split[2].zfill(6)] + row_split[3:7] + traffic_light + [row_split[10]])
    print(len(labels))
    counter = 0
    csv_rows = []
    state_counter = {"stop": 0, "warning": 0, "go": 0}

    for label in labels:
        image = cv.imread('./Lara3D/frame_{}.jpg'.format(label[0]))
        bndymin = int(label[2])
        bndymax = int(label[4])
        bndxmin = int(label[1])
        bndxmax = int(label[3])
        width = bndxmax - bndxmin
        height = bndymax - bndymin
        if bndymin < 0 and abs(bndymin) / height >= 0.125:
            continue
        if bndymax > image.shape[0] and (bndymax - image.shape[0]) / height >= 0.125:
            continue
        if bndxmin < 0 and abs(bndxmin) / width >= 0.5:
            continue
        if bndxmax > image.shape[1] and (bndxmax - image.shape[1]) / width >= 0.5:
            continue

        ymin = max(bndymin, 0)
        ymax = min(bndymax, image.shape[0])
        xmin = max(bndxmin, 0)
        xmax = min(bndxmax, image.shape[1])

        width = xmax - xmin
        height = ymax - ymin
        if width < 8 or height < 8:
            continue
        difference = height - width

        x_left, x_right, y_up, y_down = xmin, xmax, ymax, ymin
        if difference < 0:
            difference = abs(difference)
            y_down, y_up = crop2square(ymin, ymax, difference)
        else:
            x_left, x_right = crop2square(xmin, xmax, difference)
        y_down, y_up, x_left, x_right = shift(y_down, y_up, x_left, x_right, image.shape)

        # print(
        #     f"Frame num: {label[0]}, difference: {difference}, x_left: {x_left}, x_right: {x_right}, y_down: {y_down}, y_up: {y_up}")

        roi = image[y_down:y_up, x_left:x_right]
        dimension = (69, 69)
        resized = cv.resize(roi, dimension, interpolation=cv.INTER_AREA)
        cv.imwrite(f"./output/object_{str(counter).zfill(6)}.jpg", resized)

        csv_rows.append([str(counter).zfill(6), label[5], label[6]])

        counter += 1
        state_counter[label[-1]] += 1

    with open('./output/labels.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerows(csv_rows)

    print(counter)
    print(state_counter)
