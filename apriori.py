import sys

def roundJihoon(f, n):
  return round(f + 0.00000000000001, n)


def main(argv):

    relativeMinSupport = int(argv[1])
    inputFile = argv[2]
    outputFile = argv[3]

    
    #[FILE READ]
    f = open(inputFile, 'r', encoding='utf-8')

    #[VALUE INITIALIZE]
    tempSet = set()
    transactionList = list()
    wholeItemSet = set()
    C = dict()
    L = set()
    frequentItemDict = dict()
    frequentItemSet = set()
    infrequentItemSet = set()
    

    #[SAVE ALL TRANSACTION AS A LIST]
    #transactionList : List of whole transaction
    #wholeItemSet    : Whole item category of whole transaction
    while True:
        line = f.readline()
        if line != "":
            tempSet = set(map(int,line.split()))
            transactionList = transactionList+[tempSet]
            wholeItemSet = wholeItemSet|tempSet
        else:
            break
    f.close()




    #[CACULATE ABSOLUTE MINIMUM SUPPORT]
    #wholeTransactionSize : Size of whole transaction
    #absMinSupport        : Absolute minimum support count
    wholeTransactionSize=len(transactionList)
    absMinSupport = relativeMinSupport / 100.0 * wholeTransactionSize



    #[INITIAL STEP FOR COUNTING]
    # C : Initial C (C1)
    for i in transactionList:
        for j in i:
            if frozenset([j]) in C:
                C[frozenset([j])]=C[frozenset([j])]+1
            else:
                C[frozenset([j])]=1



    #[CANDIDATE GENERATION]
    outputLength=2
    while True:
        L = set()
        for elem in C:
            if C[elem] >= absMinSupport:
                L.add(elem)
                frequentItemSet.add(elem)
                frequentItemDict[elem]=C[elem]
            else:
                infrequentItemSet.add(elem)
        Cset = set()
        C = dict()
        if len(L)==0:
            break
        for i in L:
            for j in L:
                join = i|j
                if len(join)==outputLength:
                    Cset.add(join)

        prunedCset = set()
        for i in Cset:
            validation = 1
            for j in infrequentItemSet:
                if j in i:
                    validation = 0
                    #print("pruned! :",i)
            if validation ==1:
                prunedCset.add(i)

        for i in prunedCset:
            for j in transactionList:
                if i<=j:
                    if i in C:
                        C[i]=C[i]+1
                    else:
                        C[i]=1
        outputLength=outputLength+1



    fout = open(outputFile, 'wt', encoding='utf-8')

    #[GENERATING ASSOCIATION RULES]
    for i in frequentItemDict:
        for j in frequentItemDict:
            if (len(i&j)==0) and ((i|j) in frequentItemDict):
                jihoonPrint=str(set(i)) + "\t"+str(set(j))+"\t"+str(roundJihoon(frequentItemDict[i|j]/wholeTransactionSize*100.0,2))+"\t"+str(roundJihoon(frequentItemDict[i|j]/frequentItemDict[i]*100.0,2))
                jihoonPrint=jihoonPrint.replace(" ","")
                fout.write(jihoonPrint + '\n')

    fout.close()
if __name__=='__main__':
    main(sys.argv)

