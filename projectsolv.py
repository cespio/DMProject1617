#Possible solution for Data Mining Project
#Data structure
'''
graph -> dictionary key-value
key is the node id and the value is the list of its outgoing edges represented by the tuples (destination_id,edge_label)
id [(id_dest,label),(id_dest,lable)] one for each node

graphLabel -> hash that map to id to its node label
id => label

fEdges  key-value
key = (sorgent,destinazione,label arco)
value = numero di occorrenze
'''
import re
import copy
import numpy
from itertools import permutations
from itertools import chain
from random import uniform

#defintion of DFSvist for
#COLOR for backedge and forward edge? grey to black, grey to white
#dfscode visit(timeS,timeD,LabelS,LabelE,LabelD)
#adapt the dfs code to work only with LabelS
# work on the edgessss

#specific to 3 node 2 edges
#assumo connessi --> o quasi
def minDFS(graph,graphLabel):
    visits=allvisitDFS(graph,graphLabel)
    if(len(visits)>0 and (isinstance(visits[0],tuple))):
        visits=[visits]
    #int(visits)
    sortedIn=[]
    for x in visits:
        #print(x)
        if(not(isinstance(x,tuple))):
            r=sortDFSVisit(x,confrontEdges)
            #print(r)
            sortedIn.append(r)
    #meotodo per confrontare
    #print(sortedIn)
    #metodo per prendere il minimo
    if(len(sortedIn)>0):
        risf=sortDFSVisit(sortedIn,lexicoConfront)[0]
    elif(sortedIn!=[]):
        risf=sortedIn[0]
    if(sortedIn!=[]):
        result=risf
        #print(result)
        dfscode=""
        for k in result:
            for y in k:
                if(isinstance(y,int)):
                    dfscode=dfscode+str(y)
                else:
                    dfscode+=y
        return dfscode
    else:
        return None

def allvisitDFS(graph,graphLabel):
    noIn=startingNode(graph,graphLabel) #starting from node with 3 labels
    listAll=[]
    #print(noIn)
    if(len(noIn)>0):
        for x in noIn:
            R=DFS(graph,graphLabel,x)
            if(R not in listAll and len(R)>1):
                listAll.extend(R) #graph,graphLabel and starting node -> node with no input edge
    else:
        #piglio un nodo randominco
        ml=list(graphLabel.keys())
        #r=uniform(0,len(ml))
        for k in ml:
            if(len(graph[k])>0):
                R=DFS(graph,graphLabel,k)
                if(R not in listAll):
                    listAll.extend(R)

    if(listAll!=[] and isinstance(listAll[0],tuple)):
        listAll=list(set(listAll))
    return listAll


def startingNode(graph,graphLabel):
    noIn=list(graphLabel.keys())
    #print(noIn)
    for x in graph:
        for y in graph[x]:
            if(y[0] in noIn):
                noIn.remove(y[0])
        if(len(graph[x])==0 and x in noIn):
                noIn.remove(x)
    return noIn

def DFS(graph,graphLabel,starting):
    discovery={}
    discoveryTot={}
    couple={}
    father={}
    time=0
    visit=[]
    visitM=[]
    def DFS_Visit(graph,graphLabel,x,discovery,couple,visit,time): #extend
        #print("Sono in x: ",x)
        print(graph)
        if(len(graph[x])>0):
            discovery[x]=time
        l=[list(z) for z in list(permutations(graph[x]))]
        y=0
        visit1=[]
        newtime=time
        while (y<len(l)):
            del visit1[:]
            discovery_temp=copy.deepcopy(discovery)
            time=newtime
            #print("Y: ",y," discovery ",discovery_temp," time_temp ",time)
            for u in l[y]: #for each element of the adjecy list
                if(not(u[0] in discovery_temp)):
                    #print("Sono nodo ",x, "Vado in ",u[0])
                    visit1.append((discovery_temp[x],time+1,graphLabel[x],u[1],graphLabel[u[0]]))
                    discovery_temp[u[0]]=time+1
                    returnD=DFS_Visit(graph,graphLabel,u[0],discovery_temp,couple,[],time+1)
                    #print("returnone ",returnD)

                    if(len(returnD[0])>1 and isinstance(returnD[0], list)):
                        #print("VBBBBB")
                        for k in returnD[0]:
                            if(len(k)>0):
                                visit1.append(k)
                    else:
                        visit1.append(returnD[0])
                    time=returnD[1]
                    #print("VISITONE",visit1)

                else:
                    #if same number non aggiungo (i,j) -> i==j
                    if(discovery_temp[x]!=discovery_temp[u[0]]):
                        visit1.append((discovery_temp[x],discovery_temp[u[0]],graphLabel[x],u[1],graphLabel[u[0]]))


            y=y+1
            #print("Visitone ",visit1)
            visit1 = [x for x in visit1 if x != []]
            #print("Visitone dopo pulizia ",visit1)
            if(len(visit1)==1):
                visit.extend(copy.deepcopy(visit1))
                #print("Visit here : ",visit)
                #visit=list(chain.from_iterable(visit))
            if(len(visit1)>1): #da specificare un po meglio
                visit.append(copy.deepcopy(visit1))
                if(not(len(visit1)==2)):
                    visit=list(chain.from_iterable(visit))
            #print("Printone di visit ",visit)
        if(len(visit)==1 and not(isinstance(visit[0],list))):
            visit=tuple(chain.from_iterable(visit))
        return [visit,time]

    #discovery[starting]=0
    #visitM.append(DFS_Visit(graph,graphLabel,starting,discovery,couple,visit,time)[0])
    keysgraph=list(graph.keys())
    #print("PRINTONE DI KEYGRAPH : ",keysgraph)
    keysgraph.remove(starting)
    keysgraph=[starting]+keysgraph
    flag=0
    for x in keysgraph:
        if(not(x in discovery)):
            if(len(graph[x])>0):
                del visit[:]
                R=DFS_Visit(graph,graphLabel,x,discovery,couple,visit,time)[0]
                if(len(R)==2):
                    for k in R:
                            visitM.append(k)
                    break
                #print("Rrrrrr ",R)
                if(isinstance(R,tuple)):
                    visitM.append(R)
                else:
                    visitM.extend(R)
                #print("printone di visitM: ",visitM)
    return visitM

#l'obbiettivo sono gli edge
#quindi lista di adicenza vuota significa che è un nodo pozzo, ci devo essere arrivato altrimenti l'arco non è valido
#rules of ordering
'''
e1=(i1,j1)
e2=(i2,j2)
e1<e2
ord rules:
if i1 = i2 and j1<j2 -> e1<e2
if i1 < j1 and j1=i2 -> e1<e2
ordering is transitive
'''

def sortDFSVisit(visit,compareFunction):
    #print("Visit prima ", visit)
    mergeSortDFSVisit(visit,0,len(visit)-1,compareFunction)
    #print("Visit dopo ", visit)
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



#function to confront the edges for DFScode
#a=b --> (t1,t2,Ls,le,Ld)
#forward edges
'''
e1<e2
if j1<j2
'''
#backward edges
'''
e1<e2
if i1<i2
or i1=i2 and j1<j2
'''

def confrontEdges(a,b):
    if(a[0]<a[1] and b[0]<b[1] and a[1]<b[1]): #forwardedges+
        return True
    if(a[0]>a[1] and b[0]>b[1]): #backedges
        if(a[0]<b[0] or (a[0]==b[0] and a[1]<b[1])):
            return True
    else:
        if(a[0]>a[1] and b[0]<b[1]):
            if(a[0]<b[1]):
                return True
        else:
            if(a[0]<a[1] and b[0]>b[1]):
                if(a[1]<=b[0]):
                    return True
    return False


#mancano da verifcare i casi false
def lexicoConfront(a,b): #where a and b result to be two list of tuples to compare -> the result will return or 0 or 1
    #take the minimum length
    l=min(len(a),len(b))
    i=0
    while(i<l):
        #3 casi da analizzare both forward edges both backedges then between one forward and one backedges win the forward
        eA=a[i]
        eB=b[i]
        if(eA[0]<eA[1] and eB[0]<eB[1] and eA[0]<eB[0]): #nel caso in cui siano entrambi forward edges
            return True
        elif(eA[0]<eA[1] and eB[0]<eB[1] and eA[0]==eB[0]): #in caso confronto le labels
            strA=str(eA[2])+str(eA[3])+str(eA[4])
            strB=str(eB[2])+str(eB[3])+str(eB[4])
            if(strA!=strB):
                if(strA<strB):
                    return True
                else:
                    return False

        if(eA[0]>eA[1] and eB[0]>eB[1] and eA[1]<eB[1]): #nel caso in cui siano entrambi backedges
            return True
        elif(eA[0]>eA[1] and eB[0]>eB[1] and eA[1]==eB[1]):
            strA=str(eA[2])+str(eA[3])+str(eA[4])
            strB=str(eB[2])+str(eB[3])+str(eB[4])
            if(strA!=strB):
                if(strA<strB):
                    return True
                else:
                    return False
        if(eA[0]<eA[1] and eB[0]>eB[1]):
            return True
        i+=1
    return False


def myConfront(a,b):
    if(a[0]<b[0]):
        return True
    else:
        if(a[0]==b[0] and a[1]<b[1]):
            return True
        else:
            if(a[0]==b[0] and a[1]==b[1] and a[2]<b[2]):
                return True
    return False

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
            labelEdge_t=label_ed.findall(line_split[4]) #position of the label after the parsing
            if(line_split[0] in graph): #si potrebbe sintetizzare con un append
                temp=graph[line_split[0]]
                graph[line_split[0]]=temp+[(line_split[2],labelEdge_t[0])]
            else:
                graph[line_split[0]]=[(line_split[2],labelEdge_t[0])]
        if(label.match(str(line))):
            line_split1=line.rstrip("\n").split(" ")
            graphLabel[line_split1[0]]=line_split1[5]
    return graph,graphLabel

def printResult(graph):
    file_out=open("risGrahp.dot","w")
    file_out.write("digraph Ris{\n")
    for x in graph:
        t_l=graph[x]
        for y in t_l:
            file_out.write(str(x) + " -> " + str(y[0]) + "  [label=\"" + str(y[1]) + "\"];\n")
    file_out.write("}")
    file_out.close()



#GraMi implementations#
#-- Main function --#
def frequentSubG(graph,graphLabel,thr):  #graph=input graph thr=threshold
    fEdges=countFrequentEdges(graph,graphLabel,thr)
    candidateSet=subGraphExtension(list(fEdges.keys()))
    #foreach element implement the CSP and calculate its frequent -> if it is noto
    candidateSetApp=copy.shallowcopy(candidateSet)
    for el in candidateSetApp:
        if(isFrequent(el)<thr):
            del candidateSet



#frequentEdges between label --> we are working with directed graph so the order matter
def countFrequentEdges(graph,graphLabel,thr):
    #bruteforcemode passo tutta la strutture
    fEdges={}
    for x in graph:
        adjList=graph[x]
        for y in adjList:
            k=(graphLabel[x],graphLabel[y[0]],y[1])
            if(k in fEdges):
                t=fEdges[k]
                fEdges[k]=t+1
            else:
                fEdges[k]=1
    tempToDel=[k for k in fEdges if fEdges[k]<thr] #temptodel contiene tutti gli archi che non superano la threshold e che poi sono eliminati da fEdges
    for k in tempToDel: del fEdges[k]
    #return fEdgesvisitM.append(DFS_Visit(graph,graphLabel,x,discovery,couple,visit,time)[0])
    return fEdges



def subGraphExtension(fEdges):
    #print(fEdges)
    candidateSet=subExtSimple(fEdges)
    return candidateSet

def subExtSimple(fEdgesSet):
    result = []
    dfscode=set()
    m=0
    for i in range(len(fEdgesSet)):
        j=i+1
        while(j<len(fEdgesSet)):
            print("Fine ciclone")
            print("Confonto tra ",fEdgesSet[i],fEdgesSet[j])
            #print (i)
            #print (j)

            temp1 = {}
            temp2 = {}
            temp3 = {}
            temp4 = {}

            if (fEdgesSet[i][0] == fEdgesSet[i][1] == fEdgesSet[j][0]== fEdgesSet[j][1]):
                 m+=1
                 graphLabel1={'v0':str(fEdgesSet[i][0]),'v1':str(fEdgesSet[i][1]),'v2':str(fEdgesSet[i][1])}
                 graph1={'v0':[('v1',str(fEdgesSet[i][2]),('v2',str(fEdgesSet[j][2])))], 'v1':[], 'v2':[]}
                 R=minDFS(graph1,graphLabel1)
                 if(R not in dfscode):
                     result.append((graph1,graphLabel1))
                     dfscode.add(R)
                 graphLabel2={'v0':str(fEdgesSet[i][0]),'v1':str(fEdgesSet[i][1])}
                 graph2={'v0':[('v1',str(fEdgesSet[i][2]))], 'v1':[('v0',str(fEdgesSet[j][2]))]}
                 R=minDFS(graph2,graphLabel2)
                 if(R not in dfscode):
                     result.append((graph2,graphLabel2))
                     dfscode.add(R)
                 graphLabel3={'v0':str(fEdgesSet[i][0]),'v1':str(fEdgesSet[i][1]),'v2':str(fEdgesSet[j][1])}
                 graph3={'v0':[('v1',str(fEdgesSet[i][2]))],'v1':[('v2',str(fEdgesSet[j][2]))],'v2':[]}
                 R=minDFS(graph3,graphLabel3)
                 if(R not in dfscode):
                     result.append((graph3,graphLabel3))
                     dfscode.add(R)
                 graphLabel4={'v0':str(fEdgesSet[i][0]),'v1':str(fEdgesSet[j][0]),'v2':str(fEdgesSet[i][1])}
                 graph4={'v0':[],'v1':[('v0',str(fEdgesSet[i][2]))],'v2':[('v0',str(fEdgesSet[j][2]))]}
                 R=minDFS(graph4,graphLabel4)
                 if(R not in dfscode):
                     result.append((graph4,graphLabel4))
                     dfscode.add(R)

            if ((fEdgesSet[i][0] == fEdgesSet[j][0]) and (fEdgesSet[i][1] != fEdgesSet[j][1])):
                 m+=1
                 graphLabel1={'v0':str(fEdgesSet[i][0]),'v1':str(fEdgesSet[i][1]), 'v2':str(fEdgesSet[j][1])}
                 graph1={'v0':[('v1',str(fEdgesSet[i][2])),('v2',str(fEdgesSet[j][2]))], 'v1':[], 'v2':[]}
                 R=minDFS(graph1,graphLabel1)
                 if(R not in dfscode):
                     result.append((graph1,graphLabel1))
                     dfscode.add(R)

            if ((fEdgesSet[i][0] == fEdgesSet[j][0]) and (fEdgesSet[i][1] == fEdgesSet[j][1])):
                 m+=1
                 graphLabel1={'v0':str(fEdgesSet[i][0]),'v1':str(fEdgesSet[i][1]),'v2':str(fEdgesSet[j][1])}
                 graph1={'v0':[('v1',str(fEdgesSet[i][2])), ('v2',str(fEdgesSet[j][2]))], 'v1':[] , 'v2':[]}
                 print(graph1,graphLabel1)
                 R=minDFS(graph1,graphLabel1)
                 if(R not in dfscode):
                     result.append((graph1,graphLabel1))
                     dfscode.add(R)
                 graphLabel2={'v0':str(fEdgesSet[i][1]),'v1':str(fEdgesSet[i][0]),'v2':str(fEdgesSet[j][0])}
                 graph2={'v1':[('v0',str(fEdgesSet[i][2]))],'v2':[('v0',str(fEdgesSet[i][2]))], 'v0':[]}
                 R=minDFS(graph2,graphLabel2)
                 if(R not in dfscode):
                     result.append((graph2,graphLabel2))
                     dfscode.add(R)

            if ( (fEdgesSet[i][0] == fEdgesSet[j][0]) and (fEdgesSet[i][0] == fEdgesSet[j][1]) ):
                 m+=1
                 graphLabel1={'v0':str(fEdgesSet[i][0]),'v1':str(fEdgesSet[i][1]),'v2':str(fEdgesSet[j][1])}
                 graph1={'v0':[('v1',str(fEdgesSet[i][2])),('v2',str(fEdgesSet[j][2]))], 'v1':[], 'v2':[] }
                 R=minDFS(graph1,graphLabel1)
                 if(R not in dfscode):
                     result.append((graph1,graphLabel1))
                     dfscode.add(R)
                 graphLabel2={'v0':str(fEdgesSet[j][0]),'v1':str(fEdgesSet[j][1]),'v2':str(fEdgesSet[i][1])}
                 graph2={'v0':[('v1',str(fEdgesSet[j][2]))],'v1':[('v2',str(fEdgesSet[i][2]))],'v2':[]}
                 R=minDFS(graph2,graphLabel2)
                 if(R not in dfscode):
                     result.append((graph2,graphLabel2))
                     dfscode.add(R)

            if ( (fEdgesSet[i][0] == fEdgesSet[j][0]) and (fEdgesSet[i][1] == fEdgesSet[j][0])):
                 m+=1
                 graphLabel1={'v0':str(fEdgesSet[i][0]),'v1':str(fEdgesSet[i][1]),'v2':str(fEdgesSet[j][1])}
                 graph1={'v0':[('v1',str(fEdgesSet[i][2])),('v2',str(fEdgesSet[j][2]))], 'v1':[], 'v2':[] }
                 R=minDFS(graph1,graphLabel1)
                 if(R not in dfscode):
                     result.append((graph1,graphLabel1))
                     dfscode.add(R)
                 graphLabel2={'v0':str(fEdgesSet[i][0]),'v1':str(fEdgesSet[i][1]),'v2':str(fEdgesSet[j][1])}
                 graph2={'v0':[('v1',str(fEdgesSet[i][2]))],'v1':[('v2',str(fEdgesSet[j][2]))],'v2':[]}
                 R=minDFS(graph2,graphLabel2)
                 if(R not in dfscode):
                     result.append((graph2,graphLabel2))
                     dfscode.add(R)

            if ( (fEdgesSet[i][0] == fEdgesSet[j][1]) and (fEdgesSet[i][1] != fEdgesSet[j][0]) ):
                 m+=1
                 graphLabel1={'v0':str(fEdgesSet[j][0]),'v1':str(fEdgesSet[i][0]),'v2':str(fEdgesSet[i][1])}
                 graph1={'v0':[('v1',str(fEdgesSet[j][2]))], 'v1':[('v2',str(fEdgesSet[i][2]))], 'v2':[] }
                 R=minDFS(graph1,graphLabel1)
                 if(R not in dfscode):
                     result.append((graph1,graphLabel1))
                     dfscode.add(R)
            '''
            Caso aggiunto da me
            '''
            if((fEdgesSet[i][0]==fEdgesSet[i][1]) and (fEdgesSet[j][0]!=fEdgesSet[i][0]) and (fEdgesSet[j][1]==fEdgesSet[i][0])):
                graphLabel1={'v0':str(fEdgesSet[i][0]), 'v1':str(fEdgesSet[i][1]), 'v2':str(fEdgesSet[j][1])}
                graph1={'v0': [('v1',str(fEdgesSet[i][2]))], 'v2':[('v1',str(fEdgesSet[j][2]))], 'v1':[]}
                R=minDFS(graph1,graphLabel1)
                if(R not in dfscode):
                    result.append((graph1,graphLabel1))
                    dfscode.add(R)

            if ( (fEdgesSet[i][0] == fEdgesSet[j][1]) and (fEdgesSet[i][1] == fEdgesSet[j][0]) ):
                 m+=1
                 graphLabel1={'v0':str(fEdgesSet[i][0]),'v1':str(fEdgesSet[i][1]),'v2':str(fEdgesSet[j][1])}
                 graph1={'v0':[('v1',str(fEdgesSet[i][2]))], 'v1':[('v2', str(fEdgesSet[j][2]))], 'v2':[] }
                 R=minDFS(graph1,graphLabel1)
                 if(R not in dfscode):
                     result.append((graph1,graphLabel1))
                     dfscode.add(R)
                 graphLabel2={'v0':str(fEdgesSet[j][0]),'v1':str(fEdgesSet[j][1]),'v2':str(fEdgesSet[i][0])}
                 graph2={'v0':[('v1',str(fEdgesSet[j][2]))], 'v1':[('v2', str(fEdgesSet[i][2]))], 'v2':[] }
                 R=minDFS(graph2,graphLabel2)
                 if(R not in dfscode):
                     result.append((graph2,graphLabel2))
                     dfscode.add(R)
                 graphLabel3={'v0':str(fEdgesSet[i][0]),'v1':str(fEdgesSet[i][1])}
                 graph3={'v0':[('v1',str(fEdgesSet[i][2]))], 'v1':[('v0',str(fEdgesSet[j][2]))]}
                 print(graph3,graphLabel3)
                 R=minDFS(graph3,graphLabel3)
                 if(R not in dfscode):
                     result.append((graph3,graphLabel3))
                     dfscode.add(R)
            if ( (fEdgesSet[i][1] == fEdgesSet[j][1]) and (fEdgesSet[i][0] != fEdgesSet[j][1]) ):
                 m+=1
                 graphLabel1={'v0':str(fEdgesSet[i][0]),'v1':str(fEdgesSet[i][1]),'v2':str(fEdgesSet[j][1])}
                 graph1={'v0':[('v1',str(fEdgesSet[i][2]))], 'v2':[('v1', str(fEdgesSet[j][2]))], 'v1':[] }
                 R=minDFS(graph1,graphLabel1)
                 if(R not in dfscode):
                     result.append((graph1,graphLabel1))
                     dfscode.add(R)
            if ( (fEdgesSet[i][1] == fEdgesSet[j][0]) and (fEdgesSet[i][1] != fEdgesSet[j][1]) ):
                 m+=1
                 l1={'v0':str(fEdgesSet[i][0]),'v1':str(fEdgesSet[i][1]),'v2':str(fEdgesSet[j][1])}
                 graph1={'v0':[('v1',str(fEdgesSet[i][2]))], 'v1':[('v2', str(fEdgesSet[j][2]))], 'v2':[] }
                 R=minDFS(graph1,graphLabel1)
                 if(R not in dfscode):
                     result.append((graph1,graphLabel1))
                     dfscode.add(R)
            j+=1

    print("numerone di match ",m)
    print("Printo dfscode ",dfscode)
    print(len(dfscode))
    print("Printo i risultati ", result)
    print("Lunghezza result ", len(result))
    return result









def main():
    thr=int(input("Give me your threshold:"))
    graph,graphLabel=readGraph("../graphGenOut.dot") #read the file and built the graph || dictionari key(id):[(ids,edLabel),(ids,edLabe),(ids,edLabe)]
    #caso grafi not oriented
    #gl1={'1': 'A','2':'B','3':'C','4':'D','5':'E'}
    #g1={'1': [('2','a')], '2':[('3','b'),('2','c')],'3':[('5','c'),('1','a')] , '4' :[],'5':[('2','b')]}
    #gl1={'1': 'A','2':'B', '3':'C'}
    #g1={'1': [('2','a'),('3','b')], '2':[], '3':[]}
    #g1={'1': [('2','v')], '2':[('1','b')], '3':[]}
    frequentSubG(graph,graphLabel,thr)
    '''
    result=minDFS(g1,gl1)
    print("The minimum DFS code isssssss: ",result)
    result=list(chain.from_iterable(result))
    dfscode=""
    for k in result:
        if(isinstance(k,int)):
            dfscode=dfscode+str(k)
        else:
            dfscode+=k
    print(dfscode)
    #frequentSubG(graph,graphLabel,thr)
    '''

'''
a->b
|
v    OK ma lista di lista
c

a->b->c   1 solo elemento in più

a->c
   ^
   | Ok
   b

a->b
b->a ok
'''

if __name__ == "__main__":
    main()
