#graphGenerator python
#The parameter e represent the max number of possible repeted edge
#review the genearation
from random import uniform
def graphGenerator(e):
    file_out=open("graphGenOut.dot","w")
    file_out.write("digraph prova{\n")
    for y in range(e):
        print(y)
        for x in range(10):
            n1=uniform(1,50)
            for z in range(10):
                n2=uniform(1,50)
                if(n1>n2):
                    time=str(int(uniform(0,24)))
                    file_out.write(str(x) + " -> " + str(z) + "  [label=\"" + time + "\"];\n")
    file_out.write("}")
    file_out.close()

def main():
    e=int(input("Dammi sta thr -- >"))
    graphGenerator(e)
    print("AA")

if __name__ == "__main__":
    main()
