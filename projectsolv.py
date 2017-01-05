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

#defintion of DFSvist for
#COLOR for backedge and forward edge? grey to black, grey to white
#dfscode visit(timeS,timeD,LabelS,LabelE,LabelD)
#adapt the dfs code to work only with LabelS

def DFS(graph,graphLabel):
    discovery={}
    father={}
    visit=[]
    time=0
    def DFS_Visit(graph,x):
        nonlocal time
        time+=1
        discovery[x]=0
        for u in graph[x]:
            if(not(u[0] in discovery)):
                father[u[0]]=x
                visit.append((time-1,time,graphLabel[x],u[1],graphLabel[u[0]]))
                DFS_Visit(graph,u[0])
    for x in graph:
        if(not(x in discovery)):
            DFS_Visit(graph,x)

    #procedure to ordering the dfscode
    sortDFSVisit(visit)


def sortDFSVisit(visit):
    

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
    return fEdges

def subGraphExtension(subG,G,thr,fEdges):
    candidateSet={}
    res=subG

def main():
    thr=int(input("Give me your threshold:"))
    graph,graphLabel=readGraph("../graphGenOut.dot") #read the file and built the graph || dictionari key(id):[(ids,edLabel),(ids,edLabe),(ids,edLabe)]
    DFS(graph,graphLabel)
    #frequentSubG(graph,graphLabel,thr)


if __name__ == "__main__":
    main()
