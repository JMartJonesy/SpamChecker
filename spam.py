import math
import random

def extractFileData(file):
	"""
		Opens a file and reads into a list of example(class and percent)
	"""
	fileData = []
	for line in open(file):
		lineInfo = line.split()
		lineInfo[1] = float(lineInfo[1])
		fileData.append(lineInfo)
	return fileData

def findMeansAndVariances(fileData):
	"""
		Calculates the means and variances of each class
	"""
	classData = findMeans(fileData)
	return findVariances(classData, fileData)

def findMeans(fileData):
	"""
		Finds the mean for each class
	"""
	classData = dict()
	for example in fileData:
		c = example[0]
		if c not in classData:
			classData[c] = [0,0,0]
		classData[c][0] += example[1]
		classData[c][2] += 1
	
	for c, classInfo in classData.items():
		classInfo[0] /= classInfo[2]

	print(classData)	
	return classData


def findVariances(classData, fileData):
	"""
		Finds the variances for each class
	"""
	for example in fileData:
		c = classData[example[0]]
		c[1] += (example[1] - c[0])**2
	
	for c, classInfo in classData.items():
		classInfo[1] /= classInfo[2]

	return classData

def gaussianProbs(x, classData):
	"""
		Finds the probabilities that input x is in each class
		using the gaussian function
	"""
	probs = dict()
	for c, classInfo in classData.items():
		firstPart = 1/(math.sqrt(classInfo[1]) * math.sqrt(2*math.pi))
		secondTop = -1*((x-classInfo[0])**2)
		secondBot = 2*classInfo[1]
		secondPart = math.pow(math.e, secondTop/secondBot)
		probs[c] = firstPart * secondPart
	return probs

def bayes(x, classData, samples):
	"""
		Uses a bayes classifier to classify a given input
	"""
	probs = gaussianProbs(x, classData)
	argMax = 0
	maxClass = ""
	for c, prob in probs.items():
		bayesProb = prob * (classData[c][2]/samples)
		if bayesProb > argMax:
			argMax = bayesProb
			maxClass = c
	return [argMax, maxClass]

def kMeans(fileData, k):
	"""
		Run the k-Means algorithm to cluster data into k classes
	"""
	size = len(fileData) - 1
	means = [fileData[random.randint(0,size)][1] for i in range(k)]
	prevMeans = [0 for i in range(k)]
	while(prevMeans != means):
		classes = [[] for i in range(k)] 
		for example in fileData:
			minClass = findMinClass(k, means, example[1])
			classes[minClass].append(example[1])
		prevMeans = means
		means = computeMeans(classes)
	
	return means

def findMinClass(k, means, example):
	"""
		Finds the class the given example is most likely in
		using the distance from the each mean
	"""
	minDist = float("inf")
	minClass = 0
	for i in range(k):
		diff = abs(means[i] - example)
		if diff < minDist:
			minDist = diff	
			minClass = i
	return minClass

def computeMeans(classes):
	"""
		Computes the new means for the next iteration of the
		k-Means algorithm
	"""
	means = [0 for i in range(len(classes))]
	for i in range(len(classes)):
		for ex in classes[i]:
			means[i] += ex
		means[i] /= len(classes[i])
	
	return means	

if __name__ == "__main__":
	data = extractFileData("mail-data.txt")
	classData = findMeansAndVariances(data)
	print(bayes(float(input("Input x value:")), classData, len(data)))
	
	#Uncomment for k-Means
	#print(kMeans(data, int(input("Input # of classes:"))))
