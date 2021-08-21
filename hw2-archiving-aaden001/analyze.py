# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 10:44:02 2021

@author: adeni
"""
import matplotlib.pyplot as plt
import pandas as pd
import json #to work with json files
from json.decoder import JSONDecodeError #for error handling json empty/wrong input file
from collections import OrderedDict #for ordering a dictionary
from datetime import datetime #
import seaborn as sns
#from matplotlib.ticker import MultipleLocator
old = 0 # track URI less old than a week
letCount = {}
accessDate = {}
dateAccessed = "2021-02-26T21:30:00Z"
count = 1
previous =0 #track highest mementos
MAX_MOMENTOUS = [] #store URI-Rs of maximum mementos
MAX_DAYS =[]  #store URI-Rs  of maximum duration
daysMementos1 =[] #to keep track of Oldest duration
daysMementos2 =[] #to keep track of momentos length
datetimeObject = datetime.strptime(dateAccessed,"%Y-%m-%dT%H:%M:%SZ")
for x in range(1000):
    #configure file ordering
    file = "Q2/json/"+ str(count) + ".json"
    try:
        with open(file, "rb") as f:
           #load file in a variable
           data = json.load(f)
           """
           ========================
           VVVVVVVVV=Q3=VVVVVVVVVVV
           ========================
           Get the number of days and mementos size 
           Get the URL of the highest duration(in days) -URI-R of Oldest Momentus
           Get the Number of URL with less than a week old
           """
           if(len(data['mementos']['list']) > 0):
               #convert to default time format
               prevsTime = datetime.strptime(data['mementos']['first']['datetime'],"%Y-%m-%dT%H:%M:%SZ")
               #get the duration with when the date accessed
               delta = datetimeObject - prevsTime
               #store the duration
               daysMementos1.append(delta.days)
               #store the mementos length
               daysMementos2.append(len(data['mementos']['list']))
               if(delta.days > 8112):
                   previousDay = delta.days
                   MAX_DAYS.append(data['original_uri'])
                   
               if(delta.days < 7):
                   old = old +1
           """
           ========================
           VVVVVVVVVV=Q2=VVVVVVVVVV
           ========================
           When a URI has a mementos number
           first entering the dictionary -letCount- we assign the mementos
           to key and assign it with a value 1
           
           When the same memtos number is found again
           An increment is done on the value on the key
           in the dictionary
           """
           if(letCount.get(len(data['mementos']['list'])) != None):
               #get length mememto and increase count of see same number of memento by one
               previous =  len(data['mementos']['list'])
               letCount[len(data['mementos']['list'])]=letCount.get(len(data['mementos']['list'])) + 1
           else:
               #get length of memento and store a new number of mementos found
               letCount[len(data['mementos']['list'])] = 1
               previous =  len(data['mementos']['list'])
           #Gets URL with mementos > 10000     
           if(previous> 40000):
                #saved the URI-Rs in a list
                MAX_MOMENTOUS.append(data['original_uri'])
    except JSONDecodeError  as e:
        #Takes care of error file therefore giving it a 0 mememtos 
        if(letCount.get(0) != None):
            #increments by one when more errors zero mememtos are found
            letCount[0] = letCount.get(0) +1
        else:
            #store new error as a zero key with 1 value
            letCount[0] = 1    
    #change to a new file number
    count = count +1
#sort and store
dict1 = OrderedDict(sorted(letCount.items()))
#convert to pandas object
df =pd.DataFrame(dict1.items(), columns=['Mementos','URI-Rs'])
#store as a csv file
df.to_csv("Q2/mementosURI-Rs.csv",index=False)
#[print(key,':',value) for key,value in dict1.items()]
#print("\n\n")

#convert list of top mementos URL-Rs to pandas object
f = pd.DataFrame(data=[*(MAX_MOMENTOUS)], columns=['Top URI-R With the Most Mementos'])
f.to_csv("Q2/topMentos.csv",index=False)


#convert list of top duration URL-Rs to pandas object
l = pd.DataFrame(data=[*(MAX_DAYS)], columns=['Top URI-R With the Most duration'])
l.to_csv("Q3/topDuration.csv",index=False)


dM = pd.DataFrame(list(zip(daysMementos1,daysMementos2)), columns=['days','mementos'])
#sort by days
dM =dM.sort_values(by=['days'])
#store as a csv file
dM.to_csv("Q3/durationMentos.csv",index=False)
#console output
print("============================")
print("=============Q2=============")
print("======Sorted by Mementos====")
print("============================")
print(df)
print("\n\n")
print(f)
print("\n\n")
print("============================")
print("=============Q3=============")
print("========Sorted by Days======")
print("============================")
print(dM)
print("\n\n")
print(l)
print("\n\n")
print("Number of URIs less than a week Old")
print(old)
#use seaborn
sns.set_style("whitegrid")
plt.figure(figsize=(40,21))
plt.title("Q3 Output File")
g= sns.scatterplot(x="days",y="mementos",data=dM)
# Show the plot
plt.show(g)
#fig, ax = plt.subplots(figsize=(40,15),sharex=False,sharey=False)
#g=sns.scatterplot(data=dM,x="days",y="mementos",size="days",sizes=(17,50))
print("\n\n")
#For console viewing