#Possible solution for Data Mining Project
import re
def readGraph(n):
    graph={}
    iniz=re.compile('digraph [a-zA-Z]*{')
    finz="}\n"
    f=open(n,"r")
    lines=f.readlines()
    for line in lines:
        if(iniz.match(str(line))==None and finz!=line):
            line_split=line.rstrip("\n").split(" ")
            if(line_split[0] in graph):
                temp=graph[line_split[0]]
                graph[line_split[0]]=temp+[line_split[2]]
            else:
                graph[line_split[0]]=[line_split[2]]

    return graph


def collapseGraph(graph):
    graph_collapse={}

    for x in graph:
        list_w={}
        app_list=graph[x]
        for y in app_list:
            if(y in list_w):
                b=list_w[y]
                list_w[y]=b+1
            else:
                list_w[y]=1
        graph_collapse[x]=list(list_w.items())
    return graph_collapse

#try with BFS
# candidate=[]
#for x in graph:
#    for (a,b) in graph[x]:
#        if(int(b)>=int(thr)):
#            candidate.append((x,a))

#first attempt of a BFS search
#i need to visit all the edges
'''
def frequentItemset(thr,graph):
    stack=[]
    res={}
    stack.append('0') #how to select the first
    print(stack)
    while(stack!=[]):
        head=stack.pop(0)
        adjency_list=graph[head] #adjency_list del graph
        while(adjency_list!=[]):
            elem=adjency_list.pop(0)
            if (elem[1]>thr):
                print("\n"+head+"-> "+elem[0]+" weigth "+str(elem[1])+" \n")
                res[head]=elem[1]

            stack.append(elem[0])
    print(res)
'''
def frequentItemset2(thr,graph):
    for x in graph:
        adjency_list=graph[x]
        new_adl=[]
        for elem in adjency_list:
            if(elem[1]>=thr):
                new_adl.append(elem)
        graph[x]=new_adl
    return graph

def printResult(graph):
    file_out=open("risGrahp.dot","w")
    file_out.write("digraph Ris{\n")
    for x in graph:
        t_l=graph[x]
        for y in t_l:
            file_out.write(str(x) + " -> " + str(y[0]) + "  [label=\"" + str(y[1]) + "\"];\n")
    file_out.write("}")
    file_out.close()

def main():
    thr=int(input("Give me your threshold:"))
    graph=readGraph("mio.dot") #read the file
    graph_collapse=collapseGraph(graph) #collpasing the graph
    print(graph_collapse)
    print("\n")
    ris=frequentItemset2(thr,graph_collapse)
    printResult(ris)


if __name__ == "__main__":
    main()
