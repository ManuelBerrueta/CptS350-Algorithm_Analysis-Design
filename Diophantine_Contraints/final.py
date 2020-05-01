

import networkx as nx
DEBUG = 1
TESTING = 0
ALGO_TEST = 1

# CptS350 - Diophantine Constraints Using Labeled Graphs Final Exam Project


class Vertex:
    def __init__(self, node, payload):
        self.id = node
        self.payload = payload
        self.adjacent = {}

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def add_neighbor(self, neighbor, weight=0): #Here weight will be our a1, a2, a3
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()  

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def get_payload(self):
        return self.payload


class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node, payload):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node, payload)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, symbol):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], symbol)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], symbol)

    def get_vertices(self):
        return self.vert_dict.keys()


# This function converts an integer to binary in string format
# The inputs are: num an integer
#                 padding is the number of zeros infront of the conversion
# The output is a string representation of the number ie 5 = '101'
def num_to_bin(num, padding):
    tempNum = "{0:b}".format(num)
    if len(tempNum) < padding:
        binNum = ('0' * (padding - len(tempNum))) + tempNum
        return binNum
    else:
        binNum = tempNum
        return binNum


# Given a list of strings representing binary numbers
# This function will add padding based on the longest len binary number
def padding_per_max_len(str_bin_list, pad):
    pad_max_len = max(str_bin_list, key=len)
    #for eachBinStr in str_bin_list:
    #    if len(eachBinStr) > pad_max_len:
    #        pad_max_len = len(eachBinStr)
    newPaddedList = []
    for eachBinStr in str_bin_list:
        if len(eachBinStr) < pad_max_len:
            newPaddedList.append(eachBinStr + ('0' * (pad_max_len - len(eachBinStr))))
        else:
            newPaddedList.append(eachBinStr)
    
    return newPaddedList
        

def convert_to_little_endian(num, offset):
    temp_bin_num = num_to_bin(num, offset)
    return "".join(reversed(temp_bin_num))


def test_conversion(num, offset):
    print(str(num)  + " is " + num_to_bin(18,6) + " in binary big endian!\n")
    print(str(num)  + " is " + convert_to_little_endian(18, 6) + " in binary little endian!\n")


# Split the equation first
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

    
#                      1    2     3     4    5     6     7     8    9    10   11   12   13   
#    tempEquation = ["+", "C1", "x1", "+", "C2", "x2", "+", "C3", "x3", "+", "C", "=", "0"]

def C_max(equation):
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



def get_K_c(C):
    return len(convert_to_little_endian(C, 0))


def get_b_i(C, i):
    C_bin = convert_to_little_endian(C,0)
    if i > len(C_bin):                      #NOTE:  I think this is K_c+1 scenario
        b_i = 0
    else:
        b_i = C_bin[i-1]
    return b_i

# This list should already have the right padding
# This takes the list with the numbers and picks the first bit out of each one
def encoder(b_list):
    #Find the longest length
    #pad_max_len = max(b_list, key=len)
    newb_list = ['']  * len((b_list[0]))
    """ pad_max_len = len((b_list[0]))
    newb_list = [None]  * len(b_list)
    a1 = ''
    a2 = ''
    a3 = ''

    for i in range(pad_max_len):
        a1 = a1 + b_list[0][i]    
        a2 = a2 + b_list[1][i]    
        a3 = a3 + b_list[2][i]        

    newb_list.append(a1)
    newb_list.append(a2)
    newb_list.append(a3) """
    for eachItem in b_list:
        tempStr = ''
        for i, each_b in enumerate(eachItem):
            #tempStr.join(each_b)
            newb_list[i] = newb_list[i] + each_b
    return newb_list


def decoder(b_list):
    tempBin = ''
    result_List = []
    for each in b_list:
        tempBin = ''.join(reversed(each))
        result_List.append(int(tempBin, 2))
    return result_List

#NOTE: A state in M is a pair of values [carry, i] where:
#           -C_max <=  carry  <= C_max   and
#           1 <=  i  <= K_c + 1

def build_graph(input, equation):
    carry = 0
    i = 1
    C,x = split_equation(equation)
    K_c = get_K_c(C[3]) # K_c of C the constant
    initial_state = [carry, i]
    accepting_state = [0, (K_c + 1)]
    state = initial_state
    R=0
    state_id = {}
    G = Graph()
    #state_id[0] = initial_state
    #state_id[1] = accepting_state
    #G.add_vertex({0:initial_state})
    
    G.add_vertex(0, initial_state)
    G.add_vertex(1, accepting_state)
    last_state_id = 0

    last_index = 0

    for index, a in enumerate(input):
        carry = state[0]
        i = state[1]
        R = (C[0] * int(a[0])) + (C[1] * int(a[1])) + (C[2] * int(a[2])) + int(get_b_i(C[3], i)) + carry

        curent_state_id = index + 2

        # if R is divisible by 2
        if (R % 2) == 0:
            # and carry = R/2        
            if (R % 2) == 0:         #TODO: Check to make sure this is what he is asking
                carry_prime = R / 2
            
            if i >= 1 and i <= K_c:
                i_prime = i + 1
            else:
                i_prime = i
            
            next_state = [carry_prime, i_prime]
            
            
            #If this input symbol met all the requirements then we can add it to the graph
            #NOTE: Add  this next_state as a vertex/node and the carry' and i'
            G.add_vertex(curent_state_id, next_state)
            #TODO: modify cost to be the string
            G.add_edge(last_state_id, curent_state_id, a)
            # Update our state
            state = next_state
            last_state_id = index + 2
            
        #last_index = index
    return G


def input_gen(max, padding):
    input_list = []
    for i in range(max):
        input_list.append(convert_to_little_endian(i, padding))

    return input_list


if __name__ == "__main__":
    #Testing only
    if TESTING:
        myTestList = ['101', '011', '100', '110']
        resultList = []
        test_conversion(18,6)
        print(f"Testing with number 18: bin={num_to_bin(18,0)} | Little Endian={convert_to_little_endian(18,0)}")
        print(f"Testing: Kc={get_K_c(18)} | b_i(18,6)={get_b_i(18,6)} and b_i(18,4)={get_b_i(18,4)}")
        C_34 = convert_to_little_endian(34,0)
        print(f"Testing b_i with C=34: ", end='')
        #for i,b in enumerate(C_34):
        #    print(f"b_{i+1}={b} | ", end='')
        for i in range(len(C_34)):
            print(f"b_{i+1}={get_b_i(34,i+1)} | ", end='')

        print("\n")
        print(convert_to_little_endian(13,5)) #This will work, but I need the padding before hand

        resultList = encoder(myTestList)
        print(resultList)
        result_intList = decoder(resultList)
        print(result_intList)

    if ALGO_TEST:
        test_equation = ["-", "3", "x1", "-", "0", "x2", "+", "4", "x3", "+", "17", "=", "0"]
        my_Cmax = C_max(test_equation)
        print(my_Cmax) # = 5

        #Generate input list
        input_list = input_gen(8,3)
        G = build_graph(input_list, test_equation)
        print(f"G.getpayload of 0, initial_state = {G.get_vertex(0).get_payload()}")

        T1_test_1 = ["+", "3", "x1", "-", "2", "x2", "+", "1", "x3", "+", "5", "=", "0"]
        T1_test_2 = ["+", "6", "x1", "-", "4", "x2", "+", "2", "x3", "+", "9", "=", "0"]

        M1 = build_graph(input_list, T1_test_1)
        M2 = build_graph(input_list, T1_test_2)

        #M = cartesian_product(M1, M2)

        T2_test_1 = ["+", "3", "x1", "-", "2", "x2", "-", "1", "x3", "+", "3", "=", "0"]
        T2_test_2 = ["+", "6", "x1", "-", "4", "x2", "+", "1", "x3", "+", "3", "=", "0"]

        M1 = build_graph(input_list, T2_test_1)
        M2 = build_graph(input_list, T2_test_2)
        #M = cartesian_product(M1, M2)
        


    #                1    2     3     4    5     6     7     8    9    10   11   12   13   
    templateEquation = ["+", "C1", "x1", "+", "C2", "x2", "+", "C3", "x3", "+", "C", "=", "0"]

    