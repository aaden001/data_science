# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 21:07:52 2021

@author: aadeniran
"""

from PIL import Image, ImageDraw
from math import sqrt
import random
import csv
import pandas as pd
def readfile(filename):
  # This is a function that I wrote from scratch   -MCW
  data = []
  rownames = []
  colnames = []
  num_rows = 0
  with open(filename) as tsvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    for row in reader:
      if num_rows > 0:
        rownames.append(row[0])    # save the row names
        data.append([float(x) for x in row[1:]])  # save the values as floats
      else:
        for col in row[1:]:
          colnames.append(col)    # save the column names
      num_rows = num_rows + 1
  return (rownames, colnames, data)

"""
names, word, data= readfiles('tweetdata.txt')
"""

def pearson(v1, v2):
  # Simple sums
    sum1 = sum(v1)
    sum2 = sum(v2)

  # Sums of the squares
    sum1Sq = sum([pow(v, 2) for v in v1])
    sum2Sq = sum([pow(v, 2) for v in v2])

  # Sum of the products
    pSum = sum([v1[i] * v2[i] for i in range(len(v1))])

  # Calculate r (Pearson score)
    num = pSum - sum1 * sum2 / len(v1)
    den = sqrt((sum1Sq - pow(sum1, 2) / len(v1)) * (sum2Sq - pow(sum2, 2)
               / len(v1)))
    if den == 0:
        return 0

    return 1.0 - num / den        
"""
MD5 Scaling
"""
def scaledown(data, distance=pearson, rate=0.01):
    n = len(data)

  # The real distances between every pair of items
    realdist = [[distance(data[i], data[j]) for j in range(n)] for i in
                range(0, n)]

  # Randomly initialize the starting points of the locations in 2D
    loc = [[random.random(), random.random()] for i in range(n)]
    fakedist = [[0.0 for j in range(n)] for i in range(n)]

    lasterror = None
    for m in range(0, 1000):
    # Find projected distances
        for i in range(n):
            for j in range(n):
                fakedist[i][j] = sqrt(sum([pow(loc[i][x] - loc[j][x], 2)
                                      for x in range(len(loc[i]))]))

    # Move points
        grad = [[0.0, 0.0] for i in range(n)]

        totalerror = 0
        for k in range(n):
            for j in range(n):
                if j == k:
                    continue
        # The error is percent difference between the distances
                errorterm = (fakedist[j][k] - realdist[j][k]) / realdist[j][k]

        # Each point needs to be moved away from or towards the other
        # point in proportion to how much error it has
                grad[k][0] += (loc[k][0] - loc[j][0]) / fakedist[j][k] \
                    * errorterm
                grad[k][1] += (loc[k][1] - loc[j][1]) / fakedist[j][k] \
                    * errorterm

        # Keep track of the total error
                totalerror += abs(errorterm)
        print (totalerror)

    # If the answer got worse by moving the points, we are done
        if lasterror and lasterror < totalerror:
            break
        lasterror = totalerror

    # Move each of the points by the learning rate times the gradient
        for k in range(n):
            loc[k][0] -= rate * grad[k][0]
            loc[k][1] -= rate * grad[k][1]

    return loc

def draw2d(data, labels, jpeg):
    img = Image.new('RGB', (2000, 2000), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    for i in range(len(data)):
        x = (data[i][0] + 0.5) * 1000
        y = (data[i][1] + 0.5) * 1000
        draw.text((x, y), labels[i], (0, 0, 0))
    img.save(jpeg, 'JPEG')

def rotatematrix(data):
    newdata = []
    for i in range(len(data[0])):
        newrow = [data[j][i] for j in range(len(data))]
        newdata.append(newrow)
    return newdata

"""
Hierarchical Clustering
class bicluster - data structure to hold the clustering information
hcluster(rows, distance=pearson) - does the hierarchical clustering, default distance function is pearson()
printclust(clust, labels=None, n=0) - traverses the cluster and prints an ASCII text representation
"""      
class bicluster:

    def __init__(self, vec, left=None, right=None, distance=0.0, id=None,):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance

def hcluster(rows, distance=pearson):
    distances = {}
    currentclustid = -1

  # Clusters are initially just the rows
    clust = [bicluster(rows[i], id=i) for i in range(len(rows))]

    while len(clust) > 1:
        lowestpair = (0, 1)
        closest = distance(clust[0].vec, clust[1].vec)

    # loop through every pair looking for the smallest distance
        for i in range(len(clust)):
            for j in range(i + 1, len(clust)):
        # distances is the cache of distance calculations
                if (clust[i].id, clust[j].id) not in distances:
                    distances[(clust[i].id, clust[j].id)] = \
                        distance(clust[i].vec, clust[j].vec)

                d = distances[(clust[i].id, clust[j].id)]

                if d < closest:
                    closest = d
                    lowestpair = (i, j)

    # calculate the average of the two clusters
        mergevec = [(clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i])
                    / 2.0 for i in range(len(clust[0].vec))]

    # create the new cluster
        newcluster = bicluster(mergevec, left=clust[lowestpair[0]],
                               right=clust[lowestpair[1]], distance=closest,
                               id=currentclustid)

    # cluster ids that weren't in the original set are negative
        currentclustid -= 1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)

    return clust[0]


def printclust(clust, labels=None, n=0):
  # indent to make a hierarchy layout
    for i in range(n):
        print (' ', end =" ")
    if clust.id < 0:
    # negative id means that this is branch
        print ('-')
    else:
    # positive id means that this is an endpoint
        if labels == None:
            print (clust.id)
        else:
            print (labels[clust.id])

  # now print the right and left branches
    if clust.left != None:
        printclust(clust.left, labels=labels, n=n + 1)
    if clust.right != None:
        printclust(clust.right, labels=labels, n=n + 1)

"""
Dendrogram
"""
def getheight(clust):
  # Is this an endpoint? Then the height is just 1
    if clust.left == None and clust.right == None:
        return 1

  # Otherwise the height is the same of the heights of
  # each branch
    return getheight(clust.left) + getheight(clust.right)


def getdepth(clust):
  # The distance of an endpoint is 0.0
    if clust.left == None and clust.right == None:
        return 0

  # The distance of a branch is the greater of its two sides
  # plus its own distance
    return max(getdepth(clust.left), getdepth(clust.right)) + clust.distance

def drawdendrogram(clust, labels, jpeg='clusters.jpg'):
  # height and width
    h = getheight(clust) * 20
    w = 1200
    depth = getdepth(clust)

  # width is fixed, so scale distances accordingly
    scaling = float(w - 150) / depth

  # Create a new image with a white background
    img = Image.new('RGB', (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.line((0, h / 2, 10, h / 2), fill=(255, 0, 0))

  # Draw the first node
    drawnode(
        draw,
        clust,
        10,
        h / 2,
        scaling,
        labels,
        )
    img.save(jpeg, 'JPEG')
    
def drawnode(
    draw,
    clust,
    x,
    y,
    scaling,
    labels,
    ):
    if clust.id < 0:
        h1 = getheight(clust.left) * 20
        h2 = getheight(clust.right) * 20
        top = y - (h1 + h2) / 2
        bottom = y + (h1 + h2) / 2
    # Line length
        ll = clust.distance * scaling
    # Vertical line from this cluster to children
        draw.line((x, top + h1 / 2, x, bottom - h2 / 2), fill=(255, 0, 0))

    # Horizontal line to left item
        draw.line((x, top + h1 / 2, x + ll, top + h1 / 2), fill=(255, 0, 0))

    # Horizontal line to right item
        draw.line((x, bottom - h2 / 2, x + ll, bottom - h2 / 2), fill=(255, 0,
                  0))

    # Call the function to draw the left and right nodes
        drawnode(
            draw,
            clust.left,
            x + ll,
            top + h1 / 2,
            scaling,
            labels,
            )
        drawnode(
            draw,
            clust.right,
            x + ll,
            bottom - h2 / 2,
            scaling,
            labels,
            )
    else:
    # If this is an endpoint, draw the item label
        draw.text((x + 5, y - 7), labels[clust.id], (0, 0, 0))
"""
K-Means Clustering
"""       
def kcluster(rows,k,distance=pearson ):
  # Determine the minimum and maximum values for each point
    ranges = [(min([row[i] for row in rows]), max([row[i] for row in rows]))
              for i in range(len(rows[0]))]

  # Create k randomly placed centroids
    clusters = [[random.random() * (ranges[i][1] - ranges[i][0]) + ranges[i][0]
                for i in range(len(rows[0]))] for j in range(k)]

    lastmatches = None
    for t in range(100):
        print ('Iteration %d' % t)
        bestmatches = [[] for i in range(k)]

    # Find which centroid is the closest for each row
        for j in range(len(rows)):
            row = rows[j]
            bestmatch = 0
            for i in range(k):
                d = distance(clusters[i], row)
                if d < distance(clusters[bestmatch], row):
                    bestmatch = i
            bestmatches[bestmatch].append(j)

    # If the results are the same as last time, this is complete
        if bestmatches == lastmatches:
            break
        lastmatches = bestmatches

    # Move the centroids to the average of their members
        for i in range(k):
            avgs = [0.0] * len(rows[0])
            if len(bestmatches[i]) > 0:
                for rowid in bestmatches[i]:
                    for m in range(len(rows[rowid])):
                        avgs[m] += rows[rowid][m]
                for j in range(len(avgs)):
                    avgs[j] /= len(bestmatches[i])
                clusters[i] = avgs

    return bestmatches

"""
Question 3 
"""
#running the code
tweetdata, word,data =readfile("tweetdata.txt")
#clust = hcluster(data)
#print(clust.vec)

"""
Question 3  ASCIII
To view  cluster

printclust(clust,labels=tweetdata)
"""
"""
Question 3 Dendrogram


drawdendrogram(clust,tweetdata,jpeg="Q3/tweetdata.jpeg")

"""
"""
Question 4
"""
"""
For 5  kcluster
number of iteration:
    Iteration 0
    Iteration 1
    Iteration 2
    Iteration 3
    Iteration 4
    Iteration 5
    Iteration 6
    Iteration 7
    Iteration 8
    Iteration 9
    Iteration 10
    Iteration 11
    Iteration 12
Cluster summary:
    cluster  1 :  0
    cluster  2 :  42
    cluster  3 :  0
    cluster  4 :  0
    cluster  5 :  56


"""

kclust5 = kcluster(data,5)
#print(len(kclust5))
for i in range(len(kclust5)):
  print ("cluster ", i+1, ": ", len(kclust5[i]))
  for r in kclust5[i]:
      filen= 'Q4/kclust5cluster'+ str(i+1)+'.csv'
      with open(filen, 'a+') as myfile:
          myfile.write(tweetdata[r])
          myfile.write("\n")

"""
For 10  kcluster

number of iteration:
    Iteration 0
    Iteration 1
    Iteration 2
    Iteration 3
    Iteration 4
Cluster summary:   
    cluster  1 :  0
    cluster  2 :  0
    cluster  3 :  0
    cluster  4 :  5
    cluster  5 :  3
    cluster  6 :  0
    cluster  7 :  1
    cluster  8 :  87
    cluster  9 :  0
    cluster  10 :  2
"""

kclust10 = kcluster(data,10)
for i in range(len(kclust10)):
  print ("cluster ", i+1, ": ", len(kclust10[i]))
  for r in kclust10[i]:    
      filen= 'Q4/kclust10cluster'+ str(i+1)+'.csv'
      with open(filen, 'a+') as myfile:
          myfile.write(tweetdata[r])
          myfile.write("\n")

"""
For 20  kcluster

number of iteration:
    Iteration 0
    Iteration 1
    Iteration 2
    Iteration 3
    Iteration 4
    Iteration 5
clusters summary:
    cluster  1 :  0
    cluster  2 :  54
    cluster  3 :  0
    cluster  4 :  0
    cluster  5 :  7
    cluster  6 :  0
    cluster  7 :  0
    cluster  8 :  0
    cluster  9 :  0
    cluster  10 :  0
    cluster  11 :  0
    cluster  12 :  0
    cluster  13 :  0
    cluster  14 :  1
    cluster  15 :  0
    cluster  16 :  0
    cluster  17 :  6
    cluster  18 :  26
    cluster  19 :  0
    cluster  20 :  4
"""


kclust20 = kcluster(data,20)
for i in range(len(kclust20)):
  print ("cluster ", i+1, ": ", len(kclust20[i]))
  filen= 'Q4/kclust20cluster'+ str(i+1)+'.csv'
  for r in kclust20[i]:
      with open(filen, 'a+') as myfile:
          myfile.write(tweetdata[r])
          myfile.write("\n")

"""
Question 5 ='mds2d.jpg'

23380.029615352396
140722.48343299245

98 lenght of coord variable
"""
coords = scaledown(data)
print(len(coords))
draw2d(coords, tweetdata, jpeg='Q5/tweets2d.jpg')
