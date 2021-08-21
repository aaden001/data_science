# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 00:08:55 2021

@author: adeni
"""
import pandas as pd
import matplotlib.pyplot as plt


filePath = "HW4-friend-count.csv"
df = pd.read_csv(filePath,index_col=False, encoding='utf-8')
#remove extra spaces from columns (bad columns)
df.columns =[col.strip() for col in df.columns]



df = df.sort_values(by="FRIENDCOUNT")
f = "f"
#create a list of new users
newUser= []
for x  in range(98):
    c = f + str(x)
    newUser.append(c)
# replace this new list to the column user in the dataframe
df.USER = newUser
print(df) 
#print(df.keys)
print(df.FRIENDCOUNT.mean())
print(df.FRIENDCOUNT.std())
print(df.FRIENDCOUNT.median())
#using 
plt.rcParams['figure.figsize'] =40,25
plt.rcParams['font.size'] = 17;
plt.plot(df.USER,df.FRIENDCOUNT, label="FriendCount",marker='o')
plt.grid(True)
plt.xticks(rotation=90)
plt.xlabel(xlabel = "friends", fontsize=20)
plt.ylabel(ylabel= "number of friends", fontsize=20)
plt.legend(loc=6,fontsize=25);
