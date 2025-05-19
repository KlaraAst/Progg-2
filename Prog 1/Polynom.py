'''
All classes have a function called __init__(), which is always executed when the class is being initiated.
Use the __init__() function to assign values to object properties, or other operations that are necessary to do when the object is being created
'''

import matplotlib.pyplot as plt
from math import fabs

class Polynom:

    # ------------------------------------------------------------------------------------------------------#
    def __init__(self, a):  #gradtal n, koefficienter a
        """ Initerar ett polynom """
        self.a = a
        self.n = len((self.a))-1   # Om vi har 4 element i a fås gradtal 3

        termer = []
        counter = 0
        iterationer = len(self.a)-1   #För rätt gradtal

        #elif:  "if the previous conditions were not true, then try this condition"

        for i in range(-iterationer, 1, 1):  #range(start, stop, step)   La till minus för omvänd ordning på x

            if self.a[counter] == 0:
                pass                 #Skippa variabel (koeff = 0)

            elif -i == 0:
                termer.append(f"{self.a[counter]}")   #Ger x = 1

            elif -i == 1 and self.a[counter] == 1:
                termer.append(f"x")  #Ger x (koeff = 1)

            elif self.a[counter] == 1:
                termer.append(f"x^{-i}")

            elif self.a[counter] == -1:
                termer.append(f"-x^{-i}")   #Ger -x (koeff = -1)

            elif -i == 1:
                termer.append(f"{self.a[counter]}x")  #Ger koeff * x

            else:
                termer.append(f"{self.a[counter]}x^{-i}")

            counter = counter + 1

        self.termer = termer   #för användning i __str()__


    # ------------------------------------------------------------------------------------------------------#
    def __str__(self):
        """ Returns a string representation of the polynomial """

        # Format the polynomial correctly
        polynom = " + ".join(self.termer)
        polynom = polynom.replace("+ -", "- ")  #Fixar "+ -"

        return polynom


    # ------------------------------------------------------------------------------------------------------#

    def __call__(self, x):

        """ Evaluering p(x) """

        #Fler steg för debugging
        calc = []  #lägger till koefficient utan x-variabel

        for i in range(-self.n, 1):    #minus för omvänd ordning
            calc.append(self.a[i+self.n] * (x ** (-i)))  #+1 för alla termer a och +self.n i a[] för normal iterering. om self.n har längd 2 får vi start i a vid a[i+2] osv

        svar = sum(calc)

        return svar

    # ------------------------------------------------------------------------------------------------------#


    def __add__(self, other):   # other för "ytterligare self"

        """ Addition + """

        coeff_add_1 = self.a
        coeff_add_2 = other.a

        ## Hantera storlekskillnad på self.a lista

        if len(coeff_add_1) > len(coeff_add_2):

            coeff_add_2.reverse()   # Vänder på lista för att lägga till nollor längst fram

            for i in range(len(coeff_add_1) - len(coeff_add_2)):
                coeff_add_2.append(0)     #lägg til nollor för skillnad i listlängd

            coeff_add_2.reverse()   #vänder tillbaka

            coeff_new_add = [coeff_add_1[i] + coeff_add_2[i] for i in range(len(coeff_add_2))]


        if len(coeff_add_1) < len(coeff_add_2):    #else kanske bättre, men uppfylls ändå inte när listorna är lika långa

            coeff_add_1.reverse()   # Vänder på lista för att lägga till nollor längst fram

            for i in range(len(coeff_add_2) - len(coeff_add_1)):
                coeff_add_1.append(0)     #lägg til nollor för skillnad i listlängd

            coeff_add_1.reverse()   #vänder tillbaka

            coeff_new_add = [coeff_add_1[i] + coeff_add_2[i] for i in range(len(coeff_add_1))]


        return Polynom(coeff_new_add)



    # ------------------------------------------------------------------------------------------------------#

    def __sub__(self, other):

        """ Subtraktion - """

        coeff_sub_1 = self.a
        coeff_sub_2 = other.a

        coeff_new_sub = [coeff_sub_1[i]-coeff_sub_2[i] for i in range(len(coeff_sub_1))]


        return Polynom(coeff_new_sub)

    # ------------------------------------------------------------------------------------------------------#

    def __mul__(self, other):

        """ Multiplikation * """

        coeff_mult_1 = self.a
        coeff_mult_2 = other.a

        # Initialize an empty list to store the result of multiplication
        mult_coeffs = [0] * (self.n + other.n + 2)  # Lista nollor för lagring av koefficienter. +2 då n definieras som len(self.a)-1


        for i in range(len(coeff_mult_1)):
            coeff1 = coeff_mult_1[i]
            for j in range(len(coeff_mult_2)):
                coeff2 = coeff_mult_2[j]
                mult_coeffs[i + j] += coeff1 * coeff2   #multiplicerar alla koeff i other med koeff av samma grad

        return Polynom(mult_coeffs)   #grad blir rätt pga antal nollskilda variabler

    # ------------------------------------------------------------------------------------------------------#

    def __eq__(self, other):
        # Hitta vid vilket x p1 = p2???
        """ Jämförelse == """
        kontroll = 0

        for x in range(0, 101):   #Variabler som testas
            poly_1 = self.__call__(x)
            poly_2 = other.__call__(x)
            if poly_1 == poly_2:
                kontroll += 1
            if x == 100 and kontroll == 0:   #Om polynomen inte varit lika med varandra i slutet
                print('False')
            if x == 100 and kontroll > 0:   #Om polynomen varit lika med varandra i slutet
                print('True')

    # ------------------------------------------------------------------------------------------------------#

    def diff(self):

        # EX p1:
        # har: [3, 0, 1, 5]
        # ger: 3x^3 + x + 5

        # --> vill ha: [9x^2 + 1]

        """ Derivering """

        indexering = len(self.a)   #används för bestämning av grad på x^i
        coeff_diff = self.a
        coeff_diff.reverse()

        coeff_diff_new = []

        for i in range(indexering):
            coeff_diff_new.append(coeff_diff[i]*i)      #koeff * gradtal x^i

        coeff_diff_new.pop(0)   #tar bort första värdet för rätt x^i i Polynom() då gradtalet x minskar vid derivering och gradtalet är kopplat till längd av self.a i Polynom()
        coeff_diff_new.reverse()

        self.coeff_diff_new = coeff_diff_new

        return Polynom(coeff_diff_new)


    # ------------------------------------------------------------------------------------------------------#

    def plot(self ,start ,slut):

        """ Plottning """

        x_values = []
        y_values = []


        for x in range(start, slut):    #minus för omvänd ordning
            y_values.append(self.__call__(x))
            x_values.append(x)

        plt.plot(x_values,y_values)
        plt.title(f"Polynom: {self}")
        plt.xlabel('x')
        plt.ylabel('p(x)')
        plt.show()


    # ------------------------------------------------------------------------------------------------------#

    def zero(self, x0):

        """ Nollställe """

        counter = 1
        x_ = x0
        dpx = Polynom(self.coeff_diff_new)   #lägger in derivatan för användning i summafunktion

        self.a.reverse()   #inte den blekaste varför self.a är reversed till att börja med, men blir fel utan denna

        xi = x0 - self.__call__(x0)/ dpx.__call__(x0)

        tol = 10**(-4)  #tolerans

        # Divergerar normalt inom 10 iterationer

        while fabs(xi - x_) > tol:

            x_ = xi  # xi "sparas" utanför loopen och om x_ definieras sist i loopen kommer xi = x_ och while loopen avslutas
            xi = x_ - self.__call__(x_)/ dpx.__call__(x_)

            counter = counter + 1

            if counter > 30:   #antal iterationer för konvergens. arbiträr gräns vd 30
                xi = 0  # Returnerar 0 om funktionen fastnar
                break

        return xi


    # ------------------------------------------------------------------------------------------------------#

    def integrate(self):

        """ Integral """

        # EX p1:
        # har: [3, 0, 1, 5]
        # ger: 3x^3 + x + 5

        # --> vill ha: [3/4x^4 + 1/2x^2 + 5x]

        indexering = len(self.a)  # används för bestämning av grad på x^i
        coeff_int = self.a

        coeff_int_new = []
        coeff_int_new.append(0)  # lägger till index för "+C" för rätt x^i i Polynom() då gradtalet x^i ökar och gradtalet är kopplat till längd av self.a

        coeff_int.reverse()


        for i in range(indexering):
            coeff_int_new.append(coeff_int[i] / (i+1))  # koeff * gradtal x^i --> +1 för att undvika division med 0


        coeff_int_new.reverse()


        ## Beräkning
        p_int = Polynom(coeff_int_new)
        calc_int = p_int.__call__(1) - p_int.__call__(0)

        print('Polynom: ', p_int)

        return calc_int

    # ------------------------------------------------------------------------------------------------------#

