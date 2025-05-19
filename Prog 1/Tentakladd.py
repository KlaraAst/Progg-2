
def accList(a):

    sum_list = [a[0]]

    for i in range(len(a)-1):
        sum_list.append(sum_list[i]+a[i+1])

    return sum_list


x = [1, 5, 3, -4]
print(accList(x))
y = [1, 2, 3, 4, 5]
print(accList(y))


#%%

def med(str):
    string = str.split(" ")
    values = [float(i) for i in string]

    med = sum(values)/len(values)

    return med

s = '4.6 8.0 -3.7 14.3'
ss = '3.5 7.2'

med(s)
med(ss)


#%%

import random

s = 'Engodtyckligtext'
string = [i for i in s]
str_rand = []

for e in range(6):
    index_rand = random.randint(0, len(string)-1)
    str_rand.append(string[index_rand])

str_rand = ''.join(str_rand)
print(str_rand)


#%%

def missingDigits(string):

    missing = []
    str_sep = [i for i in string]

    for n in range(10):
        if str(n) not in str_sep:
            missing.append(str(n))

    return missing



s = '16789117'
print(missingDigits(s))
s = '012346789'
print(missingDigits(s))
s = '0123456789'
print(missingDigits(s))


#%%

s = 'swe Fin sWe noR dEn nor isL'
ss = 'hej HoPP tjEna hOPp hopp'

s = s.lower()
s_comma = s.split(' ')


my_dict = {}
for e in s_comma:

    if e in my_dict:
        my_dict.update({e:my_dict[e]+1})

    if e not in my_dict:
        my_dict[e] = 1

print(my_dict)


#%%

class Lottery:
    def __init__(self, nr):
        self.nr = nr
        self.nr_list = [i for i in range(1,nr+1)]

    def __str__(self):
        return 'Lottery = ' + str(self.nr_list)

    def draw(self):
        if self.nr == 0:
            return -1
        i = random.randint(0,self.nr-1)
        lot = self.nr_list.pop(i)
        self.nr -= 1
        return lot

    def isEmpty(self):
        if self.nr == 0:
            return True
        else:
            return False

n = 4
t = Lottery(n) # Initiera lotteriet, fyll den med lotter med nummer 1,2,...,n
print(t)


while not t.isEmpty(): # Så länge det finns lotter kvar
    print('lot = ', t.draw()) # Dra en lott och skriv ut numret på den

print(t)
print('lot = ', t.draw()) # Försök dra en lott till...












