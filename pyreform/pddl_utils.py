'''
Author: Andrew Probert (c) 2013

Utility functions for handling strings and sets
'''

import sys
import math
import time

def strip(s): return str(s).strip()

def striparray(input):
    output = []
    for x in input : output.append(x.strip())    
    return output

def subsets(S):
    n = len(S)
    L = list(S)
    Ss = []
    for i in xrange(1,int(math.pow(2,n))):
        s = bin(i).partition('b')[2].zfill(n)
        subset = set([])
        for j in range(0,n+1):
            if s[j:j+1]=='1':
                subset.add(L[j])
        Ss.append(subset)
    Ss.append(set([]))
    return Ss


def setToList(S, elementsAreStrings=False):
    if not elementsAreStrings:
        return sorted(list(S))
    Slist = []
    for s in S:
        Slist.append(str(s))
    return sorted(Slist)

def listToString(L):
    return str(L).replace("'", "").replace(", ", ",")  

def unrankSubset(S, r):

    sortedS = setToList(S)
    T = set([])

    for i in range(0, len(sortedS)+1):

        if r % 2 == 1:
            if i < len(sortedS):
                T.add(sortedS[i])
            
        r = r//2

    return T
        

def extractElements(E):
    elements = []
    for e in E:
        elements.append(str(e))
    return listToString(sorted(elements))[1:-1]

def append(L, l):
    for e in l: L.append(e)

def clock():
    if sys.platform.startswith('win'):
        return time.clock()
    elif sys.platform.startswith('linux'):
        return time.time()

