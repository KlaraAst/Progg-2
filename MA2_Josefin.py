
"""
Solutions to module 2 - A calculator
Student: Josefin Landgren
Mail: josefin.landgren.6712@student.uu.se
Reviewed by: Chengzi
Reviewed date: 2024-09-23
"""

import math
from tokenize import TokenError  
from MA2tokenizer import TokenizeWrapper


#Class for syntax errors
class SyntaxError(Exception):
    def __init__(self, arg):
        self.arg = arg
        super().__init__(self.arg)

#Class for evaluation errors
class EvaluationError(Exception):
    def __init__(self, arg):
        self.arg = arg
        super().__init__(self.arg)


#Function for division which rasises Evalutation error for division by 0.
def division(a, b):
    if b != 0:
        return a/b
    else:
        raise EvaluationError("Division by zero")

#Functions with 1 input:
def fac(x):
    if x%1 == 0:
        return math.factorial(x)
    else:
        raise EvaluationError(f"Argument to fac is {x}. Must integer >= 0") #Raises error if input has decimals.

def log(x):
    if x <= 0:
        raise EvaluationError(f"Argument to log is {x}. Must be > 0") #Raises error if input is equal or less than 0.
    else:
        return math.log(x)

def exp(x):
    return math.exp(x)

def cos(x):
    return math.cos(x)

def sin(x):
    return math.sin(x)


#Functions with one input
function_1 = {"sin": sin, "cos": cos, "exp": exp, "log": log, "fac": fac}

#Functions with multiple inputs
function_n = {"max": max, "sum": sum}

def statement(wtok, variables): #Delivers input-value  to assignment, or concludes run by EOL.
    """ See syntax chart for statement"""
    result = assignment(wtok, variables)
    if wtok.is_at_end():
        return result
    else:
        raise SyntaxError("Expected end of line")


def assignment(wtok, variables): #Assigns variables to names.
    """ See syntax chart for assignment"""
    result = expression(wtok, variables)
    while wtok.get_current() == "=":
        wtok.next()
        if wtok.is_name():
            variables[wtok.get_current()] = result
            wtok.next()
        else:
            raise SyntaxError("Expected name after '='")
    return result

def expression(wtok, variables): #Adds up nad subtracts results from term.
    """ See syntax chart for expression"""
    result = term(wtok, variables)
    while wtok.get_current() == '+' or wtok.get_current() == "-":
        if wtok.get_current() == "+":
            wtok.next()
            result = result + term(wtok, variables)
        else:
            wtok.next()
            result = result - term(wtok, variables)
    return result


def term(wtok, variables): #Multiplies or divides results from factor.
    """ See syntax chart for term"""
    result = factor(wtok, variables)
    while wtok.get_current() == '*' or wtok.get_current() == '/':
        if wtok.get_current() == "*":
            wtok.next()
            result = result * factor(wtok, variables)
        else:
            wtok.next()
            result = division(result, factor(wtok, variables))
    return result


def arglist(wtok, variables): #Creates input-list for functions in dict "functions_n", that need list input.
    result_lst = []
    if wtok.get_current() == '(':
        wtok.next()
        result = assignment(wtok, variables)
        result_lst.append(result)
        while wtok.get_current() == ",": #Creates a list from values
            wtok.next()
            result = assignment(wtok, variables)
            result_lst.append(result)
        if wtok.get_current() != ')':
            raise SyntaxError("Expected ')'")
        else:
            wtok.next()
    else:
        raise SyntaxError("Expected '('")
    return result_lst


def factor(wtok, variables):
    """ See syntax chart for factor"""
    if wtok.get_current() == '(': #Enters parenthesis if possible.
        wtok.next()
        result = assignment(wtok, variables)
        if wtok.get_current() != ')':
            raise SyntaxError("Expected ')'")
        else:
            wtok.next()

    elif wtok.get_current() in function_1: #Checks for functions from function_1
        var = function_1[wtok.get_current()] #Gets function from dict
        wtok.next()
        if wtok.get_current() == '(':
            wtok.next()
            result = var(assignment(wtok, variables))
            if wtok.get_current() != ')':
                raise SyntaxError("Expected ')'")
            else:
                wtok.next()
        else:
            raise SyntaxError("Expected '('")


    elif wtok.get_current() in function_n: #Checks for functions from function_n
        var = function_n[wtok.get_current()] #Gets function from dict
        wtok.next()
        result = var(arglist(wtok, variables))
        wtok.next()

    elif wtok.is_name(): #If given a name, takes corresponding value from Variables-ditionary
        if wtok.get_current() in variables:
            result = float(variables[wtok.get_current()])
            wtok.next()
        else:
            raise EvaluationError(f"Undefined variable: {wtok.get_current()}")

    elif wtok.is_number(): #If given a number, returns a number.
        result = float(wtok.get_current())
        wtok.next()


    elif wtok.get_current() == "-": #Changes parenthesis-sign if "-" before
        wtok.next()
        result = - factor(wtok, variables)
    else:
        raise SyntaxError(
            "Expected number, word or '('")
    return result


         
def main():
    """
    Handles:
       the iteration over input lines,
       commands like 'quit' and 'vars' and
       raised exceptions.
    Starts with reading the init file
    """

    print("Numerical calculator")
    variables = {"ans": 0.0, "E": math.e, "PI": math.pi}
    # Note: The unit test file initiate variables in this way. If your implementation 
    # requires another initiation you have to update the test file accordingly.
    init_file = 'MA2init.txt'
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
        if line == '' or line[0]=='#':
            continue
        wtok = TokenizeWrapper(line)

        if wtok.get_current() == 'quit': #Exits calculator if input is quit
            print('Bye')
            exit()
        elif wtok.get_current() == "vars": #Prints all saved variables if input is vars
            print(variables)
        else:
            try:
                result = statement(wtok, variables)
                variables['ans'] = result
                print('Result:', result)

            except SyntaxError as se: #Prints out Syntax errors.
                print("*** Syntax error: ", se)
                print(
                        f"Error occurred at '{wtok.get_current()}' just after '{wtok.get_previous()}'")

            except (EvaluationError, ValueError, ZeroDivisionError) as ee: #Prints out Evaluation errors.
                print("*** Evaluation error: ", ee)
                print(
                    f"Error occurred at '{wtok.get_current()}' just after '{wtok.get_previous()}'")


            except TokenError as te: #Prints out Token errors.
                print('*** Syntax error: Unbalanced parentheses')
 


if __name__ == "__main__":
    main()
