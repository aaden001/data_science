# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 18:59:18 2021

@author: aadeniran
"""
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
#read the json file
process = pd.read_json("Q3/csvjson.json")



"""
How many Tweet was gathered
"""
#answer 450 
print(process.shape[0])
#Answer 450 tweets gathered
"""
What was the time range of the tweets gathered
"""
maxx= process['Date'].min()
minn = process['Date'].max()

date_range = str(minn) + ' to ' +str(maxx)

#print(date_range)
#range from 2021-04-04 22:21:48 to 2021-03-27 20:25:22
"""
How many different accounts posted those tweets?
"""
accountNames = [] 
#put unique user name as a list
accountNames = process["Screen_name"].unique()
#convert to pandas data frame and dump as csv file

t = pd.DataFrame(accountNames, columns=["Unique Screen names"])
t.to_csv("Q3/unqiuer_screen_names.csv",index=False)
print(len(accountNames))
#answer 306 different  user
"""
For those domains that had at least one tweet, how many tweets did you discover for each domain?
To answer this question, create a bar chart showing the number of tweets for each domain.
https://stackoverflow.com/questions/17573814/count-occurrences-of-certain-words-in-pandas-dataframe
"""

#get all unique domains
#activistpost = process["Url"].str.contains("www.activistpost.com").sum()
print(process.loc[process["Url"].str.contains("www.activistpost.com")])
#try
#print(accountNames)

# Q3get the list of domains and search and get count
names =[]
totalTweet = []
#Q4 get the unique Screen_name count per domain 
uniqunamesCount =[]

d2 = pd.read_csv("Q2/finalB.csv")
#print(d2)
for index, row in d2.iterrows():
    #print(row["Domain"])
    names.append(row["Domain"])
    totalTweet.append(process["Url"].str.contains(row["Domain"]).sum())
    
    """
    Do Q4 as well
    """
    #Get the list of unique domains
    getUnique = process.loc[process["Url"].str.contains(row["Domain"])]
    uniqunamesCount.append(getUnique["Screen_name"].unique().size)
    #print(process["Url"].str.contains(row["Domain"]).sum())
    #print("{}  total tweets {}".format(row["Domain"], process["Url"].str.contains(row["Domain"]).sum())
#print(process)
#print(names)
#print(totalTweet)

#plot the graph Q3 bar chart showing the number of tweets for each domain.

ax = plt.gca()
ax.yaxis.grid()
plt.rcParams["figure.figsize"] =(15,8)
plt.bar(names,totalTweet)
plt.xticks(rotation =90)
plt.savefig("Q3/barchar.png",bbox_inches='tight')
plt.plot()
plt.show()

"""
Prepare data for Q4 (Top Ten shared domains in Q3)
arrange the values from highest to lowest
"""
d = {"Domain": names,"Total":totalTweet}
tweet = pd.DataFrame(d)
tweet.sort_values(by="Total",ascending=False,inplace=True)
tweet.to_csv("Q4/tweetPerDomain.csv",index=False)

#plot the graph Q4 bar chart showing the number of accounts for each domain.
ax = plt.gca()
ax.yaxis.grid()
plt.rcParams["figure.figsize"] =(15,8)
plt.bar(names,uniqunamesCount)
plt.xticks(rotation =90)
plt.savefig("Q4/barchar.png",bbox_inches='tight')
plt.plot()
plt.show()