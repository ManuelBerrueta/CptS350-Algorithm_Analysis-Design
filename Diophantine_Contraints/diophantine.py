#!/usr/bin/env python
# CptS 350: Design and Analysis of Algorithms
# Solving Linear Diophantine constraints using labeled graphs project
#                       by Manuel Berrueta

DEBUG = 0
TESTING = 0
ALGO_TEST = 0
INPUT_TEST = 0

def num_to_bin(num, padding):
    tempNum = "{0:b}".format(num)
    if len(tempNum) < padding:
        binNum = ('0' * (padding - len(tempNum))) + tempNum
        return binNum
    else:
        binNum = tempNum
        return binNum

def convert_to_little_endian(num, offset):
    temp_bin_num = num_to_bin(num, offset)
    return "".join(reversed(temp_bin_num))

def split_equation(equation):
    #! First split C1, C2, C3, and C
    C = []
    if equation[0] == '+':
        C.append(int(equation[1]))
    elif equation[0] == '-':
        C.append((-1) * int(equation[1]))
    else:
        print(">>>>Equation is in the wrong format")
    
    if equation[3] == '+':
        C.append(int(equation[4]))
    elif equation[3] == '-':
        C.append((-1) * int(equation[4]))
    else:
        print(">>>>Equation is in the wrong format")

    if equation[6] == '+':
        C.append(int(equation[7]))
    elif equation[6] == '-':
        C.append((-1) * int(equation[7]))
    else:
        print(">>>>Equation is in the wrong format")

    if equation[9] == '+':
        C.append(int(equation[10]))
    elif equation[9] == '-':
        print(">>>>>> ERROR: C should not be negative!\n")
        print("\t>>>>>> ERROR: C should not be negative!\n")
        C.append((-1) * int(equation[10]))
    else:
        print(">>>>Equation is in the wrong format")

    #! Split all the x's
    x = []
    x.append(equation[2])
    x.append(equation[5])
    x.append(equation[8])

    if ALGO_TEST:
        print(f"C={C}")
        print(f"x={x}")

    return C, x

def get_K_c(C):
    if C == 0:
        return 0
    else:
        return len(convert_to_little_endian(C, 0))

def get_b_i(C, i):
    C_bin = convert_to_little_endian(C,0)
    K_c = get_K_c(C)

    if ALGO_TEST:
        if i == 0:
            print("\n\n\t\t>>>>>>>>>>> [ Error with i in get_b_i, i=0 \n\n")

    if i == (K_c + 1):
        b_i = 0
    elif (i >= 1) and (i <= K_c):
        b_i = C_bin[i-1]
    else:
        print("\n\n\t\t>>>>>>>>>>> [ Error with i in get_b_i \n\n")
    return b_i

def get_C_max(equation):
    C,x = split_equation(equation)
    Cmax = 0
    #Here we loop to find the max
    for d1 in range(2):
        for d2 in range(2):
            for d3 in range(2):
                for d in range(2):
                    tempSum = abs((C[0] * d1) + (C[1] * d2) + (C[2] * d3) + d)
                    if tempSum > Cmax:
                        Cmax = tempSum
    return Cmax

# This takes the list with the numbers and picks the first bit out of each one
def encoder(b_list):
    # Find the longest length. That is check all the binary represented postive
    # integers in this list, and return the lenght of the longest represenation
    # i.e. 1 in bin is only 1, thus 1 digit, however 4 in bin is 100, thus 3 digits.
    newb_list = ['']  * len((b_list[0]))

    for eachItem in b_list:
        tempStr = ''
        for i, each_b in enumerate(eachItem):
            newb_list[i] = newb_list[i] + each_b
    return newb_list

#! Final Step
def decoder(b_list):
    tempBin = ''
    result_List = []
    for each in b_list:
        tempBin = ''.join(reversed(each))
        result_List.append(int(tempBin, 2))
    return result_List


#! Algorithm 1
# Each entry in M1 or M2 is an edge [carry, i, carry_prime, i_prime, a]
#    where a represents a1, a2, a3 ∈ {0,1}
def build_graph(equation):
    C, x = split_equation(equation)
    K_c = get_K_c(C[3]) # K_c of C the constant
    C_max = get_C_max(equation)
    
    initial_state = [0, 1]
    accepting_state = [0, (K_c + 1)]
    #M = [initial_state, accepting_state] #TODO: Not sure if I need this at the beginning?
    M = []

    #while (carry >= (-C_max)) and (carry <= C_max):
    for carry in range(-C_max, C_max+1):
        for i in range(1, (K_c + 2)): #K_c+1 but range will end at Kc if we just do +1
            for carry_prime in range(-C_max, C_max+1):
                for i_prime in range(1, (K_c + 2)): #K_c+1 but range will end at Kc if we just do +1
                    for a1 in range(0,2):
                        for a2 in range(0,2):
                            for a3 in range(0,2):
                                R = (C[0] * a1) + (C[1] * a2) + (C[2] * a3) + int(get_b_i(C[3], i)) + carry

                                if ((R % 2) == 0) and (carry_prime == (R / 2)):
                                    if i >= 1 and i <= K_c:
                                        i_prime = i + 1
                                    else:
                                        i_prime = i

                                    #M.append([carry, i, carry_prime, i_prime, a1, a2, a3])
                                    #Testing for possible easier processing
                                    a = str(a1) + str(a2) + str(a3)
                                    M.append([carry, i, carry_prime, i_prime, a]) 

    return M, initial_state, accepting_state

#Each entry in M cartesian product of M1 x M2 is an edge:
#   [carry1, i1], [carry2, i2] ----- a ----> [carryPrime1, iPrime1], [carryPrime2, iPrime2]
#   [ M1 start ], [ M2 start ] (a1, a2, a3)
# edge  0             1         4                2                       3
# DFA Cross Product Reference: https://scanftree.com/automata/dfa-cross-product-property
def cartesian_product(M1, M2):
    M = []
    for each_conn_M1 in M1: #TODO: Change each_conn_M1 to M1_edge or edge_M1
        for each_conn_M2 in M2:
            # if they have the same common edge, they are reading the same symbol
            # [4] is the edge index which is a combition of a1,a2,a3 where a1,a2,a3 are {0,1}
            if each_conn_M1[4] == each_conn_M2[4]:
                a = each_conn_M1[4] #We could pick each_conn_M2[4] since is the same thing
                #TODO: Added this 0 after 'a' to use for visited....but I am not sure this will work for DFS
                #M.append( [ [each_conn_M1[0], each_conn_M1[1]], [each_conn_M1[2], each_conn_M1[3]], [each_conn_M2[0], each_conn_M2[1]], [each_conn_M2[2], each_conn_M2[3]], a, 0 ])
                M.append( [ [each_conn_M1[0], each_conn_M1[1]], [each_conn_M2[0], each_conn_M2[1]], [each_conn_M1[2], each_conn_M1[3]], [each_conn_M2[2], each_conn_M2[3]], a, 0 ])                
    return M              # [            M1  State           ]  [       M2  State                ]  [      M1 Neighbor State         ]  [       M2  Neighbor State       ]  a  Seen

stack = []
def DFS(G, v, accepting):
    global stack
   
    for edge in G:
        if v[0] == edge[0] and v[1] == edge[1]: # if this vertex in this edge match
            #Mark it as visited
            if edge[5] != 1:
                edge[5] = 1
                stack.append(edge[4])
                if accepting[0] == edge[2] and accepting[1] == edge[3]:
                    return True
                else:
                    result = DFS(G, [edge[2], edge[3]], accepting)
                    if result:
                        return True
                    else:
                        stack.pop(-1)
    return False

def print_LD_Q(equation, result, found):
    C, x = split_equation(equation)
    if found:
        print(f"{C[0]} * {result[0]} + {C[1]} * {result[1]} + {C[2]} * {result[2]} + {C[4]} = ", end='')
    else:
        print(f"{C[0]} * {result[0]} + {C[1]} * {result[1]} + {C[2]} * {result[2]} + {C[4]} != ", end='')
    print(f"{C[0] * result[0] + C[1] * result[1] + C[2] * result[2] + C[4]}")

def check_LD_Q(found, stack):
    # Test this Linear Diophantine instance Q, to see if it has positive
    # integer solutions.
    if found:
        print("\n================$[ Path Found ]$================")
        print(f">>>>> Edges:   {stack}")
        encoded_binNums = encoder(stack)
        print(f">>>>> Encoded: {encoded_binNums}")
        result = decoder(encoded_binNums)
        print(f">>>>> Decoded: {result}")
        print(f"Thus result of this LD is: {result}\n")
    else:
        print("\n----------------{ No Path Found }----------------")
        print(">>>>>> There is no positive integer solution to this system <<<<<<\n")

if __name__ == "__main__":
    #NOTE: The equations have to be passed in as strings in list for as below:
    T1_test_1 = ["+", "3", "x1", "-", "2", "x2", "+", "1", "x3", "+", "5", "=", "0"]
    T1_test_2 = ["+", "6", "x1", "-", "4", "x2", "+", "2", "x3", "+", "9", "=", "0"]

    M1_test, initial_state_M1, accepting_state_M1 = build_graph(T1_test_1)
    #print("\n> >> >>> >>>> >>>>> >>>>>> {  M1  } <<<<<< <<<<< <<<< <<< << <")
    #print(M1_test)
    M2_test, initial_state_M2, accepting_state_M2  = build_graph(T1_test_2)
    #print("\n> >> >>> >>>> >>>>> >>>>>> {  M2  } <<<<<< <<<<< <<<< <<< << <")
    #print(M2_test)

    print(f"\nT1 Test with:\n\t\t{T1_test_1}\n\t\t{T1_test_2}")
    
    M_t1 = cartesian_product(M1_test, M2_test)

    print(f"Length of M1 in T1: {len(M1_test)}")
    print(f"Length of M2 in T1: {len(M2_test)}")
    print(f"Length of M Cartesian Product of M1 x M2 : {len(M_t1)}")
    
    M_initial_state = [initial_state_M1, initial_state_M2]
    M_accepting_state = [accepting_state_M1, accepting_state_M2]

    found = DFS(M_t1, M_initial_state, M_accepting_state)
    check_LD_Q(found, stack)

    #! T2 Test:
    T2_test_1 = ["+", "3", "x1", "-", "2", "x2", "-", "1", "x3", "+", "3", "=", "0"]
    T2_test_2 = ["+", "6", "x1", "-", "4", "x2", "+", "1", "x3", "+", "3", "=", "0"]

    M1, initial_state_M1, accepting_state_M1 = build_graph(T2_test_1)
    #print("\n> >> >>> >>>> >>>>> >>>>>> {  M1  } <<<<<< <<<<< <<<< <<< << <")
    #print(M1_test)
    #print(f"M1 length={len(M1)}")
    
    M2, initial_state_M2, accepting_state_M2 = build_graph(T2_test_2)
    #print("\n> >> >>> >>>> >>>>> >>>>>> {  M2  } <<<<<< <<<<< <<<< <<< << <")
    #print(M2_test)
    #print(f"M2 length={len(M2)}")


    print(f"\nT2 Test with:\n\t\t{T2_test_1}\n\t\t{T2_test_2}")
    
    M = cartesian_product(M1, M2)
    #print("\n\t> >> >>> >>>> >>>>> >>>>>> {  M = M1 x M2  } <<<<<< <<<<< <<<< <<< << <")
    #print(M)
    #print(f"M length={len(M)}")

    print(f"Length of M1 in T2: {len(M1)}")
    print(f"Length of M2 in T2: {len(M2)}")
    print(f"Length of M Cartesian Product of M1 x M2 : {len(M)}")

    M_initial_state = [initial_state_M1, initial_state_M2]
    M_accepting_state = [accepting_state_M1, accepting_state_M2]
    found = DFS(M, M_initial_state, M_accepting_state)
    check_LD_Q(found, stack)