#Data Mining project years 2016/17
#authors: Alessandro Rizzuto - Francesco Contaldo
#project goal: Finding Frequent subrgraphs in an oriented labelled graph

import re
import copy
import numpy
import itertools
from itertools import permutations
from itertools import chain
from random import uniform



def isFrequent(el,graph,domains,solutionSet):
    subG=el[0]
    subGLabel=el[1]
    count=[]
    listT=[]
    dictAss={}
    for k in subGLabel:
        dictAss[k]=set()
    #For each edge in the candidate sugbgraph the structure "restricted domains" is created
    for x in sorted(subG):
        if(len(subG[x])!=0):
            if(len(dictAss[x])==0):
                la=domains[subGLabel[x]]
            else:
                la=dictAss[x]
        for y in sorted(subG[x]):
            if(len(dictAss[x])!=0):
                la=dictAss[x]
            if(len(dictAss[y[0]])==0):
                lb=domains[subGLabel[y[0]]]
            else:
                lb=dictAss[y[0]]
            temp=list(itertools.product(la,lb))
            temp1=[]
            for z in temp:
                if(z[0]!=z[1]):
                    temp1.append([z[0],z[1],y[1]])
            checkEdges(temp1,dictAss,graph,x,y[0]) # -> calculates the restricted domans
    CF=countFinal(dictAss,subG,subGLabel,graph,solutionSet)
    return CF

def countFinal(dictAss,subG,subGLabel,graph,solutionSet):
    count=[]
    temp=[]
    for k in sorted(dictAss):
        temp.append(dictAss[k])
    temp=list(itertools.product(*temp))
    keys=sorted(list(dictAss.keys()))
    temp=[k for k in temp if(len(k)==len(set(k)))] #creation of all possible assignments given the restricted domains
    sol=set()
    quanti=0
    for cand in temp:
        if(str(sorted(cand)) not in sol):
            flag=0
            for sorg in subG:
                for dest in subG[sorg]:
                    id1=keys.index(sorg) #sorg
                    id2=keys.index(dest[0]) #dest
                    if((cand[id2],dest[1]) not in graph[cand[id1]]): #if the edge uses the assignment, the value exists
                        flag=1
                        break
                if(flag==1):
                    break
            if(flag==0):
                sol.add(str(sorted(cand)))
                quanti+=1
    if(sorted(sol) not in solutionSet):
        solutionSet.append(copy.deepcopy(sorted(sol)))
    else:
        quanti=-1
    return quanti

#function used to construct the restricted domains
def checkEdges(listEdges,dictAss,graph,x,y):
    matchX=[]
    matchY=[]
    for elm in sorted(listEdges):
        tempListA=graph[elm[0]]
        if((elm[1],elm[2]) in tempListA):
            dictAss[x].add(elm[0])
            dictAss[y].add(elm[1])
            matchX.append(elm[0])
            matchY.append(elm[1])
    universeMatchX=[k[0] for k in listEdges]
    universeMatchY=[k[1] for k in listEdges]
    noMatchX=list(set(universeMatchX)-set(matchX))
    noMatchY=list(set(universeMatchY)-set(matchY))
    for p in noMatchX:
        if(p in dictAss[x]):
            dictAss[x].remove(p)
    for p in noMatchY:
        if(p in dictAss[y]):
            dictAss[y].remove(p)
'''
def countCicleIntheGraph(Lab1,Lab2,W1,W2,graph,domains):
    la=domains[Lab1]
    lb=domains[Lab2]
    count=0
    for x in la:
        adj=graph[x]
        for y in adj:
            if(y[0] in lb and y[1]==W1 and ((x,W2) in graph[y[0]])):
                count+=1
                break
    return count
'''
