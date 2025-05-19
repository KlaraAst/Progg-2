
#Import class
from Polynom import Polynom




#Initierar polynom
p1 = Polynom([3, 0, 1, 5])
p2 = Polynom([1, 1, 0])
p3 = Polynom([3, 0])
p4 = Polynom([3, 0, 1, 5])

print('---------------------')

print('Polynom:')
print('p1 = ' + p1.__str__())
print('p2 = ' + p2.__str__())
print('p3 = ' + p3.__str__())

print('---------------------')

#Evaluering av x = 2
print('Evaluering kring x = 2:')
print('x1 = ', p1.__call__(2))
print('x2 = ', p2.__call__(2))
print('x3 = ', p3.__call__(2))

print('---------------------')

#Addition
print('Addition:')
print('p1 + p2 = ', p1 + p2)
#print('p2 + p3 = ', p2 + p3)
#print('p1 + p3 = ', p1 + p3)

print('---------------------')

#Subtraktion
print('Subtraktion:')
print('p1 - p2 = ', p1 - p2)
print('p2 - p1 = ', p2 - p1)

print('---------------------')

#Multiplikation
print('Multiplikation:')
print('p1 * p2 = ', p1 * p2)

print('---------------------')

#Sub-mult test
print('Sub-mult test')
print('p1 - p3 * p2 = ', p1 - p3 * p2)

print('---------------------')

#Jämförelse
print('polynom 1 = polynom 2:')
#p1 == p2
p1 == p4

print('---------------------')

#Derivering
print('Derivering')
print(p1.diff())

print('---------------------')

#Plot
p1.plot(-5, 5)

#Nollställe
print('Nollställe:')
print(p1.zero(-1))

print('---------------------')

#Integrering
print('Integrering:')
print('Integral mellan 0 och 1: ', p1.integrate())








