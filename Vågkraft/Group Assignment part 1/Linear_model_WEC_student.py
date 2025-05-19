import numpy as np
from numpy import pi, mean, sin, cos, max, arctan2, abs, arange, concatenate, zeros, flip, convolve, gradient, argmin, argmax, linspace, multiply, std
import matplotlib.pyplot as plt
from scipy.fft import fftshift, ifft
from scipy.interpolate import interp1d


########## to calculate the optimum damping coefficient gamma that gives the highest power capture ratio ################

def wave(gamma, wave_record, wc1, wc3):

   # Wave amplitude
   wave_amp = multiply(wave_record.tolist(),0.01) # amplitude for incoming wave [m]
   wave_amp -= mean(wave_amp) # fix the biased amplitude
   dt_original = 1 / 2.56 #sampling f = 2.56 Hz
   wave_time = arange(dt_original, dt_original * 4609, dt_original) #time vector for incoming wave [s]

   #----------------------------------------------------------------------------#

   #### Constants ####
   dw = 0.01 #default value for interpolation
   dt = 0.01 #default value for interpolation

   rho = 1000 #water density [kg/m3]
   g = 9.81 #gravity
   r = 2 #buoy radius [m]
   A = pi * r**2 #buoy area [m^2]
   draft = 0.5 #buoy draft (with no translator attached) [m]
   ks = 4000 #spring constant [N/m]
   m = (A * draft * rho) + 1000 #mass of buoy and piston/translator [kg]

   #-----------------------------------------------------------#

   #### Hydrodynamic data ####
   T = wc1[:, 0] #period
   w = 2 * pi / T #angular frequency
   ma = wc1[:, 3] * rho #added mass scaled with rho
   rr = wc1[:, 4] * rho * w #scaled radiation resistance
   absfe = wc3[:, 3] * rho * g #scaled absolute value of excitation force
   argfe = wc3[:, 4] #argument of excitation force


   #### Power capture ratio calculations ####
   Hs = 2.43 #represents the average height of the highest third of waves in a sea state
   Te = 6.25 #average wave period weighted by energy in the spectrum, Te ~ mean(T)
   omega_avg = 2 * pi / Te
   k = omega_avg**(2) / g

   #----------------------------------------------------------------------------#

   ##### Excitation force ####
   fe = absfe * cos(pi * argfe / 180) + 1j * absfe * sin(pi * argfe / 180) #j = imaginary part

   ##### RAO (Response Amplitude Operator) ####
   # H(w) tells us how much the buoy will move for a given wave frequency
   Hw = fe / (-(w ** (2)) * (m + ma) + 1j * w * (gamma + rr) + rho * g * A + ks) # RAO (= the transfer function between wave and buoy amplitud)

   argH = arctan2(Hw.imag, Hw.real) #argument of RAO
   argH = argH * 180 / pi #argument of RAO in degrees
   absH = abs(Hw) #absolute value of RAO

   #----------------------------------------------------------------------------#

   ##### Zero padding ####
   zeros_pad = zeros(100)
   HN = concatenate([zeros_pad,flip(Hw.real),[Hw.real[0]],Hw.real,zeros_pad]) + 1j * concatenate([zeros_pad,- flip(Hw.imag),[0],Hw.imag,zeros_pad])

   dww = abs(w[1] - w[0])
   N = (len(HN) - 1) // 2
   wHN = arange(-dww * N, dww * (N + 1), dww)


   #----------------------------------------------------------------------------#

   ###### Interpolation to increase resolution #####
   wH = arange(dw, max(wHN) + dw, dw)
   wH = concatenate([-flip(wH), [0], wH])
   real_interp = interp1d(wHN, HN.real, kind='cubic', fill_value="extrapolate")
   imag_interp = interp1d(wHN, HN.imag, kind='cubic', fill_value="extrapolate")
   H_interp = real_interp(wH) + 1j * imag_interp(wH)

   #----------------------------------------------------------------------------#

   ###### Inverse Fourier Transform #####
   dtt = 2 * pi / (len(H_interp) * dw)
   h = (1 / dtt) * fftshift(ifft(fftshift(H_interp)))
   t = ((arange(len(h)) - (len(h) + 1) / 2) * dtt)

   #----------------------------------------------------------------------------#

   ###### Trimming the impulse response #####
   h = h.real
   MAX = max(abs(h))
   eps = 0.005

   index1 = next(i for i in range(len(h)) if abs(h[i]) / MAX > eps)
   index2 = next(i for i in reversed(range(len(h))) if abs(h[i]) / MAX > eps)

   h = h[index1:index2 + 1]
   t = t[index1:index2 + 1]

   #----------------------------------------------------------------------------#

   # Interpolation and Convolution
   thI = arange(min(t), max(t) + dt, dt)
   twaveI = arange(min(wave_time), max(wave_time) + dt, dt)

   hI_interp = interp1d(t, h, kind='cubic', fill_value="extrapolate")
   waveI_interp = interp1d(wave_time, wave_amp, kind='cubic', fill_value="extrapolate")

   Ht = hI_interp(thI) # = H(t)
   WaveI = waveI_interp(twaveI)   # = z_w(t)

   z_b = convolve(Ht, WaveI) * dt  #displacement of buoy
   z_velocity = gradient(z_b, dt)   #velocity of buoy = d(z_b)/dt  [m/s]


   #----------------------------------------------------------------------------#

   # Align output with time
   min_idx = argmin(abs(thI))
   N1 = len(Ht)
   N2 = len(z_b)
   z_b = z_b[min_idx:N2 - (N1 - min_idx)]
   z_velocity = z_velocity[min_idx:N2 - (N1 - min_idx)]


   return twaveI, z_b, z_velocity, Hs, Te, k, WaveI

#---------------------------------------------------------------------------#
#%%

######## Load data #######
wave_record = np.loadtxt("Islandsberg_Wave_record")
wc1 = np.loadtxt("wcylinder1_4_05")
wc3 = np.loadtxt("wcylinder3_4_05")


### Changeable single value gamma
#input_gamma = 10**4
input_gamma = 102040.816  # ~10**5



###### Buoy displacement in time domain ######
twaveI = wave(input_gamma,wave_record,wc1,wc3)[0]
z_b = wave(input_gamma,wave_record,wc1,wc3)[1]
time_aligned = twaveI[:len(z_b)]
time_aligned_mins = [time_aligned[i]/60 for i in range(len(time_aligned))]


plt.plot(time_aligned_mins, z_b, 'g')
plt.title("Buoy Vertical Position in Time Domain")
plt.xlabel("Time [min]")
plt.ylabel("Displacement [m]")
plt.grid(True)
plt.show()


waveI = (wave(input_gamma,wave_record,wc1,wc3)[6]).tolist()
waveI.pop(0)  #same sizes for plotting


###### Buoy displacement related to waves ######
plt.plot(waveI, z_b, 'magenta')
plt.title("Vertical Buoy Position relative to Wave Elevation")
plt.xlabel("Wave elevation [m]")
plt.ylabel("Vertical displacement [m]")
plt.grid(True)
plt.show()


#%%
###### Absorbed Power #####

gamma = linspace(0,5*10**5)
P_abs_all = []
P_abs_avg = []


for g in gamma:
   z = wave(g, wave_record, wc1, wc3)[2]   #third return for wave()
   for i in range(len(z)):
       P_abs_all.append(g*z[i]**2)
   C = P_abs_all.copy() # to not link P_abs_all to P_abs_avg
   P_abs_avg.append(sum(C)/len(P_abs_all))   #Average P absorbed for timeframe (30 min of wavedata)
   P_abs_all.clear()


#----------------------------------------------------------------------------#

##### Plot absorbed Power over gamma #####

plt.plot(gamma, [P_abs_avg[i]/1000 for i in range(len(P_abs_avg))])
plt.title("Absorbed Power over Mechanical Damping Coefficient, γ")
plt.xlabel("γ [Ns/m]")
plt.ylabel("Average Absorbed Power [kW]")
plt.grid(True)
plt.show()



#### Find optimal gamma #####

index = argmax(P_abs_avg)
print(f"The most optimal γ was found as: {round(gamma[index],2)}")
print(f"At this γ, the absorbed power was calculated to be: {round(P_abs_avg[index],2)} W")


#%%
#### Power capture ratio ####

a = 2 #wave radius
rho = 1000  # water density [kg/m3]
g = 9.81  # gravity


## k, Hs and T are independent of gamma
Hs = wave(0,wave_record,wc1,wc3)[3]
Te = wave(0,wave_record,wc1,wc3)[4]
k = wave(0,wave_record,wc1,wc3)[5]
J = g**(2)*rho*Te*Hs**(2) / (64*pi)


rat_mult = 1 / (2*a*J)
P_ratio = [i*rat_mult for i in P_abs_avg]


index2 = argmax(P_ratio)
print(f"At this gamma, the Power Capture Ratio was calculated to be: {round(P_ratio[index2]*100,1)} %")


##### Plot Power Capture Ratio (PCR) over gamma #####
plt.plot(gamma, multiply(P_ratio,100))
plt.title("Power Capture Ratio (PCR) over gamma")
plt.xlabel("γ [Ns/m]")
plt.ylabel("Capture Ratio [%]")
plt.grid(True)
plt.show()
