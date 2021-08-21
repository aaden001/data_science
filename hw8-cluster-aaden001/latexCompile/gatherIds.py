# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 13:02:33 2021

@author: aadeniran
"""
import tweepy
from tweetparser import setup_api, confirm_usermetsrequiremetn
import pandas as pd
import numpy as np
def  per_account(types,secret =setup_api("secrets.json") ):
    
    #Get twitter friends screen_name of the parse account, as one arrayList
    public_tweets = tweepy.Cursor(secret.friends_ids, id = types)
    count= 1
    resultList =[] # store the final result of screen names
    for user in public_tweets.pages():
        #print(user)
        #print(user.dtypes())
        #Transverse the list of followers ids
        for i in user:
            #check if the friends meet the requirement
            #print(confirm_usermetsrequiremetn(secret,i))
            if(confirm_usermetsrequiremetn(secret,i) ==True):
                if( i not in resultList):
                    
                    #instead of the user id get the user name
                    user_sc = secret.get_user(i)
                    print("{}:{}".format(count,user_sc.screen_name))
                    resultList.append(user_sc.screen_name)
                    count += 1                    
            #Get maximum 30 file accounts screen_names
            if(count >= 30):
                break
    print(resultList)

    #build text file and save file in Q1 directory
    filename =  'Q1/' + types + '.txt'
    with open(filename, 'w') as filehandle:
        for listitem in resultList:
            filehandle.write('%s\n' % listitem)
    return resultList
"""
Tech account = @WIRED
Sport account = @WNBA
politics = @POTUS45
music = @future_of_music
"""
#Get all screen_names with that fulfils 10,000 followers and have 5000 tweets and verified
per_account("WIRED")
per_account("WNBA")
per_account("POTUS45")
per_account("future_of_music")

"""
Bring all result from the files in to One text file 
accounts.txt
"""
#get the list of the created files
column_name= ["User_screen_names"]
final = pd.DataFrame(columns= column_name)
fileList = ["Q1/WIRED.txt","Q1/WNBA.txt","Q1/POTUS45.txt","Q1/future_of_music.txt"]
df = pd.DataFrame()


for t in fileList:
    frame = pd.read_csv(t,header=None)
    frame.columns = column_name
    for ind in frame.index:
        final.loc[len(final)] =[frame['User_screen_names'][ind]]
        
#drop duplicated values keep just one of them
# dropping duplicate values
final.User_screen_names.drop_duplicates(inplace=True)  

#confirm that there are all unique values there are 113
print(final.User_screen_names.nunique())

# Number of rows to drop
n = 14
  
# Dropping last n rows using drop
final.drop(final.tail(n).index,
        inplace = True)
#print(final.User_screen_names.nunique())
numpy_array = final.to_numpy()
#print as a text file to in the same directory for future use
np.savetxt(r'accounts.txt', numpy_array,fmt="%s")