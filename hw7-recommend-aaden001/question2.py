# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 00:46:12 2021

@author: aadeniran
"""
from math import sqrt

def sim_pearson(prefs, p1, p2):
    """
    Returns the Pearson correlation coefficient for p1 and p2.
    """

# Get the list of mutually rated items
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1
            
# If they are no ratings in common, return 0
    if len(si) == 0:
        return 0

# Sum calculations
    n = len(si)

 # Sums of all the preferences
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

# Sums of the squares
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])

 # Sum of the products
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

 # Calculate r (Pearson score)
    num = pSum - sum1 * sum2 / n
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n
    ))
    if den == 0:
        return 0
    r = num / den
    return r

def getRecommendations(prefs, person, similarity=sim_pearson):
    """
     Gets recommendations for a person by using a weighted average
     of every other user’s rankings
    """
    totals = {}
    simSums = {}
    for other in prefs:
        # Don’t compare me to myself
        if other == person:
            continue
        sim = similarity(prefs, person, other)
        # Ignore scores of zero or lower
        if sim <= 0:
            continue
        for item in prefs[other]:
            # Only score movies I haven’t seen yet
            if item not in prefs[person] or prefs[person][item] == 0:
                # Similarity * Score
                totals.setdefault(item, 0)
                # The final score is calculated by multiplying each item by the
                # similarity and adding these products together
                totals[item] += prefs[other][item] * sim
                # Sum of similarities
                simSums.setdefault(item, 0)
                simSums[item] += sim
                # Create the normalized list
        rankings = [(total / simSums[item], item) for (item, total) in
                            totals.items()]
        # Return the sorted list
        rankings.sort()
        rankings.reverse()
        return rankings

def topMatches(prefs,person,n=5,similarity=sim_pearson,):
    '''
    Returns the best matches for person from the prefs dictionary. 
    Number of results and similarity function are optional params.bottomMatches
    '''

    scores = [(similarity(prefs, person, other), other) for other in prefs
              if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]

def bottomMatches(prefs,person,n=5,similarity=sim_pearson,):
    """
    Returns the lowest matches for person from the prefs dictionary.
    Number of results and similarity function are optional params.
    """
    scores = [(similarity(prefs, person, other), other) for other in prefs
              if other != person]
    scores.sort()
    scores.reverse()
    return scores[len(scores)-n: len(scores)]

def transformPrefs(prefs):
    '''
    Transform the recommendations into a mapping where persons are described
    with interest scores for a given title e.g. {title: person} instead of
    {person: title}.
    '''

    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            # Flip item and person
            result[item][person] = prefs[person][item]
    return result

def loadMovieLens():
    # Get movie titles
    movies = {}
    for line in open("movie/u.item"):
        (id, title) = line.split("|")[0:2]
        movies[id] = title
    # Load data
    #prefs = {}
    for line in open("movie/u.data"):
        (user, movieid, rating, ts) = line.split("\t")
        prefs.setdefault(user, {})
        prefs[user][movies[movieid]] = float(rating)
    #Load in users
    #users = []
    for line in open("movie/u.user"):
        (user, age, gender, occupation, zipcode) = line.split("|")
        dictA = {"user": user, "age":age, "gender": gender, "occupation" :occupation }
    users.append(dictA)


prefs ={}
users =[]
loadMovieLens()

top5 = topMatches(prefs, "301", n = 5, similarity = sim_pearson)
bottom5 = bottomMatches(prefs, "928", n = 5, similarity = sim_pearson)
"""
Question 2
(1.0000000000000029, '801')
(1.0, '845')
(1.0, '140')
(1.0, '111')
(0.999999999999992, '565')


(-1.000000000000004, '760')
(-1.000000000000004, '547')
(-1.000000000000004, '432')
(-1.000000000000004, '317')
(-1.000000000000004, '112')
"""

print("Top 5 users that  most correlate with my substitute me ")
print(*top5, sep='\n')
print("\n\n")
print(" 5 users that least correlate with my substitute me ")
print(*bottom5, sep='\n')

"""
Question 3
(5.0, 'Unforgettable (1996)')
(5.0, 'Net, The (1995)')
(5.0, 'Murder in the First (1995)')
(5.0, 'Murder at 1600 (1997)')
(5.0, 'Just Cause (1995)')


(2.0, 'Diabolique (1996)')
(2.0, 'Devil in a Blue Dress (1995)')
(2.0, 'Breakdown (1997)')
(1.0, 'Thinner (1996)')
(1.0, 'Albino Alligator (1996)')
"""
recommend = getRecommendations(prefs,"301")
print("\nTop 5 movies recommendations for substitute me: ")
print(*recommend[0:5], sep="\n")
print("\nBottom 5 movies recommendations for substitute me:")
print(*recommend[len(recommend)-5: len(recommend)], sep="\n")


"""
Question 4

[(1.000000000000004, 'Young Guns II (1990)'), (1.000000000000004, 'Reality Bites (1994)'), (1.000000000000001, 'Ran (1985)'), (1.000000000000001, 'Butch Cassidy and the Sundance Kid (1969)'), (1.0000000000000009, 'Chinatown (1974)')]



[(-1.0, 'Big Night (1996)'), (-1.0, 'Barbarella (1968)'), (-1.0, 'Another Stakeout (1993)'), (-1.0000000000000007, "Fathers' Day (1997)"), (-1.000000000000004, "Devil's Own, The (1997)")]

"""
print("\n\n")
movies = transformPrefs(prefs)
mybestmovie = "Vampire in Brooklyn (1995)"
topFive = topMatches(movies, mybestmovie)

print("My best 5 recommended movies")
print(topFive)
print("\n")
print("My worst 5 recommended movies")
worstFive = bottomMatches(movies,mybestmovie)
print(worstFive)