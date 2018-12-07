import sys
import csv
import operator
import math
import numpy as np


def read_csv(file):
    listOfRawText = []
    with open(file, 'r') as csvFile:
        csvReader = csv.reader(csvFile)
        for row in csvReader:
            listOfRawText.append(row)
    csvFile.close()
    return listOfRawText[1:]


def random_split(listOfRawText):
    index = np.random.permutation(len(listOfRawText))
    train_list = []
    dev_list = []
    for i in range(0, int(len(index) * 0.8)):
        train_list.append(listOfRawText[index[i]])
    for i in range(int(len(index) * 0.8), len(index)):
        dev_list.append(listOfRawText[index[i]])
    return train_list, dev_list

def feature_selection(raw_data):
    data = []
    for item in raw_data:
        data.append([item[0].lower(), item[1].lower(), item[2], item[4], item[5],
                     item[6].lower(), item[7].split(" ")[0].lower(), item[12], item[13]])
    return data

list_raw = read_csv("data.csv")
train_data, dev_data = random_split(list_raw)
dev_set = feature_selection(dev_data)
print(dev_set)

