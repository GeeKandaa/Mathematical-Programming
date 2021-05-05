import numpy as np
from collections import OrderedDict 
cont=False
#program loop
while cont==False:

##########################################################
# User Input
    prufer = []
    print('Please type a prufer code. Seperate elements by a comma\ne.g\n"5,4,2,3,2,4,8"')
    input_string=input("input:")

##########################################################
# String parser
    try:
        input_string=input_string.replace(" ","")
        input_list=input_string.split(",")
        for _input_string in input_list:
            prufer.append(int(_input_string))
        for ele in prufer:
            if ele>len(prufer)+2:
                print("Error. Connections reference vertices larger than the set number of vertices (n).")
                raise Exception()
            elif ele<1:
                print("Error. Connections reference vertices labelled 0 or less. Please use positive labels for vertices intialising at 1.")
                raise Exception()
        cont=True
    except:
        print("Error parsing connections. Please try entering the connections again.")

#######################################################
# Inverse prufer code algorithm
network=[]
vertices=list(range(1,len(prufer)+3))

network_length=len(prufer)+1
while len(network)!=network_length:
    for i in range(0,len(vertices)):
        if not(vertices[i] in prufer):
            smallest_i=i
            break
        
    conn=[vertices[smallest_i],prufer[0]]
    vertices.remove(vertices[smallest_i])
    prufer.remove(prufer[0])
    network.append(conn)

    if len(prufer)==0:
        if len(vertices)==2:
            conn=[vertices[0],vertices[1]]
            network.append(conn)

print("Network is: ",network)
########################################################