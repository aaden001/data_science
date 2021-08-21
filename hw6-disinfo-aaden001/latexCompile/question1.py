# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 06:45:41 2021

@author: aadeniran
"""
import pandas as pd
import numpy as np
#read the files in pandas dataframe
dfile1= pd.read_csv("D1.csv")
dfile2 = pd.read_csv("D2.csv")

#sort them in order
dfile1 = dfile1.sort_values(by='# Citations in our Alternative Narrative Tweets',ascending=False)
dfile2 = dfile2.sort_values(by='Tweet count', ascending=False)

search = dfile1.copy()

#get only 10 items
dfile1 = dfile1.head(10)
dfile2 = dfile2.head(10)


#drop unwanted columns
dfile1.drop(['Primary Orientation (Determined through Content Analysis)', 'How Cited in Alternative Narrative of Shooting Events'],axis= 1,inplace=True)
dfile2.drop(['URL count'],axis =1, inplace=True)


#rename columns
dfile1.rename(columns={"# Citations in our Alternative Narrative Tweets":"Tweets","Media Type (Determined through Content Analysis)":"Website Type"},inplace=True)
dfile2.rename(columns={"Tweet count":"Tweet"},inplace=True)

#swap order for first d1
columns_swap = ["Domain","Tweets","Website Type"]
dfile1 = dfile1.reindex(columns=columns_swap)



#add new columns to the data with NAN values
dfile1['status']= np.nan
dfile2['Website Type']= np.nan
dfile2['status']= np.nan


#change column types to string
dfile2['Website Type'] = dfile2['Website Type'].astype(str)
dfile2['status'] = dfile2['status'].astype(str)
#print(dfile2.dtypes)

numCount = 0
temp =""
 #Match domains in top 10 D2 dataframe with D1 to obtain Website Media Type
for index, row in dfile2.iterrows():
    #find a match(es) and store as a dataframe
    temp = search[search['Domain'].str.contains(row['Domain'])]
    #check if data frame is empty
    if(len(temp) == 0):
        #assign NaN value
        final = np.nan
    else:
        #assigne Media Type to final value
        final = temp['Media Type (Determined through Content Analysis)'].iloc[0]
    #insert into dfile2 dataframe
    dfile2.at[index,"Website Type"] = final

dfile1.to_csv("Q1/D1processed.csv", index = False, header=True)
dfile2.to_csv("Q1/D2processed.csv", index = False, header=True)


#print(type(search[search['Domain'].str.contains("21stcenturywire.com")].iloc[0]))
#print(dfile1)

