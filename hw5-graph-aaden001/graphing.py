# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 16:00:19 2021
@author: adeni
"""

import networkx as nx
import matplotlib.pyplot as plt
import re
import numpy as np
"""
TASK
1. Final result of the graph after breakdown
2. Iteration, color code the nodes connecting path and break.
"""

"""
https://gawron.sdsu.edu/python_for_ss/course_core/book_draft/Social_Networks/Networkx.html
def GirvanNewman():
  while (no edge left or desired number of communities unreached):
      calculate Betweeness of all edges
      remove the edge with the highest edge betweenness
      calculate the number of strongly connected component (communities)
"""
def colorCode(p,flag,listT):
    color_map = []
    lent = len(p)
    if flag == "" and len(listT) ==0:
        color_map = ['yellow'] * 34
        color_map[0] = "red"
        color_map[33] = "green"        
    elif(flag=="final" and len(listT) == 2):
        
        color_map = ['blue'] * 34
        for n in listT[0]:
            color_map[n] = "red"  
        for t in listT[1]:
            color_map[t] ="green"
    return color_map
def find_best_edge(G0):
    """
    Networkx implementation of edge_betweenness
    returns a dictionary. Make this into a list,
    sort it and return the edge with highest betweenness.
    """
    eb = nx.edge_betweenness_centrality(G0)
    eb_li = list(eb.items())
    eb_li.sort(key=lambda x: x[1], reverse=True)
    return eb_li[0][0]

def getComponent(G):
    if len(G.nodes()) == 1:
        return [G.nodes()]
    components = (G.subgraph(c) for c in nx.connected_components(G))
    components = list(components)
    count = 0
    while len(components) == 1:
        count +=1
        G.remove_edge(*find_best_edge(G))
        
        components =(G.subgraph(c) for c in nx.connected_components(G))        
        components = list(components)
    return components
def plot_theGraph(G, color, pathname,spaceing,edge_cl_map,weight_map):
    match = re.search(r'((Q[0-9]\/)([0-9a-zA-z]*\.png))',pathname)
    name = match.group(3)
    plt.figure(figsize=(15,8.8))
    plt.title(name,fontsize=20)
    if spaceing == "":
        nx.draw_kamada_kawai(G,with_labels=True, node_color = color)
    else:
        
        pos = nx.spring_layout(G, k=0.3*1/np.sqrt(len(G.nodes())) +0.1, iterations=20)
        nx.draw(G,with_labels=True ,node_color = color,pos=pos,edge_color=edge_cl_map,width = list(weight_map))

    plt.savefig(pathname, format="PNG")
    plt.show()
    plt.close()
    return 0
def set_color_edges(G,tuplesEdgeToRemove,reset):
    """
    This builds the edge attributes color and weight

    """
    totalEdges = G.number_of_edges()
    color_edge_map = ['black'] * totalEdges
    weight_map = [1.5] * totalEdges
    if(reset =="n"):
        total = -1
        for n in G.edges:
            total += 1
            if tuplesEdgeToRemove == n:
                color_edge_map[total] = 'blue'
                weight_map[total] = 3.2
    return color_edge_map,weight_map
def girvan_newman(G):
    components = (G.subgraph(c) for c in nx.connected_components(G))
    components = list(components)
    count =0
    while len(components) == 1:
        count +=1
        path = "Q2/" +str(count) +"a.png"
        #find the best Edge and return as a list
        bestEdge = find_best_edge(G)
        edge_color_mapped,weightMap = set_color_edges(G, bestEdge,"n")

        #print(edge_color_mapped)
        plot_theGraph(G,color_map,path,"spacing",edge_color_mapped,weightMap)
        #Remove the best edge
        G.remove_edge(*bestEdge)
        #ReSet everything back to black and reset the weight too
        edge_color_mapped,weightMap = set_color_edges(G, bestEdge,"")
        #Build string path after edge as been removed
        path = "Q2/" + str(count) +"b.png"
        
        plot_theGraph(G,color_map,path,"spacing",edge_color_mapped, weightMap)
        #if(count > 18):
        #    break
    return 0
try:

    karate = nx.karate_club_graph()
    t = karate
    """
    ===================================================
    Question 1a
    show group leaders in color coding
    ===================================================
    Got the data from networkx
    parsed the data to assign colorcoding for the two main leaders
    then plotted the graph
    """
    karate = nx.karate_club_graph()
    color_map = colorCode(karate, "","")
    plot_theGraph(karate,color_map, "Q1/karataHighlight.png","","","")
    """
    =======================================================================
    Question 1b , Question 2 , Question 3 and Extra Credit Q1
    show the categories based on the distribution as a color coded
    =======================================================================
    passed the retrieved data to the girvan_newman algorithm
    color coded the result of the splitted group
    then plotted the graph
    """
    #returns the broken components as two NodeView list)
    final = getComponent(karate)
    #print(final)
    #Set the colors based on the list received
    color_map = colorCode(karate,"final",final)
    plot_theGraph(karate,color_map,"Q1/finalGroup.png","","","")
    girvan_newman(t)
except Exception as e:
    print(e)