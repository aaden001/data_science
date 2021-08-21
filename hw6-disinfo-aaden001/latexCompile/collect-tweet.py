# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 14:57:42 2021

@author: aadeniran
"""
import tweepy
import pandas as pd
import json
#will use finalB
finalB =pd.read_csv("Q2/finalB.csv")
print(finalB)

# OAuth2 procedure
consumer_key = "pnUItdX31QmYpHBFlVcYbocKQ"      # INSERT YOUR KEY HERE
consumer_secret = "gFNX2iztwhfL1tROFCX3UomwRbU8GjUJhHzLQat8DGxvBcyVmw"   # INSERT YOUR KEY HERE
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

collection = []

debug = 0
for index, row in finalB.iterrows():

    search_term = row['Domain']
    for page in tweepy.Cursor(api.search, q=search_term, tweet_mode='extended', lang='en').pages():
        
        for tweet in page:
            print("Tweet  \nnnnn")
            #ensure that links are present ran 29 of each
            if(len(tweet.entities["urls"]) > 0 and debug < 30):
                #Get all the required details
                dictP = {"Id":tweet.id_str,"Screen_name":tweet.user.screen_name,"Date":tweet.created_at.strftime("%Y%m%d%H%M%S"),"Search_Term":search_term,"Full_text":tweet.full_text,"Url":tweet.entities["urls"][0]["expanded_url"]}
                collection.append(dictP)
                debug +=1
            else:
                break
        if(debug > 29):
            debug =0
            break
final = pd.DataFrame(collection)
print(final)
final.to_csv("Q3/collection.csv", index = False, header=True)
#re read the file and get into right time format
parse = lambda x: pd.datetime.strptime(x,"%Y%m%d%H%M%S")
process = pd.read_csv("Q3/collectionR.csv",parse_dates=["Date"],date_parser=parse)
#convert to the real one collectionR
process.to_csv("Q3/collectionR.csv", index = False, header=True)
#used this website to convert csv to json
"""
https://csvjson.com/csv2json
"""