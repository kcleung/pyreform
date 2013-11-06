'''
PDDL Merge and Translator - Ancillary Functions

Author: Dr. Patricia Riddle @ 2013

Translates PDDL files using an automated planner in order to improve performance

Functions used by the other modules
'''

from pddl_debug import _DEBUG, _D
from pddl_debug import _PRINT, _P
import pddl_globals as G


#R PP
def fixparam(param, TYPING):
    newparam = []
    _DEBUG("debugparam",param)
    if TYPING == True:
        newparam.insert(0,param[0])
        l = range(1,len(param))
        for i in l:
#            if i % 3 == 0:
#                newparam.insert(len(param),param[i])
            temp = param[i]
            if temp[0] == "?":
                newparam.insert(len(newparam),param[i])
    else:
        newparam=param
    _DEBUG("debugnewparam",newparam)
    return newparam

#TR R WO
def tostring(old):
    _DEBUG("old1",old)
#!    if debug == True:  len, len(old)
    if old == []:
        return ''
#!    if debug == True: "old2", old[0]
    if type(old) is str:
        return old
    if type(old) is int:
        return str(old)
    if type(old) is list:
        l = range(0,len(old))
        string = "(" + " "
        for i in l:
            string += tostring(old[i]) + " "
        return string + ")"


#!    if old == []:
#!        return ''
#!    if type(old) is str:
#!        if debug == True: "old2",old
#!        return str(old)
#!    elif type(old) is list:
#!        if debug == True: "pink"
#!        if debug == True: "len", len(old)
#!        if debug == True: "old0", old[0]
#!        if len(old) == 3: #! and len(old) == 1: #! changed from old to old[0]....changed back because losing information!!!...change to 3
#!            if debug == True: "grey"
#!            return "(" + " " + tostring(old[0]) + " " ")"
#!        elif len(old(0)) == 1 and len(old) == 3:
#!                     if debug == True: "black"
#!                     return "(" + " " + old[0] + " " + old[1] + " " + old[2] + " " + ")"
#!        elif len(old) == 1:
#!                 if debug == True: "red"
#!                 return "(" + " " + old[0] + " " ")"
#!
#!        temp = old[0]
#!        if debug == True: "temp",temp
#!        if type(old[0]) is list:
#!            if debug == True: "purple"
#!            return   str(tostring(old[0])) + str(tostring(old[1:]))
#!        elif type(old[0]) is str:
#!            if debug == True: "doublehere"
#!            if type(old[1]) is list:
#!                if debug == True: "here"
#!                A = old[0]
#!                if debug == True: "A",A
#!                B = tostring(old[1:])
#!                if debug == True: "B",B
#!                if debug == True: "A",A
#!                return  "(" + " " + A + " " +  " " + B + " " + ")"
#!            elif len(old) > 3 and type(old[1]) is str and type(old[2]) is str:
#!                if debug == True: "three"
#!                return "(" + old[0] + " " + old[1] + " " + tostring(old[2:]) + ")"
#!            elif len(old) > 2 and type(old[1]) is str and type(old[2]) is str:
#!                if debug == True: "five"
#!                return "(" + old[0] + " " + old[1] + " " + old[2] + ")"
#!            else:
#!                if debug == True: "four"
#!                A =  old[0]
#!                if debug == True: "AA",A
#!                B =  tostring(old[1])
#!                if debug == True: "BB",B
#!                return "(" + " " + A + " " + B + " " + ")"
