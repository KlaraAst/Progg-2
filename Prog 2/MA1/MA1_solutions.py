"""
Solutions to module 1
Student: 
Mail:
Reviewed by:
Reviewed date:
"""

"""
Important notes: 
These examples are intended to practice RECURSIVE thinking. Thus, you may NOT 
use any loops nor built in functions like count, reverse, zip, math.pow etc. 

You may NOT use any global variables.

You can write code in the main function that demonstrates your solutions.
If you have testcode running at the top level (i.e. outside the main function)
you have to remove it before uploading your code into Studium!
Also remove all trace and debugging printouts!

You may not import any packages other than time and math and these may
only be used in the analysis of the fib function.

In the oral presentation you must be prepared to explain your code and make minor 
modifications.

"""


import time
import math
from math import log

def multiply(m: int, n: int) -> int:  
    """ Ex1: Computes m*n using additions"""
    if m*n == 0:   #becomes 0 if either is 0
        return 0
    else:
        return m + multiply(m,n-1)

print('Multiplication:', multiply(2,3))


#%%

def harmonic(n: int) -> float:              
    """Ex2: Computes and returns the harmonc sum 1 + 1/2 + 1/3 + ... + 1/n"""
    if n == 0:
        return 0
    else:
        return 1/n + harmonic(n-1)

print('Harmonic sum:', harmonic(4))

#%%

def get_binary(x: int) -> str:
    """ Ex3: Returns the binary representation of x """
    #ex '5' = '101'
    # binary nr in spaces of multiple of 2: 1,2,4,8,16...

    #Base cases
    if x == 0:
        return '0'
    if x == 1:
        return '1'
    #Negative numbers
    if x < 0:
        return '-' + get_binary(-x)  # -(-x) for normal operations

    # Recursive step: divide by 2 and get the remainder
    return get_binary(x//2) + str(x%2)   #str(x % 2) gives 'left over' after highest binary position. Will be 0 or 1 dependingon if 1 "is needed"

'''
EX:
    get_binary(5)
    → get_binary(2) + '1'
    → (get_binary(1) + '0') + '1'
    → ('1' + '0') + '1' = '101'

'''


print('Binary rep.:', get_binary(10))



#%%

'''
Let n be the number of characters in the string.
Suppose that we can solve the problem for the n − 1 first characters in the string.
To solve the problem for a string of length 1 is trivial.
'''

def reverse_string(s: str) -> str:        
    """Ex4: Returns the s reversed """
    if len(s) <= 1:
        return s
    else:
        mid = len(s) // 2

    return reverse_string(s[mid:]) + reverse_string(s[:mid])


s = 'Banana'
print('Word:', s)
print('Word reversed:', reverse_string(s))


#%%

def largest(a: iter):                     
    """Ex5: Returns the largest element in a"""

    max = a[-1]

    if len(a) > 1:

        start = a[0]
        end = a[1:]

        if start >= max:
            end.append(start)      #save bigger number to end of list
            return largest(end)    #saves and sends this value back up the chain to the original call. Without return values get 'thrown out'
        elif start <= max:
            return largest(end)
    else:
        return max


#a = [1,2,3,4,5]
a = [2,96,43,5,8,7,4,87]
print('Largest list value:', largest(a))



#%%

def count_outer(x, s):

    if s == []:
        return 0
    else:
        start = s[0]
        end = s[1:]
        if start == x:
            return 1 + count_outer(x, end)
        else:
            return count_outer(x, end)

def count_whole(x, s):

    if s == []:
        return 0   #empty list

    else:
        start = s[0]
        end = s[1:]

        if type(start) != list:
            if start == x:
                return 1 + count_whole(x, end)
            else:
                return count_whole(x, end)

        if type(start) == list:          #if first value is list these needs to be indexed to access single values
            start_list = start[0]
            end_list = start[1:]

            if start_list == x:
                return 1 + count_whole(x, end_list)
            if type(start_list) == list:
                if start_list[0] == x:                  #if first value is another list
                    return 1 + count_whole(x, end_list)
                else:
                    return count_whole(x, end_list)
            else:
                return count_whole(x, end_list)


#x=2
x='a'
#x=4
s=[1, 4, 2, ['a', [[4], 3, 4]]]
print('Count, highest level:', count_outer(x,s))
print('Count, highest all levels:', count_whole(x,s))


#%%

def bricklek(f: str, t: str, h: str, n: int) -> str:
    """Ex7: Returns a string of instruction how to move the tiles """

    if n == 0:  #trivial solution
        return []
    if n == 1:   #direct move f->t if n = 1
        return [f + '->' + t]
    else:
        return (bricklek(f, h, t, n - 1) + [f + '->' + t] + bricklek(h, t, f, n - 1))


"Ger upprepade stegen: 'f->t','f->h','t->h' och sedan 'f->t','h->f','h->t'"

f = 'f'
t = 't'
h = 'h'
n = 3

print(bricklek(f,t,h,n))

#%%

#iterations = [e+1 for e in range(len(bricklek(f,t,h,n)))]
#it_sum = sum(iterations)/(60*60)  #hours


#%%
import time

def fib(n: int) -> int:

# A sequence of numbers starting with 0 and 1 and then each number is the sum of the two immediately preceding numbers
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)


def main():
    """ For Ex9: Returns the n:th Fibonacci number """
    # You should verify that the time for this function grows approximately as
    # Theta(1.618^n) and also estimate how long time the call fib(100) would take.
    # The time estimate for fib(100) should be in reasonable units (most certainly
    # years) and, since it is just an estimate, with no more than two digits precision.

    # a)
    start = []
    stop = []
    fib1 = 20
    fib2 = 25

    for i in range(fib1, fib2):
        start.append(time.perf_counter())
        fib(i)
        stop.append(time.perf_counter())


    dt_list = [stop[i]-start[i] for i in range(len(start))]
    t_growth = sum([dt_list[i+1]/dt_list[i] for i in range(len(start)-1)]) / (len(start)-1)

    print('Average time growth of fibonacci algoritm:', t_growth)


    # b)

    fib50 = fib(10) * 1.618**(40)  # n=50 - n=10 ==> n=40
    fib100 = fib(10) * 1.618**(90)


    print('Seconds, fib(50):',fib50)
    print('Years, fib(50):',fib50/(365*24*60*60))

    print('Seconds, fib(100):',fib100)
    print('Years, fib(100):',fib100/(365*24*60*60))



#%%

memory = {0: 0, 1: 1}

def fib_mem(n):
    if n not in memory:
        memory[n] = fib_mem(n - 1) + fib_mem(n - 2)
    return memory[n]

# Time for calculation of fib100
tstart = time.perf_counter()
fib_mem100 = fib_mem(100)
tstop = time.perf_counter()
t_tot = tstop-tstart

print('Fibonacci nr 100:', fib_mem100)
print('Time for Fibonacci nr 10 with memoization:', t_tot)



if __name__ == "__main__":
    main()

####################################################

"""
  Answers to the none-coding tasks
  ================================
  
  
  Exercise 8: Time for the tile game with 50 tiles:

    # n=2
    nr_it = -1+2^(4)
    # n=3
    nr_it = -1+2^(3)
    # n=4
    nr_it = -1+2^(4)
    
    ---> n=50: nr_it = 3,6 * 10^6 years
  
  
  
  Exercise 9: Time for Fibonacci:
    fib(50) = 399 years
    fib(100) = 11210439453081 years

  
  Exercise 10: Time for fib_mem:
  
  time for fib(100) = 57 micro*s.
  
  
  Exercise 11: Comparison sorting methods:
  
    Insertion: 
    t(n) = k*n^2   
    
    1 = k*1000^2 -> k = 1/10^6                        #k = "equalizing term" for same time for 1000 values
    n = 10^6 ==> (1/(10**6))*(10**6)**2 = 10^6 s = 12 days
    n = 10^9 ==> (1/(10**6))*(10**9)**2 = 10^12 s = 32 000 years
  
    Merge:
    t(n) = k*n*log(n)
    
    1 = k*1000*log(1000) -> k=1/3000
    n = 10^6 ==>  (1/3000) * 10**(6)*log(10**6) = 2000 s = 33 min
    n = 10^9 ==> (1/3000) * 10**(9)*log(10**9) = 3*10^6 s = 35 days
  
  
  
  Exercise 12: Comparison Theta(n) and Theta(n log n)
    
      Find c: 
      t(n) = c*n*log(n) 
      c = t(n)/(n*log(n))
      n = 10 ==> 1s -> c = 0.1
      
      Time for A: 
      A(n) = n
      Time for B:
      B(n) = 0.1*n*log(n)
      
      if t_A(n) = t_B(n), then:
      n = 0.1*n*log(n) ==> log(n) = 10 ==> n = 100
      
      =====> When n > 100 algoritm A takes less time than B
  
"""
