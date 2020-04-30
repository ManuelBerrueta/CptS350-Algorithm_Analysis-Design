#!/usr/bin/python3
import pyeda
from pyeda.inter import *
from graphviz import Source
import os

def num_to_bin(num, offset):
    tempNum = "{0:b}".format(num)
    if len(tempNum) < offset:
        binNum = ('0' * (offset - len(tempNum))) + tempNum
        return binNum
    else:
        binNum = tempNum
        return binNum

#! We'll create the graph G:
# We'll loop over the nodes to look for edges satisfying the conditions
def create_graph(nodes):
    myBDD_graph_int = []
    myBDD_graph_bin = []
    R = set()
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
                myBDD_graph_int.append((i,j))
                myBDD_graph_bin.append((num_to_bin(i, 5), num_to_bin(j, 5)))
                R.add((i,j))
    #print(f"\nGraph in Integer (Edges): {myBDD_graph_int}")
    #print(f"\nGraph in Binary (Edges): {myBDD_graph_bin}")
    #print(f"\nGraph as set R: {R}\n\n")
    return myBDD_graph_int, myBDD_graph_bin


def trans_set_of_nodes_to_bin(nodes):
    new_bin_node_set = []
    for node in nodes:
        new_bin_node_set.append(num_to_bin(node, 5))
    return new_bin_node_set



def trans_nodes_to_bool_x(nodes):
    node_set_in_bool = []
    for node in nodes:
        myBoolean_Expression = ''
        for i, bit in enumerate(node):
            
            if (int(bit) == 0):
                temp_Expression = '~x' + str(i) + ' & '
                myBoolean_Expression += temp_Expression
            elif (int(bit) == 1):
                temp_Expression = 'x' + str(i) + ' & '
                myBoolean_Expression += temp_Expression
            else:
                temp_Expression = 'ERROR: ERROR in trans_bool_ex & '
                myBoolean_Expression += temp_Expression
        node_set_in_bool.append(myBoolean_Expression[:-3])
    return node_set_in_bool

def trans_nodes_to_bool_y(nodes):
    node_set_in_bool = []
    for node in nodes:
        myBoolean_Expression = ''
        for i, bit in enumerate(node):
            
            if (int(bit) == 0):
                temp_Expression = '~y' + str(i) + ' & '
                myBoolean_Expression += temp_Expression
            elif (int(bit) == 1):
                temp_Expression = 'y' + str(i) + ' & '
                myBoolean_Expression += temp_Expression
            else:
                temp_Expression = 'ERROR: ERROR in trans_bool_ex & '
                myBoolean_Expression += temp_Expression
        node_set_in_bool.append(myBoolean_Expression[:-3])
    return node_set_in_bool



#! Translate the graph to a Boolean Expression
def trans_to_bool_ex(BDD_Graph):
    myGraph_Representation_in_Boolean_Formula = []
    for edge in BDD_Graph:
        #* in_node ---> out_node
        in_node = edge[0]
        out_node = edge[1]
        myBoolean_Expression = ''
        
        #! Build the expression:
        #* For each bit in the in_node
        for i, bit in enumerate(in_node):
            if (int(bit) == 0):
                temp_Expression = '~x' + str(i) + ' & '
                myBoolean_Expression += temp_Expression
            elif (int(bit) == 1):
                temp_Expression = 'x' + str(i) + ' & '
                myBoolean_Expression += temp_Expression
            else:
                temp_Expression = 'ERROR: ERROR in trans_bool_ex & '
                myBoolean_Expression += temp_Expression

        #* For each bit in the out_node
        for i, bit in enumerate(out_node):
            if (int(bit) == 0):
                #temp_Expression = '~x' + str(i) + ' & '
                temp_Expression = '~y' + str(i) + ' & '
                myBoolean_Expression += temp_Expression
            elif (int(bit) == 1):
                #temp_Expression = 'x' + str(i) + ' & '
                temp_Expression = 'y' + str(i) + ' & '
                myBoolean_Expression += temp_Expression
            else:
                temp_Expression = 'ERROR: ERROR in trans_bool_ex & '
                myBoolean_Expression += temp_Expression
        #! Get rid of the last 3 chars ' & ' at the end of the Expression
        #print(f"\n {myBoolean_Expression[:-3]}")
        #* Append this edge expression to the formula of the graph
        myGraph_Representation_in_Boolean_Formula.append(myBoolean_Expression[:-3])
    return myGraph_Representation_in_Boolean_Formula


#! Tranform boolean expression
def trans_to_BDD(bool_graph):
    #! Need the first expression to build the formula
    myBDD_Formula = expr(bool_graph[0])
    myBDD_Formula = expr2bdd(myBDD_Formula)

    #* For each expression string (exp_str) in the bool_graph
    for exp_str in bool_graph[1:]:
        
        #* Transorm this expression string (exp_str) to PyEDA Boolean Expression
        next_expression = expr(exp_str)
        #print(next_expression)
        #* Transform this PyEDA temp_expression to a PyEDA BDD Expression
        bdd_expression = expr2bdd(next_expression)
        myBDD_Formula = myBDD_Formula or next_expression
    
    return myBDD_Formula


#! We will perform a Boolean Compose
def boolean_compose(R_left, R_right):
    X = bddvars('x', 5)
    Y = bddvars('y', 5)
    Z = bddvars('z', 5)
    #R1 = R_left.compose({X:Z})
    #R2 = R_right.compose({Z:Y})
    for i in range(0,5):
        R1 = R_left.compose({X[i]:Z[i]})
        R2 = R_right.compose({Z[i]:Y[i]})

    R = (R1 & R2).smoothing(Z)
    return R

def transitive_closure(R):
    H = R

    while 1:
        H_prime = H
        H = H_prime | boolean_compose(H_prime, R)

        if H.equivalent(H_prime):
            return H

def compute_PE(RR2star, EVEN, PRIME):
    result = RR2star ^ EVEN ^ PRIME
    return result

def check_statementA(PE, PRIME, EVEN):
    X = bddvars('x', 5)
    Y = bddvars('y', 5)
    
    result = ~((~(((~PRIME) |  PE).smoothing(X))).smoothing(Y))
    return result

#! Part 4(a)
def  check_for_even_v(node_u, graph, even):
    for each in graph:
        num_steps = 0
        u = -1
        v = -1
        uCount = 0
        vCount = 0
        if each[0] == node_u:
            uCount += 1
            u = each[0]
            next_node = each[1]
            num_steps += 1
            if next_node in evens:
                print(f"Given input node u ={node_u}, found even v={next_node}")
                return next_node
            # Search for the next edge from u's connected node
            for nextEdge in graph: #TODO: Could to for i,nextEdge in enumerate(myBDD_graph):
                # if this nextEdge first node is u's last edge connected node
                if nextEdge[0] == next_node:
                    poss_v = nextEdge[1]
                    # and this node is even
                    if poss_v in evens:
                        num_steps += 1
                        vCount += 1
                        print(f"Given input node u ={node_u}, found even node v={poss_v}")
                        return poss_v

                        """ if num_steps == 2:
                            v = poss_v
                            two_step_match.append((u,v))
                            #break
                        if (num_steps % 2) == 0:
                            v = poss_v
                            even_steps_match.append((u,v,num_steps)) """ 

def search_for_node(node_u, node_v, counter, graph_index, graph):
    edge = graph[graph_index]
    leftNode = edge[0]
    rightNode = edge[1]

    if leftNode == node_u:
        counter += 1
        if rightNode == node_v:
            return counter
        else:
            if (graph_index + 1) >= len(graph):
                print("Did not finsh such node u and v that met the criteria")
                return -1
            search_for_node(rightNode, node_v, counter, (graph_index +1), graph)
    else:
        if (graph_index + 1) >= len(graph):
            print("Did not finsh such node u and v that met the criteria")
            return -1
        search_for_node(node_u, node_v, counter, (graph_index +1), graph)    
    #TODO: Will return count
    return counter

def search_for_node_two(node_u, node_v, counter, graph_index, graph):
    for eachEdge in graph:
        leftNode = eachEdge[0]
        rightNode = eachEdge[1]      
        if leftNode == node_u:
            counter += 1
            if rightNode == node_v:
                return counter
            else:
                """ if (graph_index + 1) >= len(graph):
                    print("Did not finsh such node u and v that met the criteria")
                    return -1 """
                return search_for_node(rightNode, node_v, counter, (graph_index +1), graph)
        """ else:
            if (graph_index + 1) >= len(graph):
                print("Did not finsh such node u and v that met the criteria")
                return -1
            search_for_node(node_u, node_v, counter, (graph_index +1), graph) """    
        #TODO: Will return count
    return counter

def pathcount(u, v, steps, graph):
    for edge in graph:            
        if edge[0] == u:
            steps += 1
            if edge[1] == v:
                if (steps % 2) == 0:
                    print(f"Found v={v} in {steps} even number of steps")
                    os._exit(1)
                else:
                    print("FOUND! + DOES NOT MEET CRITERIA")
                    return
            else:
                pathcount(edge[1], v, steps, graph)
    steps = 0




def  check_match_uv(node_u, node_v, graph, even):
    num_steps = 0
    for graphIndex, each in enumerate(graph):
        if each[0] == node_u:
            next_node = each[1]
            if next_node == node_v:
               pass
            else:
                num_steps += 1
                num_steps = search_for_node(next_node, node_v, num_steps, (graphIndex + 1), graph)
                if (num_steps % 2) == 0:
                    print(f"Given input node u ={node_u}, found even " +
                          f"v={next_node} in {num_steps} even number of steps")
                    return num_steps
                else:
                    num_steps = 0
    return num_steps


if __name__ == "__main__":
    myGraph_int = []
    myBinGraph = []
    # Create nodes 0 - 31
    nodes = list(range(0, 32))
    # Create even list
    evens = [eachNum for eachNum in nodes if eachNum % 2 == 0]
    # Create prime list
    primes = [3,5,7,11,13,17,19,23,29,31]
    print("NODES: " + str(nodes))
    print("[even]: " + str(evens))
    print("[prime]: " + str(primes))


    #! Create graph per #2 in Symbolic Graph Project:
    ''' Let G be a graph over 32 nodes (namely, node 0,   , node 31). 
    For all 0 <= i; j >= 31, there is an edge from node i to node j 
    iff (i + 3) % 32 = j % 32  or  (i + 8) % 32 = j % 32. (% is the modular
    operator in C; e.g., 35% 32=3.) A node i is even if i is an even number. 
     A node i is prime if i is a prime number. In particular, we define [even] as 
    the set {0,2,4,6,...,30}; and [prime] as the set {3,5,7,11,13,17,19,23,29,31}.
    We use R to denote the set of all edges in G. '''
    myGraph_int, myBinGraph = create_graph(nodes)
    print(f"\nGraph in Integer (Edges): {myGraph_int}")
    print(f"\nGraph in Binary  (Edges): {myBinGraph}\n")

    #! Step 3.1:
    '''Obtains BDDs RR, EV EN, PRIME for the nite sets R, [even], [prime],
        respectively. Pay attention to the use of BDD variables in your BDDs.'''
    #* Translate each edge to a Boolean Expression and convert to a formula
    myGraph_Expressions = trans_to_bool_ex(myBinGraph)
    print(f"R Expressions = {myGraph_Expressions}\n")
    
    '''Tranlate each node of the even set and prime setto binary and to
        Boolean Expression'''
    evens_bin = trans_set_of_nodes_to_bin(evens)
    EVEN = trans_nodes_to_bool_y(evens_bin)
    print(f"EVEN Expressions = {EVEN}\n")
    primes_bin = trans_set_of_nodes_to_bin(primes)
    PRIME = trans_nodes_to_bool_x(primes_bin)
    print(f"PRIME Expressions = {PRIME}\n")

    #* Translate to BDD
    RR = trans_to_BDD(myGraph_Expressions)
    print(f"RR BDD  = {RR}")
    #print("\nPRIME")
    EVEN = trans_to_BDD(EVEN)
    print(f"EVEN BDD = {EVEN}")
    #print("\nEVEN")
    PRIME = trans_to_BDD(PRIME)
    print(f"PRIME BDD = {PRIME}")


    #! Step 3.2
    '''Compute BDD RR2 for the set R ∘ R (R compose R), from BDD RR. Herein,
        RR2 encodes the set of node pairs such that one can reach the other
         in two steps.'''
    RR2 = boolean_compose(RR, RR)
    print(f"RR2 BDD  = {RR2}")

    #! Step 3.3
    '''Compute the transitive closure RR2star of RR2. Herein, RR2star encodes
        the set of all node pairs such that one can reach the other in even
         number of steps.'''
    RR2star = transitive_closure(RR2)
    print(f"RR2star BDD  = {RR2star}")


    #! Step 3.4:
    '''Compute the BDD PE, from BDDs PRIME, EVEN, and RR2star, that is to encode
        the set of all node pairs (u, v) such that u is prime and v is even and
         u can reach v in even number of steps.'''
    PE_temp_EVEN = boolean_compose(RR2star, EVEN)
    PE_temp_PRIME = boolean_compose(RR2star, PRIME)
    PE = boolean_compose(PE_temp_PRIME, PE_temp_EVEN)
    PE = compute_PE(RR2star, EVEN, PRIME)


    #print(f"PE BDD  = {PE}")
    #print(f"PE_temp_EVEN  = {PE_temp_EVEN}")
    #print(f"PE_temp_PRIME  = {PE_temp_PRIME}")
    #print(f"PE BDD  = {PE}")
    ##PE = EVEN & PRIME & RR2star
    #print(f"PE BDD  = {PE}")
    #
    #gv = Source(RR2star.to_dot())
    #gv.render('R_pdf', view=True)
#
    #gv = Source(PRIME.to_dot())
    #gv.render('PRIME_pdf', view=True)
#
    #gv = Source(EVEN.to_dot())
    #gv.render('EVEN_pdf', view=True)
#
    #! Step 3.5 Check Statement A
    '''(StatementA) for each node u in [prime], there is a node v in [even]
        such that u can reach v in even number of steps.'''
    
    result = check_statementA(PE, PRIME, EVEN)

    if (result):
        print("\033[1m" + "Statement A is True, that is:")
        print("\tfor each node u in [prime]," +
              " there is a node v in [even] such that u can reach v in even" +
                " number of steps.")
    else:
        print("\033[1m" + "Statement A is FALSE, that is:")
        print("\tfor each node u in [prime]," + 
              " there is " + "\033[1m" + "NOT" + " a node v in [even] such" +
              " that u can reach v in even number of steps.")

    print("Part 4 - Testing:")
    
    print("=Part 4(a) with node u=5")
    #! Step 4(a)
    #node_u = input("4(a) - Enter node U::> ")
    #node_v = check_for_even_v(node_u)
    node_v = check_for_even_v(5, myGraph_int, evens)
    

    #! Step 4(b)
    print("=Part 4(b) with node u=0 and v=3:")
    num_steps_uv = pathcount(0,3,0,myGraph_int)
    print("=Part 4(b) with node u=0 and v=6:")
    num_steps_uv = pathcount(0,6,0,myGraph_int)