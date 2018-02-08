import csv
import math
filename="berp-POS-training.txt"

with open(filename) as file:
    reader = csv.reader(file, delimiter="\t")
    d = list(reader)
obvDic={}
def baselineTagger():
    with open(filename) as file:
        reader = csv.reader(file, delimiter="\t")
        d = list(reader)

    for record in d:
        if len(record)==0:
            continue
        if record[2] in obvDic:
            if record[1] in obvDic[record[2]]:
                obvDic[record[2]][record[1]]=obvDic[record[2]][record[1]]+1
            else:
                obvDic[record[2]][record[1]]=1
        else:
            obvDic[record[2]]={}
            obvDic[record[2]][record[1]] = 1
    max=0
    maxKey=''
    '''for a in sentence.split():
        for key in obvDic:
            if a in obvDic[key]:
                if obvDic[key][a]>max:
                    max=obvDic[key][a]
                    maxKey=key
        if(maxKey==''):
            print('UNK')
        else:
            print(maxKey,max)
        max=0
        maxKey='''''
    print("Baseline:")
    print(obvDic)
baselineTagger()

tagDic={}
def TagCount():
    tagDic['START']=1
    for count,record in enumerate(d):
        if len(record)==0:
            d[count]=[]
            d[count].append(' ')
            d[count].append(' ')
            d[count].append('START')
            record=d[count]
        if record[2] in tagDic:
            tagDic[record[2]]=tagDic[record[2]]+1
        else:
            tagDic[record[2]] = 1

wordDic={}
def wordCount():
    for record in d:
        if(len(record)==0):
            continue
        if record[1] in wordDic:
            wordDic[record[1]]=wordDic[record[1]]+1
        else:
            wordDic[record[1]]=1
    for count,record in enumerate(d):
        if wordDic[record[1]]==1:
            d[count][1]='UNK'
            wordDic['UNK']=1

transDic={}
def Trans():
    transDic['START']={}
    transDic['START'][d[0][2]]=1
    for count,record in enumerate(d):
        if count==0:
            continue
        if len(record)==0:
            d[count]=[]
            d[count].append(' ')
            d[count].append(' ')
            d[count].append('START')
            record=d[count]
        if d[count-1][2] in transDic:
            if record[2] in transDic[d[count-1][2]]:
                transDic[d[count-1][2]][record[2]]=transDic[d[count-1][2]][record[2]]+1
            else:
                transDic[d[count-1][2]][record[2]] = 1
        else:
            transDic[d[count-1][2]]={}
            transDic[d[count-1][2]][record[2]] = 1

obvDic={}
def Obv():
    obvDic['START'] = {}
    obvDic['START'][d[0][1]] = 1
    for count,record in enumerate(d):
        if record[2] == 'START':
            if d[count+1][1] in obvDic['START']:
                obvDic['START'][d[count+1][1]]=obvDic['START'][d[count+1][1]]+1
            else:
                obvDic['START'][d[count + 1][1]] = 1
            continue
        if record[2] in obvDic:
            if record[1] in obvDic[record[2]]:
                obvDic[record[2]][record[1]] = obvDic[record[2]][record[1]] + 1
            else:
                obvDic[record[2]][record[1]] = 1
        else:
            obvDic[record[2]] = {}
            obvDic[record[2]][record[1]] = 1

TagCount()
wordCount()
Trans()
Obv()



def obvProb():
    for tag in tagDic:
        for word in wordDic:
            if word in obvDic[tag]:
                obvDic[tag][word] = math.log(obvDic[tag][word] / tagDic[tag])
            else:
                obvDic[tag][word] = -9999

def transProb():
    total = 36
    for start in tagDic:
        for end in tagDic:
            if(end in transDic[start]):
                transDic[start][end]=math.log((transDic[start][end]+1)/(tagDic[start]+total))
            else:
                transDic[start][end]=math.log(1/total)
    transDic['START']['START']=-9999

obvProb()
transProb()

taggDic=tagDic
taggDic.pop('START')

Matrix={}
for tags in tagDic:
    Matrix[tags]={}
    for words in wordDic:
        Matrix[tags][words]=0
back={}
for tags in tagDic:
    back[tags]={}
    for words in wordDic:
        back[tags][words]=''

def viterbi(sentenceList, sentenceLen):
    for q,word in enumerate(sentenceList):
        if word not in wordDic:
            sentenceList[q]='UNK'
            word=sentenceList[q]
    for i, word in enumerate(sentenceList):
        max=-999999999
        maxKey=''
        if i == 0:
            key='START'
            for tag in tagDic:
                Matrix[tag][word]=transDic[key][tag]+obvDic[tag][word]
                back[tag][word]='START'

        else:
            for key in tagDic:
                for tag in tagDic:
                    check=Matrix[tag][sentenceList[i-1]]+transDic[key][tag]+obvDic[key][word]
                    if(check>max):
                        max=check
                        maxKey=tag
                    Matrix[key][word]=check
                    back[key][word]=maxKey


mainTagTagList=[]
def getTags(sentenceList, sentenceLen):
    max=-9999999
    maxKey=''
    mainTagList = []
    for key in tagDic:
        check=Matrix[key]['.']
        if(check>max):
            max=check
            maxKey=key
    mainTagList.append('.')
    i=sentenceLen
    while(i>=0 and maxKey!='START'):
        maxKey=back[maxKey][sentenceList[i-1]]
        mainTagList.append(maxKey)
        i=i-1
    mainTagList=mainTagList[:sentenceLen]
    for tagger in reversed(mainTagList):
        if tagger=='START':
            continue
        else:
            mainTagTagList.append(tagger)

def sentences():
    sentenceList = []
    sentencelen = 0
    with open("assgn.txt") as file:
        reader = csv.reader(file, delimiter="\t")
        d = list(reader)
    for count,record in enumerate(d):
        if(count<len(d)):
            if(len(record)==0):
                viterbi(sentenceList,sentencelen)
                getTags(sentenceList,sentencelen)
                sentenceList = []
                sentencelen = 0
            else:
                sentenceList.append(record[1])
                sentencelen=sentencelen+1
        else:
            break
sentences()

print(mainTagTagList)


def writeFile():
    with open("assgn.txt") as file:
        reader = csv.reader(file, delimiter="\t")
        d = list(reader)
        f = open("rajath-tellapuram-assgn2-test-output.txt","w")
        counter=1
        print(len(d))
        print(len(mainTagTagList))
        for record in d:
            if(len(record)>0):
                f.write(record[0]+"\t"+record[0]+"\t"+mainTagTagList[counter]+"\n")
                counter+=1
            else:
                f.write("\n")
#writeFile()

