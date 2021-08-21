# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 23:31:36 2021

@author: adeni
"""

import  tweepy
import pandas as pd
import matplotlib.pyplot as plt

def auth():#authorization fo consumer key and consumer secret
    consumer_key ="pnUItdX31QmYpHBFlVcYbocKQ"
    consumer_secret ="gFNX2iztwhfL1tROFCX3UomwRbU8GjUJhHzLQat8DGxvBcyVmw"
    access_token ="3311358952-Gb5GEkFGvsv2IUFPuCEzChdkJCssh9B2mW9VsFG"
    access_token_secret ="t1UGfFdJR8qUmcxnTEMKkg3899iU63qd2zCwaNYgxPvcV"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth, wait_on_rate_limit= True)
    return api
def plot_the_pandas_data(df,fwfing):
    #using 
    if fwfing == 0:
        plt.title("Followers")
    else:
        plt.title("Followings")
    plt.rcParams['figure.figsize'] =40,25
    plt.rcParams['font.size'] = 17;
    plt.plot(df.USER,df.FRIENDCOUNT, label="FriendCount",marker='o')
    plt.grid(True)
    plt.xticks(rotation=90)
    plt.xlabel(xlabel = "friends", fontsize=20)
    plt.ylabel(ylabel= "number of friends", fontsize=20)
    plt.legend(loc=6,fontsize=25);
    
    return plt.show()
def handlePandasDF_Replacement(df):
    df = df.sort_values(by="FRIENDCOUNT")
    #print(df)
    f = "f"
    #create a list of new users
    newUser= []
    try:
        for x  in range(len(df)):
            c = f + str(x)
            newUser.append(c)
        # replace this new list to the column user in the dataframe
        df.USER = newUser
    except Exception as p:
        print(p)
    print(df)
    return df
def get_number_of_followers_followings(id,ingers):
    #get user 

    user = auth().get_user(id)
    try:
        if ingers == 0:
            #used to get the user ids followers count
            fwers_flowing = user.followers_count
        else:
            #used to get the users following count
            fwers_flowing = user.friends_count
        #print("{}: {}\n".format(user.screen_name,fwers_flowing))
    except Exception as p:
        print(p)
    return user.screen_name,fwers_flowing
def getUserFollowers(screen_name):
   users = []
   followersC = []
    #followers 
   p= tweepy.Cursor(auth().followers_ids,id=screen_name, wait_on_rate_limit= True).items(5000)
   c =1
   for ps in p:
       #parse in 0 to get the followers count
       us, count = get_number_of_followers_followings(ps,0)
       users.append(us)
       followersC.append(count)
       c=c +1
       if(c > 98):
           break;
   #inset into pandas
   prod = pd.DataFrame(list(zip(users,followersC)))
   #users.clear()
   #followersC.clear()
   #create a column names
   prod.columns = ["USER", "FRIENDCOUNT"]
   #sort and replace the names symbol fn
   prod = handlePandasDF_Replacement(prod)
   return prod
def getUserFollowings(screen_name):
   users = []
   followingsC = []
   #followings 
   p= tweepy.Cursor(auth().friends,id=screen_name, wait_on_rate_limit= True).items(5000)
   c =1
   for ps in p:
       #parse in 1 to get the following count instead
       us, count = get_number_of_followers_followings(ps.id,1)
       users.append(us)
       followingsC.append(count)
       c=c +1
       if(c > 98):
           break;
   #inset into pandas
   prod = pd.DataFrame(list(zip(users,followingsC)))
   users.clear()
   followingsC.clear()
   #create a column names
   prod.columns = ["USER", "FRIENDCOUNT"]

   #Sort and replace the names symbol fn
   prod = handlePandasDF_Replacement(prod)
   return prod
screen_name = "adeniran827"
try:
   """
   ===============Q2================
   """
   print("\n\n Get into the follower Count \n\n")
   f = getUserFollowers(screen_name)
   #data has been already sorted
   #get the men, std and meandia
   print("Mean : {}".format(f.FRIENDCOUNT.mean()))
   print("Standard deviation: {}".format(f.FRIENDCOUNT.std()))
   print("Median: {}".format(f.FRIENDCOUNT.median()))
   #print as a csv file
   f.to_csv("Q2/finalFollowers.csv",index=False)
   #plot the graph
   plot_the_pandas_data(f,0)
   #replace the names with fn
     
   #returns the dataframe of two columns USER and FRIENDCOUNT 
   #comes with user screen name and followers' count
   """
   ===============Q3================
   """
   print("\n\n Get into the followings Count \n\n")
   p = getUserFollowings(screen_name)
   #data has been already sorted
   #get the men, std and meandia
   print("Mean: {}".format(p.FRIENDCOUNT.mean()))
   print("Standard deviation: {}".format(p.FRIENDCOUNT.std()))
   print("Median: {}".format(p.FRIENDCOUNT.median()))
   #print as a csv file
   p.to_csv("Q3/finalFollowings.csv",index=False)
   #plot the graph
   plot_the_pandas_data(p,1)
   #REPEAT same code as friendPradoxpy -- I know I can make it a whole py file 
except Exception as r:
    print(r)
    