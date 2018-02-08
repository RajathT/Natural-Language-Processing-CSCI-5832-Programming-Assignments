import csv
import math
filename="hotelNegT-train.txt"

with open(filename,encoding="utf8") as file:
    reader = csv.reader(file,delimiter='\t')
    mainNegList=list(reader)
#print(mainNegList)

#print(len(mainNegList))
mainNegDicCount = {}
indiNegList = []

for i in range(len(mainNegList)):
    #print(mainNegList[i][1])
    indiNegList = mainNegList[i][1].lower().split()
    #print(indiNegList)
    for i in indiNegList:
        i.replace(",", "").replace(".", "").replace("(","").replace(")","").replace("!","")
        if i in mainNegDicCount:
            mainNegDicCount[i] = mainNegDicCount[i] + 1
        else:
            mainNegDicCount[i] = 1

print(mainNegDicCount)
countNeg = 0
for i in mainNegDicCount:
    countNeg = countNeg + mainNegDicCount[i]
#print(countNeg)

filename="hotelPosT-train.txt"

with open(filename,encoding="utf8") as file:
    reader = csv.reader(file,delimiter='\t')
    mainPosList=list(reader)
#print(mainPosList)

#print(len(mainPosList))
mainPosDicCount = {}
indiPosList = []
for i in range(len(mainPosList)):
    #print(mainNegList[i][1])
    indiPosList = mainPosList[i][1].lower().split()
    #print(indiNegList)
    for i in indiPosList:
        i.replace(",", "").replace(".", "").replace("(","").replace(")","").replace("!","")
        if i in mainPosDicCount:
            mainPosDicCount[i] = mainPosDicCount[i] + 1
        else:
            mainPosDicCount[i] = 1

print(mainPosDicCount)

countPos = 0
for i in mainPosDicCount:
    countPos = countPos + mainPosDicCount[i]
#print(countPos)

#print(countPos+countNeg)
for i in mainPosDicCount:
    mainPosDicCount[i]=math.log(mainPosDicCount[i]+1/(countPos+countNeg))
#print(mainPosDicCount)

for i in mainNegDicCount:
    mainNegDicCount[i]=math.log(mainNegDicCount[i]+1/(countPos+countNeg))
#print(mainNegDicCount)

'''if "I" in mainPosDicCount:
    print(mainPosDicCount["I"])'''
#print(len(mainNegDicCount))
for i in mainPosDicCount:
    if i not in mainNegDicCount:
        mainNegDicCount[i]=math.log(1/(countPos+countNeg))

print(mainNegDicCount)
print(len(mainNegDicCount))
#print(len(mainPosDicCount))
for i in mainNegDicCount:
    if i not in mainPosDicCount:
        mainPosDicCount[i]=math.log(1/(countPos+countNeg))
print(mainPosDicCount)
print(len(mainPosDicCount))
#print(countPos+countNeg)


filename="hotel-test.txt"
with open(filename,encoding='mac_roman', newline='') as file:
    reader = csv.reader(file,delimiter='\t')
    '''for row in reader:
        [unicode(cell, 'utf-8') for cell in row]'''
    mainDevList=list(reader)
#print(mainDevList[0][1])
f=open("results.txt","w")
for i in range(len(mainDevList)):
    testList=mainDevList[i][1].lower().split()
    #print(testList)
    posSum = 0
    for j in testList:
        j.replace(",", "").replace(".", "").replace("(","").replace(")","").replace("!","")
        if j in mainPosDicCount:
            posSum=posSum+mainPosDicCount[j]

            #print(posSum)

    negSum = 0
    for j in testList:
        j.replace(",", "").replace(".", "").replace("(","").replace(")","").replace("!","")
        if j in mainPosDicCount:
            negSum=negSum+mainNegDicCount[j]

            #print(negSum)

    if(posSum>negSum):
        finaltag="POS"
    else:
        finaltag="NEG"
    #print(finaltag)

    print(mainDevList[i][0],finaltag)
    f.write(mainDevList[i][0]+"\t"+finaltag+"\n")
f.close()





