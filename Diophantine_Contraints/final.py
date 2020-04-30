

import networkx as nx
DEBUG = 1
TESTING = 1

# CptS350 - Diophantine Constraints Using Labeled Graphs Final Exam Project


class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()  

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost = 0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

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


# This gets you the C_max 
#! ISN'T This always the same?
def C_max(equation):
    pass


def get_K_c(C):
    return len(convert_to_little_endian(C, 0))


def get_b_i(C, i):
    C_bin = convert_to_little_endian(C,0)
    if i > len(C_bin):
        b_i = 0
    else:
        b_i = C_bin[i-1]
    return b_i

# This list should already have the right padding
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


if __name__ == "__main__":
    #Testing only
    if TESTING:
        myTestList = ['1011', '0101', '0001']
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

        print(encoder(myTestList))

    #                1    2     3     4    5     6     7     8    9    10   11   12   13   
    tempEquation = ["+", "C1", "x1", "+", "C2", "x2", "+", "C3", "x3", "+", "C", "=", "0"]

    