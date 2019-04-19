import math

#Stores each class
class Group:
    #stores each do in the class
    docList = []
    #stores the centroid of the class
    centroid = []
    #keeps track of how many docs were in the doc
    count = 0
    #stores the sum of all scores to make computing the centroids easier
    totalScores = []
    def __init__(self, className):
        self.docList = []
        self.centroid = []
        self.className = className
    #adds a new doc to the class
    def addItem(self, doc):
        self.docList.append(doc)
        self.count += 1
        if(len(doc.scores) > len(self.totalScores)):
            for i in doc.scores:
                self.totalScores = self.totalScores + [0]
        for i in range(len(doc.scores)):
            self.totalScores[i] += doc.scores[i]
    #calculates the centroid of each class
    def getCentroid(self):
        for i in self.docList[0].scores:
            self.centroid = self.centroid + [0]
        for i in range (len(self.centroid)):
            self.centroid[i] = (self.totalScores[i]/self.count)

#stores the name and scores of each document along with what class it is in
class Document:
    def __init__(self, name, scores, className):
        self.name = name
        self.scores = scores
        self.className = className
#takes a document a group list as parameters and figures out which centroid the doc is closest to
def classify(doc, groupList):
    #stores the distance from each centroid
    distances = []
    #intialized to an insanely large number for comparison purpose
    lowestDistance = 100000000
    currClass = -1;
    for i in range(len(groupList)):
        tempSum = 0
        distances.append(0)
        #calculates the distance from each centoid
        for j in range(len(groupList[i].centroid)):
            tempSum += (groupList[i].centroid[j] - doc.scores[j])**2
        distances[i] = math.sqrt(tempSum)
    #Finds which centroid has the shortest distance from the doc
    for i in range(len(groupList)):
        if distances[i] < lowestDistance:
            lowestDistance = distances[i]
            currClass = i
    print(doc.name + " is of class " + groupList[currClass].className)

print("Enter in the name of the document file")
#reads in the name of the file to get the docs from
docFileName = input()
#stores all the docs
allDocs = []
#stores all of the classes
groupList = []
docFile = open(docFileName, "r")
lineOne = docFile.readline()
#reads in the files and creates doc classes for each doc in the file
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
#reads in the name of all the test docs and splits them into an array
temp = testFile.read()
testDocs = temp.split()
testFile.close()
print(len(allDocs))
#Adds each file into the approiate class 
for i in range(len(allDocs)):
    #Checks if a doc is a test doc
    inTest = False
    tempName = allDocs[i].name[:-1]
    for k in testDocs:
        if(tempName == k):
            inTest = True
    if inTest == False:
        #creates and add new files to existing classes
        found = False
        for j in range (len(groupList)):
            if groupList[j].className == allDocs[i].className:
                groupList[j].addItem((allDocs[i]))
                found = True
        if found == False:
            groupList.append(Group(allDocs[i].className))
            groupList[-1].addItem((allDocs[i]))
for i in range(len(groupList)):
    #Just removes the newline char from the end of each class name
    groupList[i].className = groupList[i].className[:-1]
    #print(groupList[i].className + " " + str(len(groupList[i].docList)))
    groupList[i].getCentroid()
#classify test docs
for i in testDocs:
    for j in allDocs:
        tempName = j.name[:-1]
        if i == tempName:
            classify(j,groupList)
#for i in groupList:
#    print(i.className)
#    print(i.count)
#    print()
