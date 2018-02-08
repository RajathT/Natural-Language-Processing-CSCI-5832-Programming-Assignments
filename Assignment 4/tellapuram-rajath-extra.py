import csv
import math
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
nltk.download('stopwords')
from nltk.corpus import stopwords

filename="hotelF-train.txt"
with open(filename,encoding="utf8") as file:
    reader = csv.reader(file,delimiter='\t')
    mainNegList=list(reader)
#print(mainNegList)
tempNegList=[]

for i in mainNegList:
    tempList=tokenizer.tokenize(i[1])
    tempNegList=tempNegList+tempList

#print(tempNegList)
tempNegList=[x.lower() for x in tempNegList]
#print(tempNegList)

stop_words = set(stopwords.words('english'))
filtered_sentence = [w for w in tempNegList if not w in stop_words]

filtered_sentence = []

for w in tempNegList:
    if w not in stop_words:
        filtered_sentence.append(w)
#print(filtered_sentence)
mainNegDicCount={}
for i in filtered_sentence:
    if i in mainNegDicCount:
        mainNegDicCount[i] = mainNegDicCount[i] + 1
    else:
        mainNegDicCount[i] = 1
print(mainNegDicCount)

filename="hotelT-train.txt"
with open(filename,encoding="utf8") as file:
    reader = csv.reader(file,delimiter='\t')
    mainPosList=list(reader)
#print(mainNegList)
tempPosList=[]

for i in mainPosList:
    tempList=tokenizer.tokenize(i[1])
    tempPosList=tempPosList+tempList

#print(tempPosList)
tempPosList=[x.lower() for x in tempPosList]
#print(tempPosList)

stop_words = set(stopwords.words('english'))
filtered_sentence = [w for w in tempPosList if not w in stop_words]

filtered_sentence = []

for w in tempPosList:
    if w not in stop_words:
        filtered_sentence.append(w)
#print(filtered_sentence)
mainPosDicCount={}
for i in filtered_sentence:
    if i in mainPosDicCount:
        mainPosDicCount[i] = mainPosDicCount[i] + 1
    else:
        mainPosDicCount[i] = 1
print(mainPosDicCount)

countNeg = 0
for i in mainNegDicCount:
    countNeg = countNeg + mainNegDicCount[i]
countPos = 0
for i in mainPosDicCount:
    countPos = countPos + mainPosDicCount[i]
#print(countPos)

#print(countPos,countNeg)
for i in mainPosDicCount:
    mainPosDicCount[i]=math.log(mainPosDicCount[i]+1/(countPos+countNeg))
#print(mainPosDicCount)

for i in mainNegDicCount:
    mainNegDicCount[i]=math.log(mainNegDicCount[i]+1/(countPos+countNeg))
#print(mainNegDicCount)


#print(len(mainNegDicCount))
for i in mainPosDicCount:
    if i not in mainNegDicCount:
        mainNegDicCount[i]=math.log(1/(countPos+countNeg))

print(mainNegDicCount)
#print(len(mainNegDicCount))
#print(len(mainPosDicCount))
for i in mainNegDicCount:
    if i not in mainPosDicCount:
        mainPosDicCount[i]=math.log(1/(countPos+countNeg))
print(mainPosDicCount)
#print(len(mainPosDicCount))
#print(countPos+countNeg)
filename="hotelDeceptionTest.txt"
with open(filename,encoding='mac_roman', newline='') as file:
    reader = csv.reader(file,delimiter='\t')
    mainDevList=list(reader)
f=open("final1.txt","w")
fr=0
tr=0
for k,i in enumerate(mainDevList):
    tempDevList=tokenizer.tokenize(i[1])
    #print(tempDevList)
    posSum = 0
    for j in tempDevList:
        if j in mainPosDicCount:
            posSum=posSum+mainPosDicCount[j]

    negSum = 0
    for j in tempDevList:
        if j in mainNegDicCount:
            negSum = negSum + mainNegDicCount[j]

    if (posSum > negSum):
        finaltag = "T"
        #if k > 63:
            #tr = tr + 1
    else:
        finaltag = "F"
        #if k <= 63:
            #fr = fr + 1
            # print(finaltag)
    #print(mainDevList[i][0], finaltag)
    f.write(mainDevList[k][0] + "\t" + finaltag + "\n")
f.close()
#print(tr, fr)
#print((tr + fr) / (k+1))