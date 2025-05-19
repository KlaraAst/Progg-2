
'''
The self parameter represents the instance of the class. It allows you to access and modify attributes for that specific object.

self.name = name means each instance has its own name attribute.
p1.name is "John", and p2.name is "Bob"—they store separate values.
self ensures that attributes belong to that specific instance, not the class itself.

'''
import random

class Person:
    def __init__(self, name, age, height):
        self.name = name  # Assign name to the instance
        self.age = age   # Assign age to the instance
        self.height = height  # Assign height to the instance

    def hotness(self):
        return "Snygghetsnivå:" + str(random.randint(1,10))   #Random siffra 1-10


# Feature inherits from Person
class Feature(Person):
    def __init__(self, name, age, height):
        super().__init__(name, age, height)

    def new_feature(self, thing):
        self.thing = thing
'''
I need to create an instance of Feature and call new_feature() on that instance to assign a value to self.thing, not just define
self.thing = thing
'''

# Creating objects (instances of the class)
#p1 = Person("John", 36, 178)
#p2 = Person("Bob", 24, 185)

p1 = Feature("John", 36, 178)
p2 = Feature("Bob", 24, 185)

p1.new_feature("Loves dino nuggets")
p2.new_feature("Eats ass")


print(p1.name)
print(p1.age)
print(p1.height)
print(p1.thing)
print(p1.hotness())

print('----------------------------')

print(p2.name)
print(p2.age)
print(p2.height)
print(p2.thing)
print(p2.hotness())

#%%

class Character:
    def __init__(self, health, damage, speed):
        self.health = health
        self.damage = damage
        self.speed = speed

    def double_speed(self):
        return '{}'.format(self.speed*2)
# Om jag har self som input blir det ett attribut och detta kallas på med double_speed('instance, t ex master_chief'). Utan self kallas classen på utan ()

master_chief = Character(200, 70, 40)
arbitor = Character(100, 60, 70)

print(master_chief.speed)
print(master_chief.double_speed())
#master_chief.double_speed()
#print(master_chief.speed)


#%%

x = 2
n = 5
a = [1,2,3,4,5]

x1 = [a[i]*x**i for i in range(n)]

