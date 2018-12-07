import sys
import csv
import operator
import math
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import tree
from sklearn import svm
from sklearn.linear_model import LogisticRegression
#   since year only have 2009 to 2012, we don't use this feature
#   range: f3,f7,f8 (distribution)
#   value: f4 (number)
#   tf: f1,f2,f5,f6 (map)


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
        train_dev.append([item[0].lower(), item[1].lower(), item[4], item[5],
                          item[6].lower(), item[7].split(" ")[0].lower(), item[12], item[13]])
    for item in test_data:
        test.append([item[11].lower(), item[9].split(" ")[2].lower(), item[7], item[3].split(" ")[2],
                     item[1].split(" ")[0].lower(), item[2].split(" ")[0].split("-")[0].lower(), item[6], item[0]])
    return train_dev, test


def feature_revise(raw_train_dev, raw_test):
    d1 = {}
    d2 = {}
    d3 = {}
    d4 = {}
    d5 = {}
    d6 = {}
    d7 = {}
    d8 = {}
    dics = [d1, d2, d3, d4, d5, d6, d7, d8]
    for items in raw_train_dev:
        for i in range(8):
            if items[i] not in dics[i]:
                dics[i][items[i]] = 1
            else:
                dics[i][items[i]] += 1
    print(dics[7])
    # lists = sorted(dics[7].items())
    # x, y = zip(*lists)
    # plt.plot(x, y)
    # plt.show()
    d1 = {}
    d2 = {}
    d3 = {}
    d4 = {}
    d5 = {}
    d6 = {}
    d7 = {}
    d8 = {}
    dics = [d1, d2, d3, d4, d5, d6, d7, d8]
    for items in raw_test:
        for i in range(8):
            if items[i] not in dics[i]:
                dics[i][items[i]] = 1
            else:
                dics[i][items[i]] += 1
    print(dics[7])
    # lists = sorted(dics[7].items())
    # x, y = zip(*lists)
    # plt.plot(x, y)
    # plt.show()


# list_raw_train_dev = read_csv("data.csv")
# list_raw_test = read_csv("cars.csv")
# raw_feature_train_dev, raw_feature_test = feature_selection(list_raw_train_dev, list_raw_test)
# feature_revise(raw_feature_train_dev, raw_feature_test)

data = read_csv("data.csv")
Y = []
corpus = []
for line in data:
    if int(line[-1]) < 10000:
        Y.append(0)
    elif int(line[-1]) >= 10000 and int(line[-1]) < 30000:
        Y.append(1)
    elif int(line[-1]) >= 30000 and int(line[-1]) < 50000:
        Y.append(2)
    elif int(line[-1]) >= 50000 and int(line[-1]) < 70000:
        Y.append(3)
    else:
        Y.append(4)
    corp = ""
    for i in range(len(line)-1):
        corp += (line[i] + " ")
    corpus.append(corp)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus).toarray()
X1 = vectorizer.fit_transform(corpus)

# print(X[0])
# data_set = []
# for i in range(len(X)):
#     data_set.append((X[i], Y[i]))
# print(len(X))
# print(len(Y))
train_X = X1[:int(len(X)*0.8)]
train_Y = Y[:int(len(Y)*0.8)]
dev_X = X1[int(len(Y)*0.8):]
dev_Y = Y[int(len(Y)*0.8):]

clf = LogisticRegression(C=1e5, solver='lbfgs', multi_class='multinomial').fit(train_X, train_Y)
# clf = svm.SVC(gamma='scale').fit(train_X, train_Y)
# clf = tree.DecisionTreeClassifier().fit(train_X, train_Y)
# clf = MultinomialNB().fit(train_X, train_Y)
predicted = clf.predict(dev_X)
print(predicted)
print(dev_Y)
correct = 0
total = 0
for i in range(len(predicted)):
    if predicted[i] == dev_Y[i]:
        correct += 1
    total += 1
accuracy = float(correct / total)
print(accuracy)
