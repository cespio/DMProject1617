#Data Mining project years 2016/17
#authors: Alessandro Rizzuto - Francesco Contaldo
#project goal: Finding Frequent subrgraphs in an oriented labelled graph
from __future__ import division
import re
import copy
import itertools
from itertools import permutations
from itertools import chain
from random import uniform


#minDFS, function that takes as input a graph and its labels and calculate the minDFScode as a string
def minDFS(graph,graphLabel):
    visits=allvisitDFS(graph,graphLabel) #calculate first all the DFSCodes related to the different DFS visits
    sortedIn=[]
    risf=[]
    result=sortDFSVisit(visits[0],simpleCMP)
    dfscode=""
    for k in result:
        for y in k:
            if(isinstance(y,int)):
                dfscode=dfscode+str(y)
            else:
                dfscode=dfscode+y
    return dfscode

#allvisitDFS takes as input a graph and its labels and then calculate all possible DFS visits using some nodes as root
#it returns a list of DFSCodes
def allvisitDFS(graph,graphLabel):
    return_temp=makeItUndir(graph,graphLabel)  #to have a connected graph we first build an undirected input graph version
    undGraph=return_temp[0]
    stragglers=return_temp[1]       #the stragglers are the set of edges that we lost building the undirected versions, e.g.: loops of two nodes
    visits=[]
    keys=sorted(list(graphLabel.values()))
    candidateRoots=[]
    for el in graphLabel:
        if(graphLabel[el]==keys[0]): #to reduce the number of visit we always start from the vertex that have the minimum label value
            candidateRoots.append(el)
    save_stragglers=copy.deepcopy(stragglers)
    for candidate in sorted(candidateRoots):
        app=DFS_visit(undGraph,graph,graphLabel,candidate,stragglers)
        stragglers=copy.deepcopy(save_stragglers)
        visits.extend(app)

    return visits

def simpleCMP(a,b):
    if(a[0]<b[0] or (a[0]==b[0] and a[1]<b[1])):
        return True
    else:
        return False

#function that implements all possible DFS visits starting from a given root
#then all the different calculated DFSCodes are stored in order to be sorted and to find the minimum
#the input for this function are the undirected graph,the original one and its labels, the starting node (candidate) and the stragglers set
def DFS_visit(undGraph,graph,graphLabel,candidate,stragglers):
    discovery={}  #hash table used to store the discovery time of each node
    visit=[]      #the list for the DFScodes
    father={}     #to avoid to come back in the undericted graph
    contenitor=[] #to store the whole the difs codes
    def DFS(undGraph,graph,graphLabel,x,visit,father,discovery,contenitor,stragglers):
        fatherperm=copy.deepcopy(father)
        discoveryperm=copy.deepcopy(discovery)
        visitperm=copy.deepcopy(visit)
        stragglersperm=copy.deepcopy(stragglers)
        perm=sortADJ(undGraph[x],graphLabel,undGraph,x)
        for p in perm:
            adjList=p
            for el in adjList:
                if(el[0] not in discovery):
                    discovery[el[0]]=len(discovery)
                    father[(x,el[0])]=1
                    father[(el[0],x)]=1
                    if(el in graph[x]): #forward edges
                        visit.append((discovery[x],discovery[el[0]],graphLabel[x],el[1],graphLabel[el[0]]))
                        if((el[0],x) in stragglers):
                            w=0
                            for app in graph[el[0]]:
                                if(app[0]==x):
                                    w=app[1]
                                    break
                            visit.append((discovery[el[0]],discovery[x],graphLabel[el[0]],w,graphLabel[x]))
                            stragglers.remove((el[0],x))
                    else: #backward edges
                        visit.append((discovery[el[0]],discovery[x],graphLabel[el[0]],el[1],graphLabel[x]))
                    DFS(undGraph,graph,graphLabel,el[0],visit,father,discovery,contenitor,stragglers)


                else:
                    if((x,el[0]) not in father and (el[0],x) not in father):
                        father[(x,el[0])]=1
                        father[(el[0],x)]=1
                        if(el in graph[x]): #forward
                            visit.append((discovery[x],discovery[el[0]],graphLabel[x],el[1],graphLabel[el[0]]))
                        else:               #backward
                            visit.append((discovery[el[0]],discovery[x],graphLabel[el[0]],el[1],graphLabel[x]))
                    elif((el[0],x) in stragglers):
                        w=0
                        for app in graph[el[0]]:
                            if(app[0]==x):
                                w=app[1]
                                break
                        visit.append((discovery[el[0]],discovery[x],graphLabel[el[0]],w,graphLabel[x]))
                        stragglers.remove((el[0],x))


            if(visit not in contenitor):
                contenitor.append(visit)
            #at the end of each possible visit there is the restore of what was present before a specific permutations
            discovery=copy.deepcopy(discoveryperm)
            father=copy.deepcopy(fatherperm)
            visit=copy.deepcopy(visitperm)
            stragglers=copy.deepcopy(stragglersperm)

    discovery[candidate]=0
    DFS(undGraph,graph,graphLabel,candidate,visit,father,discovery,contenitor,stragglers)
    lenmax=0
    ulteriorecont=[]
    for kelm in contenitor:
        lenmax=max(lenmax,len(kelm))
    for kelm in contenitor:
        if(len(kelm)==lenmax):
            if(kelm not in ulteriorecont):
                ulteriorecont.append(kelm)
    return ulteriorecont

#if are present two or more equal edges it returns all the sorted permutation, after using a merge sort on the adjency list
def sortADJ(adjList,graphLabel,graph,source):
    mergeSortADJ(adjList,0,len(adjList)-1,graphLabel,graph,source)
    adjRet=sortedPerm(0,adjList,graphLabel)
    return adjRet

def sortedPerm(index,adjList,graphLabel):
    if(index<len(adjList)):
        app=[adjList[index]]
        s=index
        ris=[]
        for k in range(index+1,len(adjList)):
            if(graphLabel[adjList[s][0]] == graphLabel[adjList[k][0]] and adjList[s][1] == adjList[k][1]):
                app.append(adjList[k])
            else:
                ris=sortedPerm(k,adjList,graphLabel)
                break
        perm=[list(z) for z in list(permutations(app))]
        ritorno=[]
        for primo in perm:
            appoggio=copy.deepcopy(primo)
            if(ris!=[]):
                for second in ris:
                    appoggio2=copy.deepcopy(second)
                    ritorno.append(appoggio+appoggio2)
            else:
                ritorno.append(appoggio)
        return ritorno

    else:
        return []

def mergeSortADJ(adjList,left,right,graphLabel,graph,source):
    if(left<right):
        center=int((left+right)/2)
        mergeSortADJ(adjList,left,center,graphLabel,graph,source)
        mergeSortADJ(adjList,center+1,right,graphLabel,graph,source)
        mergeADJ(adjList,left,center,right,graphLabel,graph,source)

def mergeADJ(adjList,left,center,right,graphLabel,graph,source):
    i=left
    j=center+1
    app=[]
    while(i<=center and j<=right):
        if((graphLabel[adjList[i][0]]<graphLabel[adjList[j][0]]) or (graphLabel[adjList[i][0]]==graphLabel[adjList[j][0]] and adjList[i][1]<=adjList[j][1])):
            app.append(adjList[i])
            i+=1
        else:
            app.append(adjList[j])
            j+=1
    while(i<=center):
        app.append(adjList[i])
        i+=1
    while(j<=right):
        app.append(adjList[j])
        j+=1
    k=left
    while(k<=right):
        adjList[k]=app[k-left]
        k+=1

def getKey(item):
    return item[2]
#function that is capable to transform a directed graph into an undirected one, saving at the same the 2 nodes loop edges
def makeItUndir(graph,graphLabel):
    undGraph={}
    couple=[]
    stragglers=[]
    graphLabelR={}
    for el in graphLabel:
        graphLabelR[graphLabel[el]]=el
    for sourceIn in sorted(graphLabelR):
        source=graphLabelR[sourceIn]
        listA=graph[graphLabelR[sourceIn]]
        listB=[]
        for ap in listA:
            listB.append((ap[0],ap[1],graphLabel[ap[0]]))
        listB=sorted(listB,key=getKey)
        listB=[(el[0],el[1]) for el in listB]
        for dest in listB:
            if((source,dest[0]) not in couple and (dest[0],source) not in couple):
                if(source not in undGraph):
                    undGraph[source]=[dest]
                else:
                    undGraph[source].append(dest)

                if(dest[0] not in undGraph):
                    undGraph[dest[0]]=[(source,dest[1])]
                else:
                    undGraph[dest[0]].append((source,dest[1]))
                couple.append((source,dest[0]))
            else:
                if((source,dest[0]) in couple):
                    stragglers.append((dest[0],source))
                else:
                    stragglers.append((source,dest[0]))
    for x in undGraph:
        undGraph[x]=sorted(undGraph[x])
    return undGraph,stragglers

#take the minimum of all DFScodes expolitng lexicoConfront
def minDFSVisit(sortedIn,lexicoConfront):
    mini=sortedIn[0]

    i=0
    for visit in sortedIn:
        i+=1
        if(lexicoConfront(visit,mini)):
            mini=visit

    return mini

#merge sort for the DFSCodes, input list of DFSCodes with compareFunction=confrontEdges
def sortDFSVisit(visit,compareFunction):
    mergeSortDFSVisit(visit,0,len(visit)-1,compareFunction)
    return visit


def mergeSortDFSVisit(visit,left,right,compareFunction):
    if (left<right):
        center=int((left+right)/2)
        mergeSortDFSVisit(visit,left,center,compareFunction)
        mergeSortDFSVisit(visit,center+1,right,compareFunction)
        merge(visit,left,center,right,compareFunction)

def merge(visit,left,center,right,compareFunction):
    i=left
    j=center+1
    app=[]
    while(i<=center and j<=right):
        if(compareFunction(visit[i],visit[j])):
            app.append(visit[i])
            i+=1
        else:
            app.append(visit[j])
            j+=1
    while(i<=center):
        app.append(visit[i])
        i+=1
    while(j<=right):
        app.append(visit[j])
        j+=1
    k=left
    while(k<=right):
        visit[k]=app[k-left]
        k+=1

#function that takes in input two edges and compute the comparison among them
def confrontEdges(a,b):
    if(a[0]<a[1] and b[0]<b[1] and a[1]<b[1]): #forwardedges
        #print a[0],a[1]," ## ",b[0],b[1],"TRUE"
        return True
    if(a[0]>a[1] and b[0]>b[1]): #backedges
        if(a[0]<b[0] or (a[0]==b[0] and a[1]<b[1])):
            #print a[0],a[1]," ## ",b[0],b[1],"TRUE"
            return True
    else:
        if(a[0]>a[1] and b[0]<b[1]): #A backedges and B forwardedges
            if(a[0]<b[1]):
                #print a[0],a[1]," ## ",b[0],b[1],"TRUE"
                return True
        else:
            if(a[0]<a[1] and b[0]>b[1]):#A forwardedges and B backedges
                if(a[1]<=b[0]):
                    #print a[0],a[1]," ## ",b[0],b[1],"TRUE"
                    return True
    #print a[0],a[1]," ## ",b[0],b[1],"FALSE"
    return False

def lexicoConfront(a,b): #where a and b result to be two lists of tuples to compare -> the result will return or True or False
    l=min(len(a),len(b)) #take the minimum length
    i=0
    while(i<l):#3 possible cases both forwardedges both backedges then, between one backedge and a forward one, the latter wins
        eA=a[i]
        eB=b[i]
        if(eA!=eB):
            if(eA[0]<eA[1] and eB[0]<eB[1] and eB[0]<eA[0]): #both forward edges
                return True
            else:
                if(eA[0]<eA[1] and eB[0]<eB[1] and eA[0]==eB[0]): #lexicgraphical confront among the label values
                    strA=str(eA[2])+str(eA[3])+str(eA[4])
                    strB=str(eB[2])+str(eB[3])+str(eB[4])
                    if(strA!=strB):
                        if(strA<strB):
                            return True
                        else:
                            return False

            if(eA[0]>eA[1] and eB[0]>eB[1] and eA[1]<eB[1]): #both backedges
                return True
            else:

                if(eA[0]>eA[1] and eB[0]>eB[1] and eA[1]==eB[1]):
                    strA=str(eA[2])+str(eA[3])+str(eA[4])
                    strB=str(eB[2])+str(eB[3])+str(eB[4])
                    if(strA!=strB):
                        if(strA<strB):
                            return True
                        else:
                            return False

            if(eA[0]<eA[1] and eB[0]>eB[1]): #confront between a forwardedge and a backedge
                return True
            else:
                return False
            return False

        i+=1
    if(len(a)==len(b)):
        return True
    else:
        if(len(a)==l):
            return True
        else:
            return False


#Jaro similarity between string
def jaroSimilarity(string1,string2):
    lenS = len(string1)
    lenT = len(string2)
    if lenS == 0 and lenT == 0:
        return 1
    match_distance = (max(lenS, lenT) // 2) - 1
    s_matches = [False] * lenS
    t_matches = [False] * lenT
    matches = 0
    transpositions = 0
    for i in range(lenS):
        start = max(0, i-match_distance)
        end = min(i+match_distance+1, lenT)
        for j in range(start, end):
            if t_matches[j]:
                continue
            if string1[i] != string2[j]:
                continue
            s_matches[i] = True
            t_matches[j] = True
            matches += 1
            break
    if matches == 0:
        return 0
    k = 0
    for i in range(lenS):
        if not s_matches[i]:
            continue
        while not t_matches[k]:
            k += 1
        if string1[i] != string2[k]:
            transpositions += 1
        k += 1
    return ((matches / lenS) + (matches / lenT) + ((matches - transpositions/2) / matches)) / 3
