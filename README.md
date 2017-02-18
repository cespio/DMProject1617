INTRODUCTION
------------
Authours:

Alessandro Rizzuto

Francesco Contaldo 

Project:

Data Mining Project "Frequent Pattern Mining on a single Graph"

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
'python graphGen.py NumberOfLabel NumberOfHours(weight)'

the first parameter is referred to the number of possible values that can be assigned to a single node. Range of value valid 0..13

the second parameter is used to decide the number of possible values that the different weights (hours) can take. Range of valid value 0..24

The automated generated graph is created in the test folder


Main Program
------------
To mine the graph use:
'python projectsolve SupportThreshold SizeThreshold'

The first parameter is the number of occurrences, the second one is the number of relations inside the frequent subgraphs.

The found subgraphs are stored in the test directory with the dot notation.
