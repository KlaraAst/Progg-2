from inspect import cleandoc, getsource # modifiera inte denna rad, detta är bara till för enkel rättning/presentation
import math
import numpy as np

def OU1_1():
    svar="""datatypen int() representerar heltal och datatypen float() representerar reella tal"""
    print(cleandoc(svar)) # modifiera inte denna rad

def OU1_2():
    svar="""Vid dynamisk typning kan typen av variabel ändras under körning utan att ge fel. Kan t ex vara om en variabel beräknas och ändras i en for-loop. En statisk variabel är
     en definierad konstant"""
    print(cleandoc(svar)) # modifiera inte denna rad

def OU1_3(x):

    svar = math.exp(math.sin(2*math.pi*x))+math.log(1/x)*(math.cos(x*math.pi/3)**(4))+math.sqrt(3*x)
    return svar

#print('OU1_3:', OU1_3(float(input('x-värde:'))))


input4 = OU1_3(2)
def OU1_4():
    print(input4)


def OU1_5():
    svar="""Detta är inbyggda datatyper som används för att lagra data. En lista är en ordnad samling med index 0-n. Man kan lägga till och ta bort element fritt och de kan innehålla 
    dubletter. Skapas med namn = []. En tupel är också en ordnad sekvens (efter index) men man kan inte ändra i en tupel efter att jag skapat den. Skapas med namn = (). 
    Ett lexikon (dict) är en oordnad samling (ej efter index) som instället ordnar element efter nycklar och värden. Kan exempelvis vara en lista av personuppgifter för en viss person
    där namnet på personen blir nyckeln och sedan kan värden vara saker som email, telefonnummer etc. Skapas med namn = {}"""
    print(cleandoc(svar)) # modifiera inte denna rad
    
def OU1_6():

    my_lex = {
        "Mjölk": 15,
        "Potatis" : 20,
        "Skinka": 25
    }
    return my_lex

my_lexx = OU1_6()

def OU1_7(my_lexx):

    print(my_lexx["Potatis"])

def OU1_8(my_lexx):

    priser = my_lexx.values()
    print(sum(priser))

def OU1_9(my_lexx):

    my_lexx.pop("Potatis")
    my_lexx["Morot"] = 10

    priser_ny = my_lexx.values()
    print(sum(priser_ny))


if __name__ == '__main__':
    # kommentera bort rader nedan med "#"" om du inte vill se allt vid varje körning
    # vid redovisning (eller inlämning) ta fram alla rader
    print("OU1_1:\n"); print("Svar:"); OU1_1(); print("-"*80)
    print("OU1_2:\n"); print("Svar:"); OU1_2(); print("-"*80)
    print("OU1_3:\n"); print(getsource(OU1_3)); print("-"*80)
    print("OU1_4:\n"); print(getsource(OU1_4)); print("Svar:"); OU1_4(); print("-"*80)
    print("OU1_5:\n"); print("Svar:"); OU1_5(); print("-"*80)
    print("OU1_6:\n"); print(getsource(OU1_6)); print("-"*80)
    print("OU1_7:\n"); print(getsource(OU1_7)); print("Svar:"); OU1_7(my_lexx); print("-"*80)
    print("OU1_8:\n"); print(getsource(OU1_8)); print("Svar:"); OU1_8(my_lexx); print("-"*80)
    print("OU1_9:\n"); print(getsource(OU1_9)); print("Svar:"); OU1_9(my_lexx); print("-"*80)