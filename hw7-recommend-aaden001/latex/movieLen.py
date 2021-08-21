# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 20:09:11 2021

@author: aadeniran
"""
import pandas as pd

def closetToMeAgeGendOccu(item,data):

    #load movies data into variables
    movies = {}
    for line in open(str(item)):
        (id, title) = line.split('|')[0:2]
        movies[id] = title
    # Load data
    prefs = {}
    for line in open(str(data)):
        (user, movieid, rating, ts) = line.split('\t')
        prefs.setdefault(user, {})
        prefs[user][movies[movieid]] = float(rating)
    #Load in users
    users = []
    for line in open('movie/u.user'):
        (user, age, gender, occupation, zipcode) = line.split('|')
        dictA = {'user': user, 'age':age, 'gender': gender, 'occupation' :occupation }
        users.append(dictA)
    
    count = 1
    #hold 3 similar user in term of age gender and category
    similarUser =[]
    #Find all users that have things common with me 
    for a in users:
        """
        Here i parsed in my age gender and occupation
        to find users of my age gender and occupation category.
        I take only 3 users
        """
        if a['age'] == '24' and a['gender'] == 'M' and a['occupation'] == 'student' and count < 4 :
            similarUser.append(a['user'])
            count += 1
    
    #print user movie likes
    for a in similarUser:
        """
        Based on similar users like me,
        I obtained these similar users top 3 favorite films 
        """
        if a in prefs:
            #this gets the movie names, and the movie rating per user
            p = pd.DataFrame(list(prefs[a].items()),columns=["Movie Names","Rating"])
            #this sort the users movie list based on rating in decending order
            p.sort_values("Rating",ascending=False, inplace=True)
            #gets the top3 films
            top3 = p.head(3)
            #gets the bottom 3 films
            bottom3 = p.tail(3)
            #print("Top 3 films for User {}:".format(a))
            #print(top3)
            #print("\n\n")
            #print("Bottom 3 films for User {}:".format(a))
            #print(bottom3)
            #print("\n")
            top3.to_csv("Q1/"+a+"top3.csv",index=False)
            bottom3.to_csv("Q1/"+a+"bottom.csv",index=False)
    


"""
Question 1 solution
"""
closetToMeAgeGendOccu('movie/u.item','movie/u.data')
