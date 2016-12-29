#Possible solution for Data Mining Project
import re
#possible problem with graph duplication
def readGraph(n):
    graph={}
    graph_fin={}
    iniz=re.compile('digraph [a-zA-Z]*{')
    label=re.compile('[0-9]+ [\[label=]')
    finz="}"
    f=open(n,"r")
    lines=f.readlines()
    for line in lines:
        if(iniz.match(str(line))==None and finz!=line and label.match(str(line))==None):
            line_split=line.rstrip("\n").split(" ")
            print (line_split)
            if(line_split[0] in graph):
                temp=graph[line_split[0]]
                graph[line_split[0]]=temp+[line_split[2]]
            else:
                graph[line_split[0]]=[line_split[2]]
        if(label.match(str(line))):
            line_split1=line.rstrip("\n").split(" ")
            graph_fin[(line_split1[0],line_split1[5])]=graph[line_split1[0]]
    return graph_fin

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
    graph=readGraph("../graphGenOut.dot") #read the file and built the graph || dictionari key(id,label):[ids,ids,ids]



if __name__ == "__main__":
    main()
