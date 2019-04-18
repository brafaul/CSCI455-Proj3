import math

class Group:
    docList = []
    centroid = []
    count = 0
    totalScores = []
    def __init__(self, className):
        self.docList = []
        self.centroid = []
        self.className = className
    def addItem(self, doc):
        self.docList.append(doc)
        self.count += 1
        if(len(doc.scores) > len(self.totalScores)):
            for i in doc.scores:
                self.totalScores = self.totalScores + [0]
        for i in range(len(doc.scores)):
            self.totalScores[i] += doc.scores[i]

    def getCentroid(self):
        for i in self.docList[0].scores:
            self.centroid = self.centroid + [0]
        for i in range (len(self.centroid)):
            self.centroid[i] = (self.totalScores[i]/self.count)

class Document:
    def __init__(self, name, scores, className):
        self.name = name
        self.scores = scores
        self.className = className

def classify(doc, groupList):
    distances = []
    lowestDistance = 100000000
    currClass = -1;
    for i in range(len(groupList)):
        tempSum = 0
        distances.append(0)
        #print(groupList[i].centroid)
        for j in range(len(groupList[i].centroid)):
            tempSum += (groupList[i].centroid[j] - doc.scores[j])**2
            #print(tempSum)
        distances[i] = math.sqrt(tempSum)
        #print(str(distances[i]) + " " +groupList[i].className)
    #for i in :
        #print(doc.name + " " + str(i))
    for i in range(len(groupList)):
        if distances[i] < lowestDistance:
            lowestDistance = distances[i]
            currClass = i
    #print(lowestDistance)
    print(doc.name + " is of class " + groupList[currClass].className)

print("Enter in the name of the document file")
docFileName = input()
allDocs = []
groupList = []
docFile = open(docFileName, "r")
lineOne = docFile.readline()
while(lineOne):
    lineTwo = docFile.readline()
    className = docFile.readline()
    floats = [float(x) for x in lineTwo.split()]
    allDocs.append((Document(lineOne, floats, className)))
    discard = docFile.readline()
    lineOne = docFile.readline()
docFile.close()
print("Please enter in the name of the test file")
testFileName = input()
testFile = open(testFileName, "r")
temp = testFile.read()
testDocs = temp.split()
#for i in testFiles:
#    print(i)
print(len(allDocs))
for i in range(len(allDocs)):
    inTest = False
    tempName = allDocs[i].name[:-1]
    for k in testDocs:
        if(tempName == k):
            inTest = True
            #print(tempName)
    if inTest == False:
        found = False
        #print(allDocs[i].name)
        for j in range (len(groupList)):
            if groupList[j].className == allDocs[i].className:
                groupList[j].addItem((allDocs[i]))
                found = True
                #print("found")
        if found == False:
            #print("not found")
            groupList.append(Group(allDocs[i].className))
            groupList[-1].addItem((allDocs[i]))
for i in range(len(groupList)):
    groupList[i].className = groupList[i].className[:-1]
    print(groupList[i].className + " " + str(len(groupList[i].docList)))
    groupList[i].getCentroid()
    #print(groupList[i].centroid)
for i in testDocs:
    for j in allDocs:
        tempName = j.name[:-1]
        if i == tempName:
            classify(j,groupList)
for i in groupList:
    print(i.className)
    print(i.count)
    #print(len(i.docList))
    #for j in i.centroid:
    #     print(j)
    print()
