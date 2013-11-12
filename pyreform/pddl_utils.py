'''
Author: Andrew Probert (c) 2013
Contact: andrew.probert@auckland.ac.nz

Utility functions for handling strings and sets

-------

Copyright (C) 2013 Andrew Probert, University of Auckland

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

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

