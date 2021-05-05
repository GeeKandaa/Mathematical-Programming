import numpy as np
from collections import OrderedDict 
cont=False
#program loop
while cont==False:

##########################################################
# User Input
    con_c = []
    print('Please type a weighted list of connections (e.g "(1,2),4;") seperated by a semicolon.\ne.g\n"(1,2),4;(1,3),1;(2,3),5;(2,4),4"')
    input_string=input("input:")

##########################################################
# String parser
    try:
        input_string=input_string.replace(" ","")
        input_list=input_string.split(";")
        for _input_string in input_list:
            _input_string=_input_string.replace("(","").replace(")","")
            input_vec = _input_string.split(",")
            con_c.append([int(input_vec[0]),int(input_vec[1]),int(input_vec[2])])

        cont=True
    except:
        print("Error parsing connections. Please try entering the connections again.")

def find_cycle(network):
    # sorted_network = sorted(network, key=lambda x: (x[0], x[1]))
    starts=[]
    ends=[]
    for edge in connected_network:
        if not(edge[0] in ends and edge[1] in ends) and not(edge[0] in starts and edge[1] in starts):
            starts.append(edge[0])
            ends.append(edge[1])
        else:
            return True
    return False
#######################################################
# Prufer code algorithm
con_c= sorted(con_c, key=lambda x: (x[2]))
connected_network=[]
for edge in con_c:
    connected_network.append(edge)
    if find_cycle(connected_network):
        del connected_network[-1]
for ele in connected_network:
    del ele[-1]
print("Minimum spanning tree is: ", connected_network)
########################################################

