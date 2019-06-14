#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 12:40:58 2019

@author: jlamb
"""

import numpy as np

from mpi4py import MPI

def merge(v1,v2):
    i=j=k=0 # Counters: integer
    n1 = len(v1) #Number of elements in parameter n1: integer
    n2 = len(v2) #Number of elements in parameter n2: integer
    result = np.zeros(n1+n2,dtype=int) # container array (n1+n2 x 1), elements are all zero and$
    while i< n1 and j < n2:
        if v1[i]  < v2[j]:
            result[k] = v1[i]
            i+=1
            k+=1
        else  :
            result[k] = v2[j]
            j+=1
            k+=1

    if i==n1:
        result[k:]=v2[j:]

    if j==n2:
        result[k:]=v1[i:]

    return result


def merge_alt(v1,v2):
    result = np.concatenate((v1,v2))
    result.sort()
    return result

start = MPI.Wtime()
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
status = MPI.Status()


### parameters
Nmax = int(1e7)
Nel  = int(1e6*1.25)

debug=True
merge_flag = 0 # 0: using for loops; 1: using numpy built-in;

if Nel%size !=0:
    print("The  number of elements of the original vector is not a multiple of size! Exiting!")
    exit(1)

# generate array of random integers:
u = np.random.randint(Nmax, size=int(Nel/size))
v = np.zeros(Nel, dtype = int)
if rank==0:
    print("total size:",Nel," int or ",v.nbytes/1e6," Mbytes")
    print("local size:",Nel/size," int or ",u.nbytes/1e6," Mbytes")
end_setting_up = MPI.Wtime()

u1 = np.sort(u) # numpy implementation of the quicksort. (not in-place!)

end_local_sort  = MPI.Wtime()

comm.Gather(u1, v)

if rank == 0:
    if merge_flag == 0:
        sor = np.zeros([size, int(Nel/size)], dtype=int)
        b = int(len(v)/size)
        for i in range(size):
            sor[i] = v[b*i:b*(i+1)]

        sortTimeStart = MPI.Wtime()

        k = 2
        while size*2/k != 1:
            sor2 = np.zeros([int(size/k), int(Nel/size*k)], dtype = int)
            for i in range(0, int(size*2/k), 2):
                sor2[int(i/2)] = merge(sor[i],sor[i+1])
            sor = sor2
            k *= 2
    

    end = MPI.Wtime()
    print("--------------------------------")
    print("total time :",end-start)
    print("--------------------------------")
    print("setting up time :",end_setting_up-start)
    print("local sorting time :",end_local_sort-end_setting_up)
    print("Sorted Vector :",sor[0])
    print("Merge Time : ",end-sortTimeStart)


    if debug==True:
        if np.array_equal(sor[0],  np.sort(v)):
            print("Sorting correct!")