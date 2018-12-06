import sys
import csv
import operator

def readCsvFile(file):
    listOfRawText = []
    with open(file, 'r') as csvFile:
        csvReader = csv.reader(csvFile)
        for row in csvReader:
            listOfRawText.append(row)
    csvFile.close()
    #for row in listOfRawText:
        #print (row)
    return listOfRawText


def getFeaturesDictFromRawText(listOfRawText):
    wholeText = []
    for i in range(1, len(listOfRawText)):
        sentence = ""
        for j in range(len(listOfRawText[i])):
            if j == 2:
                sentence += 'year of ' + listOfRawText[i][j] + ' '
            elif j == 4:
                sentence += 'Engine HP ' + listOfRawText[i][j] + ' '
            elif j == 5:
                sentence += 'Engine Cylinders ' + listOfRawText[i][j] + ' '
            elif j == 8:
                sentence += 'Number of Doors ' + listOfRawText[i][j] + ' '
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


def inferenceExactMatch(data,parameters):
    for j in len(parameters):
        if parameters[j] != '-1':
            parameter =  parameters[j]
            resList = []


def getScore(query, doc):
    #exact match
    score = 0
    wordsOfQuery = query.lower().split()
    wordsOfDoc = doc.lower().split()
    for word1 in wordsOfQuery:
        if word1 in wordsOfDoc:
            if word1 == wordsOfDoc[0]:
                score += 30000
            else:
                score += 10000
    return score



def getBM25Score(query, doc, docLen):
    wordsOfQuery = query.lower().split()
    wordsOfDoc = doc.lower().split()

    k1 = 1.5
    b = 0.9
    k3 = 500

    for word1 in wordsOfQuery:
        if word1 in wordsOfDoc:

            # idf = math.log((sd.num_docs - sd.doc_count + 0.5) / (sd.doc_count + 0.5))
            # tf = (k1 + 1) * sd.doc_term_count / (k1 * (1 - b + b * sd.doc_size / sd.avg_dl) + sd.doc_term_count)
            # qtf = (k3 + 1) * sd.query_term_weight / (k3 + sd.query_term_weight)
            # res = idf * tf * qtf

            idf = math.log((docLen - sd.doc_count + 0.5) / (sd.doc_count + 0.5))
            tf = (k1 + 1) * sd.doc_term_count / (k1 * (1 - b + b * sd.doc_size / sd.avg_dl) + sd.doc_term_count)
            qtf = (k3 + 1) * sd.query_term_weight / (k3 + sd.query_term_weight)
            res = idf * tf * qtf


    return res

def getNumberOfDocs(listOfRawText):
    return len(listOfRawText) - 1

# def docTermCount(listOfRawText, term):
#     for line in listOfRawText:
#         wordsOfDoc = line.lower().split()
#     for word1 in wordsOfDoc:



def rankDoc(query, docList, rankResNum, listOfRawText):
    scoreDict = {}
    resDocList = []
    for index in range(len(docList)):
        score = getScore(query, docList[index])
        scoreDict[index] = score
    sortedDict = sorted(scoreDict.items(), key = operator.itemgetter(1), reverse=True)
    # print (sortedDict)
    for i in range(rankResNum):
        index = sortedDict[i][0]
        resDocList.append(listOfRawText[index + 1])
    return(resDocList)


listOfRawText = readCsvFile(sys.argv[1])
docList = getFeaturesDictFromRawText(listOfRawText)
rankResNum = 100
resDocList = rankDoc('ford crown 2009 victoria', docList, rankResNum, listOfRawText)
[print(item) for item in resDocList]

