import numpy as np
from numpy import pi, sin, abs, multiply
import matplotlib.pyplot as plt
import math


######## Load data #######
wave_record = np.loadtxt("Islandsberg_Wave_record")
wc1 = np.loadtxt("wcylinder1_4_05")
wc3 = np.loadtxt("wcylinder3_4_05")

''' y = A*sin(Px) + D  --> A = amplitude, P = period, D = vertical shift '''

def sine(x,A,Te):

    if x > 0:
        return [A*sin(Te*x)] + sine(x-1,A,Te)
    else:
        return []


Te = 6.25 # average wave period weighted by energy in the spectrum
A = multiply(wave_record.tolist(),0.01) # amplitude for incoming waves [m]
A_abs = [abs(i) for i in A]  #Abs values for amplitudes
H = multiply(A_abs,2)  #significant wave height

#### All Wave Amplitudes ####
x_all = 1000
x_list = [i+1 for i in range(x_all)]  #list 1-x for plot
y_all = sine(x_all, A, Te)

plt.plot(x_list,y_all)
plt.title('Sinusoidal Wave Representation - All Amplitudes')
plt.xlabel('Time [s]')
plt.ylabel('Amplitudes')
plt.show()



######### Highest Wave Amplitude Sinusoidal #########
x_max = 1000
x_list = [i+1 for i in range(x_max)]  #list 1-x for plot

A_max = max(A_abs)
y_max = sine(x_max, A_max, Te)


######### Lowest Wave Period Sinusoidal ########
x_min = 1000
#x_list = [i+1 for i in range(x_min)]  #list 1-x for plot

A_min = min([a for a in A_abs if a > 1.5])  #Amplitude of waves for H > 3
y_min = sine(x_min, A_min, Te)


plt.plot(x_list,y_max,'b')
plt.plot(x_list,y_min,'r')
plt.title('Sinusoidal Wave Representation - Power Generating Amplitudes')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude [m]')
plt.grid(True)
plt.show()


#### Signifcant Wave Amplitudes ####

Sig = [a for a in A_abs if a > 0.5]  #Significant wave amplitudes                    XXXXX   A = 0.5???

Per = (len(Sig)/len(A))*100
print(f'Percentage of Power Generating Waves:{round(Per,3)}%')







