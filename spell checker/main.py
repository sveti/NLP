import os.path
import json

#keep the alphabet
alphabet=[chr(i) for i in range(ord('A'),ord('Z')+1)]

#get the soundex code of the word
def soundex(word):
    word = word.upper()
    removeThese = "AEIOUHWY"

    #remove from the inital word all these
    redactedWord = "".join(c for c in dict.fromkeys(word[1:]) if c not in removeThese)

    #handle two letter words
    if(redactedWord==""):
        return ""

    soundex=word[0]+"-"

    codeOne="BFPV"
    codeTwo="CGJKQSXZ"
    codeThree="DT"
    codeFive="MN"

    for i in redactedWord:
        if(codeOne.find(i) != -1):
            soundex+="1"
        elif(codeTwo.find(i) != -1):
            soundex+="2"
        elif(codeThree.find(i) != -1):
            soundex+="3"
        elif(i == "L"):
            soundex+="4"
        elif(codeFive.find(i) != -1):
            soundex+="5"
        elif(i =="R"):
            soundex+="6"
    return soundex

def createSoundexFile(wordsFileName,soundexDict,filename,allWords):
    wordsFile = [line.rstrip() for line in open(wordsFileName)]
    for word in wordsFile:
        allWords.append(word)
        soundexCode = soundex(word)
        if (soundexCode in soundexDict):
            soundexDict[soundexCode].append(word)
        else:
            soundexDict[soundexCode] = [word]
    with open(filename, 'w+') as outfile:
        json.dump(soundexDict, outfile)

#get all word variations via deletion
def delVariations(word):
    deletionSet = set()
    for i in range(len(word)):
        deletionSet.add(word[:i] + word[i + 1:])
    return deletionSet

#get all word variations via insertion
def insertVariations(word):
    insertionSet = set()
    for i in range(len(word) + 1):
        for letter in alphabet:
            insertionSet.add(word[:i] + letter + word[i:])
    return insertionSet

#get all word variations via replacement
def replaceVariations(word):
    replacementSet = set()
    for i in range(len(word)):
        for letter in alphabet:
            replacementSet.add(word[:i] +letter+ word[i + 1:])

    return replacementSet

def wordVariations(word):
    #get all the deletions on level 1 and merge them with level 1 + deletion, replacement and insertion
    deletionSet= set()
    deletionSet1=delVariations(word)

    for i in deletionSet1:
        deletionSet.update(delVariations(i))
        deletionSet.update(insertVariations(i))
        deletionSet.update(replaceVariations(i))

    deletionSet.update(deletionSet1)

    insertionSet=set()
    insertionSet1 = insertVariations(word)

    for i in insertionSet1:
        insertionSet.update(delVariations(i))
        insertionSet.update(insertVariations(i))
        insertionSet.update(replaceVariations(i))
    insertionSet.update(insertionSet1)

    replacementSet=set()
    replacementSet1 = replaceVariations(word)

    for i in replacementSet1:
        replacementSet.update(delVariations(i))
        replacementSet.update(insertVariations(i))
        replacementSet.update(replaceVariations(i))
    replacementSet.update(replacementSet1)

    #merge all 3 sets
    allSet = set()
    allSet = deletionSet
    allSet.update(insertionSet)
    allSet.update(replacementSet)
    return allSet

def getCandidates(allSet,dict):
    candidates = {}
    for w in allSet:
        soundexSuggestion = soundex(w)
        if soundexSuggestion in dict:
            if w in dict[soundexSuggestion]:
                #if the word is in here, this means it is in the words file => it is a word
                if w in candidates:
                    candidates[w]+=1
                else:
                    candidates[w]=1

    return candidates



def main():
    #find the main source of words
    print("Searching for a file with english words!")
    wordsFileName = "wordsEN.txt"

    #keep all the words of the words file in an array
    allWords = []

    #store the soundex of the words
    soundexDict = {}

    if (os.path.isfile(wordsFileName)):
        #found the words file
        print("Found it!")
        # the search for the soundex file begins
        print("Searching for a soundex file")
        filename = "soundex.json"

        #it exists, let's read it and store the info in a dict
        if (os.path.isfile(filename)):
            print("Found it! Reading it...")
            with open(filename) as infile:
                soundexDict = json.load(infile)
            wordsFile = [line.rstrip() for line in open(wordsFileName)]
            for word in wordsFile:
                allWords.append(word)
        else:
            #create it from scratch
            print("File not found, creating one!")
            createSoundexFile(wordsFileName,soundexDict,filename,allWords)
    else:
        print("File not found!")


    print("Enter a word")
    givenWord=input().upper()
    print("The word is " + givenWord)

    #keep the possible candidates as key and ans value how likely are they
    candidatesDict = {}

    #get the word variations
    preCandidatesSet = wordVariations(givenWord)

    candidatesDict=getCandidates(preCandidatesSet,soundexDict)

    #get the soundex candidates
    soundexCandidates = soundexDict[soundex(givenWord)]
    for w in soundexCandidates:
        if w in preCandidatesSet:
            candidatesDict[w]+=1

    #get the 10 monst likely candidates if there are 10
    candidatesDict = sorted(candidatesDict.items(), key=lambda x:x[1],reverse=True)
    print("Do you mean:")
    for w in candidatesDict[:10]:
        print(w[0])

if __name__ == "__main__":
    main()