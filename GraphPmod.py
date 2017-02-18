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


import DFSmod

'''
Candidate generation
'''

#generation of the simplest candidate, no more than 3 nodes and at least two edges
#the construction is done with the respect of the constraint related to labels and edge values
def subExtSimple(fEdgesSet):
    result = []
    dfscode=set() #set used to store the value returned by the minDFSCode, it is used to avoid the creation of equal candidate.
    for i in range(len(fEdgesSet)):
        j=i+1
        while(j<len(fEdgesSet)):
            m=0
            temp1 = {}
            temp2 = {}
            temp3 = {}
            temp4 = {}
            if ((fEdgesSet[i][0] == fEdgesSet[j][1]) and (fEdgesSet[i][1] == fEdgesSet [j][0]) and (fEdgesSet[i][0] != fEdgesSet [i][1]) and (fEdgesSet[j][0] != fEdgesSet [j][1])):
                 graphLabel1={'v0':str(fEdgesSet[i][0]),'v1':str(fEdgesSet[i][1])}
                 graph1={'v0':[('v1', str(fEdgesSet[i][2]))], 'v1':[('v0', str(fEdgesSet[j][2]))]}
                 if(abs(int(fEdgesSet[i][2]) - int(fEdgesSet[j][2])) <=4):
                     R=DFSmod.minDFS(graph1,graphLabel1) #use of the DFScode to check the presence of repetitions
                     if(R not in dfscode):
                        result.append((graph1,graphLabel1,(min(int(fEdgesSet[i][2]),int(fEdgesSet[j][2])),max(int(fEdgesSet[i][2]),int(fEdgesSet[j][2]))),R))
                        dfscode.add(R)

            if ((fEdgesSet[i][1] == fEdgesSet[j][1]) and (fEdgesSet[i][0] != fEdgesSet[i][1]) and (fEdgesSet[i][1] != fEdgesSet[j][0]) and (fEdgesSet[i][0] != fEdgesSet[j][0]) and (fEdgesSet[i][0] != fEdgesSet[j][1]) ):
                 graphLabel1={'v0':str(fEdgesSet[i][1]),'v1':str(fEdgesSet[i][0]), 'v2':str(fEdgesSet[j][0])}
                 graph1={'v0':[], 'v1':[('v0', str(fEdgesSet[i][2]))], 'v2':[('v0', str(fEdgesSet[j][2]))]}
                 if(abs(int(fEdgesSet[i][2]) - int(fEdgesSet[j][2])) <=4):
                     R=DFSmod.minDFS(graph1,graphLabel1)
                     if(R not in dfscode):
                        result.append((graph1,graphLabel1,(min(int(fEdgesSet[i][2]),int(fEdgesSet[j][2])),max(int(fEdgesSet[i][2]),int(fEdgesSet[j][2]))),R))
                        dfscode.add(R)
            if ((fEdgesSet[i][0] == fEdgesSet[j][1]) and (fEdgesSet[i][0] != fEdgesSet[i][1]) and (fEdgesSet[i][0] != fEdgesSet[j][0]) and (fEdgesSet[i][1] != fEdgesSet[j][0]) and (fEdgesSet[i][1] != fEdgesSet[j][1]) ):
                 graphLabel1={'v0':str(fEdgesSet[j][0]),'v1':str(fEdgesSet[i][0]), 'v2':str(fEdgesSet[i][1])}
                 graph1={'v0':[('v1', str(fEdgesSet[j][2]))], 'v1':[('v2', str(fEdgesSet[i][2]))], 'v2':[]}
                 if(abs(int(fEdgesSet[i][2]) - int(fEdgesSet[j][2])) <=4):
                     R=DFSmod.minDFS(graph1,graphLabel1)
                     if(R not in dfscode):
                        result.append((graph1,graphLabel1,(min(int(fEdgesSet[i][2]),int(fEdgesSet[j][2])),max(int(fEdgesSet[i][2]),int(fEdgesSet[j][2]))),R))
                        dfscode.add(R)
            if ((fEdgesSet[i][0] == fEdgesSet[j][0]) and (fEdgesSet[i][0] != fEdgesSet[i][1]) and (fEdgesSet[i][0] != fEdgesSet[j][1]) and (fEdgesSet[i][1] != fEdgesSet[j][0]) and (fEdgesSet[i][1] != fEdgesSet[j][1]) ):
                 graphLabel1={'v0':str(fEdgesSet[i][0]),'v1':str(fEdgesSet[i][1]), 'v2':str(fEdgesSet[j][1])}
                 graph1={'v0':[('v1', str(fEdgesSet[i][2])), ('v2', str(fEdgesSet[j][2]))], 'v1':[], 'v2':[]}
                 if(abs(int(fEdgesSet[i][2]) - int(fEdgesSet[j][2])) <=4):
                     R=DFSmod.minDFS(graph1,graphLabel1)
                     if(R not in dfscode):
                        result.append((graph1,graphLabel1,(min(int(fEdgesSet[i][2]),int(fEdgesSet[j][2])),max(int(fEdgesSet[i][2]),int(fEdgesSet[j][2]))),R))
                        dfscode.add(R)
            j=j+1


    return result

#generation of bigger candidate
def subExtComplex(candidateSet,fEdges):
    dfsCode=set() #DFSCode set
    result=[]
    for candidato in candidateSet:
        grafo=candidato[0]
        subDomains=candidato[1]
        minE=int(candidato[2][0])
        maxE=int(candidato[2][1])
        domains=getDomains(subDomains)
        appset={}
        for source in grafo: #for each nodes in the graph we look for all the possible frequent edges that can be attached to the source node
            if(subDomains[source] not in appset):
                possibleFe=[z for z in fEdges if((z[0]==subDomains[source] and z[1]!=z[0] and z[1] not in domains ) or (z[1]==subDomains[source] and z[1]!=z[0] and z[0] not in domains))]
                appset[subDomains[source]]=possibleFe
            else:
                possibleFe=appset[subDomains[source]]
            newVer="v"+str(len(subDomains))
            for el in possibleFe:
                flagAd=0
                #preserving the 4 hours difference
                nMaxE=maxE
                nMinE=minE
                nEdg=int(el[2])
                if((maxE-minE)==4):
                    if(minE<=nEdg and maxE>=nEdg):
                        flagAd=1
                else:
                    if(nEdg<minE and (maxE-nEdg)<=4):
                        flagAd=1
                        nMinE=nEdg
                    elif(nEdg>maxE and (nEdg-minE)<=4):
                        flagAd=1
                        nMax=nEdg
                if(flagAd==1):
                    sbCopy=copy.deepcopy(subDomains)
                    grafoCopy=copy.deepcopy(grafo)
                    if(el[0]==subDomains[source]):
                        grafoCopy[source].append((newVer,el[2]))
                        grafoCopy[newVer]=[]
                        sbCopy[newVer]=el[1]
                    else:
                        grafoCopy[newVer]=[(source,el[2])]
                        sbCopy[newVer]=el[0]

                    dfsc=DFSmod.minDFS(grafoCopy,sbCopy) #use of the DFScode to check the presence of repetitions
                    if(dfsc not in dfsCode):
                        dfsCode.add(dfsc)
                        result.append((grafoCopy,sbCopy,(nMinE,nMaxE),dfsc))
                    #adding an edge among the already existent nodes
                    if(el[0]==subDomains[source]):
                        for nuovo in grafo:
                            if(subDomains[nuovo]==el[1]):
                                flag=0
                                vertex=nuovo
                                for elDentro in grafoCopy[source]:
                                    if(elDentro[0]==nuovo):
                                        flag=1
                                        break
                                if(flag==0):
                                    sbCopy=copy.deepcopy(subDomains)
                                    grafoCopy=copy.deepcopy(grafo)
                                    grafoCopy[source].append((vertex,el[2]))
                                    dfsc=DFSmod.minDFS(grafoCopy,sbCopy)
                                    if(dfsc not in dfsCode):
                                        dfsCode.add(dfsc)
                                        result.append((grafoCopy,sbCopy,(nMinE,nMaxE),dfsc))
    return result


#function used to get the domains given the labels associated to a graph
def getDomains(graphLabel):
    domains={}
    for x in graphLabel:
        la=graphLabel[x]
        if(la not in domains):
            domains[la]=[x]
        else:
            domains[la].append(x)
    return domains

'''
Input and output functions
'''
def readGraph(n):
    graph={}
    graphLabel={}
    iniz=re.compile('digraph [a-zA-Z]*{')
    label=re.compile('[0-9]+ [\[label=]')
    label_ed=re.compile('[0-9]+')
    finz="}"
    f=open(n,"r")
    lines=f.readlines()
    for line in lines:
        if(iniz.match(str(line))==None and finz!=line and label.match(str(line))==None):
            line_split=line.rstrip("\n").split(" ")
            if(len(line_split)!=1):
                labelEdge_t=label_ed.findall(line_split[4])
                if(line_split[0] in graph):
                    temp=graph[line_split[0]]
                    graph[line_split[0]]=temp+[(line_split[2],labelEdge_t[0])]
                else:
                    graph[line_split[0]]=[(line_split[2],labelEdge_t[0])]

        if(label.match(str(line))):
            line_split1=line.rstrip("\n").split(" ")
            graphLabel[line_split1[0]]=line_split1[5]
            if(line_split1[0] not in graph):
                graph[line_split1[0]]=[]
    return graph,graphLabel

def printResult(graph,graphLabel,i):
    file_out=open("test/risGrahp"+str(i)+".dot","w",)
    file_out.write("digraph Ris{\n")
    for x in graph:
        t_l=graph[x]
        for y in t_l:
            file_out.write(str(x) + " -> " + str(y[0]) + "  [label=\"" + str(y[1]) + "\"];\n")

    for x in graphLabel:
        file_out.write(str(x) + " [ label = \" "+graphLabel[x]+" \" ] \n")
    file_out.write("}")
    file_out.close()
