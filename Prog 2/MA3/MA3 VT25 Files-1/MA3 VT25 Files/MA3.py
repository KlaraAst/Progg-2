""" MA3.py

Student: Klara Asterland
Mail: klara.asterland.6081@student.uu.se
Reviewed by:
Date reviewed:

"""
import random
import time
from functools import reduce

import matplotlib.pyplot as plt
import math as m
from math import pi, gamma
import numpy as np
from numpy import abs
import concurrent.futures as future
from statistics import mean 
from time import perf_counter as pc


# ------------------------------------------------------------------------------ #

def approximate_pi(n): # Ex1
    #n is the number of points
    # Write your code here
    r = 2 #m
    A_sq = 4 * r**2 #m^2 --> Area of square
    A_ci = pi * r*2 #m^2 --> Area of circle

    #since pi can be described by pi = 4*A_ci/A_sq, with a large nr of n we can describe pi as:
    #==> Sort which points are where:

    xpoint, ypoint = [random.uniform(-r,r) for x in range(n)], [random.uniform(-r,r) for y in range(n)]   #uniform = range of random float numbers

    xpoints_circle = []
    ypoints_circle = []
    xpoints_square = []
    ypoints_square = []


    for i in range(n):

        y = xpoint[i]**2 + ypoint[i]**2   #circle equation ==> accounts for both -2 and 2 coordinates

        if y <= 2*r:  #smaller or equal to diameter
            xpoints_circle.append(xpoint[i])
            ypoints_circle.append(ypoint[i])
        elif y > 2*r:
            xpoints_square.append(xpoint[i])
            ypoints_square.append(ypoint[i])
        else:
            print('Boundary Error')
            break

    plt.scatter(xpoints_circle, ypoints_circle, color='red')
    plt.xlabel('X')
    plt.ylabel('Y')

    plt.scatter(xpoints_square, ypoints_square, color='blue')
    #plt.show()

    pie_approx = 4*len(xpoints_circle)/(len(xpoints_square)+len(xpoints_circle)) # pie = 4 * n_c/(n_c + n_sq)

    return pie_approx


# ------------------------------------------------------------------------------ #


def sphere_volume(n, d): #Ex2, approximation
    #n is the number of points
    # d is the number of dimensions of the sphere

    r = 1

    '''
    – Comprehension
    – Lambda function
    – map()
    – functools.reduce()
    – filter()
    – zip()
    '''

    # List with sublists
    xpoints = [[random.uniform(-r,r) for x in range(d)] for i in range(n)]  #dimension = nr of numbers per zip(), n = nr of points

    '''
    - lambda: A small, anonymous function for when you need a short function for a single use
    - map: Applies a function to each item in an iterable (like a list)
    - reduce: Reduces an iterable to a single value by applying a function cumulatively
    '''

    def sph(n):   #calculates x1**2 + x2**2...+ xd**2
        # lambda takes the values in n into the single use function x iteratively through map
        # reduce adds 'right' and 'left' pairs from the result of map. map() gives iterative list
        return reduce(lambda a, b: a + b, map(lambda x: x ** 2, n))   # a,b = lambda parameters, : separates parameter list from expression a + b
        # first case: a = map(...)[0], b = map(...)[1] ==> a+b
        # second case: a = a + b, b = map(...)[2] ==> (a+b) + map(...)[2]  osv.

    # List comprehension
    sph_points = [sph(sublist) for sublist in xpoints if sph(sublist) <= 1]  #points in sphere
    all_points = n

    ## Creating enclosing "hyper cube" ##
    V_cube = (2*r)**d  #cube volume

    #Monte Carlo: V_sph = V_cube * n_sph/(n_sph + n_cube)
    V_sph = V_cube * (len(sph_points)/all_points)

    return V_sph



# ------------------------------------------------------------------------------ #

def hypersphere_exact(d): #Ex2, real value
    # d is the number of dimensions of the sphere

    #general
    #V_d = (r**d) * pi**(d/2) / (gamma(d/2 + 1))

    # r=1
    V_d = pi**(d/2) / (gamma(d/2 + 1))

    return V_d



# ------------------------------------------------------------------------------ #

#%%
'''
ProcessPoolExecutor runs your code in separate processes, each with its own Python interpreter.

### Parameters: ###

- max_workers: It is number of Process aka size of pool. If the value is None, then on Windows by default 61 process
 are created even if number of cores available is more than that.
 
- mp_context: It is the multiprocessing context, If None or empty then the default multiprocessing context is used.
 It allows user to control starting method.
 
- initializer: initializer takes a callable which is invoked on start of each worker Process.

- initargs: It’s a tuple of arguments passed to initializer.

'''


#Ex3: parallel code - parallelize for loop
def sphere_volume_parallel1(n,d,np=10):
    #n is the number of points
    # d is the number of dimensions of the sphere
    #np is the number of processes

    '''
    - Define a wrapper function that takes n and d as input.
    - Use executor.map() to distribute the tasks.
    - Collect the results.
    - Compare the time with sequential version.
    '''

    start = pc()
    with future.ProcessPoolExecutor() as exe:
        # I want to give the worker a function to run, not the result of running it. Using lambda without parameters passes
        # the function to exe.map() without running it immediately. n and d are already fixed from the outer scope, so no need to repeat or pass them dynamically.
        res = [exe.map(lambda _: sphere_volume(n,d),range(np))]  #range(np) triggers lambda 10 times, and when passed to exe.map these are run in parallell
    stop = pc()

    return stop-start   #parallell time


# ------------------------------------------------------------------------------ #


#Ex4: parallel code - parallelize actual computations by splitting data
def sphere_volume_parallel2(n,d,np=10):
    #n is the number of points
    # d is the number of dimensions of the sphere
    #np is the number of processes

    # Parallelize computations by splitting nr of points instead of repetitions. We get the sum of sub-volumes from each chunk

    start = pc()
    with future.ProcessPoolExecutor() as exe:
        n_split = n // np   #whole value split of total datapoints into 10 different sub-point lists
        res = [exe.map(lambda _: sphere_volume(n_split,d),range(np))]   #runs sub-lists of points np(=10) times
    stop = pc()

    return stop-start




def main():
    #Ex1

    print('Small n Vol: ', sphere_volume(10, 3))
    print('Large n Vol: ', sphere_volume(10000, 3))

    dots = [1000, 10000, 100000]
    for n in dots:
        approximate_pi(n)

    #Ex2
    n = 100000
    d = 2
    sphere_volume(n,d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)}")

    n = 100000
    d = 11
    sphere_volume(n,d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)}")

    #Ex3
    n = 100000
    d = 11
    start = pc()
    for y in range (10):
        sphere_volume(n,d)
    stop = pc()
    print(f"Ex3: Sequential time of {d} and {n}: {stop-start}")
    print("What is parallel time?")
    print(f'The parallel processing time of splitting processes is: {sphere_volume_parallel1(n,d,np=10)} s.')

    #Ex4
    n = 1000000
    d = 11
    start = pc()
    sphere_volume(n,d)
    stop = pc()
    print(f"Ex4: Sequential time of {d} and {n}: {stop-start}")
    print("What is parallel time?")
    print(f'The parallel processing time of splitting number of points is: {sphere_volume_parallel2(n, d, np=10)} s.')




if __name__ == '__main__':
	main()
