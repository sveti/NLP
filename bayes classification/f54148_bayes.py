import os.path
import string

def cleanLine(line):
    return line.translate(str.maketrans('','',string.punctuation+'„“')).rstrip().lower()


def checkProbability(newfileName,bagOfWords,frequencyOfBOWOther,frequencyOfBOWUni,initialOtherProbabily,iniatialUniProbability):
    probabilityOfOthers = initialOtherProbabily
    probabilityOfUni = iniatialUniProbability
    if (os.path.isfile(newfileName)):
        file = open(newfileName, "r", encoding='utf-8')
        for line in file:
            for i in cleanLine(line).split():
                if i in bagOfWords:
                    probabilityOfOthers *= frequencyOfBOWOther[i]
                    probabilityOfUni *= frequencyOfBOWUni[i]

    if probabilityOfOthers > probabilityOfUni:
        print("It is in others")
    else:
        print("It is in uni")

def main():
    uniFile="uni.txt"
    othersFile = "others.txt"
    othersCorpus=[]
    uniCorpus=[]

    if(os.path.isfile(othersFile)):
        file = open(othersFile,"r", encoding='utf-8')
        for line in file:
            for i in cleanLine(line).split():
                if i.isalnum():
                    othersCorpus.append(i)

    if(os.path.isfile(uniFile)):
        file = open(uniFile,"r", encoding='utf-8')
        for line in file:
            for i in cleanLine(line).split():
                if i.isalnum():
                    uniCorpus.append(i)

    initialOtherProbabily = len(othersCorpus)/(len(uniCorpus)+len(othersCorpus))
    iniatialUniProbability = len(uniCorpus)/(len(uniCorpus)+len(othersCorpus))

    bagOfWordsOthers = "bagOfWordsOthers.txt"
    bagOfWordsUni = "bagOfWordsUni.txt"

    bagOfWordsOthersArray = []
    bagOfWordsUniArray = []

    if (os.path.isfile(bagOfWordsOthers)):
        file = open(bagOfWordsOthers, "r",encoding='utf-8')
        for line in file:
            bagOfWordsOthersArray.append(line.strip())
    if (os.path.isfile(bagOfWordsUni)):
        file = open(bagOfWordsUni, "r", encoding='utf-8')
        for line in file:
            bagOfWordsUniArray.append(line.strip())

    bagOfWords = bagOfWordsOthersArray + bagOfWordsUniArray

    othersSet = set(othersCorpus)
    uniSet = set(uniCorpus)

    wordFormsInOther = len(othersSet)
    wordFormsInUni = len(uniSet)

    totalDictionaryLength = wordFormsInOther + wordFormsInUni

    probabilityOfBOWOther = {}
    probabilityOfBOWUni = {}
    for i in bagOfWords:
        probabilityOfBOWOther[i] = (othersCorpus.count(i)+1)/(len(othersCorpus)+totalDictionaryLength)
        probabilityOfBOWUni[i] = (uniCorpus.count(i)+1)/(len(uniCorpus)+totalDictionaryLength)

    checkProbability("newFileUni.txt",bagOfWords,probabilityOfBOWOther,probabilityOfBOWUni,initialOtherProbabily,iniatialUniProbability)
    checkProbability("newFileOthers.txt",bagOfWords,probabilityOfBOWOther,probabilityOfBOWUni,initialOtherProbabily,iniatialUniProbability)



if __name__=="__main__":
    main()