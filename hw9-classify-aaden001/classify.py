# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 03:46:18 2021

@author: aadeniran
"""
import re
import math

"""
Splits the document into a list of words by non-alphs characters
"""
def getwords(doc):
  splitter=re.compile('\W+')  # different than book
  #print (doc)
  # Split the words by non-alpha characters
  words=[s.lower() for s in splitter.split(doc) 
          if len(s)>2 and len(s)<20]
  
  # Return the unique set of words only
  uniq_words = dict([(w,1) for w in words])

  return uniq_words

class basic_classifier:

  def __init__(self,getfeatures,filename=None):
    # Counts of feature/category combinations
    self.fc={}
    # Counts of documents in each category
    self.cc={}
    self.getfeatures=getfeatures
    
  # Increase the count of a feature/category pair  
  def incf(self,f,cat):
    self.fc.setdefault(f, {})
    self.fc[f].setdefault(cat, 0)
    self.fc[f][cat]+=1
  
  # Increase the count of a category  
  def incc(self,cat):
    self.cc.setdefault(cat, 0)
    self.cc[cat]+=1  

  # The number of times a feature has appeared in a category
  def fcount(self,f,cat):
    if f in self.fc and cat in self.fc[f]:
      return float(self.fc[f][cat])
    return 0.0

  # The number of items in a category
  def catcount(self,cat):
    if cat in self.cc:
        return float(self.cc[cat])
    return 0

  # The total number of items
  def totalcount(self):
    return sum(self.cc.values())

  # The list of all categories
  def categories(self):
    return self.cc.keys()

  def train(self,item,cat):
    features=self.getfeatures(item)
    # Increment the count for every feature with this category
    for f in features:
      self.incf(f,cat)

    # Increment the count for this category
    self.incc(cat)

  def fprob(self,f,cat):
    if self.catcount(cat)==0: return 0

    # The total number of times this feature appeared in this 
    # category divided by the total number of items in this category
    return self.fcount(f,cat)/self.catcount(cat)

    """
    default weight=1.0,ap=0.5 
    weight >= 0.6 and ap >= 0.9 for the classifier to be wrong
    weight >=0.7  and ap >= 0.8
    weight >=0.8  and ap >= 0.7
    weight >=0.9  and ap >= 0.6
    weight =15  and ap = 0.5  
    """
  def weightedprob(self,f,cat,prf,weight=1.0,ap=0.5):
    # Calculate current probability
    basicprob=prf(f,cat)

    # Count the number of times this feature has appeared in
    # all categories
    totals=sum([self.fcount(f,c) for c in self.categories()])

    # Calculate the weighted average
    bp=((weight*ap)+(totals*basicprob))/(weight+totals)
    return bp

#class naivebayes(classifier):   # change for basic_classifier
class naivebayes(basic_classifier):
  def __init__(self,getfeatures):   
    #classifier.__init__(self,getfeatures)  # change for basic_classifier
    basic_classifier.__init__(self,getfeatures)
    self.thresholds={}
  
  def docprob(self,item,cat):
    features=self.getfeatures(item)   

    # Multiply the probabilities of all the features together
    p=1
    for f in features: p*=self.weightedprob(f,cat,self.fprob)
    return p

  def prob(self,item,cat):
    catprob=self.catcount(cat)/self.totalcount()
    docprob=self.docprob(item,cat)
    return docprob*catprob
  
  def setthreshold(self,cat,t):
    self.thresholds[cat]=t
    
  def getthreshold(self,cat):
    if cat not in self.thresholds: return 1.0
    return self.thresholds[cat]
  
  def classify(self,item,default=None):
    probs={}
    # Find the category with the highest probability
    max=0.0
    for cat in self.categories():
      probs[cat]=self.prob(item,cat)
      if probs[cat]>max: 
        max=probs[cat]
        best=cat

    # Make sure the probability exceeds threshold*next best
    for cat in probs:
      if cat==best: continue
      if probs[cat]*self.getthreshold(best)>probs[best]: return default
    return best