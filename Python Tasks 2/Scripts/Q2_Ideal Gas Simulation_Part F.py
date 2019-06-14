#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 12:44:46 2018

@authors: James Lamb, Pawel Manikowski
"""

import numpy as np
from matplotlib import pyplot as plt

def random_position(L):
        return L * np.random.rand(2) 

class Particle(object):
        pos = np.array([0,0])
        vel = np.array([0,0])
        mass=1 
        radius = 0.01

        # The class "constructor" 
        def __init__(self, pos, vel):
            self.pos = pos
            self.vel = vel
           
        def energy(self):
            self.energy = 0.5*self.mass*np.sum(self.vel**2)
            return(self.energy)

        def evolve(self,dt):
            self.pos = self.pos + self.vel * dt
            self.vel = self.vel

        def flip_vx(self):
            self.vel[0] = -self.vel[0]

        def flip_vy(self):
            self.vel[1] = -self.vel[1]
        
        def info(self):
            print("position:",self.pos,"  velocity: ",self.vel)
            
from mpi4py import MPI 
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

m=1
N = 100 # number of particles
Niter = 10000
dt = 0.01
steps = 50

y_pv = []
y_kn = []
x_vol = []

for ww in range(steps):
    V = ww*0.5+0.5     # volume of the box
    L = V**0.5         # the length of the square box in each direction
    list_particles=[]
    energy_particles = []

    for i in range(N):
        rand_pos = random_position(L)
        rand_v =  np.random.rand(2) # each component of the velocity has a uniform distribution in the interval [0,1]
        list_particles.append(Particle(rand_pos,rand_v))
        energy_particles.append((list_particles[i].energy()))

    average_energy = sum(energy_particles)/N #average energy per particle per proccess
    sum_of_average_energy = comm.reduce(average_energy, op=MPI.SUM)

    if rank == 0:
        K = sum_of_average_energy/size
    
    fx = []

    for i in range(Niter):
    
        for k in range(N):
            p = list_particles[k]
     
            p.evolve(dt)
        
            # if the particle is starting to enter the border of the box, flip the appropriate component of its velocity.
            if p.pos[0] >= L:
                fx.append(2*m*p.vel[0]/dt) # calculating the force 
                p.flip_vx()
                p.pos = np.array([L,p.pos[1]])
            
            if p.pos[1] >= L:
                p.flip_vy()
                p.pos = np.array([p.pos[0],L])
          
            if p.pos[0] <= 0:
                p.flip_vx()
                p.pos = np.array([0,p.pos[1]])
           
            if p.pos[1] <= 0:
                p.flip_vy()
                p.pos = np.array([p.pos[0],0])
       
    forces_fx = sum(fx)/Niter
    average_pres = forces_fx/L
    P = comm.reduce(average_pres, op = MPI.SUM)
    
    if rank == 0:
        y_pv.append(P*V)
        y_kn.append(K*size*N)
        x_vol.append(V)
        print("----------------------SUMMARY-----------------------")
        print("Total number of particles:        ", N*size)
        print("Number of iterations:             ", Niter)
        print("Time interval (dt):               ", dt)
        print("Lenght of the side of the square: " ,L)
        print("Volume (L^2):                     ", L**2)
        print("----------------------------------------------------")
        print("Total average pressure (P)        ", P)
        print("Total average energy: (Ntot*K):   ", K*size*N)
        print("P*V:                              ", P*V)
        print("----------------------------------------------------")
    
    
    
    
# plot
if rank == 0:
    plt.title('Plot of P*V and Ntot*K')
    plt.plot(x_vol,y_pv,'b-',label='P*V')
    plt.plot(x_vol,y_kn,'r-',label='Ntot*K')
    plt.xlabel('Volume')
    plt.grid()
    plt.ylim(0,300)
    plt.legend()
    plt.show()




