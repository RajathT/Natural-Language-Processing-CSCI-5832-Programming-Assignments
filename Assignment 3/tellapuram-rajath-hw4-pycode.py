import re,math
workfile="gene.txt"
with open(workfile, 'r') as f:
    read_data = f.readlines()
f.closed

mainList=[]
for i in range(len(read_data)):
    read_data[i] = read_data[i].strip('\n')
    list=re.split(r'\t+', read_data[i])
    mainList.append(list)
#print(mainList)

tagDic={}
def TagCount():
    tagDic['START']=1
    for record in mainList:
        if(record[0]!=""):
            if record[2] in tagDic:
                tagDic[record[2]] = tagDic[record[2]] + 1
            else:
                tagDic[record[2]] = 1
        else:
            tagDic['START']+=1

TagCount()
#print(tagDic)

wordDic={}
def wordCount():
    for record in mainList:
        if(record[0]!=""):
            if record[1] in wordDic:
                wordDic[record[1]] = wordDic[record[1]] + 1
            else:
                wordDic[record[1]] = 1
        else:
            continue

wordCount()
#print(wordDic)

obvDic={}
def Obv():
    for count,record in enumerate(mainList):
        if (record[0] != ""):
            if record[1] in obvDic:
                if record[2] in obvDic[record[1]]:
                    obvDic[record[1]][record[2]] = obvDic[record[1]][record[2]] + 1
                else:
                    obvDic[record[1]][record[2]] = 1
            else:
                obvDic[record[1]] = {}
                obvDic[record[1]][record[2]] = 1
        else:
            continue

Obv()
#print(obvDic)

#print(obvDic['an'])

transDic={}
def Trans():
    skip=0
    transDic['START'] = {}
    transDic['START'][mainList[0][2]] = 1
    for count,record in enumerate(mainList):
        if skip==0:
            skip+=1
            continue
        else:
            #print(count,skip,record,mainList[count-1])
            if (record[0] != ""):
                if mainList[count-1][2] in transDic:
                    if record[2] in transDic[mainList[count-1][2]]:
                        transDic[mainList[count-1][2]][record[2]]=transDic[mainList[count-1][2]][record[2]]+1
                    else:
                        transDic[mainList[count-1][2]][record[2]] = 1
                else:
                    transDic[mainList[count-1][2]]={}
                    transDic[mainList[count-1][2]][record[2]] = 1
                skip+=1
            else:
                skip=0
                if mainList[count+1][2] in transDic['START']:
                    transDic['START'][mainList[count+1][2]]=transDic['START'][mainList[count+1][2]]+1
                else:
                    transDic['START'][mainList[count+1][2]] = 1

Trans()
#print(transDic)

def obvProb():
    for word in wordDic:
        for tag in transDic:
            if tag is not 'START':
                if tag in obvDic[word]:
                    #print(word,tag,obvDic[word][tag],tagDic[tag])
                    obvDic[word][tag] = math.log(obvDic[word][tag] / tagDic[tag])
                    #print(obvDic[word][tag])
                else:
                    obvDic[word][tag] = -9999

obvProb()
#print(obvDic)

def transProb():
    total = 3
    for start in transDic:
        for end in transDic:
            if end is not 'START':
                if end in transDic[start]:
                    transDic[start][end]=math.log((transDic[start][end]+1)/(tagDic[start]+total))
                else:
                    transDic[start][end]=math.log(1/(tagDic[start]+total))

transProb()
print(transDic)
obvDic['UNK']={}
for tag in tagDic:
    min = 9999
    if tag is not 'START':
        for word in wordDic:
            if obvDic[word][tag]==-9999:
                continue
            else:
                if obvDic[word][tag]<min:
                    min=obvDic[word][tag]
        obvDic['UNK'][tag]=min

#print(obvDic['UNK'])

matrix=[]
back=[]
maxValue=-999999
maxKey=''
matrix.append([])
back.append([])
#print(obvDic['determined'])

def viterbi(sentenceList, sentenceLen):
    #print(sentenceList,sentenceLen)
    Matrix = [[0 for x in range(3)] for y in range(sentenceLen)]
    Back = [['' for x in range(3)] for y in range(sentenceLen)]
    for i,word in enumerate(sentenceList):
        if word not in wordDic:
            word='UNK'
        if i==0:
            key='START'
            j=0
            for tag in transDic:
                if tag is not 'START':
                    value=transDic[key][tag]+obvDic[word][tag]
                    Matrix[i][j]=value
                    Back[i][j]=key
                    j+=1
        else:
            k = 0
            for key in transDic:
                if key is not 'START':
                    j=0
                    maxValue = -999999
                    maxKey = ''
                    for tag in transDic:
                        if tag is not 'START':
                            value=Matrix[i-1][j]+transDic[tag][key]+obvDic[word][key]
                            #print(i,j,value,maxValue,matrix[i-1][j],tag,key,transDic[tag][key], obvDic[word][key])
                            if value>maxValue:
                                maxValue=value
                                maxKey=tag
                            j+=1
                    Matrix[i][k]=maxValue
                    Back[i][k]=maxKey
                    k+=1
    getTag(Matrix,Back,sentenceLen)

mainOutput=[]
def getTag(M,B,sl):
    finalTags=[]
    final=[]
    max=-999999
    for i in range(3):
        if M[sl-1][i]>max:
            max=M[sl-1][i]
            key=i
    #print(key,max)
    if key==0:
        finalTags.append('O')
    elif key==1:
        finalTags.append('B')
    elif key==2:
        finalTags.append('I')
    #print(finalTags)

    for i in range(sl-1,0,-1):
        tag=B[i][key]
        if tag == 'O':
            key=0
        elif tag == 'B':
            key=1
        elif tag == 'I':
            key=2
        finalTags.append(tag)
    for i in reversed(finalTags):
        final.append(i)
    #print(final,len(final))
    mainOutput.append(final)

mainOut=[]

def sentences():
    sentenceList = []
    sentencelen = 0
    workfile1="F17-assgn4-test.txt"
    with open(workfile1, 'r') as f1:
        read_data1 = f1.readlines()
    f1.closed

    mainList1 = []
    for i in range(len(read_data1)):
        read_data1[i] = read_data1[i].strip('\n')
        list1 = re.split(r'\t+', read_data1[i])
        mainList1.append(list1)
        mainOut.append(list1)
    #print(mainList1)

    for count,record in enumerate(mainList1):
        #print(count,len(read_data1),record)
        if(count<len(read_data1)):
            if (record[0] != ""):
                sentenceList.append(record[1])
                sentencelen = sentencelen + 1
            else:
                viterbi(sentenceList, sentencelen)
                #getTags(sentenceList, sentencelen)
                sentenceList = []
                sentencelen = 0
        else:
            break


sentences()

finalList=[]
#print(mainOutput[0])


for i in range (len(mainOutput)):
    for j in range(len(mainOutput[i])):
        finalList.append(mainOutput[i][j])
    finalList.append('')

#print(len(finalList),len(mainOut))

#for i,record in enumerate(mainOut):
 #   print(record,finalList[i])

f=open("output.txt","w")

for i,record in enumerate(mainOut):
    if(record[0]==''):
        f.write(record[0]+"\n")
        continue
    f.write(record[0]+"\t"+record[1]+"\t"+finalList[i]+"\n")

f.close()

