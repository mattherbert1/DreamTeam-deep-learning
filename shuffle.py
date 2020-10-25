import csv

import numpy as np

if __name__ == "__main__":
    valid_split = 0.2
    test_split = 0.1

    label_dict = {}
    result_train, result_valid, result_test = [], [], []
    with open('./output/labels.csv') as file:
        for row in file:
            row_split = row.rstrip().split(',')
            label_dict.setdefault((row_split[-2], row_split[-1]), []).append(row_split)

    for label_specific_objects in label_dict.values():
        nb_samples = len(label_specific_objects)
        train = label_specific_objects[0:int(nb_samples * (1 - valid_split - test_split))]
        valid = label_specific_objects[
                int(nb_samples * (1 - valid_split - test_split)):int(nb_samples * (1 - test_split))]
        test = label_specific_objects[int(nb_samples * (1 - test_split)):]
        result_train.extend(train)
        result_valid.extend(valid)
        result_test.extend(test)

    with open('./carla-dataset/labels.csv') as file:
        for row in file:
            row_split = row.rstrip().split(',')
            result_test.append(row_split)

    result_train, result_valid, result_test = np.array(result_train), np.array(result_valid), np.array(result_test)

    randperm = np.random.permutation(len(result_train))
    result_train = result_train[randperm]

    with open('./output/train_labels.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerows(result_train)

    with open('./output/valid_labels.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerows(result_valid)

    with open('./output/test_labels.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerows(result_test)

