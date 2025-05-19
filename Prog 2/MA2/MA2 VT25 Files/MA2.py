
""" linked_list.py

Student: Klara Asterland
Mail: klara.asterland.6081@student.uu.se
Reviewed by:
Date reviewed:
"""

class Person: #for Ex7
    def __init__(self, name, pnr):
        self.name = name
        self.pnr = pnr

    def __str__(self):
        return f"{self.name}:{self.pnr}"


    #----------------Added functions------------------#

    def __lt__(self,other): #larger than
        if self.pnr > other.pnr:     #compare phone numbers
            return self.pnr > other.pnr
        if self.pnr < other.pnr:
            return self.pnr < other.pnr


    def __le__(self,other): #larger or equal to
        if self.pnr >= other.pnr:     #compare first digits
            return self.pnr >= other.pnr
        else:
            return self.pnr >= other.pnr


    def __eq__(self,other): #equal to
        if self.pnr == other.pnr:
            return self.pnr == other.pnr
    #--------------------------------------------------#


class LinkedList: #This is the main class that represents the entire linked list

    class Node:
        def __init__(self, data, succ):
            self.data = data   #the value stored in the node
            self.succ = succ   #a reference to the next node in the list

    def __init__(self):
        self.first = None

    def __iter__(self):            # Discussed in the section on iterators and generators
        current = self.first
        while current:
            yield current.data   #yield acts as a return statement but next time the generator is called, it will continue where it left off.
            current = current.succ

    '''
    __iter__() is works similarly to doing:
    for value in linked_list:
        print(value)
    '''

    def __in__(self, x):           # Discussed in the section on operator overloading
        for d in self:
            if d == x:
                return True
            elif x < d:
                return False
        return False

    def insert(self, x):
        if self.first is None or x <= self.first.data:   # size comparison operator
            self.first = self.Node(x, self.first)
        else:
            f = self.first
            while f.succ and x > f.succ.data:
                f = f.succ
            f.succ = self.Node(x, f.succ)

    def print(self):
        print('(', end='')
        f = self.first
        while f:
            print(f.data, end='')
            f = f.succ
            if f:
                print(', ', end='')
        print(')')

#------------------------- To be implemented ----------------------#

    def length(self):          #   Ex1
        current = self.first  #current value = start value = None
        counter = 0

        while current:
            counter += 1
            current = current.succ #move to next node
        return counter

    def mean(self):
        current = self.first
        summa = 0

        while current:
            summa += current.data  #sum up node value
            current = current.succ #move to next node
        if self.length() == 0:
            return 0   #avoid zero division
        else:
            mean = summa/self.length()
            return mean

    def remove_last(self):       # Ex2
        current = self.first

        if self.length() == 0:  #if we have an empty list
            return ValueError

        if current.succ == None:   #if list has one element
            value = current
            current = None  #linked list is None
            return value

        while current.succ.succ != None:  #while the next node is the node before null, i.e. at the last node
            current = current.succ #move to next node

        r_l = current.succ.data #removed value
        current.succ = None #current.succ is after while-loop the last node
        return r_l


    def remove(self, x):         # Ex3

        current = self.first #first node
        prev = None #previous node to first, starts of as None
        first = []  #store first instance of x for comparison

        if self.length() == 0:  #if we have an empty list
            raise ValueError('Empty list')

        while current:  #while the next node is the node before null, i.e. at the last node
            if current.data == x:
                if current.data not in first:
                    first.append(current.data)
                    if prev is None: #if x is first value in linked list
                        self.first = current.succ #first value written over as succeeding value
                    else:
                        prev.succ = current.succ   #succeeding previous value is succeeding value in list, aka skip current value
                return True
            else:
                prev = current  # current node becomes previous node as we move to next node
                current = current.succ  # current node moves to succeeding node

        if len(first) == 0:  # without this I always get false
            return False
        else:
            return 'CodeError'


    def to_list(self):            # Ex4
        #Write a recursive method to_list (self) which returns a standard Python list with the values from the linked list in the same order
        def recurse(node): #inner recursive function to access node level
            if node is None:   #first value self.first
                return []
            else:
                current = node   #current node
                return [current.data] + recurse(current.succ)  #insert succeeding node to recurse function
        return recurse(self.first)


    def __str__(self):            # Ex5

        str_list = [str(x) for x in self]  #values to strings
        string = ', '.join(str_list)  #specify , and blankspace between elements in str_list

        return f'({string})' #adding () on sides

    def copy_1(self):
        result = LinkedList()    # will run for every x value to insert ==> len(x_list) = n iterations --> O(n)
        for x in self:   # O(n)
            result.insert(x)  # traverses all x values --> O(n)
        return result  #O(1)

    ''' Complexity for this implementation: O(n*n*n*1) = O(n^3)'''

    def copy(self):               # Ex6, Should be more efficient
        return [x for x in self]   # O(n) from iteration over x in self, O(n) from creating new list with n elements
    ''' Complexity for this implementation: O(n*n) = O(n^2)'''


#---------------------------------------------------------------#


def main():
    lst = LinkedList()
    for x in [1, 1, 1, 2, 3, 4, 2, 1, 9, 7]:
        lst.insert(x)
    lst.print()

    # Test code:
    print(f'Linked List length: {lst.length()}')
    print(f'Linked List mean: {lst.mean()}')
    print(f'Linked List removed last value: {lst.remove_last()}')
    lst.print()
    x = 7
    print(f'Linked List removed first instance of {x}: {lst.remove(x)}')
    lst.print()
    print(f'Linked list to standard list: {lst.to_list()}')
    print(f'Standard list to string: {lst.__str__()}')
    print(f'Copied, optimized, list: {lst.copy()}')  #only gives copy of values, not whole linked list object ??

    ## EX 7
    plist = LinkedList()  #New linked list

    p = Person('John', 1234567689)
    plist.insert(p)
    print(f'Person: {plist}')

    q = Person('Lisa', 987654321)
    plist.insert(q)
    print(f'Person: {plist}')


if __name__ == '__main__':
    main()