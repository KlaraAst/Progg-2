import numpy as np
from numpy import pi, sin, cos, linspace, zeros
import matplotlib.pyplot as plt
import math
from math import sqrt

'''
y = A*sin(wt)

w = 2pi*f = 2pi/T

'''

#%%

t = 4 # s
t_list = linspace(0,t,100) #array 1 --> x for plot


########### Scenario 1 ###########

T1 = 1.3 # average wave period
A1 = 0.07 # amplitude for incoming waves [m]
w1 = 2*pi/T1

y1 = []

for i in t_list:
    y1.append(A1*sin(w1*i))


plt.plot(t_list,y1, 'b')
plt.plot(t_list, zeros(len(t_list)), 'black', linestyle='dashed')
plt.title('Sinusoidal Wave Representation - Scenario 1')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude [m]')
#plt.show()



########### Scenario 2 ###########

T2 = 1 # average wave period
A2 = 0.14 # amplitude for incoming waves [m]
w2 = 2*pi/T2

y2 = []

for i in t_list:
    y2.append(A2*sin(w2*i))


plt.plot(t_list,y2, 'r')
#plt.plot(x_list, zeros(len(x_list)), 'black', linestyle='dashed')
plt.title('Sinusoidal Wave Representation - Scenario 1 and 2')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude [m]')
plt.show()


#%%

######### Surface Elevation ##########


def n_time(t,x,A,T,w):

    H = 2*A #average height of the highest 1/3 of all waves
    'Shallow water'
    wave_length = T * sqrt(9.81 * 0.35)  #waterdepth = 0.35 m
    k = 2*pi / wave_length

    n_tx_time = [(H/2)*cos(k*x-w*i) for i in t]

    return n_tx_time


def n_dist(t,x,A,T,w):

    H = 2*A
    wave_length = T * sqrt(9.81 * 0.35)  #waterdepth = 0.35 m
    k = 2*pi / wave_length

    n_tx_dist = [(H/2)*cos(k*i-w*t) for i in x]

    return n_tx_dist



#### Scenarios, distance traveled ####
x1 = 1.80/T1 # [m/s] 180 cm per period
x1_list = linspace(0,5,100) # m/s * s

x2 = 1.00/T2 # [m/s]
x2_list = linspace(0,5,100)


Sf_t_1 = n_time(t_list,x1,A1,T1,w1)
Sf_t_2 = n_time(t_list,x2,A2,T2,w2)

Sf_x_1 = n_dist(t,x1_list,A1,T1,w1)
Sf_x_2 = n_dist(t,x2_list,A2,T2,w2)


####### Scenario 1 ########

plt.plot(t_list,Sf_t_1, 'g')
#plt.plot(x_list, zeros(len(x_list)), 'black', linestyle='dashed')
plt.title('Surface Elevation over Time - Scenario 1 and 2')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude [m]')
#plt.show()

plt.plot(t_list,Sf_t_2, 'magenta')
#plt.title('Surface Elevation over Time - Scenario 2')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude [m]')
plt.show()



####### Scenario 2 ########

plt.plot(x1_list,Sf_x_1, 'g')
#plt.plot(x_list, zeros(len(x_list)), 'black', linestyle='dashed')
plt.title('Surface Elevation over Distance - Scenario 1 and 2')
plt.xlabel('Distance [m]')
plt.ylabel('Amplitude [m]')

plt.plot(x2_list,Sf_x_2, 'magenta')
#lt.title('Surface Elevation over Distance - Scenario 2')
plt.xlabel('Distance [m]')
plt.ylabel('Amplitude [m]')
plt.show()





