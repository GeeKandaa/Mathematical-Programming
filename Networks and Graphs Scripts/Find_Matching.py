import numpy as np
from collections import OrderedDict 

class edge(object):
    def __init__(self, start, end, capacity):
        self.start=start
        self.end=end
        self.capacity=capacity
        self.flow=0

class network(object):
    def __init__(self, vertices_n):
        self.connections = [[] for i in range(vertices_n+1)]


    def append_Edge(self, start, end, capacity):
        if start == end:
            print("Looped vertex present in list. Cannot proceed")
            raise ValueError("Ensure no vertex connects to itself in graph.")
        edge_forward = edge(start, end, capacity)
        edge_backward = edge(end, start, 0)
        edge_forward.edge_backward = edge_backward
        edge_backward.edge_backward = edge_forward
        self.connections[start].append(edge_forward)
        self.connections[end].append(edge_backward)


    def find_Route(self, start, end_target, route):
        if start == end_target:
            return route
        for connection in self.connections[start]:
            residual = connection.capacity - connection.flow
            if residual > 0 and not ([connection,residual] in route):
                route += [[connection,residual]]
                res = self.find_Route(connection.end, end_target, route)
                if res != None:
                    return res
        
    def find_matching(self, start, end):
        route = self.find_Route(start, end, [])
        while route!=None:
            flow=min(residual for _edge, residual in route)
            for _edge, residual in route:
                _edge.flow += flow
                _edge.edge_backward.flow -= flow
            route=self.find_Route(start, end, [])
        sum=0
        for layer in self.connections:
            for _edge in layer:
                sum+=_edge.flow
        return self.connections

##########################################################
#input loop
cont=False
while cont==False:

##########################################################
# User Input
    con_c = []
    print('Please type a list of connections (e.g "1,2") seperated by a semicolon.\ne.g\n"1,5;1,6;1,7;2,5;3,6;3,8;4,7;4,8"')
    input_string=input("input:")

##########################################################
# String parser
    try:
        input_string=input_string.replace(" ","")
        input_list=input_string.split(";")
        for _input_string in input_list:
            input_vec = _input_string.split(",")
            con_c.append([int(input_vec[0]),int(input_vec[1])])

        cont=True
    except:
        print("Error parsing connections. Please try entering the connections again.")

##########################################################
# Define parts, create directed edges list
v1=[]
v2=[]
directed_connections=[]
for vertex in con_c:
    if vertex[1] in v1 or vertex[0] in v2:
        vertex[0],vertex[1]=vertex[1],vertex[0]
    if vertex[1] in v1 or vertex[0] in v2:
        print("Ill defined graph. Cannot split into distinct parts")
        raise ValueError ("Ensure graph is bipartite.")
    v1.append(vertex[0])
    v2.append(vertex[1])
    directed_connections.append([vertex[0],vertex[1]])
v1=list(dict.fromkeys(v1))
v2=list(dict.fromkeys(v2))
print("v1=",v1)
print("v2=",v2)
# Set up network
sink = max(max(v1),max(v2))+1
net = network(sink)
for v in v1:
    net.append_Edge(0,v,1)
for connected in directed_connections:
    net.append_Edge(connected[0],connected[1], 1)
for v in v2:
    net.append_Edge(v,sink,1)

# F-F Algorithm
res=net.find_matching(0,sink)

# parse results to find matching
res = [results for results in res if len(results)!=0]
result=[]
for i in range(len(res)):
    result += [results for results in res[i] if results.flow == 1]
result=[results for results in result if results.start in v1 and results.end in v2]
res=""
for i in range(len(result)):
    if i == 0:
        res+=" ("+str(result[i].start)+","+str(result[i].end)+")"
    else:
        res+=",("+str(result[i].start)+","+str(result[i].end)+")"
print("Matching found to be: "+res)


