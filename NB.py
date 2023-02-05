#main goal of this file will be to track total counts of a word per classifier type, which will in turn allow us to calculate naive bayes probability for each classifier type
#we will do this by using a list of dictionaries. Each list item will store a dictionary for a classifier
naiveBayesList = []
firstDict = {}
correctPredictions = 0
naiveBayesList.append(firstDict)

def dictSum(myDict):
    sum = 0
    for x in myDict:
        if isinstance(myDict[x], int):
            sum+=myDict[x]
    return sum



smallTrainingString = ''
smallTrainingList = []
with open("movie-review-small.NB", 'r', encoding ='utf-8') as smallTraining:
    smallTrainingList = [line.rstrip().split(', ') for line in smallTraining]

trainingString = ''
trainingList = []
with open("processed-movies-training.txt", 'r', encoding ='utf-8') as trainingFile:
    trainingList = [line.rstrip().split(', ') for line in trainingFile]

testString = ''
testList = []
with open("processed-movies-test.txt", 'r', encoding ='utf-8') as testFile:
    testList = [line.rstrip().split(', ') for line in testFile]
#we use the key $classifier to track what type of classifier our dictionary tracks. The $ at the beginning prevents possible duplicate entries of the word classifier
#classifierNum tracks nonmatching classifiers, and if all of the current dictionaries do not match then that means we add an extra dictionary with that classifier


pairCount = 0
classifierNum = 1
classifierMax = 1
stlTempList = []
currentClassifier = ''
wasChecked = 0
for line in smallTrainingList:
    for pair in line:
        stlTempList = pair.split(':')
        if pairCount == 0:
            currentClassifier = stlTempList[1]
            for dict in naiveBayesList:
                if "$classifier" not in dict:
                    dict["$classifier"] = currentClassifier
                if dict["$classifier"] != currentClassifier:
                    classifierNum+=1
                if classifierNum > classifierMax:
                    newDict = {'$classifier':currentClassifier}
                    naiveBayesList.append(newDict)
                    classifierMax+=1
            classifierNum = 1
        if pairCount > 0:
            for dict in naiveBayesList:
                if dict["$classifier"] == currentClassifier:
                    if stlTempList[0] not in dict:
                        dict[stlTempList[0]] = int(stlTempList[1])
                    else:
                        dict[stlTempList[0]] += int(stlTempList[1])
        pairCount+=1    
    pairCount = 0
#traininglist added counts to dictionary to build 
for line in trainingList:
    for pair in line:
        stlTempList = pair.split(':')
        if pairCount == 0:
            currentClassifier = stlTempList[1]
            for dict in naiveBayesList:
                if "$classifier" not in dict:
                    dict["$classifier"] = currentClassifier
                if dict["$classifier"] != currentClassifier:
                    classifierNum+=1
                if classifierNum > classifierMax:
                    newDict = {'$classifier':currentClassifier}
                    naiveBayesList.append(newDict)
                    classifierMax+=1
            classifierNum = 1
        if pairCount > 0:
            for dict in naiveBayesList:
                if dict["$classifier"] == currentClassifier:
                    if stlTempList[0] not in dict:
                        dict[stlTempList[0]] = int(stlTempList[1])
                    else:
                        dict[stlTempList[0]] += int(stlTempList[1])
        pairCount+=1    
    pairCount = 0

smallTestVector = ['fast:1', 'couple:1', 'shoot:1', 'fly:1']
comedyTestProbability = 0
actionTestProbability = 0
#print(naiveBayesList)
tempList = []

#now calculating probability with add one smoothing
#calculating for small test data, with the comedy and action classifier
for pair in smallTestVector:
    tempList = pair.split(':')
    for tDict in naiveBayesList:
        if tDict['$classifier'] == 'comedy':
            if tempList[0] in tDict and comedyTestProbability == 0:
                comedyTestProbability = ((tDict[tempList[0]] + 1)/(dictSum(tDict) + (len(tDict)-1)))
            elif tempList[0] in tDict and comedyTestProbability != 0:
                comedyTestProbability *= ((tDict[tempList[0]] + 1)/(dictSum(tDict) + (len(tDict)-1)))
            elif tempList[0] not in tDict and comedyTestProbability == 0:
                comedyTestProbability = (1/(dictSum(tDict) + (len(tDict)-1)))
            elif tempList[0] not in tDict and comedyTestProbability != 0:
                comedyTestProbability *= (1/(dictSum(tDict) + (len(tDict)-1)))
        elif tDict['$classifier'] == 'action':
            if tempList[0] in tDict and actionTestProbability == 0:
                actionTestProbability = ((tDict[tempList[0]] + 1)/(dictSum(tDict) + (len(tDict)-1)))
            elif tempList[0] in tDict and actionTestProbability != 0:
               actionTestProbability *= ((tDict[tempList[0]] + 1 )/(dictSum(tDict) + (len(tDict)-1)))
            elif tempList[0] not in tDict and actionTestProbability == 0:
                actionTestProbability = (1/(dictSum(tDict) + (len(tDict)-1)))
            elif tempList[0] not in tDict and actionTestProbability != 0:
                actionTestProbability *= (1/(dictSum(tDict) + (len(tDict)-1)))
#calculating for real test data with pos and neg classifier, need to be able to give a probability and prediction for every review, while tracking the original classifier to flag correct prediction 
#also need to read in a review at a time, which we currently have as a list of list of key value pairs. also must append these values to a string to be printed.

outputString = ''
negProb = 0
posProb = 0
predictedClassifier = ''
count = 0
negSum = comSum = posSum = actSum = 0
posLength = negLength = comLength = actLength = 0
for Dict in naiveBayesList:
    if Dict['$classifier'] == 'negative':
        negSum = dictSum(Dict)
        negLength = (len(Dict)-1)
    if Dict['$classifier'] == 'positive':
        posSum = dictSum(Dict)
        posLength = (len(Dict)-1)
    if Dict['$classifier'] == 'comedy':
        comSum = dictSum(Dict)
        comLength = (len(Dict)-1)
    if Dict['$classifier'] == 'action':
        actSum = dictSum(Dict)
        actLength = (len(Dict)-1)

for reviewVector in testList:
    print("Review " + str(count))
    for pair in reviewVector:
        tempList = pair.split(':')
        if pairCount == 0:
            currentClassifier = tempList[1]
            outputString += "\nOriginal Classifier:" + currentClassifier
        elif pairCount > 0:
            for tDict in naiveBayesList:
                if tDict['$classifier'] == 'negative':
                    if tempList[0] in tDict and negProb == 0:
                        negProb = ((tDict[tempList[0]] + 1)/(negSum + negLength))
                    elif tempList[0] in tDict and negProb != 0:
                        negProb *= ((tDict[tempList[0]] + 1)/(negSum + negLength))
                    elif tempList[0] not in tDict and negProb == 0:
                        negProb = (1/(negSum + negLength))
                    elif tempList[0] not in tDict and negProb != 0:
                        negProb *= (1/(negSum + negLength))
                elif tDict['$classifier'] == 'positive':
                    if tempList[0] in tDict and posProb == 0:
                        posProb = ((tDict[tempList[0]] + 1)/(posSum + posLength))
                    elif tempList[0] in tDict and posProb != 0:
                        posProb *= ((tDict[tempList[0]] + 1)/(posSum + posLength))
                    elif tempList[0] not in tDict and posProb == 0:
                        posProb = (1/(posSum + posLength))
                    elif tempList[0] not in tDict and posProb != 0:
                        posProb *= (1/(posSum + posLength))                
        pairCount+=1
    outputString = outputString + ", Neg Prob:" + str(negProb*0.5) + ", Pos Prob:" + str(posProb*0.5)
    if negProb > posProb:
        outputString += ", Predicted Classifier:negative"
        predictedClassifier = 'negative'
    elif posProb > negProb:
        outputString += ", Predicted Classifier:positive"
        predictedClassifier = 'positive'
    else:
        outputString += ", Predicted Classifier:unsure"
        predictedClassifier = 'unsure'
    if predictedClassifier == currentClassifier:
        correctPredictions+=1
        outputString += ", Prediction:Correct"
    elif predictedClassifier != currentClassifier:
        outputString += ", Prediction:Wrong"
    outputString = outputString + ", Related Review:" + str(reviewVector)
    pairCount = negProb = posProb = 0        
    count+=1

outputString+="\n Overall Accuracy:" + str(correctPredictions) + "/25000" + " or " + str(correctPredictions/25000) 

print("Comedy test sentence probability:" + str(comedyTestProbability*(2/5)))
print("Action test sentence probability:" + str(actionTestProbability*(3/5)))
with open('final-output.txt', 'w+',  encoding ='utf-8') as finalTestFile:
    finalTestFile.write(outputString)

parameterString = 'Naive Bayes Training Word Counts:\n'
#also need to write a parameter file, which I assume are the count of words per classifier, as well as their sum
parameterString += str(naiveBayesList)
parameterString += "\nNaive Bayes Training Word Totals:\nAction:" + str(actSum) + ", Comedy:" + str(comSum) + ", Negative:"   + str(negSum) + ", Positive:" + str(posSum)
parameterString += "\nNaive Bayes Training Word Vocab Sizes:\nAction:" + str(actLength) + ", Comedy:" + str(comLength) + ", Negative:"   + str(negLength) + ", Positive:" + str(posLength)
with open('final-parameters.txt', 'w+',  encoding ='utf-8') as finalParameterFile:
    finalParameterFile.write(parameterString)

