import numpy as np
import random

from mpi4py import MPI

def merge(v1,v2):
    i=j=k=0 # Counters: integer
    n1 = len(v1) #Number of elements in parameter n1: integer
    n2 = len(v2) #Number of elements in parameter n2: integer
    result = np.zeros(n1+n2,dtype=int) # container array (n1+n2 x 1), elements are all zero and of integer type. Used to store sorted array for return value
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
    result = np.concatenate((v1,v2)) # Array containing unsorted values of v1 and v2 for sorting in next line of code. Array is size ((len(v1)+len(v2)) x 1) and contains type equal to v1, v2. Considering use in this code, type would be integer.
    result.sort()
    return result

start = MPI.Wtime() # Program starting time: floating point number.
comm = MPI.COMM_WORLD # MPI communicator
rank = comm.Get_rank() # Rank of process: integer
size = comm.Get_size() # Number of processes: integer
status = MPI.Status() # Structure representing status of a recieved message
   
### parameters
Nmax = int(1e7) # An integer, for use in random array generation, represents the maximum of the range of randomly generated numbers.
Nel  = int(1e6) # An integer, total number of elements to be generated in random array.
debug=True # A boolean, used to trigger testing of parallelised sorted array values with serial sorted array values and trigger printing of result.
merge_flag = 1 # 0: using for loops; 1: using numpy built-in; 


if Nel%size !=0:
    print("The  number of elements of the original vector is not a multiple of size! Exiting!")
    exit(1)

# generate array of random integers:
v = np.random.randint(Nmax, size=Nel) # A (Nel x 1) sized numpy array (In this case, (1000000 x 1)), integer elements are of value, x, where, 0 < x < Nmax (in this case x = [0,10000000]) 
u = np.zeros(int(Nel/size),dtype=int) # A integer numpy array of size (floor(Nel/size) x 1) (in this case with 4 parallel processes running: (250000 x 1)) of which each element is 0 .


if rank==0:
    print("total size:",Nel," int or ",v.nbytes/1e6," Mbytes")
    print("local size :", Nel/size,"int or ",u.nbytes/1e6," Mbytes")
 
 
# scatter the original vector accros the communicator.
comm.Scatter(v,u)
end_setting_up = MPI.Wtime()

u1 = np.sort(u) # numpy implementation of the quicksort. (not in-place! )
end_local_sort  = MPI.Wtime()

# Now perform the tree merge.
step = 1
while step<size:
    
    if rank%(2*step)==0:
        if rank+step<size:
            print("rank:",rank,"receiving from ",rank+step,"step=",step,"of length",len(u)*step)
            u2 = np.zeros(len(u)*step,dtype=int) # Container array, used to contain u1 of "neighboured" process for merge function, array type: integer
            comm.Recv(u2, source = rank+step)
            if merge_flag==0:
                u1=merge(u1,u2)
            if merge_flag==1:
                u1 = merge_alt(u1,u2)
         
    else:
        neighbor =  rank-step #Rank number of closest prior process containing relevant u1 array. Integer
        if rank >0 and rank%step == 0:
            print("rank:",rank,"sending to ",neighbor,"step=",step,"of length",len(u1))
            comm.Send(u1, dest=neighbor)

    step = 2*step
   
end = MPI.Wtime()

# print final timings
if rank ==0:
    print("total time :",end-start)
    print("time setting up (include generate random array and scatter it) :",end_setting_up-start)
    print("time local sort :",end_local_sort-end_setting_up)
    print("time to merge arrays using a tree-merge :",end-end_local_sort)

    if debug==True:
        if np.array_equal( u1,  np.sort(v)):
            print("Sorting correct!")

