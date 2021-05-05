import numpy as np
from collections import OrderedDict 
cont=False
while cont==False:
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

for i in range(0,n):
    nb=[]
    for connection in con_c:
        if i+1 in connection:
            if i+1==connection[0]:
                nb.append(connection[1])
            else:
                nb.append(connection[0])
    print("i:",i+1,"         nb before: ",nb)
    nb = list(OrderedDict.fromkeys(nb))
    for j in range(0,len(nb)):
        nb[j]=c[nb[j]-1]
    print("neighbourhood of vertex",i+1,"=",nb)
    if min(nb)-1>0:
        c[i]=min(nb)-1
        print("vertex",i+1," has colour group",c[i])
    else:
        res=max(nb)+1
        for num in nb:
            if num+1 in nb:
                continue
            else:
                if num+1<res:
                    res=num+1
        c[i]=res
        print("vertex",i+1," has colour group",c[i])

print("\n The ordered list of colour groups is: ",c)
print("\n The chromatic number is: ", max(c))                   

 