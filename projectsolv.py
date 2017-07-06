#Data Mining project years 2016/17
#authors: Alessandro Rizzuto - Francesco Contaldo
#project goal: Finding Frequent subrgraphs in an oriented labelled graph

import re
import copy
#import numpy
import itertools
from itertools import permutations
from itertools import chain
from random import uniform
import time

import GraphPmod
import CSP
import DFSmod

import sys

#main function that solves the problem
#the parameters are the graph, the graphLabel and the two thresholds
def frequentSubG(graph,graphLabel,thr,size):
    fEdges=countFrequentEdges(graph,graphLabel,thr) #take only the frequent edges from the input graph
    candidateSet=GraphPmod.subExtSimple(sorted(list(fEdges.keys()))) #generation of size 2 (size is the number of edges)
    candidateSetApp=copy.deepcopy(candidateSet)
    domains=GraphPmod.getDomains(graphLabel)
    solutionSet=[] #list used to avoid the presence of already existing assignments
    for el in candidateSetApp:
        if(CSP.isFrequent((el[0],el[1]),graph,domains,solutionSet,el[3])<thr):
            candidateSet.remove(el)
    iterations=2 #number of iterations -> at least solutions with size 2
    candidateSetPrevious=candidateSet
    while(len(candidateSet)!=0 and iterations<size):
        candidateSetPrevious=candidateSet
        candidateSetNew=GraphPmod.nuovaGenerazione(candidateSet,list(fEdges.keys())) #genration of bigger candidates -> adding all possible frequent edges
        candidateSetNewApp=copy.deepcopy(candidateSetNew)
        solutionSet=[]
        for el in candidateSetNewApp:
            r=CSP.isFrequent((el[0],el[1]),graph,domains,solutionSet,el[3])
            if(r<thr): #counting the occurrences of the candidate subgraph
                candidateSetNew.remove(el) #if the candidate does not respect the threshold is discarded
        candidateSet=candidateSetNew

        if(len(candidateSetNew)!=0):
            candidateSetPrevious=candidateSetNew
        iterations+=1
    p=0
    if(iterations==2):
        for t in candidateSetPrevious:
            GraphPmod.printResult(t[0],t[1],p)
            p+=1
        print("Number of total solutions -> ",len(candidateSetPrevious))
        print("Number of merged solutions -> ",len(candidateSetPrevious))
        print("Number of relations -> ",iterations)
    else:
        mergedResult=[]
        whoIsMerged=set()
        candidateC=copy.deepcopy(candidateSetPrevious)
        #comparing all the pairs of frequent subgraph
        candidateSetPrevious=sorted(candidateSetPrevious, key=lambda k: k[3])
        for k in range(len(candidateSetPrevious)):

            dfs1 = candidateSetPrevious[k][3]
            flagMerged=0
            if(dfs1 not in whoIsMerged):
                #whoIsMerged.add(k)
                whoIsMerged.add(dfs1)
                for i in range(k+1, len(candidateSetPrevious)):
                    dfs2 = candidateSetPrevious[i][3]
                    if (dfs2 not in whoIsMerged):
                        JarJar = DFSmod.jaroSimilarity(dfs1, dfs2)
                        if ((iterations == 3 and JarJar >= 0.9) or (iterations>3 and JarJar >= 0.8)): #if the Jaro Similarity is respected the two result are merged
                            #once one graph is merged into another it is discarded and no more considered
                            #print "MERGED ",dfs1,dfs2,JarJar
                            #print dfs1,dfs2
                            whoIsMerged.add(dfs2)
                            flagMerged=1
                            domain2=GraphPmod.getDomains(candidateSetPrevious[i][1])
                            domain1=GraphPmod.getDomains(candidateSetPrevious[k][1])
                            toAdd=[]
                            for t in candidateSetPrevious[k][1]:
                                for y in candidateSetPrevious[i][1]:
                                    if candidateSetPrevious[k][1][t] == candidateSetPrevious[i][1][y]:
                                        adjListI=candidateSetPrevious[i][0][y]
                                        for j in adjListI:
                                            labelDest=candidateSetPrevious[i][1][j[0]]
                                            newLabelDest=None
                                            if(labelDest in domain1):
                                                newLabelDest=domain1[labelDest][0]
                                            else:
                                                newLabelDest="v"+str(len(candidateSetPrevious[k][1]))
                                                toAdd.append((newLabelDest,labelDest))
                                                candidateSetPrevious[k][0][newLabelDest]=[]
                                            newEdges=(newLabelDest,j[1])
                                            if(newEdges not in candidateSetPrevious[k][0][t]):
                                                candidateSetPrevious[k][0][t].append(newEdges)
                                #break
                            for toA in toAdd:
                                candidateSetPrevious[k][1][toA[0]]=toA[1]
            #if(flagMerged==1 or (flagMerged==0 and k not in whoIsMerged)):
                #if(flagMerged==0):
                    #print "ALONE",dfs1
                mergedResult.append(copy.deepcopy(candidateSetPrevious[k]))
            #mergedResult.append(copy.deepcopy(candidateSetPrevious[k]))
            #whoIsMerged.add(k)


        p=0
        for el in mergedResult:
            GraphPmod.printResult(el[0],el[1],p)
            p+=1

        print("Number of merged solutions -> ",len(mergedResult))
        print("Number of total solutions -> ",len(candidateSetPrevious))
        print("Number of relations -> ",iterations)


#frequentEdges between label --> we are working with directed graph so the order matters
def countFrequentEdges(graph,graphLabel,thr):
    NOR=0 #count the number of relations on which we are working on
    fEdges={} #dictionary used to count the edges in the graph -> the keys are triple (source,dest,weight)
    #visit of all the structure
    for source in graph:
        adjList=graph[source]
        for dest in adjList:
            NOR+=1
            k=(graphLabel[source],graphLabel[dest[0]],dest[1])
            if(k in fEdges):
                t=fEdges[k]
                fEdges[k]=t+1
            else:
                fEdges[k]=1
    tempToDel=[k for k in fEdges if fEdges[k]<thr] #tempToDel contains all the edges that don't respect the threshold
    for k in tempToDel: del fEdges[k]
    #return fEdgesvisitM.append(DFS_Visit(graph,graphLabel,x,discovery,couple,visit,time)[0])
    #print("NUMBER OF EDGES ",NOR)
    return fEdges


def main():
    thr=int(sys.argv[1]) #input  -> support threshold
    size=int(sys.argv[2]) #input  -> size threshold
    graph,graphLabel=GraphPmod.readGraph("test/graphGenOut.dot") #read the file and build the graph || dictionary key(id):[(ids,edLabel),(ids,edLabel),(ids,edLabel)]
    frequentSubG(graph,graphLabel,thr,size)

if __name__ == "__main__":
    main()
