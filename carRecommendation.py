import sys
import csv
import operator
import math
import numpy as np
from flask import Flask, render_template, request, url_for

price_history = []
make_history = []


# need to call at the beginning of the project
def readCsvFile(file):
    listOfRawText = []
    with open(file, 'r') as csvFile:
        csvReader = csv.reader(csvFile)
        for row in csvReader:
            listOfRawText.append(row)
    csvFile.close()
    #for row in listOfRawText:
        #print (row)
    return listOfRawText[1:]


def getFeaturesDictFromRawText(listOfRawText):
    wholeText = []
    for i in range(len(listOfRawText)):
        sentence = ""
        for j in range(len(listOfRawText[i])):
            if j == 2:
                sentence += 'year' + listOfRawText[i][j] + ' '
            elif j == 4:
                sentence += 'Engine HP ' + listOfRawText[i][j] + ' '
            elif j == 5:
                sentence += 'Engine Cylinders ' + listOfRawText[i][j] + ' '
            elif j == 8:
                sentence += 'Doors Number ' + listOfRawText[i][j] + ' '
            elif j == 12:
                sentence += 'highway MPG ' + listOfRawText[i][j] + ' '
            elif j == 13:
                sentence += 'city mpg' + listOfRawText[i][j] + ' '
            elif j == 14:
                continue
            elif j == 15:
                sentence += 'price ' + listOfRawText[i][j]
            else:
                sentence += listOfRawText[i][j] + ' '
        wholeText.append(sentence)

    #[print(item) for item in wholeText]
    return wholeText


def buildDocCountDict(docList):
    dictOfDocCount = {}
    for doc in docList:
        wordsOfDoc = doc.lower().split()
        for word in wordsOfDoc:
            if word in dictOfDocCount.keys():
                dictOfDocCount[word] += 1
            else:
                dictOfDocCount[word] = 1
    return dictOfDocCount

# def getScore(query, doc):
#     #exact match
#     score = 0
#     wordsOfQuery = query.lower().split()
#     wordsOfDoc = doc.lower().split()
#     for word1 in wordsOfQuery:
#         if word1 in wordsOfDoc:
#             if word1 == wordsOfDoc[0]:
#                 score += 30000
#             else:
#                 score += 10000
#     return score


def getBM25Score(query, doc, numberOfDoc, avgLenOfDoc, dictOfDocCount):
    wordsOfQuery = query.lower().replace('fancy', 'exotic,luxury')
    wordsOfQuery = wordsOfQuery.replace('rich', '300000 dollar')
    wordsOfQuery = wordsOfQuery.replace('fastest', 'exotic,performance')
    wordsOfQuery = wordsOfQuery.replace('car', 'cars')
    wordsOfQuery = wordsOfQuery.split()
    wordsOfDoc = doc.lower().split()
    res = 0

    k1 = 1.5
    b = 0.9
    k3 = 500

    queryLen = len(query)
    word1Index = 0
    for word1 in wordsOfDoc:
        # if word1 in wordsOfQuery or ('-' in word1 and
        # (word1.split('-')[0] in wordsOfQuery or word1.split('-')[1] in wordsOfQuery)):
        #
        #     docCount = dictOfDocCount[word1]
        #     #docCount = getDocCount(docList, term)
        #     queryTermWeight = 1
        #     if word1 in wordsOfQuery:
        #         queryTermWeight = (queryLen - wordsOfQuery.index(word1)) * 3
        #     else:
        #         queryTermWeight = queryLen
        #
        #     idf = math.log((numberOfDoc - docCount + 0.5) / (docCount + 0.5))
        #     tf = (k1 + 1) * 1 / (k1 * (1 - b + b * len(wordsOfDoc) / avgLenOfDoc) + 1)
        #     qtf = (k3 + 1) * queryTermWeight / (k3 + queryTermWeight)
        #     res += idf * tf * qtf

        for word2 in wordsOfQuery:
            if word1 == word2 or (len(word2) >= 3 and (word1Index == 0 or word1Index == 9) and (not word2.isdigit()) and word1.find(word2) >= 0):
                docCount = dictOfDocCount[word1]
                #docCount = getDocCount(docList, term)
                queryTermWeight = 1
                if word2 in wordsOfQuery:
                    queryTermWeight = (queryLen - wordsOfQuery.index(word2)) * 3
                else:
                    queryTermWeight = queryLen

                idf = math.log((numberOfDoc - docCount + 0.5) / (docCount + 0.5))
                tf = (k1 + 1) * 1 / (k1 * (1 - b + b * len(wordsOfDoc) / avgLenOfDoc) + 1)
                qtf = (k3 + 1) * queryTermWeight / (k3 + queryTermWeight)
                res += idf * tf * qtf



        if word1.isdigit():
            num = int(word1)
            # deal with year difference
            if num <= 2018 and num >= 1990 and not num == 2000:
                for word2 in wordsOfQuery:
                    if word2.isdigit():
                        num2 = int(word2)
                        if num2 <= 2018 and num2 >= 1990 and not num2 == 2000:
                            res -= abs(num - num2) * 0.05

            #deal with price difference
            if wordsOfDoc[word1Index - 1] == 'price':
                for j in range(len(wordsOfQuery)):
                    if wordsOfQuery[j].isdigit() and j + 1 != len(wordsOfQuery) and wordsOfQuery[j + 1] == 'dollar':
                        res -= abs(int(word1) - int(wordsOfQuery[j])) * 0.0005
        word1Index += 1
    #print(res)
    return res


def getNumberOfDocs(docList):
    return len(docList)

# def getDocCount(docList, term):
#     count = 0
#     for line in docList:
#         wordsOfDoc = line.lower().split()
#         if term.lower() in wordsOfDoc:
#             count += 1
#     return count


def getAvgLenOfDoc(docList):
    counter = 0
    for line in docList:
        counter += len(line.split())
    return counter / len(docList)


def rankDoc(query, docList, rankResNum, listOfRawText, dictOfDocCount):
    numberOfDoc = getNumberOfDocs(docList)
    avgLenOfDoc = getAvgLenOfDoc(docList)

    scoreDict = {}
    resDocList = []
    for index in range(len(docList)):
        #score = getScore(query, docList[index])
        score = getBM25Score(query, docList[index], numberOfDoc, avgLenOfDoc, dictOfDocCount)

        scoreDict[index] = score

    sortedDict = sorted(scoreDict.items(), key = operator.itemgetter(1), reverse=True)
    # print (sortedDict)
    for i in range(rankResNum):
        index = sortedDict[i][0]
        resDocList.append(listOfRawText[index])
    return(resDocList)


def getMakeTypeNum(listOfRawText):
    tempDict = {}
    for i in range(1, len(listOfRawText)):
        if not listOfRawText[i][0] in tempDict.keys():
            tempDict[listOfRawText[i][0]] = 1
    # for key in tempDict.keys():
    #     print(key)
    # print (len(tempDict))
    return len(tempDict)


def recommendation_system(price_list, make_list):
    dist_recommendation = {}
    total_price = 0
    num_price = len(price_list)
    for price in price_list:
        total_price += int(price)
    mean_price = float(total_price) / num_price
    list_raw_predictons = readCsvFile(sys.argv[2])
    for item in list_raw_predictons:
        entry = item[0] + " $" + item[1]
        if entry not in dist_recommendation:
            dist_recommendation[entry] = np.absolute(int(item[1]) - mean_price)
    sorted_rec = [(k, dist_recommendation[k]) for k in sorted(dist_recommendation, key=dist_recommendation.get, reverse=False)]
    recommend_list = []
    for k, v in sorted_rec:
        for make in make_list:
            if make in str(k).split(" "):
                recommend_list.append(str(k).split(" "))
                break
        if len(recommend_list) >= 5:
            break
    return recommend_list

app = Flask(__name__)

@app.route('/')
def car_search():
    return render_template('index.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      listOfRawText = readCsvFile(sys.argv[1])
      listOfRawText = np.random.permutation(listOfRawText)
      docList = getFeaturesDictFromRawText(listOfRawText)
      dictOfDocCount = buildDocCountDict(docList)
      rankResNum = 30
      resDocList = rankDoc(str(result['query']), docList, rankResNum, listOfRawText, dictOfDocCount)
      price_history.append(resDocList[0][15])
      make_history.append(resDocList[0][0])
      return render_template("result.html", result=resDocList)

@app.route('/back')
def backtohome():
    recommendations = []
    if len(price_history) >= 1:
        recommendations = recommendation_system(price_history, make_history)
    return render_template('index.html', rec=recommendations)

if __name__ == '__main__':
   app.run(debug=True)