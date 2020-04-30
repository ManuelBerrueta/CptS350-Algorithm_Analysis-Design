#!/usr/bin/env
from pyeda.inter import *

nodes = list(range(0, 32))
evens = [eachNum for eachNum in nodes if eachNum % 2 == 0]
primes = [3,5,7,11,13,17,19,23,29,31]
print("NODES: " + str(nodes))
print("[even]: " + str(evens))
print("[prime]: " + str(primes))

#! Global Working Variables
myBDD_graph = []
R = set()

#! Create graph per Step 2.
'''
Let G be a graph over 32 nodes (namely, node 0,   , node 31). 
For all 0 <= i; j >= 31, there is an edge from node i to node j 
iff (i + 3) % 32 = j % 32  or  (i + 8) % 32 = j % 32. (% is the modular
operator in C; e.g., 35% 32=3.) A node i is even if i is an even number. 
 A node i is prime if i is a prime number. In particular, we define [even] as 
the set {0,2,4,6,...,30}; and [prime] as the set {3,5,7,11,13,17,19,23,29,31}.
We use R to denote the set of all edges in G.
'''

#We'll loop over the nodes to look for edges satisfying the conditions
for i in nodes:
    for j in nodes:
        condition_1 = False
        condition_2 = False
        if ((i + 3) % 32) == (j % 32):
            condition_1 = True
        if ((i + 8) % 32) == (j % 32):
            condition_2 = True
        # If either of the two conditions are satisfied, we add this edge to our graph
        if condition_1 or condition_2:
            myBDD_graph.append((i,j))
            R.add((i,j))
print("Graph(Edges):" + str(myBDD_graph))
print("Graph(setofEdges):" + str(set(myBDD_graph)))
print("R" + str(R))


'''(StatementA) for each node u in [prime], there is a node v in [even] such that u can reach v
in even number of steps.'''

reachable_nodes_per_statementA = []

uCount = 0
vCount = 0
two_step_match = []
even_steps_match = []

#Check for 2 step matches
for each in myBDD_graph:
    num_steps = 0
    u = -1
    v = -1
    if each[0] in primes:
        uCount += 1
        u = each[0]
        next_node = each[1]
        num_steps += 1
        # Search for the next edge from u's connected node
        for nextEdge in myBDD_graph: #TODO: Could to for i,nextEdge in enumerate(myBDD_graph):
            # if this nextEdge first node is u's last edge connected node
            print("BDD AT each step: " + str(myBDD_graph))
            if nextEdge[0] == next_node:
                poss_v = nextEdge[1]
                # and this node is even
                if poss_v in evens:
                    num_steps += 1
                    vCount += 1
                    if num_steps == 2:
                        v = poss_v
                        two_step_match.append((u,v))
                        #break
                    if (num_steps % 2) == 0:
                        v = poss_v
                        even_steps_match.append((u,v,num_steps))
#Possibly need recursive check
#TODO: write a function where it recursively goes through the rest of the data structure

print("Two Step Matches:" + str(two_step_match))
print("Even Matches (u,v, # of Steps):" + str(even_steps_match))

count_primes = 0
for each in primes:
    for eachMatch in two_step_match:
        if each == eachMatch[0]:
            count_primes += 1
            break

if count_primes == primes.__len__():
    print("TRUE: for each node u in [prime], there is a node v in [even] such "
    + "that u can reach v in even number of steps ")







