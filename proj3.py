#ACCURACY IS VERY LOW

import math
import random

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
    #print(doc.name)
    #print(doc.scores)
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
            #print(currClass)
        #print(str(distances[i]) + groupList[i].className)
    #print(doc.name + " is of class " + groupList[currClass].className)
    return str(groupList[currClass].className)

print("Enter in the name of the document file")
#reads in the name of the file to get the docs from
docFileName = input()
#stores all the docs
allDocs = []
docFile = open(docFileName, "r")
lineOne = docFile.readline()
#reads in the files and creates doc classes for each doc in the file
while(lineOne):
    lineTwo = docFile.readline()
    className = docFile.readline()
    floats = [float(x) for x in lineTwo.split()]
    allDocs.append((Document(lineOne, floats, className)))
    #Removes the empty line between file descriptions
    discard = docFile.readline()
    lineOne = docFile.readline()
docFile.close()

#shuffle order of tf-IDF values
random.shuffle(allDocs)
#sum for average accuracy
sum = 0

for i in range(5):
	#stores all of the classes
	groupList = []
	#separate test file for each fold
	testFileName = str(i) + ".txt"
	testFile = open(testFileName, "w")
	#starting point 
	s = int(i/5 * 8282)
	#endpoint
	e = int((i+1) / 5 * 8282 -1)

	for d in range(s, e):
		testFile.write(allDocs[d].name)
	testFile.close()

#print("Please enter in the name of the test file")
#testFileName = input()
	testFile = open(testFileName, "r")
#reads in the name of all the test docs and splits them into an array
	temp = testFile.read()
	testDocs = temp.split()
	testFile.close()
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
					groupList[-1].addItem((allDocs[i]))
					found = True
			if found == False:
				groupList.append(Group(allDocs[i].className))
				groupList[-1].addItem((allDocs[i]))
	for i in range(len(groupList)):
		groupList[i].className = groupList[i].className[:-1]
		groupList[i].getCentroid()

	correct = 0
	for i in testDocs:
		for j in allDocs:
			tempName = j.name[:-1]
			if i == tempName:
				tempClass = classify(j,groupList)		
				if(tempClass == j.className[:-1]):
					correct += 1
	print("Accuracy is " + str((correct/(len(testDocs))*100)))
	
	sum += correct/(len(testDocs))*100

#find average accuracy
avgAcc = sum / 5
print(len(groupList))
print("Average Accuracy: " + str(avgAcc))
#print("Do you want to do 5-fold testing")