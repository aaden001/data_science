# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 04:38:14 2021

@author: aadeniran
"""

from classify import *
import os
import glob
import pandas as pd

"""
Create a list of that classified topic as on topic and a list that classifies topic as off-topic
"""
goodList =[]
badList =[]

def sampleTrain(cl):
 for a in goodList:
     #for shopping
     cl.train(a, "on-topic")
     
 for b in badList:
     #for non-shopping classification
     cl.train(b, "off-topic")

"""
Train files pertaining to my topic 
"""

#Enter all shopping training data
path = 'Q1/train/mytopic'
for filename in glob.glob(os.path.join(path, '*.txt')):
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        text = f.read()
        encoded = text.encode("ascii", "ignore")
        decode_string = encoded.decode()
        goodList.append(decode_string)
"""
Train files not pertaining to my topic 
"""
#Enter all non shopping training data
path = 'Q1/train/notmytopic/'
for filename in glob.glob(os.path.join(path, '*.txt')):
     with open(os.path.join(os.getcwd(), filename), 'r') as f:
        text = f.read()
        encoded = text.encode("ascii", "ignore")
        decode_string = encoded.decode()
        badList.append(decode_string)
        

#call the classifier and store trained set using sampleTrain() function

cl = naivebayes(getwords)
sampleTrain(cl)

print("End of training \n")

#create a pandas data frame for table creation.
table = pd.DataFrame(columns=["Filename","actualTopic","classifiedAs"])

#Test shopping test data
print("Shopping test data: \n")
path = 'Q1/test/mytopic'
#Read text files from the directory above
for filename in glob.glob(os.path.join(path, '*.txt')):
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        text = f.read()
        #encode the text file as ascii then decode it back
        classValue = cl.classify(text.encode("ascii", "ignore").decode(), default='unknown')
        #create a row for the pandas dataframe
        new_row = {'Filename':filename, 'actualTopic':"shopping", 'classifiedAs':classValue}
        #insert row into the data frame
        table = table.append(new_row,ignore_index=True)
        print("For ", filename, " classified as ", classValue)

print("\n\n")
#Test non shopping test data
print("Non-shopping test data:\n")
path = 'Q1/test/notmytopic/'
for filename in glob.glob(os.path.join(path, '*.txt')):
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        text = f.read()
        #encode the text file as ascii then decode it back
        classValue = cl.classify(text.encode("ascii", "ignore").decode(), default='unknown')
        #create a row for the pandas dataframe
        new_row = {'Filename':filename, 'actualTopic':"non-shopping", 'classifiedAs':classValue}
        #insert row into the data frame
        table = table.append(new_row,ignore_index=True)
        print("For ", filename, " classified as ", classValue)

table.to_csv("Q5/final.csv",index=False)