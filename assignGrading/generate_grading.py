# oauth2 for basecamp so annoying
from typing import NamedTuple
import math

# assign weight
types = {
    "format": 1,
    "math": 2,
    "propmath": 3,
    "shortans": 3,
    "longans": 4
}

allGraders = 21
numGraders = allGraders
numSubmissions = 515

addFailed = True
failedSubmissions = 18
failedFile = "FailedAutograder.txt"

class item(object):
    def __init__(self, name, type, numPpl=None):
        self.name = name
        self.type = type
        self.numPpl = numPpl

def printMode(result, curItem, first, last, mode = 0): # 0=normal, 1=failed submissions by name
    if(first>last):
        return
    if(mode == 1):
        f = open(failedFile, "r")
        names = f.readlines()
        f.close()
        curResult = curItem.name+":"
        for i in range(first-1, last):
            if(i!=first-1):
                curResult += ", "
            curResult += str(names[i].strip())
        result.append(curResult)
        f.close()
    elif(mode == 0):
        if(first!=last):
            result.append(curItem.name+":"+str(first)+"-"+str(last))
        else:
            result.append(curItem.name+":"+str(first))
        

def splitItem(result, curItem, ppl, submissions, mode = 0):
    numTask = int(math.ceil(submissions/ppl))
    print(curItem.name + " | ppl:" + str(ppl)+" submissions/person:"+str(numTask))
    pplExtraWork = submissions%ppl # num ppl that will have 1 more task to do than others
    last = 0 # first submission starts at 1
    for i in range(ppl):
        first = last+1
        last = first+numTask-1
        if(i>=pplExtraWork):
            last -= 1
        if(i == ppl-1): # almost there bug # TODO This is unfair to last person oop, but ceil so mb ok
            last = submissions
        # print(" "+str(first)+" "+str(last))
        printMode(result, curItem, first, last, mode)
        # if(first!=last):
        #     result.append(curItem.name+":"+str(first)+"-"+str(last))
        # else:
        #     result.append(curItem.name+":"+str(first))

allQs = [
item("Q1", "format", 4),
item("Q3.1", "format", 21)
]

remainingQs = []
for curItem in allQs:
    if(curItem.numPpl == None):
        remainingQs.append(curItem)
    

allQs.sort(key=lambda x: types[x.type], reverse=True) # heavier weights first

# remove forced number of graders questions, add them to ans
ans = []
gradeWeight = 0 # remaining for distribution
totalGW = 0
for curItem in allQs:
    totalGW += types[curItem.type]
    if(curItem.numPpl==None):
        gradeWeight += types[curItem.type]
        print("skipping")
    else:
        # ans.append(curItem.name+":"+)
        splitItem(ans, curItem, curItem.numPpl, numSubmissions)
        numGraders -= curItem.numPpl
        if(numGraders < 0):
            print("error: not enough graders to enforce grader constraint")
print("total graders: "+str(allGraders))
print("distributing graders: "+str(numGraders))
print()
print("total grade weight: "+str(totalGW))
print("remaining grade weight: "+str(gradeWeight))
print()

remainingGraders = numGraders
# numGraders/gradeWeight is num people per Q
for curItem in remainingQs:
    numPpl = int(math.ceil(numGraders*types[curItem.type]/gradeWeight)) # people assigned to this item
    remainingGraders -= numPpl
    if(remainingGraders < 0): # oops we don't have that many people
        numPpl += remainingGraders
    
    print(str(numPpl)+" "+str(remainingGraders))
    
    splitItem(ans, curItem, numPpl, numSubmissions)

failedAns = []
if(addFailed):
    splitItem(failedAns, item("Failed", "longans"), allGraders, failedSubmissions, 1)

print(ans)
print(len(ans))
print("------------------")

print("[", end ="")
for i in range(len(ans)):
    print("\"", end ="")
    print(ans[i], end ="")
    if(addFailed and i<len(failedAns)):
        print(" "+str(failedAns[i]), end="")
    print("\"", end ="")
    if(not (i==len(ans)-1)):
        print(", ", end ="")
print("]", end ="")
print()

print("Reminders:")
print(" - Create to-do list and select it")
print(" - Set due date")
print(" - Assign people")