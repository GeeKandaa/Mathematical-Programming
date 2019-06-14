#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
authors: James Lamb, Pawel Manikowski

Coursework 1

Q3 Guitar string simulation
------------------------------
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# inital conditions
L = 1.0             # lenght of the string (m)
d = L/10      
f = 440             # frequency 
c = 2*L*f
h = 0.005           # height of the string (m)


"""------------------------------------------PART A --------------------------------------"""
"""---------------------------------FUNCTION RETURNING ANALYTICAL SOLUTION----------------"""

print("PART A - Analytical solution vs initial condition ")
print("--------------------------------------------------")
"""
function yy(x,t,n) returns the analitycal solution for x<L and for t>0
where x is a vector position and t is time
"""
def yy(x,t,n):
    if x > L or t < 0:
        raise Exception("x must be less or equal L (in our case 1) and t must be more or equal to 0")
    yxt = 0.0
    for i in range(1,n):
        yxt = yxt + (2*h*L**2*math.sin((i*math.pi*d)/L)*math.sin((i*math.pi*x)/L)
        *math.cos((c*i*math.pi*t)/L))/(math.pi**2*i**2*d*(L-d))
    return yxt

""" function init(x) returns the initial condition of f(x) for t=0 """
def init(x):
    initx=0.0
    if x > 0 and x <= d:
        initx = h*x/d
    if x > d  and x <= L:
        initx = ((L-x)*h)/(L-d)
    return initx

print("\nAnalytical solution: ", yy(0.01,0,1000))
print("Initial condition:   ",init(0.01))
#print("\nAnalytical solution: ", yy(0.03,0,1000))
#print("Initial condition:   ",init(0.03))
#print("\nAnalytical solution: ", yy(0.077,0,1000))
#print("Initial condition:   ",init(0.077))
print("\nTheoretical value for x=0.1 and t=0 is 0.005")
print("in our case yxt = 0.004994371073887768") 
print("therefore, the algorithm returns expected value")



"""-----------------------------------------PART B------------------------------------------"""
"""-------------------------------------------PLOT------------------------------------------"""

print("\n\n\nPART B - Plots of analytical solution and initial condition")
print("-----------------------------------------------------------")
f2 = np.vectorize(yy)                    # need to vectorize the function y(x,t,n)
f3 = np.vectorize(init)                 # and init(x)
x1 = np.arange(0.00, 1.01, 0.01)        # x values for analitical analisys and intial condition f(x) from 0 to 1 with step 0.01

plt.figure(1)

plt.subplot(211)
plt.title('Comparing analytical solution with initial condition of f(x)')
plt.plot(x1,f2(x1,0,1000),'b',label='Analytical solution for t=0') # t=0, n =1000
plt.axis([-0.1,1.1,-0.001,0.006])
plt.grid(True)
plt.legend()
plt.ylabel('height h (m)')

plt.subplot(212)
plt.plot(x1,f3(x1),'r',label = 'Initial condition of f(x)')
plt.xlabel('Length of the string L (m)')
plt.ylabel('height h (m)')
plt.axis([-0.1,1.1,-0.001,0.006])
plt.grid(True)
plt.legend()

plt.show()

print("We can see that the two plots match")



"""------------------------------------------PART C--------------------------------------"""
"""----------------FUNCTION THAT IMPLEMENTS THE ALGHORITHM-------------------------------"""

print("\n\n\nPART C - Defining function that implements algorithm (1) ")
print("--------------------------------------------------------")

def Solver_steper(y,i,dx,dt,Nx,c):
    alpha = c*dt/dx
    u = np.zeros(Nx)
    if alpha > 1:
        raise Exception("alpha (c*dt/dx) must be less than 1")
    else:
        for j in range(1,Nx):
            if i == 0:
                u[j] = -y[i,j]+2*(1-alpha**2)*y[i,j]+alpha**2*(y[i,j+1]+y[i,j-1])
            else:
                u[j] =-y[i-1,j]+2*(1-alpha**2)*y[i,j]+alpha**2*(y[i,j+1]+y[i,j-1])
    return u
    
""" ------------------------------------------PART D -----------------------------------"""
""" ---------PREDICTION OF THE MOTION FOR A NUMBER OF STEPS > 1000----------------------"""

print("\n\n\nPART D - Implementation of the algoritm (1)")
print("-------------------------------------------")

nsteps = 1500   # time steps
Nx = 200        # position steps
dx = L/Nx       # dx*Nx must be equal 1
dt = dx/c       # for alpha=1

# defining initial conidition for the array y 
y = np.zeros((nsteps+1,Nx+1)) 
for k in range (1,Nx+1):
    y[0,k] = init(k*dx)

# using the alhorithm to calculate the rest of the array y
for i in range(0,nsteps):
    u = Solver_steper(y,i,dx,dt,Nx,c)
    for k in range (1,Nx):
        y[i+1,k] = u[k]

# printing the array y
print("\nMatrix of the motion of the string for 1500 time steps:\n")        
print(y)

""" ------------------------------------------PART D (CONT)-----------------------------"""
""" ---------COMPUTE AND PLOT THE RESIDUAL AS A FUNCTION OF TIME------------------------"""

print("\nPART D (Cont) - Computation of an error")
r = np.zeros(nsteps)
for i in range(0,nsteps):
    for j in range(0,Nx):
        r[i] = r[i] + (y[i,j]-yy(dx*j, dt*i, 100))**2


print("\nPART D (Cont) - Plot of an error")
x_value = np.arange(0,nsteps,1)
plt.plot(x_value,r[x_value])
plt.title('The residual as a function of time')
plt.grid(True)
plt.ylabel('error')
plt.xlabel('time steps')

plt.show()

""" ------------------------------------------PART E------------------------------------"""
""" ----------------------------------------ANIMATION-----------------------------------"""
# L = 1, dx = 0.005 (reminder)


print("\n\n\nPART E - Animation for the initial condition ilustrating the motion of the string")
print("---------------------------------------------------------------------------------")

fig, ax = plt.subplots()

x = np.arange(0,Nx+1,1)

line, = ax.plot(x/Nx, y[0,x])

plt.title('Motion of the string for initial condition')
plt.axis([-0.1,1.1,-0.006,0.006])
plt.grid(True)
plt.xlabel('length of the string (m)')
plt.ylabel('height (m)')
plt.show()
def animate1(i):
    line.set_ydata(y[0+i,x])
    
ani1 = animation.FuncAnimation(fig, animate1, np.arange(1, 1500),interval=25, blit=False)
    
ani1.save('init_cond.mp4', fps=50)


print("\nPART E (Cont) - Animation for the stationary wave solution ilustrating the mothion of the string ")
print("fn(x) = A*sin(x*pi*n/L) for A = 0.005 and n = 3 ")

n = 3
A = 0.005

# defining the funtion for stationary wave
def stan_wav(i):
    stan_wav = A*np.sin(i*n*np.pi/L)
    return stan_wav

y_stat = np.zeros((nsteps+1,Nx+1)) 

# initial conditions for stationary wave:
for k in range (1,Nx+1):
    y_stat[0,k] = stan_wav(k*dx)
    
# rest of the matrix:
for i in range(0,nsteps):
    u = Solver_steper(y_stat,i,dx,dt,Nx,c)
    for k in range (1,Nx):
        y_stat[i+1,k] = u[k]

# creating animation
fig, ax = plt.subplots()

x = np.arange(0,Nx+1,1)

line, = ax.plot(x/Nx, y_stat[0,x])

plt.title('Motion of the string for stationary wave')
plt.axis([-0.1,1.1,-0.006,0.006])
plt.grid(True)
plt.xlabel('length of the string (m)')
plt.ylabel('height (m)')
plt.show()

def animate2(i):
    line.set_ydata(y_stat[0+i,x])
    
ani2 = animation.FuncAnimation(fig, animate2, np.arange(1, 1500),interval=25, blit=False)
    
ani2.save('stat_wave.mp4', fps=50)

print("\n\nAnimations completed")