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


#generation of the simplest candidate, no more than 3 nodes and at least two edges
#the construction is done with the respect of the constraint related to labels and edge values
def subExtSimple(fEdgesSet):
    result = []
    a=0
    b=0
    dfscode=set() #set used to store the value returned by the minDFSCode, it is used to avoid the creation of equal candidate.
    for i in range(len(fEdgesSet)):
        j=i+1
        while(j<len(fEdgesSet)):


            m=0
            temp1 = {}
            temp2 = {}
            temp3 = {}
            temp4 = {}
            #print(str(fEdgesSet[i])+" "+str(fEdgesSet[j]))
            if ((fEdgesSet[i][0] == fEdgesSet[j][1]) and (fEdgesSet[i][1] == fEdgesSet [j][0]) and (fEdgesSet[i][0] != fEdgesSet [i][1]) and (fEdgesSet[j][0] != fEdgesSet [j][1])):
                 graphLabel1={'v0':str(fEdgesSet[i][0]),'v1':str(fEdgesSet[i][1])}
                 graph1={'v0':[('v1', str(fEdgesSet[i][2]))], 'v1':[('v0', str(fEdgesSet[j][2]))]}
                 if(abs(int(fEdgesSet[i][2]) - int(fEdgesSet[j][2])) <=4):
                    # print("A")
                     R=DFSmod.minDFS(graph1,graphLabel1) #use of the DFScode to check the presence of repetitions
                     b+=1
                     if(R not in dfscode):

                        result.append((graph1,graphLabel1,(min(int(fEdgesSet[i][2]),int(fEdgesSet[j][2])),max(int(fEdgesSet[i][2]),int(fEdgesSet[j][2]))),R))
                        dfscode.add(R)

            if ((fEdgesSet[i][1] == fEdgesSet[j][1]) and (fEdgesSet[i][0] != fEdgesSet[i][1]) and (fEdgesSet[i][1] != fEdgesSet[j][0]) and (fEdgesSet[i][0] != fEdgesSet[j][0]) and (fEdgesSet[i][0] != fEdgesSet[j][1]) ):
                 graphLabel1={'v0':str(fEdgesSet[i][1]),'v1':str(fEdgesSet[i][0]), 'v2':str(fEdgesSet[j][0])}
                 graph1={'v0':[], 'v1':[('v0', str(fEdgesSet[i][2]))], 'v2':[('v0', str(fEdgesSet[j][2]))]}
                 if(abs(int(fEdgesSet[i][2]) - int(fEdgesSet[j][2])) <=4):
                    # print("B")
                     R=DFSmod.minDFS(graph1,graphLabel1)
                     b+=1
                     if(R not in dfscode):
                        result.append((graph1,graphLabel1,(min(int(fEdgesSet[i][2]),int(fEdgesSet[j][2])),max(int(fEdgesSet[i][2]),int(fEdgesSet[j][2]))),R))
                        dfscode.add(R)
            if ((fEdgesSet[i][0] == fEdgesSet[j][1]) and (fEdgesSet[i][0] != fEdgesSet[i][1]) and (fEdgesSet[i][0] != fEdgesSet[j][0]) and (fEdgesSet[i][1] != fEdgesSet[j][0]) and (fEdgesSet[i][1] != fEdgesSet[j][1]) ):
                 graphLabel1={'v0':str(fEdgesSet[j][0]),'v1':str(fEdgesSet[i][0]), 'v2':str(fEdgesSet[i][1])}
                 graph1={'v0':[('v1', str(fEdgesSet[j][2]))], 'v1':[('v2', str(fEdgesSet[i][2]))], 'v2':[]}
                 if(abs(int(fEdgesSet[i][2]) - int(fEdgesSet[j][2])) <=4):
                     R=DFSmod.minDFS(graph1,graphLabel1)
                     b+=1
                    # print("C")
                     if(R not in dfscode):
                        result.append((graph1,graphLabel1,(min(int(fEdgesSet[i][2]),int(fEdgesSet[j][2])),max(int(fEdgesSet[i][2]),int(fEdgesSet[j][2]))),R))
                        dfscode.add(R)
            if ((fEdgesSet[i][0] == fEdgesSet[j][0]) and (fEdgesSet[i][0] != fEdgesSet[i][1]) and (fEdgesSet[i][0] != fEdgesSet[j][1]) and (fEdgesSet[i][1] != fEdgesSet[j][0]) and (fEdgesSet[i][1] != fEdgesSet[j][1]) ):
                 graphLabel1={'v0':str(fEdgesSet[i][0]),'v1':str(fEdgesSet[i][1]), 'v2':str(fEdgesSet[j][1])}
                 graph1={'v0':[('v1', str(fEdgesSet[i][2])), ('v2', str(fEdgesSet[j][2]))], 'v1':[], 'v2':[]}
                 if(abs(int(fEdgesSet[i][2]) - int(fEdgesSet[j][2])) <=4):
                     R=DFSmod.minDFS(graph1,graphLabel1)
                     b+=1
                    # print("D")
                     if(R not in dfscode):
                        result.append((graph1,graphLabel1,(min(int(fEdgesSet[i][2]),int(fEdgesSet[j][2])),max(int(fEdgesSet[i][2]),int(fEdgesSet[j][2]))),R))
                        dfscode.add(R)
            j=j+1
            a+=1
    return result

#generation of bigger candidate
def nuovaGenerazione(candidateSet,fEdges):
    result=[]
    dfsCode=set()
    for candidato in candidateSet:
        grafo=copy.deepcopy(candidato[0])
        subDomains=copy.deepcopy(candidato[1])
        minE=int(candidato[2][0])
        maxE=int(candidato[2][1])
        domains=getDomains(subDomains)
        newVer="v"+str(len(subDomains))
        possibleFe=[z for z in fEdges if (z[0] in domains and z[1] not in domains  and z[0]!=z[1] ) or (z[1] in domains and z[0] not in domains and z[1]!=z[0]) or (z[0] in domains and z[1] in domains and z[0]!=z[1])]
        for freq in possibleFe:
            flagAd=0
            match=0
            nMaxE=maxE
            nMinE=minE
            nEdg=int(freq[2])
            if((maxE-minE)==4):
                if(minE<=nEdg and maxE>=nEdg):
                    flagAd=1
            else:
                if(nEdg<minE and (maxE-nEdg)<=4):
                    flagAd=1
                    nMinE=nEdg
                elif(nEdg>maxE and (nEdg-minE)<=4):
                    flagAd=1
                    nMaxE=nEdg
            if(freq[0] in domains and freq[1] not in domains and flagAd==1 and match==0):
                node=copy.deepcopy(domains[freq[0]][0])
                grafoCopy=copy.deepcopy(grafo)
                sbCopy=copy.deepcopy(subDomains)
                sbCopy[newVer]=freq[1]
                grafoCopy[node].append((newVer,freq[2]))
                grafoCopy[newVer]=[]
                dfsc=DFSmod.minDFS(grafoCopy,sbCopy) #use of the DFScode to check the presence of repetitions7
                match=1
                if(dfsc not in dfsCode):
                    dfsCode.add(dfsc)
                    result.append((grafoCopy,sbCopy,(nMinE,nMaxE),dfsc))
            if((freq[0] not in domains) and (freq[1] in domains) and flagAd==1 and match==0):
                node=copy.deepcopy(domains[freq[1]][0])
                grafoCopy=copy.deepcopy(grafo)
                sbCopy=copy.deepcopy(subDomains)
                sbCopy[newVer]=freq[0]
                grafoCopy[newVer]=[(node,freq[2])]
                dfsc=DFSmod.minDFS(grafoCopy,sbCopy) #use of the DFScode to check the presence of repetitions7
                match=1

                if(dfsc not in dfsCode):
                    dfsCode.add(dfsc)
                    result.append((grafoCopy,sbCopy,(nMinE,nMaxE),dfsc))
            if(freq[0] in domains and freq[1] in domains and flagAd==1 and match==0):
                nodeS=domains[freq[0]][0]
                nodeD=domains[freq[1]][0]
                grafoCopy=copy.deepcopy(grafo)
                sbCopy=copy.deepcopy(subDomains)
                presente=0
                for it in grafoCopy[nodeS]:
                    if(it[0]==nodeD):
                        presente=1
                if(presente==0):
                    grafoCopy[nodeS].append((nodeD,str(freq[2])))
                    dfsc=DFSmod.minDFS(grafoCopy,sbCopy) #use of the DFScode to check the presence of repetitions7
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

'''
def subExtComplex(candidateSet,fEdges):
    dfsCode=set() #DFSCode set
    result=[]
    for candidato in candidateSet:
        grafo=copy.deepcopy(candidato[0])
        subDomains=copy.deepcopy(candidato[1])
        minE=int(candidato[2][0])
        maxE=int(candidato[2][1])
        domains=getDomains(subDomains)
        appset={}
        for source in grafo: #for each nodes in the graph we look for all the possible frequent edges that can be attached to the source node
            temp=0
            if(subDomains[source] not in appset):
                possibleFe=[z for z in fEdges if((z[0]==subDomains[source] and z[1]!=z[0] and z[1] not in domains ) or (z[1]==subDomains[source] and z[1]!=z[0] and z[0] not in domains) or (z[0]==subDomains[source] and z[1]!=z[0] and z[1] in domains))]
                appset[subDomains[source]]=possibleFe
            else:
                possibleFe=appset[subDomains[source]]
            newVer="v"+str(len(subDomains))
            for el in possibleFe:

                skip=0
                flagAd=0
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
                        nMaxE=nEdg
                if(flagAd==1):
                    #adding an edge among the already existent nodes
                    sbCopy=copy.deepcopy(subDomains)
                    grafoCopy=copy.deepcopy(grafo)
                    flag=0
                    if(el[0]==subDomains[source]): ##confronto la labels
                        for nuovo in grafo:
                            if(subDomains[nuovo]==el[1]):
                                flag=0
                                vertex=nuovo
                                for elDentro in grafo[source]:
                                    if(elDentro[0]==nuovo):
                                        flag=1
                                        skip=1

                                if(flag==0):
                                    sbCopy1=copy.deepcopy(subDomains)
                                    grafoCopy1=copy.deepcopy(grafo)
                                    grafoCopy1[source].append((vertex,el[2]))
                                    dfsc1=DFSmod.minDFS(grafoCopy1,sbCopy1)
                                    temp+=1
                                    skip=1
                                    if(dfsc1 not in dfsCode):
                                        dfsCode.add(dfsc1)
                                        result.append((grafoCopy1,sbCopy1,(nMinE,nMaxE),dfsc1))
                    if(skip==0):
                        create=0
                        sbCopy=copy.deepcopy(subDomains)
                        grafoCopy=copy.deepcopy(grafo)
                        if(el[0]==subDomains[source]):
                            flag=0
                            grafoCopy[source].append((newVer,el[2]))
                            grafoCopy[newVer]=[]

                            sbCopy[newVer]=el[1]
                            create=1
                        else:
                            for nuovo in grafo:

                                if(subDomains[nuovo]==el[0]):
                                    flag=1
                            if(flag!=1):
                                grafoCopy[newVer]=[(source,el[2])]
                                sbCopy[newVer]=el[0]
                                create=1
                                #print candidato[3]+" caso 2 con arco "+str(el)
                        if(create==1):
                            print grafo
                            print grafoCopy
                            print sbCopy
                            dfsc=DFSmod.minDFS(grafoCopy,sbCopy) #use of the DFScode to check the presence of repetitions7
                            temp+=1
                            if(dfsc not in dfsCode):
                                dfsCode.add(dfsc)
                                result.append((grafoCopy,sbCopy,(nMinE,nMaxE),dfsc))

    return result
'''
