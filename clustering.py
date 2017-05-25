import sys
import random
import math

def fileRead(inputFile):
    f = open(inputFile, 'r', encoding='utf-8')
    objectList = list()
    while True:
        line = f.readline()
        if line != "":
            temp = line.split()
            temp[0] = int(temp[0])
            temp[1] = float(temp[1])
            temp[2] = float(temp[2])
            objectList.append(temp + [None])
        else:
            break
    f.close()
    return objectList

def fileWrite(classList,inputFile):
    i = -1
    for cls in classList:
        i = i+1
        outputFile = inputFile[0:len(inputFile)-4]+'_cluster_'+str(i)+'.txt'
        fout = open(outputFile, 'wt', encoding='utf-8')
        for element in cls:
            fout.write(str(element) + '\n')
        fout.close()


def calculateDistance(x1,y1,x2,y2):
    result = math.sqrt(((x1-x2)*(x1-x2))+((y1-y2)*(y1-y2)))
    return result

def returnNeighborhood(object, Eps, objectList):
    returnList = list()
    for i in objectList:
        if Eps>=calculateDistance(object[1],object[2],i[1],i[2]):
            returnList.append(i)
    returnList.remove(object)
    return returnList

def dbscan(objectList,Eps,MinPts):
    unvisitedList = objectList[:]

    classList = list()

    while unvisitedList!=[]:
        p = random.choice(unvisitedList)
        unvisitedList.remove(p)
        p = objectList[p[0]]
        neigh=returnNeighborhood(p,Eps,objectList)
        if len(neigh)>=MinPts:
            classCount = classCount + 1
            classTempList = list()
            p[3] = classCount
            classTempList = classTempList+[p[0]]
            N = neigh[:]
            idx = 0
            while True:
                if idx == len(N)-1:
                    break
                p_ = N[idx]
                print("this time N is: ",len(N))
                if unvisitedList.__contains__(p_):
                    unvisitedList.remove(p_)
                    p_neigh = returnNeighborhood(p_,Eps,objectList)
                    if len(p_neigh)>=MinPts:
                        N= N + p_neigh
                if objectList[p_[0]][3]==None:
                    objectList[p_[0]][3]=classCount
                    classTempList = classTempList + [objectList[p_[0]][0]]
                idx = idx+1
            print("one class is over")
            classTempList.sort()
            classList = classList+[classTempList]
        else:
            p[3] = 'noise'
    return classList

def removeUnintendedClass(classList,n):
    while len(classList)!=n:
        min =  len(classList[0])
        min_idx = 0
        for cls in range(len(classList)):
            if len(classList[cls]) < min:
                min = len(classList[cls])
                min_idx = cls
        classList.remove(classList[min_idx])


def main(argv):
    
    #Argv Input
    inputFile = argv[1]
    n = int(argv[2])
    Eps = int(argv[3])
    MinPts = int(argv[4])

    print("number of class :",n)
    print("Eps :",Eps)
    print("MinPts :",MinPts)
    
    #Class Name 0,1,2,3,4, ....
    classCount=-1


    # FileRead
    objectList = fileRead(inputFile)

    classList=dbscan(objectList,Eps,MinPts)

    removeUnintendedClass(classList,n)

    fileWrite(classList,inputFile)


if __name__ == '__main__':
    main(sys.argv)
