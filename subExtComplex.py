import re
import copy
import numpy
import itertools
from itertools import permutations
from itertools import chain
from random import uniform


def frequentSubG(graph,graphLabel,thr):  #graph=input graph thr=threshold
    fEdges=countFrequentEdges(graph,graphLabel,thr)
    print(fEdges)
    print(len(fEdges))
    candidateSet=subExtSimple(list(fEdges.keys()))
    print (candidateSet)
    print("Lunghezza prima di CSP",len(candidateSet))
    candidateSetApp=copy.deepcopy(candidateSet)
    #sarebbe da implementare strutture condivise per i domini
    #oppure calcolarli una volta sola prima
    #domini struttura come 'label':set di nodi
    tolti=0
    domains=getDomains(graphLabel)
    for el in candidateSetApp:
        if(isFrequent(el,graph,domains)<thr):
            tolti+=1
            candidateSet.remove(el)
    print("Lunghezza dopo CSP",len(candidateSet),"tolti ",tolti)
    i=0
    candidatesBig = subExtComplex(candidateSet, list(fEdges.keys()))
    '''
    for z in candidateSet:
        printResult(z[0],z[1],str(i))
        i+=1
    '''

def subExtComplex(candidateSet, fEdges):
    print("\nsubExtComplex ha questo candidate set: \n")
    print (candidateSet)

    print("\nsubExtComplex ha questi fEdges: \n")
    print(fEdges)

    newSubGraphs1 = []
    newSubGraphs2 = []
    newSubGraphs3 = []
    candidateSetClean = {}
    subDomains = {}
    for k in candidateSet:
        candidateSetClean = k[0]
    for j in candidateSet:
        subDomains = j[1]

    print (candidateSetClean)
    print (subDomains)
    #vertIndex = (len(subDomains) - 1)
    #vertex = "v" + str(vertIndex)
    #supportDomain = {}
    #resultSuppDomains = {}

    for i in fEdges:
        for t in subDomains:
            if ((i[0] == subDomains[t]) and (i[1] != subDomains[t])):
                 vertIndex = (len(subDomains) - 1) + 1
                 #vertex = "v" + str(vertIndex)
                 #vertIndex += 1
                 vertex = "v" + str(vertIndex)
                 supportDomain = {}
                 resultSuppDomains = {}
                 candidateSetSupp = {}
                 candidateSetSupp = copy.deepcopy(candidateSetClean)
                 #print ("Candidate set di supporto prima: ", candidateSetSupp)
                 #print ("Elemento t", candidateSetSupp[t])

                 candidateSetSupp[t].append((vertex, i[2]))
                 candidateSetSupp[vertex] = []
                 #print("Candidato t", candidateSetSupp[t])
                 #print("Set totale di supporto", candidateSetSupp)
                 #print("Candidati puliti", candidateSetClean)
                 if (vertex not in supportDomain):
                      supportDomain[vertex] = i[1]
                 resultSuppDomains = copy.deepcopy(subDomains)
                 for k in supportDomain:
                      if (k not in resultSuppDomains):
                           resultSuppDomains[k] = supportDomain[k]
                 candidateSet = []

                 candidateSet.append(candidateSetSupp)
                 candidateSet.append(resultSuppDomains)
                 newSubGraphs1.append(candidateSet)

                 print("I miei nuovi domini: ", resultSuppDomains)
                 print("Il mio nuovo sottografo e': ", candidateSet)
    print("Risultati per il primo caso", newSubGraphs1)

    for i in fEdges:
        for t in subDomains:
            if ((i[1] == subDomains[t]) and (i[0] != subDomains[t])):
                 vertIndex = (len(subDomains) - 1) + 1
                 #vertex = "v" + str(vertIndex)
                 #vertIndex += 1
                 vertex = "v" + str(vertIndex)
                 supportDomain = {}
                 resultSuppDomains = {}
                 candidateSetSupp = {}
                 candidateSetSupp = copy.deepcopy(candidateSetClean)
                 #print ("Candidate set di supporto prima: ", candidateSetSupp)
                 #print ("Elemento t", candidateSetSupp[t])

                 #candidateSetSupp[t].append((vertex, i[2]))
                 candidateSetSupp[vertex] = [(t, i[2])]
                 #print("Candidato t", candidateSetSupp[t])
                 #print("Set totale di supporto", candidateSetSupp)
                 #print("Candidati puliti", candidateSetClean)
                 if (vertex not in supportDomain):
                      supportDomain[vertex] = i[0]
                 resultSuppDomains = copy.deepcopy(subDomains)
                 for k in supportDomain:
                      if (k not in resultSuppDomains):
                           resultSuppDomains[k] = supportDomain[k]
                 candidateSet = []

                 candidateSet.append(candidateSetSupp)
                 candidateSet.append(resultSuppDomains)
                 newSubGraphs2.append(candidateSet)

                 print("I miei nuovi domini: ", resultSuppDomains)
                 print("Il mio nuovo sottografo e': ", candidateSet)

    print("Le soluzioni per il secondo caso", newSubGraphs2)

    for i in fEdges:
        for t in subDomains:
            if ((i[0] == subDomains[t])):
                for k in subDomains:
                    if (i[1] == subDomains[k]):
                        couple = (k, i[2])
                        print("Couple di 0: ", couple[0])
                        flag = 0
                        for x in candidateSetClean[t]:
                            print("x di 0: ", x[0])
                            if (couple[0] == x[0]):
                                flag = 1
                                break

                        if (flag == 0):
                            vertIndex = (len(subDomains) - 1) + 1
                            vertex = "v" + str(vertIndex)
                            candidateSetSupp = {}
                            candidateSetSupp = copy.deepcopy(candidateSetClean)
                            candidateSetSupp[t].append(couple)

                            candidateSet = []
                            candidateSet.append(candidateSetSupp)
                            candidateSet.append(subDomains)
                            newSubGraphs3.append(candidateSet)
    print("Soluzioni per il terzo caso", newSubGraphs3)

    result = []
    result.extend(newSubGraphs1)
    result.extend(newSubGraphs2)
    result.extend(newSubGraphs3)
    print("Lunghezza soluzione 1 :", len(newSubGraphs1))
    print("Lunghezza soluzione 2 :", len(newSubGraphs2))
    print("Lunghezza soluzione 3 :", len(newSubGraphs3))
    print("RISULTATO GLOBALE: ", result)
    print("LUNGHEZZA GLOBALE: ", len(result))
    return result



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

def subGraphExtensionFirst(fEdges):
    #print(fEdges)
    candidateSet=subExtSimple(fEdges)
    return candidateSet

def getDomains(graphLabel):  #mi ricavo i domini
    domains={}
    for x in graphLabel:
        la=graphLabel[x]
        if(la not in domains):
            domains[la]=[x]
        else:
            domains[la].append(x)
    #print(domains)
    return domains

def isFrequent(el,graph,domains): #funzione fondamentale che permete di calcolare le occorrenze nel grafo, l'elemeno el (grafo+label)
    subG=el[0]
    subGLabel=el[1] #-> graph di label
    #node consistency verificata col dominio
    #arc  consistency da verificare
    count=[]
    if(len(subGLabel)!=2):#specifico per i cicli
        #print("adesso contiamo per ",subG,subGLabel)
        listT=[]
        dictAss={}
        for k in subGLabel:
            dictAss[k]=set()
        for x in sorted(subG):
            print("Uso nodo ",x, "Con label ",subGLabel[x])
            if(len(subG[x])!=0):
                if(len(dictAss[x])==0):
                    print("Yes")
                    la=domains[subGLabel[x]]
                else:
                    print("No")
                    la=dictAss[x]
            else:
                la=[]
            #print("La sua la e' ",la)
            for y in sorted(subG[x]):
                if(len(dictAss[x])!=0):
                    la=dictAss[x]
                print("Da ",x, " andiamo verso ",y," con label ",subGLabel[y[0]])
                if(len(dictAss[y[0]])==0):
                    #print("Yes")
                    lb=domains[subGLabel[y[0]]]
                else:
                    #print("No")
                    lb=dictAss[y[0]]#
                #temp=list(zip(la,lb))
                temp=list(itertools.product(la,lb))
                #print("Temp ",temp)
                temp1=[]
                for z in temp:
                    if(z[0]!=z[1]):
                        temp1.append([z[0],z[1],y[1]])
                #print("Temp1 ",temp1)
                checkEdges(temp1,dictAss,graph,x,y[0])
                print("DICTASS   ",dictAss)
        CF=countFinal(dictAss,subG,subGLabel,graph)
        print("CFFF ",CF)

        return CF
    '''
        nodes=[]
        print(subG)
        print(subGLabel)
        for x in sorted(subGLabel):
            Lab1=subGLabel[x]
            print (x)
            N2=subG[x][0]
            print (N2)
            break
        print (N2 in subG.keys())
        Lab2=subGLabel[N2]
        print ("Ciao!")
        W1=subG[x][0][1]
        W2=subG[N2][0][1]
        count.append(countCicleIntheGraph(Lab1,Lab2,W1,W2,graph,domains))
        print("Forza Inter")
        #count.append(countCicleIntheGraph(subGLabel[source],subGLabel[dest[0]],dest[1],graph,domains))
    '''

def countFinal(dictAss,subG,subGLabel,graph):
    count=[]
    print(subG)
    print(subGLabel)
    print(dictAss)
    for a in sorted(subG):
        for b in sorted(subG[a]):
            temp=0
            la=dictAss[a]
            lb=dictAss[b[0]]
            mix=list(itertools.product(la,lb))
            for elm in mix:
                if(elm[0]!=elm[1]):
                    if((elm[1],b[1]) in graph[elm[0]]):
                        temp+=1
            count.append(temp)
    return max(count)


def checkEdges(listEdges,dictAss,graph,x,y):
    matchX=[]
    matchY=[]
    for elm in sorted(listEdges):
        tempListA=graph[elm[0]]
        #print("UAGLION tempListA ",tempListA)
        print("controllo ",elm)
        if((elm[1],elm[2]) in tempListA): #cosi' perdo riferimento al peso
            flag=1
            print("c'e'")
            dictAss[x].add(elm[0])
            dictAss[y].add(elm[1])
            matchX.append(elm[0])
            matchY.append(elm[1])
    universeMatchX=[k[0] for k in listEdges]
    universeMatchY=[k[1] for k in listEdges]
    noMatchX=list(set(universeMatchX)-set(matchX))
    noMatchY=list(set(universeMatchY)-set(matchY))
    #("NoMATCHHHHHElm ",noMatch," con x ",x)
    #print("Dopo checkEdges ",dictAss)
    for p in noMatchX:
        if(p in dictAss[x]):
            dictAss[x].remove(p)
    for p in noMatchY:
        if(p in dictAss[y]):
            dictAss[y].remove(p)

def countCicleIntheGraph(Lab1,Lab2,W1,W2,graph,domains): #pere la struttura dei grafi
    la=domains[Lab1]
    lb=domains[Lab2]
    #W1 -> la1 to l2
    #w2 -> la2 to la1
    count=0
    for x in la:
        adj=graph[x]
        for y in adj:
            if(y[0] in lb and y[1]==W1 and ((x,W2) in graph[y[0]])):
                count+=1
                break
    return count

def subExtSimple(fEdgesSet):
     result = []
     #candidateSet = {}
     #k1 = fEdgesSet.keys()
     #k2 = k1
     #while

     for i in range(len(fEdgesSet)):
         j=i+1
         while(j<len(fEdgesSet)):
            #print("Fine ciclone")
            m=0
            print("Confonto tra ",fEdgesSet[i],fEdgesSet[j])
            #print (i)
            #print (j)

            graphLabel1 = {}
            graph1 = {}
            graphLabel2 = {}
            graph2 = {}
            graphLabel3 = {}
            graph3 =  {}
            graphLabel4 = {}
            graph4 = {}

            if (fEdgesSet[i][0] == fEdgesSet[i][1] == fEdgesSet[j][0]== fEdgesSet[j][1]):
                m+=1
                graphLabel1={'v0':str(fEdgesSet[i][0]),'v1':str(fEdgesSet[i][1]),'v2':str(fEdgesSet[i][1])}
                graph1={'v0':[('v1',str(fEdgesSet[i][2])),('v2',str(fEdgesSet[j][2]))], 'v1':[], 'v2':[]}
                result.append((graph1, graphLabel1))

                graphLabel2={'v0':str(fEdgesSet[i][0]),'v1':str(fEdgesSet[i][1])}
                graph2={'v0':[('v1',str(fEdgesSet[i][2]))], 'v1':[('v0',str(fEdgesSet[j][2]))]}
                result.append((graph2, graphLabel2))

                graphLabel3={'v0':str(fEdgesSet[i][0]),'v1':str(fEdgesSet[i][1]),'v2':str(fEdgesSet[j][1])}
                graph3={'v0':[('v1',str(fEdgesSet[i][2]))],'v1':[('v2',str(fEdgesSet[j][2]))],'v2':[]}
                result.append((graph3, graphLabel3))

                graphLabel4={'v0':str(fEdgesSet[i][0]),'v1':str(fEdgesSet[j][0]),'v2':str(fEdgesSet[i][1])}
                graph4={'v0':[],'v1':[('v0',str(fEdgesSet[i][2]))],'v2':[('v0',str(fEdgesSet[j][2]))]}
                result.append((graph4, graphLabel4))

            if ((fEdgesSet[i][0] != fEdgesSet[i][1]) and (fEdgesSet[i][1] == fEdgesSet [j][0]) and (fEdgesSet[j][0] == fEdgesSet[j][1]) ):
                 graphLabel1={'v0':str(fEdgesSet[i][0]),'v1':str(fEdgesSet[i][1]),'v2':str(fEdgesSet[j][1])}
                 graph1={'v0':[('v1',str(fEdgesSet[i][2]) )], 'v1':[ ('v2', str(fEdgesSet[j][2]))], 'v2':[]}
                 result.append((graph1, graphLabel1))

                 graphLabel2={'v0':str(fEdgesSet[j][1]),'v1':str(fEdgesSet[i][0]),'v2':str(fEdgesSet[j][0])}
                 graph2={'v0':[], 'v1':[('v0',str(fEdgesSet[i][2]))], 'v2':[('v0', str(fEdgesSet[j][2]))]}
                 result.append((graph2, graphLabel2))

            if ((fEdgesSet[i][0] != fEdgesSet[i][1]) and (fEdgesSet[i][0] == fEdgesSet [j][0]) and (fEdgesSet[j][0] == fEdgesSet[j][1]) ):
                 graphLabel1={'v0':str(fEdgesSet[j][0]),'v1':str(fEdgesSet[i][1]),'v2':str(fEdgesSet[j][1])}
                 graph1={'v0':[('v1',str(fEdgesSet[i][2])), ('v2', str(fEdgesSet[j][2])) ], 'v1':[], 'v2':[]}
                 result.append((graph1, graphLabel1))

                 graphLabel2={'v0':str(fEdgesSet[j][0]),'v1':str(fEdgesSet[j][1]),'v2':str(fEdgesSet[i][1])}
                 graph2={'v0':[('v1',str(fEdgesSet[j][2]))], 'v1':[('v2',str(fEdgesSet[i][2]))], 'v2':[]}
                 result.append((graph2, graphLabel2))

            if ( (fEdgesSet[i][0] == fEdgesSet[i][1]) and (fEdgesSet[i][1] == fEdgesSet [j][1]) and (fEdgesSet[j][0] != fEdgesSet[j][1]) ):
                 graphLabel1={'v0':str(fEdgesSet[i][1]),'v1':str(fEdgesSet[i][0]),'v2':str(fEdgesSet[j][0])}
                 graph1={'v0':[], 'v1':[('v0',str(fEdgesSet[i][2])) ], 'v2':[('v0',str(fEdgesSet[j][2])) ]}
                 result.append((graph1, graphLabel1))

                 graphLabel2={'v0':str(fEdgesSet[j][0]),'v1':str(fEdgesSet[j][1]),'v2':str(fEdgesSet[i][1])}
                 graph2={'v0':[('v1',str(fEdgesSet[j][2]))], 'v1':[('v2',str(fEdgesSet[i][2]))], 'v2':[]}
                 result.append((graph2, graphLabel2))

            if ((fEdgesSet[i][0] == fEdgesSet[i][1]) and (fEdgesSet[i][1] == fEdgesSet [j][0]) and (fEdgesSet[j][0] != fEdgesSet[j][1]) ):
                 graphLabel1={'v0':str(fEdgesSet[i][0]),'v1':str(fEdgesSet[i][1]),'v2':str(fEdgesSet[j][1])}
                 graph1={'v0':[('v1', str(fEdgesSet[i][2]))], 'v1':[('v2',str(fEdgesSet[j][2])) ], 'v2':[] }
                 result.append((graph1, graphLabel1))

                 graphLabel2={'v0':str(fEdgesSet[i][0]),'v1':str(fEdgesSet[i][1]),'v2':str(fEdgesSet[j][1])}
                 graph2={'v0':[('v1',str(fEdgesSet[i][2])), ('v2', str(fEdgesSet[j][2]))], 'v1':[], 'v2':[]}
                 result.append((graph2, graphLabel2))

            if ((fEdgesSet[i][0] == fEdgesSet[j][0]) and (fEdgesSet[i][1] == fEdgesSet [j][1]) ):
                 graphLabel1={'v0':str(fEdgesSet[i][0]),'v1':str(fEdgesSet[i][1]),'v2':str(fEdgesSet[j][1])}
                 graph1={'v0':[('v1', str(fEdgesSet[i][2])), ('v2', str(fEdgesSet[j][2]))], 'v1':[], 'v2':[]}
                 result.append((graph1, graphLabel1))

                 graphLabel2={'v0':str(fEdgesSet[i][1]),'v1':str(fEdgesSet[i][0]),'v2':str(fEdgesSet[j][0])}
                 graph2={'v0':[], 'v1':[('v0',str(fEdgesSet[i][2]))], 'v2':[('v0',str(fEdgesSet[j][2]))]}
                 result.append((graph2, graphLabel2))

            if ((fEdgesSet[i][0] == fEdgesSet[j][1]) and (fEdgesSet[i][1] == fEdgesSet [j][0]) ):
                 graphLabel1={'v0':str(fEdgesSet[i][0]),'v1':str(fEdgesSet[i][1])}
                 graph1={'v0':[('v1', str(fEdgesSet[i][2]))], 'v1':[('v0', str(fEdgesSet[j][2]))]}
                 result.append((graphLabel1, graph1))

                 graphLabel2={'v0':str(fEdgesSet[i][0]),'v1':str(fEdgesSet[i][1]),'v2':str(fEdgesSet[j][1])}
                 graph2={'v0':[('v1', str(fEdgesSet[i][2]))], 'v1':[('v2',str(fEdgesSet[j][2]))], 'v2':[]}
                 result.append((graph2, graphLabel2))

                 graphLabel3={'v0':str(fEdgesSet[j][0]),'v1':str(fEdgesSet[j][1]),'v2':str(fEdgesSet[i][1])}
                 graph3={'v0':[('v1', str(fEdgesSet[j][2]))], 'v1':[('v2',str(fEdgesSet[i][2]))], 'v2':[]}
                 result.append((graph3, graphLabel3))

            if ((fEdgesSet[i][0] == fEdgesSet[j][0]) and (fEdgesSet[i][1] == fEdgesSet [j][1])):
                 graphLabel1={'v0':str(fEdgesSet[i][0]),'v1':str(fEdgesSet[i][1]), 'v2':str(fEdgesSet[j][1])}
                 graph1={'v0':[('v1', str(fEdgesSet[i][2])), ('v2', str(fEdgesSet[j][2]))], 'v1':[], 'v2':[]}
                 result.append((graph1, graphLabel1))

                 graphLabel2={'v0':str(fEdgesSet[i][1]),'v1':str(fEdgesSet[i][0]),'v2':str(fEdgesSet[j][0])}
                 graph2={'v0':[], 'v1':[('v0',str(fEdgesSet[i][2]))], 'v2':[('v0',str(fEdgesSet[j][2]))]}
                 result.append((graph2, graphLabel2))

            if ((fEdgesSet[i][1] == fEdgesSet[j][1]) and (fEdgesSet[i][0] != fEdgesSet[i][1]) and (fEdgesSet[i][1] != fEdgesSet[j][0]) and (fEdgesSet[i][0] != fEdgesSet[j][0]) and (fEdgesSet[i][0] != fEdgesSet[j][1]) ):
                 graphLabel1={'v0':str(fEdgesSet[i][1]),'v1':str(fEdgesSet[i][0]), 'v2':str(fEdgesSet[j][0])}
                 graph1={'v0':[], 'v1':[('v0', str(fEdgesSet[i][2]))], 'v2':[('v0', str(fEdgesSet[j][2]))]}
                 result.append((graph1, graphLabel1))

            if ((fEdgesSet[i][0] == fEdgesSet[j][1]) and (fEdgesSet[i][0] != fEdgesSet[i][1]) and (fEdgesSet[i][0] != fEdgesSet[j][0]) and (fEdgesSet[i][1] != fEdgesSet[j][0]) and (fEdgesSet[i][1] != fEdgesSet[j][1]) ):
                 graphLabel1={'v0':str(fEdgesSet[j][0]),'v1':str(fEdgesSet[i][0]), 'v2':str(fEdgesSet[i][1])}
                 graph1={'v0':[('v1', str(fEdgesSet[j][2]))], 'v1':[('v2', str(fEdgesSet[i][2]))], 'v2':[]}
                 result.append((graph1, graphLabel1))

            if ((fEdgesSet[i][0] == fEdgesSet[j][0]) and (fEdgesSet[i][0] != fEdgesSet[i][1]) and (fEdgesSet[i][0] != fEdgesSet[j][1]) and (fEdgesSet[i][1] != fEdgesSet[j][0]) and (fEdgesSet[i][1] != fEdgesSet[j][1]) ):
                 graphLabel1={'v0':str(fEdgesSet[i][0]),'v1':str(fEdgesSet[i][1]), 'v2':str(fEdgesSet[j][1])}
                 graph1={'v0':[('v1', str(fEdgesSet[i][2])), ('v2', str(fEdgesSet[j][2]))], 'v1':[], 'v2':[]}
                 result.append((graph1, graphLabel1))

            j=j+1

     return result


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


def main():
    thr=int(input("Give me your threshold:"))
    graph,graphLabel=readGraph("../graphGenOut.dot") #read the file and built the graph || dictionari key(id):[(ids,edLabel),(ids,edLabe),(ids,edLabe)]
    frequentSubG(graph,graphLabel,thr)
if __name__ == "__main__":
    main()
