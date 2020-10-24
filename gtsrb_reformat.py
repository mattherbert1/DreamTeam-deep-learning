import cv2 as cv
from itertools import islice
import os

if __name__ == "__main__":
    sign_ids = ['00000', '00001', '00002', '00003',
                '00004', '00005', '00013', '00014']
    sign_labels = ['speedlimit', 'yield', 'stop']
    counter = 0

    with open(f'./output/labels.csv', "r") as file:
        for line in file:
            pass
        last_line = line
        counter = int(last_line.rstrip().split(',')[0])
    label_counter = counter

    with open(f'./output/labels.csv', "a") as csv_output_file:
        csv_output_file.write("\n")
        for sign_id in sign_ids:
            with open(f'./GTSRB/Final_Training/Images/{sign_id}/GT-{sign_id}.csv') as csv_input_file:
                for row in islice(csv_input_file, 1, None):
                    label_counter += 1
                    row_split = row.rstrip().split(';')
                    csv_output_file.write(f"{str(label_counter).zfill(6)},TrafficSign,")
                    if int(row_split[-1]) in range(0, 6):
                        csv_output_file.write(f"{str(sign_labels[0])}\n")
                    elif row_split[-1] == "13":
                        csv_output_file.write(f"{str(sign_labels[1])}\n")
                    elif row_split[-1] == "14":
                        csv_output_file.write(f"{str(sign_labels[2])}\n")

    for sign_id in sign_ids:
        ppm_filenames = [f"./GTSRB/Final_Training/Images/{sign_id}/{filename}" for filename in
                         os.listdir(f"./GTSRB/Final_Training/Images/{sign_id}") if
                         filename.endswith('.ppm')]
        for ppm_file in ppm_filenames:
            counter += 1
            image = cv.imread(ppm_file)
            dimension = (69, 69)
            resized = cv.resize(image, dimension, interpolation=cv.INTER_AREA)
            cv.imwrite(f"./output/object_{str(counter).zfill(6)}.jpg", resized)
