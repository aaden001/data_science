# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 00:36:05 2021

@author: adeni
"""
import pandas as pd
from urllib.parse import urlparse # for requesting parse


filePath = "Q2/final.csv"


storeSingleD =[]
myList = []


df = pd.read_csv(filePath,index_col=False, encoding='utf-8')
#convert to list
myList = df.values.tolist()



"""
Get through the URL
get the domain of url domain = urlparse('http://www.example.test/foo/bar').netloc
If array doesnt contain the domain
store in a new pandas datast(list becasueit much better) 

"""
#skip same domain and take first ten of the list
newList = []
count = 1
for item in myList:
    domain = urlparse(item[4]).netloc
    
    if (domain in storeSingleD):
        pass
    else:
        try:
            count = count +1
            storeSingleD.append(domain)
            newList.append([item[3],item[2],round(item[0],5),"","", item[4]])
        except Exception as r:
            print(r)
            
    if count > 10:
        break
#convert to pandas dataFrame
dp= pd.DataFrame(newList, columns=['Frequency','Total Word','TF','IDF','TF-IDF','URL'])        
dp.to_csv("Q2/actualFinal.csv",index=False)