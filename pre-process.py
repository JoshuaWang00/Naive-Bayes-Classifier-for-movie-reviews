import os
import string
#return every file directory of the positive and negative test reviews as a list, so we can open all of them

neTrainFiles = sorted(os.listdir("movie-review-HW2/aclImdb/train/neg"), key=len)
poTrainFiles = sorted(os.listdir("movie-review-HW2/aclImdb/train/pos"), key=len)
neTestFiles =  sorted(os.listdir("movie-review-HW2/aclImdb/test/neg"), key=len)
poTestFiles = sorted(os.listdir("movie-review-HW2/aclImdb/test/pos"), key=len)
#turn vocab file into a reusable dictionary that tracks word count
vocabDict = {}
with open("movie-review-HW2/aclImdb/imdb.vocab", 'r', encoding ='utf-8') as vocabF:
    for line in vocabF:
       key = line.split()
       vocabDict[''.join(key)] = 0
#convert the training and then test files into an array of processed reviews
print("Grabbing training files into a list, this will take a while...")

ntfCount = 0
neReviewList = []
for file in neTrainFiles:
    with open("movie-review-HW2/aclImdb/train/neg/" + neTrainFiles[ntfCount], 'r', encoding ='utf-8') as review:
        neReview = str([x.rstrip().lower() for x in review])
        neReview = neReview.translate(str.maketrans('','',string.punctuation))
        neReviewList.append(neReview)
    ntfCount+=1

ptfCount = 0
poReviewList = []
for file in poTrainFiles:
    with open("movie-review-HW2/aclImdb/train/pos/" + poTrainFiles[ptfCount], 'r', encoding ='utf-8') as review:
        poReview = str([x.rstrip().lower() for x in review])
        poReview = poReview.translate(str.maketrans('','',string.punctuation))
        poReviewList.append(poReview)
    ptfCount+=1

print("Grabbing test files into a list, this will take a while...")

nTestCount = 0
neTeReviewList = []
for file in neTestFiles:
    with open("movie-review-HW2/aclImdb/test/neg/" + neTestFiles[nTestCount], 'r', encoding ='utf-8') as review:
        neTeReview = str([x.rstrip().lower() for x in review])
        neTeReview = neTeReview.translate(str.maketrans('','',string.punctuation))
        neTeReviewList.append(neTeReview)
    nTestCount+=1

pTestCount = 0
poTeReviewList = []
for file in poTestFiles:
    with open("movie-review-HW2/aclImdb/test/pos/" + poTestFiles[pTestCount], 'r', encoding ='utf-8') as review:
        poTeReview = str([x.rstrip().lower() for x in review])
        poTeReview = poTeReview.translate(str.maketrans('','',string.punctuation))
        poTeReviewList.append(poTeReview)
    pTestCount+=1
print("All necessary files compiled... now turning reviews into vectors")
#convert each review to a vector that tracks the count of appearing vocab words
finalTrainString = ''
finalTestString = ''
tempString = ''
count = 0
# our training file will append all negative review vectors then all positive review vectors
#if certain unseen words are counted in reviews and if they are not found in our vocab we exclude them from our vector, since our vector is supposed to represent vocab word counts

for review in neReviewList:
    count+=1
    print("Review " + str(count) + " compiled")
    vocabDict = dict.fromkeys(vocabDict, 0)
    revWords = review.split()
    finalTrainString+="label:negative"
    for word in revWords:
        if word in vocabDict:
            vocabDict[word]+=1 
    for x in list(set(revWords)):
        if x in vocabDict:
            tempString = ", " + x + ":" + str(vocabDict[x])
            finalTrainString+=tempString
    finalTrainString+="\n"

for review in poReviewList:
    count+=1
    print("Review " + str(count) + " compiled")
    vocabDict = dict.fromkeys(vocabDict, 0)
    revWords = review.split()
    finalTrainString+="label:positive"
    for word in revWords:
        if word in vocabDict:
            vocabDict[word]+=1 
    for x in list(set(revWords)):
        if x in vocabDict:
            tempString = ", " + x + ":" + str(vocabDict[x])
            finalTrainString+=tempString
    finalTrainString+="\n"

for review in neTeReviewList:
    count+=1
    print("Review " + str(count) + " compiled")
    vocabDict = dict.fromkeys(vocabDict, 0)
    revWords = review.split()
    finalTestString+="label:negative"
    for word in revWords:
        if word in vocabDict:
            vocabDict[word]+=1 
    for x in list(set(revWords)):
        if x in vocabDict:
            tempString = ", " + x + ":" + str(vocabDict[x])
            finalTestString+=tempString
    finalTestString+="\n"

for review in poTeReviewList:
    count+=1
    print("Review " + str(count) + " compiled")
    vocabDict = dict.fromkeys(vocabDict, 0)
    revWords = review.split()
    finalTestString+="label:positive"
    for word in revWords:
        if word in vocabDict:
            vocabDict[word]+=1 
    for x in list(set(revWords)):
        if x in vocabDict:
            tempString = ", " + x + ":" + str(vocabDict[x])
            finalTestString+=tempString
    finalTestString+="\n"

with open('processed-movies-training.txt', 'w+',  encoding ='utf-8') as finalTrainFile:
    finalTrainFile.write(finalTrainString)

with open('processed-movies-test.txt', 'w+',  encoding ='utf-8') as finalTestFile:
    finalTestFile.write(finalTestString)