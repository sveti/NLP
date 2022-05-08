# coding=utf8
import string
import math
import os.path
import sys

def cleanString(text):
    #remove all punctuation, whitespaces, make it all lowercase
    return text.translate(str.maketrans('','', string.punctuation)).rstrip().lower()


#split the input text in list of ngrams
#in this case bigrams -> n=2
def ngrams(text, n):
    text = text.split(' ')
    output = []
    for i in range(len(text)-n+1):
        output.append(text[i:i+n])
    return output


def main():

    #get filename from command line
    filename = sys.argv[-1]

    #store all the bigams
    bigrams=[]

    #in order to get the probability of the sentece I love you, we need to calculate the probability of P(love|I) * P(you|love)

    #splitting the needed input into bigrams
    p1 = ["i", "love"]
    p2 = ["love", "you"]
    # counters for the occurrences of the needed bigrams
    counterP1 = 0
    counterP2 = 0

    #count the occurances of the words I and Love, in order to get P(love|I) and P(you|love)
    countOfI=0
    countOfLove=0

    if(os.path.isfile(filename)):
        file = open(filename,"r")

        for line in file:
            #trim the input
            line = cleanString(line)
            #count the total occurrences of the words I and Love
            countOfI += line.count("i")
            countOfLove += line.count("love")
            #bigram splitting
            for i in ngrams(line,2):
                if (i == p1):
                    counterP1 += 1
                elif (i == p2):
                    counterP2 += 1


        # print(counterP1)
        # print(counterP2)
        # print(countOfI)
        # print(countOfLove)
        # print(counterP1/countOfI)
        # print(counterP2/countOfLove)


        probability = counterP1/countOfI * counterP2/countOfLove

        print('The probability of "I love you" is')
        print(probability)
    else:
        print("File"+ filename + " was not found!")

if __name__ == "__main__":
    main()