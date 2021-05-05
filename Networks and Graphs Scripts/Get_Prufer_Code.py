import numpy as np
from collections import OrderedDict 
cont=False
#program loop
while cont==False:

##########################################################
# User Input
    n = input("number of vertices: ")
    try:
        n=int(n)
        cont=True
    except:
        print("Error. Please input an integer.")

cont=False
while cont==False:
    c = np.zeros(n)
    con_c = []
    print('Please type a list of connections (e.g "1,2") seperated by a semicolon.\ne.g\n"1,2;1,3;3,5;2,5"')
    input_string=input("input:")

##########################################################
# String parser
    try:
        input_string=input_string.replace(" ","")
        input_list=input_string.split(";")
        for _input_string in input_list:
            input_vec=_input_string.split(",")
            con_c.append([int(input_vec[0]),int(input_vec[1])])
        for con in con_c:
            if con[0]>n or con[1]>n:
                print("Error. Connections reference vertices larger than the set number of vertices (n).")
                raise Exception()
            elif con[0]<1 or con[1]<1:
                print("Error. Connections reference vertices labelled 0 or less. Please use positive labels for vertices intialising at 1.")
                raise Exception()
        cont=True
    except:
        print("Error parsing connections. Please try entering the connections again.")

#######################################################
# Prufer code algorithm
code=[]
while len(code)!=n-2:
    for i in range(0,n):
        s_i = -1
        for connection in con_c:
            if i+1 in connection:
                if s_i == i+1:
                    s_i = -1
                    break
                else:
                    s_i = i+1
                    if i+1==connection[0]:
                        t_i=connection[1]
                    else:
                        t_i=connection[0]
        if s_i != -1:
            code.append(t_i)
            for connection in reversed(con_c):
                if s_i in connection:
                    con_c.remove(connection)
            break

print("Prufer code is: ",code)
########################################################