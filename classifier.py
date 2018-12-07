import sys
import csv
import operator
import math
import numpy as np


def read_csv(file):
    raw_list = []
    with open(file, 'r') as csvFile:
        csv_reader = csv.reader(csvFile)
        for row in csv_reader:
            raw_list.append(row)
    csvFile.close()
    return raw_list[1:]


def random_split(listOfRawText):
    index = np.random.permutation(len(listOfRawText))
    train_list = []
    dev_list = []
    for i in range(0, int(len(index) * 0.8)):
        train_list.append(listOfRawText[index[i]])
    for i in range(int(len(index) * 0.8), len(index)):
        dev_list.append(listOfRawText[index[i]])
    return train_list, dev_list


def feature_selection(train_dev_data, test_data):
    train_dev = []
    test = []
    for item in train_dev_data:
        train_dev.append([item[0].lower(), item[1].lower(), item[2], item[4], item[5],
                          item[6].lower(), item[7].split(" ")[0].lower(), item[12], item[13]])
    for item in test_data:
        test.append([item[11].lower(), item[9].split(" ")[2].lower(), item[17], item[7], item[3].split(" ")[2],
                     item[1].split(" ")[0].lower(), item[2].split(" ")[0].split("-")[0].lower(), item[6], item[0]])
    return train_dev, test


def feature_revise(raw_feature):
    make = []
    model = []
    transmission = []
    drive = []
    print(raw_feature)
    for item in raw_feature:
        if item[0] not in make:
            make.append(item[0])
        if item[1] not in model:
            model.append(item[1])
        if item[5] not in transmission:
            transmission.append(item[5])
        if item[6] not in drive:
            drive.append(item[6])
    print(make)
    print(model)
    print(transmission)
    print(drive)
    print(drive.index("four"))


list_raw_train_dev = read_csv("data.csv")
list_raw_test = read_csv("cars.csv")
raw_feature_train_dev, raw_feature_test = feature_selection(list_raw_train_dev, list_raw_test)
print([item for item in raw_feature_train_dev][0:100])
print([item for item in raw_feature_test][0:100])
# train_data, dev_data = random_split(list_raw)
# dev_set = feature_selection(dev_data)
# train_set = feature_selection(train_data)
# dev_rev = feature_revise(dev_set)

