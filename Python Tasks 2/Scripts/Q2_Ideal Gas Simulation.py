#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 12:44:46 2018

@authors: James Lamb, Pawel Manikowski
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

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

#L = 1
#V = L**2
#or
V = 2.5     # volume of the box
L = V**0.5  # the length of the square box in each direction



if rank == 0:
    plot_flag = False
else:
    plot_flag = False

list_particles=[]
energy_particles = []

for i in range(N):
    rand_pos = random_position(L)
    rand_v =  np.random.rand(2) # each component of the velocity has a uniform distribution in the interval [0,1]
    list_particles.append(Particle(rand_pos,rand_v))
    #energy
    energy_particles.append((list_particles[i].energy()))

""" ENERGY """
average_energy = sum(energy_particles)/N #average energy per particle per proccess
print("--------------------------Process ",rank,"------------------------------------")
print("Average energy for   ",N," particles is equal to: ", average_energy)    
sum_of_average_energy = comm.reduce(average_energy, op=MPI.SUM)

if rank == 0:
    K = sum_of_average_energy/size
    print("Average energy for   ",size," processes is equal to: ",K)
""" END """

if plot_flag == True:
    res = []
    for i in range(N):
        res.append(np.array(list_particles[i].pos))

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
          
        if plot_flag == True:
            res[k] = np.vstack([res[k],p.pos])

"""---------PRESSURE----------------"""     
forces_fx = sum(fx)/Niter
average_pres = forces_fx/L
print("Average pressure for ",N," particles is equal to: ", average_pres)  
print("------------------------------------------------------------------------------")  
P = comm.reduce(average_pres, op = MPI.SUM)
"""-----------END------------------"""
if rank == 0:

    print("-----------------------------SUMMARY--------------------------------")
    print("Total number of particles (N*size):   ", N*size)
    print("Number of iterations (Niter):         ", Niter)
    print("Time interval (dt):                   ", dt)
    print("Lenght of the side of the square: (L) " ,L)
    print("Volume (L^2):                         ", V)
    print("--------------------------------------------------------------------")
    print("Total average pressure (P)            ", P)
    print("Total average energy: (Ntot*K):       ", K*size*N)
    print("P*V:                                  ", P*V)
    print("--------------------------------------------------------------------")
       
""" END """



if plot_flag == True:
    ### display one trajectory
    pos = res[0]
    plt.plot(pos[:,0],pos[:,1],'k-')
    plt.show()

    
    ###produce an animation 
    fig =plt.figure()
    ax = fig.add_subplot(111, autoscale_on=False, xlim=(0, L), ylim=(0, L))
    ax.grid()


    patch=[]
    for i in range(N):
        patch.append(plt.Circle(res[i][0,:],list_particles[i].radius,fc="r"))
        ax.add_patch(patch[i])

    def animate(i):
        for j in range(N):
            x,y=res[j][i,:]
            patch[j].center= (x,y)
            

    def init():
        line.set_data([], [])
        time_text.set_text('')
        return line, time_text

    ani = animation.FuncAnimation(fig, animate, np.arange(0, Niter),
                                interval=25, blit=False)
    ani.save("gas.mp4",fps=25)
    


