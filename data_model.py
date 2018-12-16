# Written for Data Mining 472 Project 2
# author: Seth Turnage
# date: 11/25/2018
# id: 1210810585
# desc: 
#       1. Creates a document term matrix
#       2. Randomly splits dataset into training and testing model, taken from the index and values of the dictionary, respectively
#       3. Trains and Tests Model
#       4. Outputs Evaluation

import glob, os
import pandas as pd
import numpy as np
import math
import json
import pprint
import matplotlib.pyplot as plt
#incase I wanted to add synonym detection
from nltk.corpus import wordnet
from sklearn.linear_model import LogisticRegression,SGDClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
def regressionFrom_TF_IDF(TF_IDF_INPUT, EVALUATE = True,name="anonymous regression model"):
    document_Term_Matrix = pd.DataFrame.from_dict(TF_IDF_INPUT)
    print("\nDocument term matrix for "+name+" created.\n")
    pprint.pprint(document_Term_Matrix)
    #figure out the correct index
    X = []
    for key in document_Term_Matrix.keys():
            X.append(TF_IDF_INPUT[key])
    #Y = [*TF_IDF_INPUT]
    Y = []
    for key in document_Term_Matrix.keys():
            total = 0
            for index_value in TF_IDF_INPUT[key]:
                if (index_value > 0):
                    total+=1
            Y.append(total)
    X_train, X_test, y_train, y_test = train_test_split(X, Y, random_state=12)
    #create regression model
    regressionModel = LogisticRegression()
    #train and test it 
    #print(X_train)
    regressionModel.fit(X_train, y_train)
    #EVALUATE IT
    if EVALUATE == True:
        print("Calculating regression model:\n\n")
        from sklearn.metrics import mean_squared_error
        predictions = regressionModel.predict(X_test)
        error = mean_squared_error(y_test, predictions)  
        print("Mean Squared Error for "+name+" is "+str(error)+"\n")
    
        