#graphGenerator python
#The parameter e represent the max number of possible repeted edge
#review the genearation
import numpy
from random import uniform

#no labels foreign and outside no sense
labels={
    "1": "Urban",
    "2": "Movement",
    "3": "Nature",
    "4": "Social",
    "5": "Commerical",
    "6": "Road",
    "7": "XXX",
    "8": "Zone1",
    "9": "Zone2",
}


def writeLables(lab,file_out):
    for x in lab:
        n=uniform(1,9)
        lab[x]=labels[str(int(n))]
        file_out.write(str(x) + "[label=\""+lab[x]+"\"]\n")


def graphGenerator(n):
    file_out=open("../graphGenOut.dot","w")
    file_out.write("digraph prova{\n")
    flag=0
    labels_node={}
    matrix=numpy.zeros((n,n))
    for y in range(n):
        flag=0
        while(flag==0):
            n1=uniform(1,100)
            for z in range(n):
                n2=uniform(1,100)
                if(n1>n2 and matrix[y][z]==0 and y!=z):
                    time=str(int(uniform(0,24)))
                    matrix[y][z]=1
                    labels_node[y]=None
                    labels_node[z]=None
                    file_out.write(str(y) + " -> " + str(z) + "  [label=\"" + time + "\"];\n")
                    flag=1
    writeLables(labels_node,file_out)
    file_out.write("}")
    file_out.close()

def main():
    n=int(input("Dammi er numero de nodi --> "))
    graphGenerator(n)
    print("Graph Generated")

if __name__ == "__main__":
    main()
