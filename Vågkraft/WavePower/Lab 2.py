import numpy as np
from numpy import sqrt, pi, log, exp
import math
import pandas as pd
import matplotlib.pyplot as plt

'''
Carry out a simple decay test:
  - analyse the decay time, buoyancy and draft and the physics behind it qualitatively
  - compute the natural frequency quantitatively
  - By computing the RAO, you will compare the response of the system for different sea states using focused waves 
'''



#Reading xlsx-file and converting to DataFrame object
W1 = pd.DataFrame(pd.read_excel("S5_FW-1.xlsx"))
W2 = pd.DataFrame(pd.read_excel("S6_FW-1.xlsx"))
W3 = pd.DataFrame(pd.read_excel("S8_FW-1.xlsx"))
W4 = pd.DataFrame(pd.read_excel("S9_FW-1.xlsx"))
W5 = pd.DataFrame(pd.read_excel("S10_FW-1.xlsx"))


############### Plotting ##################

w1_heave = W1['HeaveBuoyPosition'].tolist()
w1_elev = W1['SurfaceElevation'].tolist()

w2_heave = W2['HeaveBuoyPosition'].tolist()
w2_elev = W2['SurfaceElevation'].tolist()

w3_heave = W3['HeaveBuoyPosition'].tolist()
w3_elev = W3['SurfaceElevation'].tolist()

w4_heave = W4['HeaveBuoyPosition'].tolist()
w4_elev = W4['SurfaceElevation'].tolist()

w5_heave = W5['HeaveBuoyPosition'].tolist()
w5_elev = W5['SurfaceElevation'].tolist()



heave_lists = [w1_heave,w2_heave,w3_heave,w4_heave,w5_heave]
elev_lists = [w1_elev,w2_elev,w3_elev,w4_elev,w5_elev]


####### Replace NaN with 0 ########

counter = 0
time_steps = [i for i in range(len(w1_heave))] #discrete time steps

#### Elevation ####
for l in elev_lists:
    for i in range(len(l)):
        if math.isnan(l[i]):   #replacing NaN values with 0
            l[i] = 0

#### Heave ####
for h in heave_lists:
    for i in range(len(h)):
        if math.isnan(h[i]):   #replacing NaN values with 0
            h[i] = 0




plt.plot(time_steps,w1_elev)
plt.xlabel('Dicrete Time Steps')
plt.ylabel('Wave Elevation')
plt.grid(True)
#plt.show()


plt.plot(time_steps[6000:15000],w1_elev[6000:15000],'r')
plt.title('Zoomed in Surface elevation')
plt.xlabel('Discrete Time Steps')
plt.ylabel('Wave Elevation')
plt.grid(True)
plt.show()


plt.plot(time_steps[6000:15000],w1_heave[6000:15000],'g')
plt.title('Zoomed in Heave Position')
plt.xlabel('Discrete Time Steps')
plt.ylabel('Heave Buoy Position')
plt.grid(True)
plt.show()




###################### RAO ######################

RAO = []
Tp = [1.64, 2.1, 2.56, 3.20, 4.29]

for i in range(5):
    h_max = np.max(heave_lists[i])
    e_max = np.max(elev_lists[i])
    RAO.append(h_max/e_max)


plt.plot(Tp,RAO,'b')
plt.title('Response Amplitude Operator over Periods')
plt.ylabel('RAO')
plt.xlabel('Period')
plt.grid(True)
plt.show()



#%%


def vibration_rate(m,t1,t2,x1,x2):

    scale = 30  #lambda
    td = t2 - t1  # period of damped vibration

    wd = 2*pi/(td)   #damped angular frequency
    log_dec = log(x1/x2)  # logaritmic decrement
    damp_rat = sqrt(log_dec**2/(4*pi**2 + log_dec**2))

    wn = wd / (sqrt(1 - damp_rat ** 2))  #undamped natural angular velocity
    f = wn/(2*pi)   #natural frequency

    K = wn**2*m  #stiffness of system
    Cc = 2 * m * sqrt(K / m)  # critical damping
    C = damp_rat*Cc  # damping of system

    #### Scale to full-size ####
    F_wn = wn*(scale**(-0.5))   #full-size wn with Froude scaling
    F_K = K * scale ** 2
    F_C = C * scale ** 2.5

    return wn,f,F_wn,K,C,F_K,F_C

m = 24.87 #kg
t1 = 2.80 #s
t2 = 3.9
x1 = 0.095 #m
x2 = 0.039

print(f'wn for 1:30: {vibration_rate(m,t1, t2, x1, x2)[0]}')
print(f'f for 1:30: {vibration_rate(m,t1, t2, x1, x2)[1]}')
print(f'f for full size: {vibration_rate(m,t1, t2, x1, x2)[2]}')

print(f'stiffness K for 1:30: {vibration_rate(m,t1, t2, x1, x2)[3]}')
print(f'damping for 1:30: {vibration_rate(m,t1, t2, x1, x2)[4]}')
print(f'stiffness K for full-size: {vibration_rate(m,t1, t2, x1, x2)[5]}')
print(f'damping for full-size: {vibration_rate(m,t1, t2, x1, x2)[6]}')










