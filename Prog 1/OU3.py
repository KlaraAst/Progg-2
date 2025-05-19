from math import exp, fabs
import matplotlib.pyplot as plt
from sympy import Symbol, diff, lambdify
from scipy.optimize import fsolve
import numpy as np


def f(x):
    fx = (exp(x)/3) - x**(2) + 1
    return fx


#### Får inte detta att fungera
'''
def df(f, x):

    x = Symbol('x')
    y = f
    dfx = diff(y, x)

    return dfx
'''

def df(x):

    dfx = -2*x + 1/3*exp(x)

    return dfx



def nr(f, df, x0, tol):        ### Hur vet jag att metoden divergerar eller har fastnat???

    counter = 1
    x_ = x0
    xi = x0 - f(x0) / df(x0)

 #Divergerar normalt inom 10 iterationer

    while fabs(xi - x_) > tol:

        x_ = xi  #xi "sparas" utanför loopen och om x_ definieras sist i loopen kommer xi = x_ och while loopen avslutas
        xi = x_ - f(x_)/df(x_)

        counter = counter + 1

        if counter > 30:
            xi = 0    #Returnerar 0 om funktionen fastnar

            break

    return xi, counter



# ------------------------------------------------------------------------------------------------------#


################ Plot ###################

def f(x):
    fx = (exp(x)/3) - x**(2) + 1
    return fx


x_list = []
y_list = []

roots = []

for i in range (-40,50):

    y_list.append(f(i/10))
    x_list.append(i/10)


plt.plot(x_list,y_list)
plt.xlabel('x')
plt.ylabel('y')
plt.show()


# ------------------------------------------------------------------------------------------------------#

#%%

############## Kallar funktion #################


x0 = -1.5     #Startgissning görs från observation av plot
#Startgissnig 100 ger ingen konvergens

tol = 10**(-4)
x_konv = nr(f, df, x0, tol)[0]
counter = nr(f, df, x0, tol)[1]

if counter != 31:   #Printar om vi inte breakat while-loop --> 31 är arbiträrt vald gräns för antal iterationer då normal mängd iterationer är 10
    print('Antal iterationer:', counter)
    print('Konvergens vid:', x_konv)

if counter == 31:  #Printar om vi breakat while-loop
    print('Konvergens ej hittad')
    print('xi = ', x_konv)


# ------------------------------------------------------------------------------------------------------#
#%%
###### Kontrollerar rötter med fsolve ######

roots = [fsolve(f, -2)[0],fsolve(f, 1)[0],fsolve(f, 3)[0]]   #Gissningar (-2, 1, 3) nära rot efter observation
print('Kontroll av funktionens rötter med fsolve:', roots)




















