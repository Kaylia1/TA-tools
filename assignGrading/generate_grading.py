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
numSubmissions = 473

class item(object):
    def __init__(self, name, type, numPpl=None):
        self.name = name
        self.type = type
        self.numPpl = numPpl

def splitItem(result, curItem, ppl, submissions):
    numTask = int(math.ceil(submissions/ppl))
    print(curItem.name + " | ppl:" + str(ppl)+" submissions/person:"+str(numTask))
    pplExtraWork = submissions%ppl # num ppl that will have 1 more task to do than others
    last = 0 # first submission starts at 1
    for i in range(ppl):
        first = last+1
        last = first+numTask-1
        if(i>=pplExtraWork):
            last -= 1
        print(" "+str(first)+" "+str(last))
        result.append(curItem.name+":"+str(first)+"-"+str(last))

allQs = [
item("Q1.1", "format", 2), item("Q1.2", "format",2), item("Q1.3", "format",2), item("Q1.4", "format",2),
item("Q3", "longans"), item("Q4.2", "longans")
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
    numPpl = int(math.ceil(numGraders*types[curItem.type]/gradeWeight))
    remainingGraders -= numPpl
    if(remainingGraders < 0): # oops we don't have that many people
        numPpl += remainingGraders
    
    splitItem(ans, curItem, numPpl, numSubmissions)
    # numTask = int(math.ceil(numSubmissions/numPpl))
    # remainingSubmissions = numSubmissions
    # print(curItem.name + " | " + str(numPpl)+" "+str(numTask))
    # pplExtraWork = numSubmissions%numPpl # num ppl that will have 1 more task to do than others
    # print("ppl w extra work: "+str(pplExtraWork))
    # last = 0 # first submission starts at 1
    # for i in range(numPpl):
    #     first = last+1
    #     last = first+numTask-1
    #     if(i>=pplExtraWork):
    #         last -= 1
    #     print(" "+str(first)+" "+str(last))
    #     ans.append(curItem.name+":"+str(first)+"-"+str(last))

print(ans)
print("Reminders:")
print(" - Create to-do list and select it")
print(" - Set due date")
print(" - Assign people")