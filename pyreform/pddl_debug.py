'''
PDDL Merge and Translator - Debug Module

Author: Dr. Patricia Riddle @ 2013

Debug and Print functions/macros

'''

DEBUG = False

def _DEBUG(*args):

    if DEBUG: print str(args)[1:-1]

_D = _DEBUG


DOPRINT = True

def _PRINT(*args):

    if DOPRINT: print str(args)[1:-1]

_P = _PRINT
