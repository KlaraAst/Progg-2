import matplotlib.pyplot as plt
from math import cos, sin, pi
import numpy as np

# Konstanter
g = 9.82
a = pi/4 #[rad]
v0 = 10 #[m/s]

def OU2_1(t):

    x = (v0 * t * cos(a))
    y = (-0.5*g*t**(2)+v0*t*sin(a))

    return x,y

# Plot
x_list = []
y_list = []
counter = 0


for t in range(0, 200): # trivial interval chosen

    x_list.append(OU2_1(t/100)[0]) #/100 för mindre timesteps

    if OU2_1(t/100)[1] < 0:
        y_list.append(0)
    if OU2_1(t/100)[1] < 0 and y_list[counter-1] == 0:   #om föregående tal i listan är noll
        break
    else:
        y_list.append(OU2_1(t/100)[1])

    counter =+ 1  # Indexing for y_list

    #y_list.append(OU2_1(t / 10)[1])

# Adding reference line for y = 0
y_ref = np.zeros(12)  #12 just because it fits nicely in figure

plt.plot(x_list,y_list,y_ref)
plt.xlabel('x')
plt.ylabel('y')
plt.show()




#%%

''' 
Om hindret ligger 15m bort och är 5m högt innebär det att när x = 15 måste y > 5
'''

#alfa = input('initiell vinkel')
#v_0 = input('initiell hastighet')


def OU2_2(alfa, v_0):

    x_list = []
    y_list = []
    counter = 0

    for t in range(0, 2500):  # trivial interval chosen

        x = (v_0 * (t/100) * cos(alfa))
        y = (-0.5 * g * (t/100) ** (2) + v_0 * (t/100) * sin(alfa))

        x_list.append(x)  # /100 för mindre timesteps

        if y < 0:
            y_list.append(0)
        if y < 0 and y_list[counter - 1] == 0:  # om föregående tal i listan är noll
            break
        else:
            y_list.append(y)

        counter = + 1  # Indexing for y_list

    return x_list, y_list


#%%
if __name__ == '__main__':
    # kommentera bort rader nedan med "#"" om du inte vill se allt vid varje körning
    # vid redovisning (eller inlämning) ta fram alla rader
    OU2_1(t)


    x_axis1 = OU2_2(pi/3,16.9)[0]
    y_axis1 = OU2_2(pi/3,16.9)[1]

    x_axis2 = OU2_2(2*pi/9,15.9)[0]
    y_axis2 = OU2_2(2*pi/9,15.9)[1]

    x_axis3 = OU2_2(pi/6,16.9)[0]
    y_axis3 = OU2_2(pi/6,16.9)[1]


    # Skapar hinder
    hinder = []
    for i in range(26):
        hinder.append(0)
    hinder.pop(15)
    hinder.insert(15, 5)


    plt.plot(x_axis1, y_axis1, hinder)
    plt.plot(x_axis2, y_axis2, 'r')
    plt.plot(x_axis3, y_axis3, 'g')

    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

