import matplotlib.pyplot as plt
import numpy as np
import math


"""
Funktionernas syfte är att få fram ändringarna per tidssteg. Denna kan sedan loopas och adderas (/subtraheras) till
startvärden beroende på tidsstegens storlek
"""



######### Change in power from excess reactivity in reactor #########
def P_new(P, k, t):

   L_N = 0.0001 #[s] ---> livslängd, prompta neutroner
   rho = (k-1)/k    #resistivitet

   P_fuel = P * math.exp((rho * t) / L_N)

   return P_fuel



############# Temperature Change in fuel from power surge ###############
def dT_dt(dP_dt, t):

   m_fuel = 10.97 # [kg] bränsle
   Cp_UO2 = 0.4 # Värmekapacitet för uranoxid

   dT_fuel = dP_dt*t/(m_fuel*Cp_UO2)    # Temperature change from increased power in reactor from excess reactivity

   return dT_fuel




############### Steam volume Change ################
def dV_steam (U_H2O,V_steam,T_fuel,a,t):


   ## Moderator values ##
   Press = 70  # [bar] ---> tryck (antas konstant)
   rho_steam = 0.0365  # [g/cm^3] ---> densitet för vattenånga vid 70 bar (https://www.thermexcel.com/english/tables/vapeau1.htm)
   T_kaps = T_fuel-700 #[*C]

   ## Power increase from fuel temperature increase
   U_real = U_H2O*(1-a) #[W/(cm*K)] ---> Heat transfer coefficient från kapslingen till vätska
   P_heat = U_real * (T_kaps - T_mod)

   # Entropiändring
   u_70 = 2581 # [kJ/kg] internal energy at 70 bar (7000 kPa)       ### https://engineering.wayne.edu/mechanical/pdfs/thermodynamic-_tables-updated.pdf
   dh_steam = u_70 + Press * V_steam  # enthalpy, steam --> s.200 i PH

   # Steam volume change
   dVsteam_dt = (((P_heat - P_cool) * t / dh_steam) / rho_steam)  # Volymändring, ånga

   return dVsteam_dt




########## Void-Coefficient change + New moderator volume ############
def da_dt(V_steam,dV_steam,a):


  V_steam_new = V_steam + dV_steam
  V_mod_new = V_steam_new/a


  da = dV_steam / V_mod_new

  return da




############# Multiplication factor change #################
def dk_dt(da,dT):

   ### Återkopplingskoefficienter ###
   dk_da = -100 * 10**(-5)  # [pcm] ---> 0.0001% förändring i reaktivitet per % void
   dk_dT = -4 * 10**(-5)  # [pcm/K] = -4*0.0001% minskning av k för varje grad K ---> förändring i reaktivitet vid förändring i bränsletemperatur

   dk = dk_da*da+dk_dT*dT

   return dk


# -------------------------------------------------------------------------------------- #


############## STARTVÄRDEN från konstanter givna och reaktordata #################

time = np.arange(0,1,0.001)   # Timeframe
time_step = 0.001   # Timesteps
k = 1.02  # Kriticitet innan olycka
a = 0.25 #[Void: 25%]

'''
V_mod/V_fuel = 2.8
V_steam/V_mod = 0.25
'''

V_fuel = 100  #[cm^3]
V_steam_start = V_fuel * 2.8 * 0.25
V_mod = V_steam_start * (1 / 0.25)
Press = 70 #[bar]

T_fuel = 1000 #[*C]
T_kaps = T_fuel-700
T_mod = 285.83  #Moderatortemp 70 bar

L_fuel = 1 #[cm] Längd av bränslestav
P0 = 150 * L_fuel  # [W] --> Reaktoreffekt, tot

U_H2O = 14.3  # [W/(cm*K)]
P_cool = (U_H2O * (1 - 0.25)) * (T_kaps - T_mod)  # Kyleffekt antas konstant för ögonblick efter olycka


# -------------------------------------------------------------------------------------- #

########## List generations #########

P = [P0]
T = [T_fuel]
Void = [a]
V_steam = [V_steam_start]
k_ = [k]
dP = []
dT_list = []
da_list = []

counter = 0

for t in time:

   P_fuel = P_new(P[counter], k_[counter], time_step)
   if P_fuel < 0:
       P_fuel = 0      # Dödar reaktorn vid P = 0
   P.append(P_fuel)


   dP.append(P_fuel-P0)
   dT = dT_dt(dP[counter], time_step)
   dT_list.append(dT)
   T.append(T[counter] + dT)


   #dV_steam(dP_dt, V_steam)
   dVsteam_dt = dV_steam(U_H2O,V_steam[counter],T[counter],Void[counter],t)
   V_steam.append(V_steam[counter] + dVsteam_dt)


   #da_dt(V_steam, dVsteam_dt, a)

   da = da_dt(V_steam[counter], dVsteam_dt, Void[counter])
   Void.append(Void[counter] + da)
   da_list.append(da)


   #dk_dt(da_dt, dT_dt, a)
   dk = dk_dt(da,dT)
   k_.append(k_[counter] + dk)

   counter = counter + 1

# -------------------------------------------------------------------------------------- #

############## Plotting #################

## Fuel temp
xpoints1 = np.arange(0,1.001,0.001)
ypoints1 = np.array(T)


plt.plot(xpoints1, ypoints1, 'g')
plt.xlabel('t [s]')
plt.ylabel('Temperatur, bränsle [*C]')

plt.show()

# -------------------------------------------------------------------------------------- #

## Effect increase
xpoints2 = np.arange(0,1.001,0.001)
ypoints2 = np.array(P)

fig = plt.figure(figsize = (8, 7))
plt.plot(xpoints2, ypoints2, 'b')
plt.xlabel('t [s]')
plt.ylabel('Reaktoreffekt [W]')

plt.show()


# -------------------------------------------------------------------------------------- #

## Void
xpoints3 = np.arange(0,1.001,0.001)
Void_procent = [i * 100 for i in Void]     # För %
ypoints3 = np.array(Void_procent)


plt.plot(xpoints3, ypoints3, 'r')
plt.xlabel('t [s]')
plt.ylabel('Void [%]')


plt.show()

# -------------------------------------------------------------------------------------- #

## Multiplication factor
xpoints4 = np.arange(0,1.001,0.001)
ypoints4 = np.array(k_)

plt.plot(xpoints4, ypoints4, 'y')
plt.xlabel('t [s]')
plt.ylabel('Multiplikations-factor, k')

plt.show()

#%%
# -------------------------------------------------------------------------------------- #

## Ångvolym

#plot 1:
x = np.arange(0,1.001,0.001)
y = np.array(V_steam)
plt.plot(x,y)
plt.title('Volymändring, ångvolym [$cm^3$]')
plt.ylabel('$V_{ånga}$ [$cm^3$]')
plt.xlabel('t [s]')
plt.plot(x,y,'r')

plt.show()








