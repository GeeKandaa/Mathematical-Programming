#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 14:26:00 2018

@author: James Lamb, Pawel Manikowski
"""

import numpy as np
from mpi4py import MPI 


# function returning a random vector of length n
def random_vector(n):
    return np.random.random(n)
    
# function returning random square matrix of size nxn
def random_square_matrix(n):
    return np.random.random((n,n))

# generating 4x4 matrix (n=4) and 4- dimensional vector
n = 4
v_vector = random_vector(n)
A_matrix = random_square_matrix(n)

# function returning a list (l) of blocks 2x2 matrices 
def blocks_of_matrix():
    b0 = A_matrix[0:2,0:2]
    b1 = A_matrix[0:2,2:4]
    b2 = A_matrix[2:4,0:2]
    b3 = A_matrix[2:4,2:4]
    l = [b0,b1,b2,b3]
    return l

# function returning a list (l) of four two dimensioncal vectors (x,y)
def blocks_of_vector():
    x = v_vector[0:2]
    y = v_vector[2:4]
    l = [x, y, x, y]
    return l

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# there will be 4 proccesses. Therefore, size = 4
if size !=4:
    exit(1)

# displaying the original matrix and vector for comparison/verification
if rank == 0:
    print("original matrix on process 0: ", blocks_of_matrix())
    print("original vector on process 0: ", blocks_of_vector())
    
# scattering matrices blocks to each proccess    
mat_loc=comm.scatter(blocks_of_matrix(),root=0)

# scattering vectors to each proccess
vec_loc=comm.scatter(blocks_of_vector(),root=0)

# multiplying a 2x2 matrix with 2 dimensional vector for each proccess
u = mat_loc.dot(vec_loc)

# printing the output for each proccess
print("--------------------------------------------------")
print("process #",rank," matrix [b",rank,"]: ",mat_loc) 
print("process #",rank," has vector =",vec_loc) 
print("process #",rank," multiplication of matrix and vector: ",u) 
print("--------------------------------------------------")

# gathering u1,...,u4 in one array from each proccess
suma = comm.gather(u,root=0)

# comparing/displaying the expected and calculated value of the matrix 
if rank == 0:
    print("-------------------------------------------------------------")
    print("EXPECTED VALUE OF MATRIX AND VECTOR MULTIPLICATION: ", A_matrix.dot(v_vector))
    print("CALCULATED MATRIX: ", np.concatenate((suma[0]+suma[1],suma[2]+suma[3])))
    print("-------------------------------------------------------------")
    
    

      