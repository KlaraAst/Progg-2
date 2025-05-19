"""
Solutions to module 4 - A calculator
Student: Klara Asterland
Mail: klara.asterland.6081@student.uu.se
"""
from scipy.special import result

"""
Note:
The program is only working for a very tiny set of operations.
You have to add and/or modify code in ALL functions as well as add some new functions.
Use the syntax charts when you write the functions!
However, the class SyntaxError is complete as well as handling in main
of SyntaxError and TokenError.
"""

import math
from tokenize import TokenError  
from MA4tokenizer import TokenizeWrapper


class SyntaxError(Exception):  #our own exception class
    def __init__(self, arg):
        self.arg = arg
        super().__init__(self.arg)

'''
wtok = "wrapper tokenizer" --> Splits input string into tokens. Provides methods like:
      - get_current() → the current token
      - get_previous() → the previous token
      - next() → move to the next token (only operation that moves along the input!)
      - is_number() → check if the current token is a number
      - is_name() → check if it's a valid variable name
      
variables = a dictionary that stores all variable names and their current values      

'''
############################################################################################################

def statement(wtok, variables):
    """ See syntax chart for statement"""
    result = assignment(wtok, variables)
    return result

############################################################################################################

def assignment(wtok, variables):  #Calculate the value first, then store it in a variable if '=' appears

    #Detects and handles custom variable assignments (= x, = y). main() loop stores only the most recent result in ans

    if wtok.get_current() != '=':
        result = expression(wtok, variables) # if assignment() sees no '=' it calls expression()
    if wtok.get_current() == '=':
        variables[f'{wtok.next()}'] = result

    return result

############################################################################################################

def expression(wtok, variables): #Handles addition and subtraction (+, -)

    #"Do + and - from left to right, but wait — let me evaluate the more important stuff (like * and /) first"

    result = term(wtok, variables)
    while wtok.get_current() == '+' or wtok.get_current() == '-':  # handle + and -. Continues if it encounters either or
        if wtok.get_current() == '+':
            wtok.next()
            result = result + term(wtok, variables)  #add next term
        if wtok.get_current() == '-':
            wtok.next()
            result = result - term(wtok, variables)  #subtract next term

    return result

############################################################################################################

def term(wtok, variables):  #Handles multiplication and division (*, /)

#Called by expression() to deal with the next higher level of priority.

    result = factor(wtok, variables)
    while wtok.get_current() == '*' or wtok.get_current() == '/':  # handle * and /. Continues if it encounters either or
        if wtok.get_current() == '*':
            wtok.next()
            result = result * factor(wtok, variables)  #step to deepest layer (factor()) to find factor to multiply
        if wtok.get_current() == '/':
            wtok.next()
            result = result / factor(wtok, variables)  #step to deepest layer to find factor to multiply
    return result

############################################################################################################

def factor(wtok, variables): #Handles numbers, parentheses, and variables

#“I’m the part that knows what a number is, or how to evaluate something like (1 + 2) or a variable like x.”

#------------------------ Sign after parenthesis -----------------------#

    if wtok.get_current() == '-':  # get_current is value after '('
        wtok.next() #value after '-'
        result = -float(wtok.get_current())  # lump sign and value together as negative float value
        wtok.next()  # the value after "lumped" value

    elif wtok.get_current() == '+':  # get_current is value after '('
        wtok.next()  # the value after '+'
        result = float(wtok.get_current())  # lump sign and value together by removing first sign
        wtok.next()  # value after "lumped" value

#------------------------------------------------------------------------#

    elif wtok.is_name():  #if token is valid variable name
        name = wtok.get_current()  #func name
        wtok.next() #move to parenthesis

        #before entering recursive loop for trig_input
        if wtok.get_current() != '(':
            raise SyntaxError("Expected '(' after function name")   #spelling error with missing (

        wtok.next() #move into parenthesis
        trig_input = assignment(wtok, variables)  # Recursively evaluate everything inside, and return the result as one value. Loops outside of wtok.is_name

        # After recursive loop for trig_input
        if wtok.get_current() != ')':
            raise SyntaxError("Expected ')' after function argument")   #spelling error with missing )


        # Non-numerical value trig_input, like pi or x
        if trig_input.is_number() == False:

            if trig_input in variables:
                if name == 'sin':
                    result = math.sin(variables[trig_input])   #get the stored value for trig_input
                if name == 'cos':
                    result = math.cos(variables[trig_input])
            else:
                raise SyntaxError("Invalid variable for calculation of function")


        # Numerical value for trig_input
        if name == 'sin':
            result = math.sin(trig_input)
        if name == 'cos':
            result = math.cos(trig_input)
        else:
            raise SyntaxError("Invalid function")


    elif wtok.get_current() == '(':
        wtok.next() #move past '('
        result = assignment(wtok, variables) # “When you see (, recursively evaluate everything inside, and return the result as one value"

        if wtok.get_current()!= ')':  #when it enters this recursive if-loop the second time, we'll have a closing ')'. If not we have an error
            raise SyntaxError("Expected ')'")

        else:
            wtok.next()  # ← This "consumes" the closing ')'

    elif wtok.is_number():
        result = float(wtok.get_current()) #assign values inside ()
        wtok.next()

    else:
        raise SyntaxError(
            "Expected number or '('")

    return result                      #returns 1 value or symbol to be used in term() and expression()

############################################################################################################
         
def main(): #Handles input/output and stores result in ans
    """
    Handles:
       the iteration over input lines,
       commands like 'quit' and 'vars' and
       raised exceptions.
    Starts with reading the init file
    """
    
    print("Numerical calculator")
    #variables = {"ans": 0.0, "E": math.e, "PI": math.pi}    #Stored variables from calculator
    my_variables = {"ans": 0.0, "E": math.e, "PI": math.pi}  # My stored variables, including constants

    # Note: The unit test file initiate variables in this way. If your implementation 
    # requires another initiation you have to update the test file accordingly.
    init_file = 'MA4init.txt'
    lines_from_file = ''
    try:
        with open(init_file, 'r') as file:
            lines_from_file = file.readlines()
    except FileNotFoundError:
        pass


    while True:
        if lines_from_file:
            line = lines_from_file.pop(0).strip()
            print('init  :', line)
        else:
            line = input('\nInput : ')
        if line == '' or line[0] =='#':    #skipping empty lines and comments
            continue
        wtok = TokenizeWrapper(line)    #tokenize line in MA4init

        if wtok.get_current() == 'quit':
            print('Bye')
            exit()
        else:
            try:
                result = statement(wtok, my_variables)
                my_variables['ans'] = result
                print('Result:', result)

            except SyntaxError as se:
                print("*** Syntax error: ", se)
                print(
                f"Error occurred at '{wtok.get_current()}' just after '{wtok.get_previous()}'")

            except TokenError as te:
                print('*** Syntax error: Unbalanced parentheses')
 


if __name__ == "__main__":
    main()
