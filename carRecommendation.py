import sys
import csv
import numpy as np


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
        print (listOfRawText[0])
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

    [print(item) for item in wholeText]
    return wholeText

def inferenceExactMatch(data,parameters):
    for j in len(parameters):
        if parameters[j] != '-1':
            parameter =  parameters[j]
            resList = []


listOfRawText = readCsvFile(sys.argv[1])
price = getFeaturesDictFromRawText(listOfRawText)