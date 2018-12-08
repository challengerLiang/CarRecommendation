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


def random_split(data):
    index = np.random.permutation(len(data))
    train_list = []
    dev_list = []
    for i in range(0, int(len(index) * 0.8)):
        train_list.append(data[index[i]])
    for i in range(int(len(index) * 0.8), len(index)):
        dev_list.append(data[index[i]])
    return train_list, dev_list


def feature_selection(train_dev_data, test_data):
    train_dev = []
    test = []
    for item in train_dev_data:
        train_dev.append([item[0].lower(), item[1].lower(), item[4], item[5],
                          item[6].lower(), item[7].split(" ")[0].lower(), item[12], item[13], item[-1]])
    for item in test_data:
        test.append([item[11].lower(), item[9].split(" ")[2].lower(), item[7], item[3].split(" ")[2],
                     item[1].split(" ")[0].lower(), item[2].split(" ")[0].split("-")[0].lower(), item[6], item[0]])
    return train_dev, test


def feature_revise(raw_train_dev, raw_test):
    revise_train_dev = []
    revise_test = []
    raw_total = raw_train_dev + raw_test
    make = []
    model = []
    cylinders = ['6', '4', '5', '8', '12', '0', '10', '3', '16']
    transmission = []
    drive = []
    for items in raw_total:
        if items[0] not in make:
            make.append(items[0])
        if items[1] not in model:
            model.append(items[1])
        if items[4] not in transmission:
            transmission.append(items[4])
        if items[5] not in drive:
            drive.append(items[5])

    for items in raw_train_dev:
        hp = -1
        if not items[2] == '':
            hp = int(items[2])
        else:
            hp = 400
        vec_2 = -1
        if hp < 150:
            vec_2 = 0
        elif hp >= 150 and hp < 250:
            vec_2 = 1
        elif hp >= 250 and hp < 350:
            vec_2 = 2
        elif hp >= 350 and hp < 450:
            vec_2 = 3
        elif hp >= 450 and hp < 550:
            vec_2 = 4
        else:
            vec_2 = 5
        hw_mpg = int(items[6])
        ct_mpg = int(items[7])
        vec_6 = -1
        vec_7 = -1
        if hw_mpg < 17:
            vec_6 = 0
        elif hw_mpg >= 17 and hw_mpg < 23:
            vec_6 = 1
        elif hw_mpg >= 23 and hw_mpg < 27:
            vec_6 = 2
        else:
            vec_6 = 3
        if ct_mpg < 12:
            vec_7 = 0
        elif ct_mpg >= 12 and hw_mpg < 18:
            vec_7 = 1
        elif ct_mpg >= 18 and hw_mpg < 22:
            vec_7 = 2
        else:
            vec_7 = 3

        vec_3 = 0
        if items[3] in cylinders:
            vec_3 = int(items[3])

        gold = -1
        price = int(items[-1])
        if price < 10000:
            gold = 0
        elif price >= 10000 and price < 30000:
            gold = 1
        elif price >= 30000 and price < 50000:
            gold = 2
        elif price >= 50000 and price < 70000:
            gold = 3
        # elif price >= 40000 and price < 50000:
        #     gold = 4
        # elif price >= 50000 and price < 60000:
        #     gold = 5
        # elif price >= 60000 and price < 70000:
        #     gold = 6
        # elif price >= 70000 and price < 100000:
        #     gold = 7
        # elif price >= 100000 and price < 200000:
        #     gold = 8
        else:
            gold = 4

        revise_train_dev.append([make.index(items[0]), model.index(items[1]), vec_2, vec_3,
                                 transmission.index(items[4]), drive.index(items[5]), vec_6, vec_7, gold])

    for items in raw_test:
        hp = -1
        if not items[2] == '':
            hp = int(items[2])
        else:
            hp = 400
        vec_2 = -1
        if hp < 150:
            vec_2 = 0
        elif hp >= 150 and hp < 250:
            vec_2 = 1
        elif hp >= 250 and hp < 350:
            vec_2 = 2
        elif hp >= 350 and hp < 450:
            vec_2 = 3
        elif hp >= 450 and hp < 550:
            vec_2 = 4
        else:
            vec_2 = 5
        hw_mpg = int(items[6])
        ct_mpg = int(items[7])
        vec_6 = -1
        vec_7 = -1
        if hw_mpg < 17:
            vec_6 = 0
        elif hw_mpg >= 17 and hw_mpg < 23:
            vec_6 = 1
        elif hw_mpg >= 23 and hw_mpg < 27:
            vec_6 = 2
        else:
            vec_6 = 3
        if ct_mpg < 12:
            vec_7 = 0
        elif ct_mpg >= 12 and hw_mpg < 18:
            vec_7 = 1
        elif ct_mpg >= 18 and hw_mpg < 22:
            vec_7 = 2
        else:
            vec_7 = 3

        vec_3 = -1
        if items[3] in cylinders:
            vec_3 = int(items[3])

        revise_test.append([make.index(items[0]), model.index(items[1]), vec_2, vec_3,
                            transmission.index(items[4]), drive.index(items[5]), vec_6, vec_7])

    return revise_train_dev, revise_test


def feature_check(raw_train_dev, raw_test):
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
    print(dics[5])
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
    print(dics[5])
    # lists = sorted(dics[7].items())
    # x, y = zip(*lists)
    # plt.plot(x, y)
    # plt.show()


def split_x_y(data):
    x_list = []
    y_list = []
    for items in data:
        x_list.append(items[0:-1])
        y_list.append(items[-1])
    return x_list, y_list


def train_evaluation(classifier, train_x, train_y, dev_x, dev_y):
    model = classifier.fit(train_x, train_y)
    predicted = model.predict(dev_x)
    correct = 0
    total = 0
    for i in range(len(predicted)):
        if predicted[i] == dev_y[i]:
            correct += 1
        total += 1
    accuracy = float(correct / total)
    return model, accuracy


list_raw_train_dev = read_csv("data.csv")
list_raw_test = read_csv("cars.csv")
raw_feature_train_dev, raw_feature_test = feature_selection(list_raw_train_dev, list_raw_test)
# feature_check(raw_feature_train_dev, raw_feature_test)
train_dev, test = feature_revise(raw_feature_train_dev, raw_feature_test)
train, dev = random_split(train_dev)
train_X, train_Y = split_x_y(train)
dev_X, dev_Y = split_x_y(dev)
model, accuracy = train_evaluation(MultinomialNB(), train_X, train_Y, dev_X, dev_Y)
print(accuracy)



# tf-idf-vectorizer:

# data = read_csv("data.csv")
# Y = []
# corpus = []
# for line in data:
#     if int(line[-1]) < 10000:
#         Y.append(0)
#     elif int(line[-1]) >= 10000 and int(line[-1]) < 30000:
#         Y.append(1)
#     elif int(line[-1]) >= 30000 and int(line[-1]) < 50000:
#         Y.append(2)
#     elif int(line[-1]) >= 50000 and int(line[-1]) < 70000:
#         Y.append(3)
#     else:
#         Y.append(4)
#     corp = ""
#     for i in range(len(line)-1):
#         corp += (line[i] + " ")
#     corpus.append(corp)
#
# vectorizer = TfidfVectorizer()
# X = vectorizer.fit_transform(corpus).toarray()
# X1 = vectorizer.fit_transform(corpus)
#
# train_X = X1[:int(len(X)*0.8)]
# train_Y = Y[:int(len(Y)*0.8)]
# dev_X = X1[int(len(Y)*0.8):]
# dev_Y = Y[int(len(Y)*0.8):]

# clf = LogisticRegression(C=1e5, solver='lbfgs', multi_class='multinomial').fit(train_X, train_Y)
# clf = svm.SVC(gamma='scale').fit(train_X, train_Y)
# clf = tree.DecisionTreeClassifier().fit(train_X, train_Y)
# clf = MultinomialNB().fit(train_X, train_Y)

# predicted = clf.predict(dev_X)
# print(predicted)
# print(dev_Y)
# correct = 0
# total = 0
# for i in range(len(predicted)):
#     if predicted[i] == dev_Y[i]:
#         correct += 1
#     total += 1
# accuracy = float(correct / total)
# print(accuracy)
