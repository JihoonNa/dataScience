import sys
import random
import math
import operator


def main(argv):

    #input file names
    inputFile = argv[1]
    resultFile = argv[2]
    #output file name
    outputFile = inputFile + "_prediction.txt"

    # file read
    objectList = returnToRankVectorDict(inputFile)
    resultList = readResultFile(resultFile)

    #make mean dictionary
    meanDict = makeMeanDict(objectList)

    user = None
    simUserList = None

    #calculate unknown item rank using collaborate filtering
    for pred in resultList:
        if user != pred[0]:
            user = pred[0]
            simUserList = selectSimilarUser(objectList, user, 30)
            #print(user, simUserList)
        sum = 0
        simSum = 0
        compareItem = pred[1]
        for simUser in simUserList:
            similarity = simUser[1]
            simUserRank = objectList[simUser[0]][compareItem]
            if simUserRank != None:
                sum = sum + similarity * (simUserRank-meanDict[simUser[0]])
                simSum = simSum + similarity
        pred[2] = meanDict[user]+sum+0.0000000001/(simSum+0.0000000001)
        if pred[2]<1:
            pred[2] = 1
        if pred[2]>5:
            pred[2] = 5
        #print(pred[2])

        pred[2] = round(pred[2])


    #write result file
    f = open(outputFile, 'w')
    for pred in resultList:
        f.write(str(pred[0])+'\t'+str(pred[1])+'\t'+str(pred[2])+'\n')
    f.close()



#Mean dictionary for every user
def makeMeanDict(objectList):
    meanDict = dict()
    for i in objectList:
        meanDict[i] = mean(objectList[i])
        #print(objectList[i])
        #print(meanDict[i])
    return meanDict

#calculate mean
def mean(itemList):
    summation = 0
    count = 0
    for i in itemList:
        if i != None:
            count = count + 1
            summation = summation + i
    return float(summation) / count

#calculate standard deviation
def std(itemList):
    means = mean(itemList)
    summation = 0
    for i in itemList:
        if i != None:
            summation = summation + ((i - means) * (i - means))
    return math.sqrt(summation)

#calculate similarity
def sim(itemList1, itemList2):
    mean1 = mean(itemList1)
    mean2 = mean(itemList2)
    std1 = std(itemList1)
    std2 = std(itemList2)
    summation = 0
    for i in range(len(itemList1)):
        if (itemList1[i] != None) and (itemList2[i] != None):
            summation = summation + ((itemList1[i] - mean1) * (itemList2[i] - mean2))
    #print("correlation is :", summation)
    #print("std1 :", std1)
    #print("std2 :", std2)
    return float(summation) / (std1 * std2)


#select num similar user
def selectSimilarUser(objectList, user, num):
    simDict = dict()
    for compareUser in objectList:
        simDict[compareUser] = sim(objectList[user], objectList[compareUser])
    del simDict[user]
    sortedSimDict = sorted(simDict.items(), key=operator.itemgetter(1), reverse=True)
    return sortedSimDict[:num]


#read result file for make result
def readResultFile(resultFile):
    f = open(resultFile, 'r', encoding='utf-8')
    resultList = list()
    while True:
        line = f.readline()
        if line != "":
            temp = line.split()
            UserID = int(temp[0])
            ItemID = int(temp[1])
            resultList = resultList+[[UserID,ItemID,None]]
        else:
            break
    f.close()
    return resultList

#make rank vector for recommendation algorithm
def returnToRankVectorDict(inputFile):
    f = open(inputFile, 'r', encoding='utf-8')
    rankData = dict()
    maxItem = 0
    while True:
        line = f.readline()
        if line != "":
            temp = line.split()
            UserID = int(temp[0])
            ItemID = int(temp[1])
            if ItemID > maxItem:
                maxItem = ItemID
            Rank = int(temp[2])
            if UserID not in rankData:
                rankData[UserID] = [None] * 2000
            rankData[UserID][ItemID] = Rank
        else:
            break
    for user in rankData:
        rankData[user] = rankData[user][:maxItem]
    f.close()
    return rankData


if __name__ == '__main__':
    main(sys.argv)

