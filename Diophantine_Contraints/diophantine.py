
DEBUG = 1
TESTING = 0
ALGO_TEST = 1
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

#! Algorithm 1
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

    return M

def cartesian_product(M1, M2):
    M = []
    for each_conn_M1 in M1:
        for each_conn_M2 in M2:
            # if they have the same common edge, they are reading the same symbol
            if each_conn_M1[4] == each_conn_M2[4]:
                a = each_conn_M1[4] #We could pick each_conn_M2[4] since is the same thing
                M.append( [ [each_conn_M1[0], each_conn_M1[1]], [each_conn_M1[2], each_conn_M1[3]], [each_conn_M2[0], each_conn_M2[1]], [each_conn_M2[2], each_conn_M2[3]], a ])
    return M


if __name__ == "__main__":
    T1_test_1 = ["+", "3", "x1", "-", "2", "x2", "+", "1", "x3", "+", "5", "=", "0"]
    T1_test_2 = ["+", "6", "x1", "-", "4", "x2", "+", "2", "x3", "+", "9", "=", "0"]

    M1_test = build_graph(T1_test_1)
    #print("\n> >> >>> >>>> >>>>> >>>>>> {  M1  } <<<<<< <<<<< <<<< <<< << <")
    #print(M1_test)
    M2_test = build_graph(T1_test_2)
    #print("\n> >> >>> >>>> >>>>> >>>>>> {  M2  } <<<<<< <<<<< <<<< <<< << <")
    #print(M2_test)
    #M = cartesian_product(M1_test, M2_test, input_list)
    M_test = cartesian_product(M1_test, M2_test)
    with open("M__test_output.txt", "w") as outfile:
        outfile.write(str(M_test))


    T2_test_1 = ["+", "3", "x1", "-", "2", "x2", "-", "1", "x3", "+", "3", "=", "0"]
    T2_test_2 = ["+", "6", "x1", "-", "4", "x2", "+", "1", "x3", "+", "3", "=", "0"]

    M1 = build_graph(T2_test_1)
    print("\n> >> >>> >>>> >>>>> >>>>>> {  M1  } <<<<<< <<<<< <<<< <<< << <")
    print(M1_test)
    M2 = build_graph(T2_test_2)
    print("\n> >> >>> >>>> >>>>> >>>>>> {  M2  } <<<<<< <<<<< <<<< <<< << <")
    print(M2_test)

    M = cartesian_product(M1, M2)

    print("\n\t> >> >>> >>>> >>>>> >>>>>> {  M = M1 x M2  } <<<<<< <<<<< <<<< <<< << <")
    print(M)

    with open("M_output.txt", "w") as outfile:
        outfile.write(str(M))




# Each entry in M1,M2 is [carry, i, carry_prime, i_prime, a1, a2, a3]

