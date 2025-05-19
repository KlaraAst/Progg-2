
############## Q1

'''
a = 3
b = 4
c = 5

x=a+b
x*=2
y=x+c
z=x+y
x=0
y=0


x = 208
years = int(x/12)

# // = heltalsdivision, % = moduloperator, ger resterande månader kvar
print(f"{x//12} år", f"{x % 12} månader")



s1="Python is great"
s2 = s1[10:]


list_a = [1, 8, 9, 15]
list_a.insert(1,2)
list_a.append(4)
list_a.sort(reverse=True)


matrix = [3,5,3,2,2,5,3,8,9]
matrix[7] = 7


list_b = [2, 3, 2, 3, 1, 2, 5]
list_c = list(set(list_b))


s1 = {2, 3, 4}
s2 = {1, 2, 3}
union = s1.union(s2)
print(s1.intersection(s2))
print(s2.difference(s1))


tentares = {"Kalle": 14,  "Sofia": 18,  "Josefin": 12}
tentares["Josefin"] = 14
tentares["Oscar"] = 17
namn = tentares.keys()

'''

#%%

############## Q2

import numpy as np
import matplotlib.pyplot as plt

#x=np.array([1, 2])
#x=np.arange(0,10)
#x=np.arange(0,1,0.1)
#x=np.linspace(0,1,11)

A=np.matrix([[1,2], [3,4]])
#A=np.zeros([10,10])
AA = 2*A
B= A/AA

x=np.linspace(0,5,20)
y=[np.sin(i**2) for i in x]

plt.plot(x,y,'r',marker = 'o')
#plt.show()

'''
C = float(input('Ange grader celcius:'))
F =1.8*C+32
print(round(F, 2))
'''

#%%
'''
s1=float(input('Temp1: '))
s2=float(input('Temp2: '))
s3=float(input('Temp3: '))


if abs(s1 - s2) > 10 or abs(s1 - s3) > 10 or abs(s2 - s3) > 10:
    print('LARM: Avvikande temperaturer!')
else:
    print('Normala temperaturer!')
    
'''

#%%

#pris=float(input('Ange totala priset: '))
pris = 400

if pris >= 500 and pris <= 1000:
    rabatt = 0.05
elif pris >= 1000 and pris <= 2000:
    rabatt = 0.1
elif pris >= 2000:
    rabatt = 0.15
else:
    rabatt = 0

print(f'Priset blir {pris-rabatt*pris} kr')

#%%

lista = [10, 15, 24, 17, 9, 8, 3]

for e in lista:
    for i in range(e+1):
        print('*', end='')
    print()


#%%

import random

t = [0, 0, 0, 0, 0]  # skapa en tom lista
for i in range(5):
    t[i] = random.randint(1, 6)
kast = 1

while len(set(t)) > 1:

    for i in range(5):
        t[i] = random.randint(1, 6)

    kast += 1

print(f'Det krävdes {kast} kast för att få 5st {t[0]}:or.')



#%%
import random

t=[0,0,0,0,0] # skapa en tom lista

for i in range(5):
    t[i]=random.randint(1,6)

kast=1
lika_kast = []

for k in range(10000):

    if len(set(t)) > 1: # Kör sålänge alla värden inte är lika då set inte kan ha dubletter
         for i in range(5):
               t[i]=random.randint(1,6)
         kast += 1

    if len(set(t)) == 1:
        lika_kast.append(kast)

        #Nytt kast
        for i in range(5):
            t[i] = random.randint(1, 6)
        kast += 1



#print(f'Det krävdes {kast} kast för att få 5st {t[0]}:or.')
print(f'Det krävdes {lika_kast} kast för att få 5st av samma.')



#%%

def triarea(b,h):

    area = b * h / 2

    return area



file=open('minfil.txt', 'w')

file.write(f'Detta är en textfil,\n')
file.write(f'skapad med Python.\n')
file.close()

'''

import numpy as np
data=np.loadtxt('people.csv',delimiter=',',dtype=str)
for row in data:
    print(row)


import csv
with open('people.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        print(row)



#import numpy as np
data=np.array([[0.0, 0.0],
    [1.0, 3.4],
    [2.0, 4.5],
    [3.0, 5.1],
    [4.0, 5.4],
    [5.0, 5.5],
    [6.0, 5.0],
    [7.0, 3.1],
    [8.0, 0.4]])
np.savetxt('mydata.csv', data, fmt='%.1f',delimiter=',',header='Tid (s), Fart (m/s)')


import matplotlib.pyplot as plt
data=np.loadtxt('mydata.csv',delimiter=',')
plt.plot(data[:,0],data[:,1])
plt.show()
'''

#%%


##### Q5

class Dice:
    def __init__(self, sides):
        self.sides = sides
        self.value = random.randint(1, self.sides)

    def __str__(self):
        return f"Tärning med {self.sides} sidor, nuvarande värde: {self.value}"

    def roll(self):
        #Ger nytt tärningskast
        self.value = random.randint(1, self.sides)

    def upside(self):
        return self.value


T1 = Dice(6)
print(T1)
T1.roll()
print(T1)


#%%


class Yatzy:
    def __init__(self):
        self.dice_list = []
        for _ in range(5):
            self.dice_list.append(Dice(6))

    def __str__(self):
        return str([d.upside() for d in self.dice_list])

    def roll(self):
        for d in self.dice_list:
            d.roll()

game = Yatzy()
for _ in range(10):
    game.roll()
    print(game)


    def play(self):
        self.roll()
        print(self)
        for _ in range(2):
            throwlist=input('Ange vilka tärningar vill du kasta om (tex som 145): ')
            for dice in throwlist:
                self.dice_list[int(dice)-1].roll()
            print(self)

#%%

x = [9, 2]
for a, b in enumerate(x):
    print(a, b)


z = [i+1 for i in range(10)]
a = 2
b = 9
print(z[a:0:b])








