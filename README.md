INTRODUCTION
------------
Authours:

*Alessandro Rizzuto 187156

*Francesco Contaldo 190626

Project:
Data Mining Project "Frequent Pattern Mining on a single Graph"


The whole work has been done exploiting the work presented in this paper: Mohammed Elseidy, Ehab Abdelhamid, Spiros Skiadopoulos, and Panos Kalnis. "GRAMI: Frequent Subgraph and Pattern Mining in a Single Large Graph. PVLDB, 7(7):517-528, 2014."

The core algorithms and concepts have been implemented from scratch for this university project

INSTRUCTIONS
-----------

DOT
---
Both input and output respect the dot notation to describe a graph
https://en.wikipedia.org/wiki/DOT_(graph_description_language)

to transform a dot file into visible pdf format use
'dot -Tps NameFile.dot -o  NameFile.pdf'

Graph Generation
-------------
To generate a random input graph use the following command:
'python graphGen.py NumberOfNodes NumberOfLabel NumberOfHours(weight)'

the second parameter is referred to the number of possible values that can be assigned to a single node. Range of value valid 0..13

the third parameter is used to decide the number of possible values that the different weights (hours) can take. Range of valid value 0..24

The automated generated graph is created in the test folder with the name 'graphGenOut.dot'


Main Program
------------
To mine the graph use:
'python projectsolve SupportThreshold SizeThreshold'

The first parameter is the number of occurrences, the second one is the number of relations inside the frequent subgraphs.

The program use as input the graph inside the file 'graphGenOut.dot' inside the test folder

The found subgraphs are stored in the test directory with the dot notation.
