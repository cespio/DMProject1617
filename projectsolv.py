#Possible solution for Data Mining Project
import re
#possible problem with graph duplication
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
    print(fEdges)# then remove all the elements that have value < thr

#frequentEdges between label --> we are working with directed graph so the order matter
def countFrequentEdges(graph,graphLabel,thr):
    #bruteforcemode passo tutta la strutture
    count={}
    for x in graph:
        adjList=graph[x]
        for y in adjList:
            k=(graphLabel[x],graphLabel[y[0]],y[1])
            if(k in count):
                t=count[k]
                count[k]=t+1
            else:
                count[k]=1
    return count


def main():
    thr=int(input("Give me your threshold:"))
    graph,graphLabel=readGraph("../graphGenOut.dot") #read the file and built the graph || dictionari key(id):[(ids,edLabel),(ids,edLabe),(ids,edLabe)]
    frequentSubG(graph,graphLabel,thr)


if __name__ == "__main__":
    main()
