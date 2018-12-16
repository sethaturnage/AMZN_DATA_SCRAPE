# Written for Data Mining 472 Project 2
# author: Seth Turnage
# date: 11/25/2018
# id: 1210810585
# desc: TD-IDF algorithm: returns array containing: positive reviews, negative reviews
import glob, os
import pandas as pd
import numpy as np
import math
import pprint
import json
import matplotlib.pyplot as plt
from nltk.corpus import wordnet
from autocorrect import spell

#List of stopwords
stopwords = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "i","ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the","this"]
#source: http://xpo6.com/list-of-english-stop-words/

def TF_IDF(localdirectory,displaygraphs=True):
    asins = []
    GoodReviews = {'ASIN':[],'ReviewId':[],'Text':[]}
    GoodReviewWords = {}
    GoodReviewWordsKeyList = []
    BadReviews = {'ASIN':[],'ReviewId':[],'Text':[]}
    BadReviewWords = {}
    BadReviewWordsKeyList = []
    os.chdir(localdirectory)
    for file in glob.glob("*.json"):
        with open(file) as json_data:
            d = json.load(json_data)
            retrievedASIN = os.path.splitext(os.path.basename(file))[0]
            asins.append(retrievedASIN)
            for index in range(0,len(d['Reviews'])):
                if d['Reviews'][index]['Rating'] < 3.0:
                    BadReviews['ASIN'].append(retrievedASIN)
                    BadReviews['ReviewId'].append(str(index))
                    SpellCorrectedList=[]
                    rawlist = sorted( list(filter(None,[word for word in d['Reviews'][index]['Text'].replace("\""," ").replace("."," ").replace(","," ").replace("!"," ").replace("?"," ").lower().split(" ") if word not in stopwords])) )
                    for word in rawlist:
                         SpellCorrectedList.append(spell(word))
                    BadReviews['Text'].append(SpellCorrectedList)    
                elif d['Reviews'][index]['Rating'] > 3.0: 
                    GoodReviews['ASIN'].append(retrievedASIN)
                    GoodReviews['ReviewId'].append(str(index))
                    SpellCorrectedList=[]
                    rawlist = sorted(list(filter(None,[word for word in d['Reviews'][index]['Text'].replace("\""," ").replace("."," ").replace(","," ").replace("!"," ").replace("?"," ").lower().split(" ") if word not in stopwords])))
                    for word in rawlist:
                         SpellCorrectedList.append(spell(word))
                    GoodReviews['Text'].append(SpellCorrectedList)
            
        for index in range(0,len(GoodReviews['Text'])):
            for term in GoodReviews['Text'][index]:
                GoodReviewWords.setdefault(term,[]).append(GoodReviews['ASIN'][index]+"_"+GoodReviews['ReviewId'][index])
        #print(GoodReviewWords)
        

        for index in range(0,len(BadReviews['Text'])):
            for term in BadReviews['Text'][index]:
                BadReviewWords.setdefault(term,[]).append(BadReviews['ASIN'][index]+"_"+BadReviews['ReviewId'][index])
        
        #print(BadReviewWords)
    #calculate TF-IDF
    GoodReviewWordsKeyList.append([*GoodReviewWords])
    BadReviewWordsKeyList.append([*BadReviewWords])
    freq_list_good = {}
    #print("got here")
    for docNumber, ASIN in enumerate(asins):
        #print(GoodReviewWords)W
        for term in GoodReviewWords.keys():
            #print(term + " TFIDF being collected")
            Document_Frequency = 0.00
            Frequency_Across_All_Documents = 0.00
            Number_Of_Documents = 0.00
            previous = ""
            for reviewID in GoodReviewWords[term]:
                if reviewID == previous:
                    Number_Of_Documents = Number_Of_Documents
                else:
                    Number_Of_Documents += 1.00

                if (reviewID.split("_")[0] == ASIN):
                    Document_Frequency +=1

                Frequency_Across_All_Documents+=1
  
                if term in freq_list_good:
                    if len(freq_list_good[term]) > docNumber:
                        if (freq_list_good[term][docNumber] >= 0.00 and Frequency_Across_All_Documents > 0 and Document_Frequency > 0 and Number_Of_Documents > 0):
                            freq_list_good[term][docNumber] = float(math.log(Document_Frequency*(Number_Of_Documents/Frequency_Across_All_Documents),2))
                        else:
                            freq_list_good[term][docNumber] = 0.00
                    else:
                        if (Frequency_Across_All_Documents > 0 and Document_Frequency > 0 and Number_Of_Documents > 0):
                            freq_list_good[term].append(float(math.log(Document_Frequency*(Number_Of_Documents/Frequency_Across_All_Documents),2)))
                        else:
                            for index in range(len(freq_list_good[term]),docNumber+1):
                                freq_list_good[term].append(0.00)
                else:
                    freq_list_good[term] = []
                    for index in range(0,docNumber):
                       freq_list_good[term].append(0.00)

    print("TF-IDF for good user reviews placed in dictionary.")
    pprint.pprint(freq_list_good)
    freq_list_bad = {}
    #print("got here")
    for docNumber, ASIN in enumerate(asins):
        #print(GoodReviewWords)W
        for term in BadReviewWords.keys():
            #print(term + " TFIDF being collected")
            Document_Frequency = 0.00
            Frequency_Across_All_Documents = 0.00
            Number_Of_Documents = 0.00
            previous = ""
            for reviewID in BadReviewWords[term]:
                if reviewID == previous:
                    Number_Of_Documents = Number_Of_Documents
                else:
                    Number_Of_Documents += 1.00

                if (reviewID.split("_")[0] == ASIN):
                    Document_Frequency +=1

                Frequency_Across_All_Documents+=1
  
                if term in freq_list_bad:
                    if len(freq_list_bad[term]) > docNumber:
                        if (freq_list_bad[term][docNumber] >= 0.00 and Frequency_Across_All_Documents > 0 and Document_Frequency > 0 and Number_Of_Documents > 0):
                            freq_list_bad[term][docNumber] = float(math.log(Document_Frequency*(Number_Of_Documents/Frequency_Across_All_Documents),2))
                        else:
                            freq_list_bad[term][docNumber] = 0.00
                    else:
                        if (Frequency_Across_All_Documents > 0 and Document_Frequency > 0 and Number_Of_Documents > 0):
                            freq_list_bad[term].append(float(math.log(Document_Frequency*(Number_Of_Documents/Frequency_Across_All_Documents),2)))
                        else:
                            for index in range(len(freq_list_bad[term]),docNumber+1):
                                freq_list_bad[term].append(0.00)
                else:
                    freq_list_bad[term] = []
                    for index in range(0,docNumber):
                       freq_list_bad[term].append(0.00)
        print("TF-IDF for bad user reviews placed in dictionary.")
        pprint.pprint(freq_list_bad)
    return [freq_list_good, freq_list_bad]
            

                
                


