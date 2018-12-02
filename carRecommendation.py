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


def getFeaturesFromRawText(listOfRawText):
    for i in range(1, len(listOfRawText)):
        #print (listOfRawText[0])
        price = listOfRawText[i][15]
        print (price)
        return price



listOfRawText = readCsvFile(sys.argv[1])
price = getFeaturesFromRawText(listOfRawText)
print(price)