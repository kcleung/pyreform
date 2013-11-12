'''
PDDL Merge and Translator - Reformulation Module

Author: Dr. Patricia Riddle @ 2013
Contact: pat@cs.auckland.ac.nz

Translates PDDL files using an automated planner in order to improve performance

This module contains functions used to reformulate the PDDL input files

-------

Copyright (C) 2013  Dr. Patricia Riddle, University of Auckland

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

import copy
import re
import sys
from pyparsing import nestedExpr

import pddl_typing
from pddl_debug import _DEBUG, _D
from pddl_debug import _PRINT, _P
import pddl_ancillary as ancillary
import pddl_globals as G


def changepredicates(predicates):
    if predicates == []:
        return []
    ans1 = changepredicates1(predicates[0])
    ans2 = changepredicates(predicates[1:])
    ans2.insert(0,ans1)
    return ans2

def changepredicates1(changepredicate):
    if not isinstance(G.savepredicate,list):
#        print "predicatescooby",changepredicate,"shaggy",savepredicate,"storage",storage,"predicate",predicate
        if changepredicate[0] == G.savepredicate or changepredicate[0] == G.predicate:
            return G.storage[1]
#            return predicates
        return changepredicate

#R
def checktypeof(mytype,othertype,ontology):
    #_PRINT("mytype",mytype,"othertype",othertype,"ontology",ontology)
    if ontology == []:
        return False
    type1 = ontology[0]
    #_PRINT("type1",type1)
    #_PRINT("type1[0]",type1[0])
    if mytype in type1[0] and othertype == type1[1]:
        #_PRINT("true")
        return True
    else:
        return checktypeof(mytype,othertype,ontology[1:])

#R
def remove_empty(new_counter_type):
    if new_counter_type == []:
        return []
    elif new_counter_type[0] == []:
        return remove_empty(new_counter_type[1:])
    else:
        temp = remove_empty(new_counter_type[1:])
        temp.insert(0,new_counter_type[0])
        return temp

#R
def make_listoflist(extra_list):
    #_PRINT("extra_list",extra_list)
    if extra_list == []:
        return []
    else:
        returnlist = make_listoflist(extra_list[1:])
        returnlist.insert(0,[extra_list[0]])
        return returnlist

#R
def flatten_new(counts):
    if counts == []:
        return []
    if isinstance(counts[0],list):
        temp = counts[0]
        return_list = flatten_new(counts[1:])
        return_list.insert(0,temp[-1])
        return return_list

#R
def insertinlist(firstitem,seconditem,myset,used):
    #global newfound
    #_PRINT("ssmyset",myset,"firstitem",firstitem,"seconditem",seconditem,"newfound",G.newfound)
    if myset == []:
        if G.newfound == False:
            newpair = [firstitem,seconditem]
            myset = [newpair]
            used.insert(0,firstitem)
            used.insert(0,seconditem)
            return myset
        else:
            return []
    first = insertinlist1(firstitem,seconditem,myset[0],used)
#    G.newfound = False
    second = insertinlist(firstitem,seconditem,myset[1:],used)
    #_PRINT("first",first)
    #_PRINT("second",second)
    if second == []:
        double = [first]
    else:
#        double = [first]
        second.insert(0,first)
        double = second
    #_PRINT("double",double)
    return double

#R
def insertinlist1(firstitem,seconditem,myset,used):
    #global newfound
    if firstitem in myset:
        if seconditem in myset:
            #_PRINT("here1",firstitem,seconditem,myset)
            G.newfound = True
            return myset
        else:
            myset.insert(0,seconditem)
            used.insert(0,seconditem)
            G.newfound=True
            return myset
    elif seconditem in myset:
        G.newfound=True
        myset.insert(0,firstitem)
        used.insert(0,firstitem)
    else:
#        newpair = [firstitem,seconditem]
#        myset.append(newpair)
#        used.insert(0,firstitem)
#        used.insert(0,seconditem)
        return myset

#R
def removeduplicates(lists,extra_list):
    #_PRINT("lists",lists,"extra_list",extra_list)
    final = []
    l = range(0,len(extra_list))
    for i in l:
        found = False
        m = range(0,len(lists))
        for j in m:
            temp = extra_list[i]
            #_PRINT("extra_list[i]",extra_list[i],"lists[j]",lists[j])
            if temp[0] in lists[j]:
                #_PRINT("yesy")
                found = True
        if found == False:
            final.insert(0,extra_list[i])
    #_PRINT("final",final)
    return final


#R
def returnothertypes(predicate,typeof):
    _DEBUG("predicate",predicate,"typeof",typeof)
    othertype = []
    l = range(1,len(predicate))
    for i in l:
          if (i % 3 == 0):
              _DEBUG("predicate[i]",predicate[i])
              if predicate[i] <> typeof:
                  othertype.insert(0,predicate[i])
    _DEBUG("othertype",othertype)
    return othertype


#R
def addnum(types):
    _DEBUG("kermit",types)
    types.insert(1,"object")
    types.insert(1,"-")
    types.insert(1,"num")
    _DEBUG("piggy",types)
    return types

#R
def find_object(item,original_objects):
    l = range(0,len(original_objects))
    for i in l:
        if item == original_objects[i]:
            return i


#R
def addbacktypes(new_objects,original_objects,typing):
    if new_objects == []:
        return []
    elif len(new_objects) == 1:
        index1 = find_object(new_objects[0],original_objects)
        _DEBUG("index1",index1)
        return_objects = [typing[index1]]
        return_objects.insert(0,"-")
        return_objects.insert(0,new_objects[0])
        return return_objects
    elif isinstance(new_objects[0],int) and isinstance(new_objects[1],int):
        _DEBUG("new_objects[0]",new_objects[0],"new_objects[1]",new_objects[1])
        return_objects = addbacktypes(new_objects[1:],original_objects,typing)
        return_objects.insert(0,new_objects[0])
        return return_objects
    elif isinstance(new_objects[0],int) and not isinstance(new_objects[1],int):
        _DEBUG("new_objects[0]",new_objects[0],"new_objects[1]",new_objects[1])
        return_objects = addbacktypes(new_objects[1:],original_objects,typing)
        return_objects.insert(0,"num")
        return_objects.insert(0,"-")
        return_objects.insert(0,new_objects[0])
        return return_objects
    else:
        index1 = find_object(new_objects[0],original_objects)
        index2 = find_object(new_objects[1],original_objects)
        _DEBUG("new_objects[0]",new_objects[0],"new_objects[1]",new_objects[1])
        _DEBUG("index1",index1,"index2",index2)
        if (typing[index1] != typing[index2]):
            return_objects = addbacktypes(new_objects[1:],original_objects,typing)
            return_objects.insert(0,typing[index1])
            return_objects.insert(0,"-")
            return_objects.insert(0,new_objects[0])
            return return_objects
        else:
            return_objects = addbacktypes(new_objects[1:],original_objects,typing)
            return_objects.insert(0,new_objects[0])
            return return_objects


#R
def maketype(lists,original_objects,typing):
    _DEBUG("maketypelists",lists)
    if isinstance(lists[0],list):
        return maketype(lists[0],original_objects,typing)
    else:
        l = range(0,len(original_objects))
        for i in l:
            _DEBUG("lists[0]",lists[0],"orig",original_objects[i])
            if lists[0] == original_objects[i]:
                _DEBUG("foundi",i,"type",typing[i])
                return typing[i]

#R
def return_places(typeof,counts,counter_type,original_list,typing,predicates,myobjects):
    #global new_predicate
    #global NEWPREDICATE
#    if debug == True:
    _DEBUG("return_places")
    _DEBUG("counts",counts)
    _DEBUG("counter_type",counter_type)
    _DEBUG("original_list",original_list)
    _DEBUG("typing",typing)
    _DEBUG("predicates",predicates)
    _DEBUG("typeof",typeof)
    makecountslist = []
    l = range(0,len(predicates))
    for i in l:
        _DEBUG("typeof",typeof,"predicates[i]",predicates[i])
        if typeof in predicates[i]:
            temp = predicates[i]
            if temp[0] <> G.savepredicate:
                _DEBUG("yesssssssssssssss")
                G.NEWPREDICATE = True
                G.new_predicate = temp[0]
#            if debug == True:
                _DEBUG("new_predicate",G.new_predicate)
                _DEBUG("length",len(predicates))
#%%%7
                othertype = returnothertypes(temp,typeof)
#            if len(predicates) == 7:
#                print "predicates[i]",predicates[i],"typeof",typeof
#                temp = predicates[i]
#                if temp[3] == typeof:
#                    print "temp[6]",temp[6]
#                    othertype = temp[6]
#            if debug == True:
                #_PRINT("othertype",othertype)
                if len(othertype) == 1:
                    realothertype = othertype[0]
                setofobjects = returnobjectset(realothertype,myobjects)
#            if debug == True:
                #_PRINT("setofobjects",setofobjects)
                #_PRINT("counts",counts)
                newcounts = flatten_new(counts)
#            if debug == True:
                #_PRINT("eeeenewcounts",newcounts)
                makecounts = pddl_typing.makecounts_type(newcounts,setofobjects)
#            if debug == True:
                #_PRINT("makecountas",makecounts)
                makecountslist.extend(makecounts)
    #_PRINT("makecountslist",makecountslist)
    return makecountslist

#R
def flatten(counts):
    _DEBUG("acounts",counts)
    if counts == []:
        return counts
    if isinstance(counts[0],list):
        if len(counts[0]) > 1:
            _DEBUG("ffffcounts[0]",counts[0])
            temp = counts[0]
            _DEBUG("temp",temp[1:])
            first = flatten(temp[1:])
            _DEBUG("first",first)
            second = flatten(counts[1:])
            _DEBUG("second",second)
            first.extend(second)
            return first
        else:
            first = flatten(counts[0])
            _DEBUG("first2",first)
            second = flatten(counts[1:])
            _DEBUG("second2",second)
            first.extend(second)
            _DEBUG("first4")
            return first
    else:
        first = counts[0]
        _DEBUG("first3",first)
        second = flatten(counts[1:])
        _DEBUG("second3",second)
        second.insert(0,first)
        _DEBUG("second4",second)
        return second

#R
def returnobjectset(othertype,myobjects):
    if myobjects == []:
        return []
#    if debug == True:
    _DEBUG("myobjects",myobjects)
    _DEBUG("othertype",othertype)
    l = range(0,len(myobjects))
    for i in l:
        #_PRINT("i",i,"myobjects[i]",myobjects[i])
        if myobjects[i] == "-":
#            if debug == True:
            _DEBUG("myobjects[i+1]",myobjects[i+1])
            if myobjects[i+1] == othertype or checktypeof(myobjects[i+1],othertype,G.ontology):         #must check if it is a type of type....need whole type list
                if i == 1:
                    temp = myobjects[0]
                    #_PRINT("importanta",temp,"really",myobjects)
                else:
#                    temp = myobjects[0:i-1]
                    temp = myobjects[0:i]                                          #important change
                    #_PRINT("importantb",temp,"really",myobjects)
                _DEBUG("temp",temp)
                temp2 = returnobjectset(othertype,myobjects[i+2:])
                temp2.insert(0,temp)
                return temp2
            else:
                return returnobjectset(othertype,myobjects[i+2:])
#R
def findmax(lists):
    if lists == []:
        return 0
    count = len(lists[0])
    return count + findmax(lists[1:])





#R
def inboth(list1,list2):                                                       #!returns a set of items that are in both lists
    _DEBUG("slw",list1,list2)
    ret_list = []
    if list2 == []:
        return list1
    for i in list1:
        for j in list2:
            if i == j:
                ret_list.insert(0,[i])
    return ret_list

#R
def completesets(lists,objects,init):                           #! this returns the complete set of objects that has to be change (includes singletons) - list is a list of lists
    _DEBUG("cup",lists)
    if lists == []:
        return lists
    if isinstance(lists[0],list):
        temp = completesets1(lists[0],objects,init)
        _DEBUG("temp",temp)
        temp2 = completesets(lists[1:],objects,init)
        _DEBUG("temp2",temp2)
        extra = inboth(temp,temp2)
        _DEBUG("extra",extra)
        return extra

#R
def completesets1(lists,objects,init):                         #! this returns the complete set of objects that has to be change (includes singletons) - lists is a list
    _DEBUG("reallists",lists)
    _DEBUG("objects",objects)
    _DEBUG("init",init)
    found = False
    type = False
    temp = []
    for i in lists:
        for k in init:
            _DEBUG("k",k,"i",i,"k1",k[1])
            if len(k) == 2 and k[1] == i:
                type = k[0]
                _DEBUG("type",type)
    for i in objects:
        for k in init:
            _DEBUG("k" , k)
            if len(k) > 1 and k[0] == type and k[1] == i:
                found = False
                _DEBUG("pirate",i)
                for j in lists:
                    if i == j:
                        found = True
                if found == False:
                    temp.insert(0,i)
    _DEBUG("NEWLIST",temp)
    return temp

#R
def remove_duplicates(seq):                                                  #!removes duplicates in a sequence          NOT USED CURRENTLY
    X = []
    for i in seq:
        if not i in X:
            X.append(i)
    return X

#R
def addobjects(new_objects,max_num):                                          #! adds new objects in (like numbers)
    _DEBUG("max_num",max_num)
    _DEBUG("new_objects",new_objects)
    l = range(0,max_num+1)
    for i in l:
        new_objects.insert(0,i)
    return new_objects

#R
def changeactions(lists,actions,num):                                     #! alters the actions to handle the new predicates, lists - list of objects, actions -list of actions
    _DEBUG("listsdebug",lists)
    _DEBUG("lists",lists)
    _DEBUG("actions",actions)
    if actions == []:
        return []
    firstaction = actions[0]
    newaction = changeactions1(lists,firstaction,num)
    _DEBUG("newaction",newaction)
    newactions = changeactions(lists,actions[1:],num) #why does this say list and not lists??? afraid to change -- doesn't actually use "lists" anywhere!!!
    _DEBUG("newactions",newactions)
    newactions.insert(0,newaction)
    _DEBUG("finalactions",newactions)
    _DEBUG("G.storage3a",G.storage3)
    return newactions

#R
def changeactions1(lists,firstaction,num):                         #! alters the action to handle the new predicates, lists - list of objects, firstaction - a single action
    #global storage2
    #global storage3
    
    #global new_predicate
    #global typeof

    
    #_DEBUG("new_predicate", G.new_predicate)
    
    if 'TYPING' in globals(): _PRINT("TYPING", G.TYPING)
    _DEBUG("reallyimportant", lists, firstaction)
    _PRINT("firstaction",firstaction)
    front1 = firstaction[0]
    _DEBUG("front1",front1)
    front2 = firstaction[1]
    _DEBUG("front",front2)
    param1 = firstaction[2]
    param2 = firstaction[3]
    _DEBUG("param",param1,param2)
    precond1 = firstaction[4]
    precond2 = firstaction[5]
    _PRINT("precond",precond2)
    effect1 = firstaction[6]
    effect2 = firstaction[7]
    _DEBUG("effect",effect2)
    _DEBUG("denny",firstaction)
    _PRINT("typeof",G.typeof)
    if (G.TYPING == False and checkprecond(precond2)) or (G.TYPING == True and pddl_typing.checkprecond_typing(precond2,firstaction,G.typeof)) or (G.TYPING == True and checkextra(precond2,firstaction,G.new_predicate)):
        G.storage2.insert(0,front2)
        #_PRINT("storage2", storage2)
        _DEBUG("YES")
        _DEBUG("precond2",precond2)
        _DEBUG("effect2",effect2)
        G.storage.insert(len(G.storage),front2)
        #_PRINT("storagec", storage)
        G.storage3.insert(len(G.storage3),front2)
        #_PRINT("storage3", storage3)
        _DEBUG("param2",param2)
        param3 =  ancillary.fixparam(param2, G.TYPING)                   #!removes typing if needed
        _DEBUG("param3",param3)
        G.storage3.insert(len(G.storage3),param3)
        #_PRINT("storage3", storage3)
        _DEBUG("debguparam3",G.storage3,"param3",param3)
        neweffect = changeeffect(effect2,0,firstaction)
        _DEBUG("debugG.storage3a",G.storage3)
        _DEBUG("neweffectbbbb",neweffect)
        _DEBUG("neweffect",neweffect)
        newprecond = changeprecond(precond2,front2,num,lists,firstaction)
        _DEBUG("debigstorage3b",G.storage3)
        _DEBUG("aaanewprecond",newprecond)
        new_param2 = copy.deepcopy(param2)
        newparam = changeparam(new_param2)
        _DEBUG("here1")
        _DEBUG("storage3b",G.storage3)
        return [front1,front2,param1,newparam,precond1,newprecond,effect1,neweffect]
#    elif (G.TYPING == True and checkextra(precond2,firstaction,newpredicate))
    _DEBUG("here2")
    return firstaction

#R
def changeparam(param):                                                   #! change the parameters on the actions (add ?num1 and ?num2)
    _DEBUG("totalnumber",G.totalnumber)
    l = range(0,G.totalnumber)
    if G.TYPING == True:
        param.insert(0,"num")
        param.insert(0,"-")
    for i in l:
        var = "?num" + str(i)
        param.insert(0, var)
    return param

#R
def changeeffect(effect,num,action):                                                 #! change the effect of the action by replacing old predicate with new predicate
    _DEBUG("storage",G.storage)
    _DEBUG("aaaeffect",effect,"num",num)
    #global direction
    #global var1
    #global var2
    #global totalnumber
    #global storage
    _DEBUG("effect",effect)
    if effect == []:
        return []
    if effect[0] == "and":
        neweffect = changeeffect(effect[1:],num,action)
        _DEBUG("neweffecta",neweffect)
        neweffect.insert(0,effect[0])
        return neweffect
    first=effect[0]
#    if debug == True:
#    print "aaafirst",first,"first[0]",first[0],"new_predicate",G.new_predicate,"NEWPREDICATE",G.NEWPREDICATE
#    tester = pddl_typing.checkprecond_typing2(first,action,G.typeof)
#    print "DDDDDebug",first,"action",action,"typeof",G.typeof,"truth",tester
    _DEBUG("TYPING:",G.TYPING)
    _DEBUG("HELPfirst", first, "predicate", G.predicate)
    if ((first[0] == G.predicate or (G.NEWPREDICATE == True and first[0] == G.new_predicate)) and (G.TYPING == False or pddl_typing.checkprecond_typing2(first,action,G.typeof))):        #current bug need to look through list of rpedicates????
        _DEBUG("yesy")
        number = num + 1
        newvar1 = "?num" + str(number)
        temp1 = ["count1a1a", first[1] , first[2], newvar1] #! changed these
###        G.storage.insert(len(G.storage),first[0])
#        G.storage.insert(len(G.storage),first[1])
#        G.storage.insert(len(G.storage),first[2])
#        stor1 = ["not" ,  temp1]
#        G.storage.insert(len(G.storage),stor1)
        _DEBUG("yea",temp1)
        G.direction.insert(len(G.direction),"up")
        G.var1 = first[1]
        G.var2 = first[2]
        _DEBUG("var1",G.var1)
        newvar2 = "?num" + str(num)
        temp3 = ["count1a1a", first[1] , first[2], newvar2]
        temp2 = ["not"]
#        G.storage.insert(len(G.storage),temp2[0])
#        G.storage.insert(len(G.storage),first[0])
#        G.storage.insert(len(G.storage),first[1])
#        G.storage.insert(len(G.storage),first[2])
        G.storage.insert(len(G.storage),temp3)
        #_PRINT("storage", storage)
        temp2.append(temp3)
        num = num + 2
        if num > G.totalnumber:
            G.totalnumber = num
        neweffect = changeeffect(effect[1:],num,action)
        _DEBUG("neweffectb",neweffect)
        neweffect.insert(0,temp1)
        neweffect.insert(0,temp2)
        return neweffect
    elif first[0] == "not":
        _DEBUG("here",first[0])
        temp = first[1]
        _DEBUG("temp",temp[0],G.predicate)
        if (temp[0] == G.predicate) or (G.NEWPREDICATE == True and temp[0] == G.new_predicate):
            _DEBUG("EVER")
            number = num + 1
            newvar1 = "?num" + str(number)
            temp1 = ["count1a1a", temp[1] , temp[2], newvar1]
#            G.storage.insert(len(G.storage),temp[0])
#            G.storage.insert(len(G.storage),temp[1])
#            G.storage.insert(len(G.storage),temp[2])
            stor2 = [ "not" , temp1]
#            G.storage.insert(len(G.storage),stor2)
            G.direction.insert(len(G.direction),"down")
            G.var1 = temp[1]
            G.var2 = temp[2]
            _DEBUG("var",G.var1,G.var2)
            newvar2 = "?num" + str(num)
            temp3 = ["count1a1a", temp[1], temp[2], newvar2]
            temp2 = ["not"]
#            G.storage.insert(len(G.storage),temp2[0])
#            G.storage.insert(len(G.storage),temp[0])
#            G.storage.insert(len(G.storage),temp[1])
#            G.storage.insert(len(G.storage),temp[2])
            G.storage.insert(len(G.storage),temp3)
            #_PRINT("storagea", storage)
            temp2.append(temp3)
            num = num + 2
            if num > G.totalnumber:
                G.totalnumber = num
            neweffect = changeeffect(effect[1:],num,action)
            _DEBUG("neweffectc",neweffect)
            neweffect.insert(0,temp1)
            neweffect.insert(0,temp2)
            return neweffect
        else:
            neweffect = changeeffect(effect[1:],num,action)
            neweffect.insert(0,first)
            return neweffect
    else:
        neweffect = changeeffect(effect[1:],num,action)
        neweffect.insert(0,first)
        return neweffect

#R
def changeprecond1(precond,action,num):                                                        #! change precondition of the action by replacing old predicate with new predicate
    _DEBUG("num",num)
    number = 0
    #global direction
    _DEBUG("aaaprecond",precond,"direction",G.direction)
    ans = []
    _DEBUG("precond",precond)
    if precond == []:
        return []
    l = range(0,len(G.storage))
    _DEBUG("DDDG.storage",G.storage,"l",l,"action",action)
    for i in l:
        _DEBUG("i",i,"G.storage[i]",G.storage[i],"action",action,"l",l)
        if G.storage[i] == action:
            j = range(i+1,len(G.storage))
            _DEBUG("j",j)
            count = 0
            for k in j:
                _DEBUG("G.storage[k]",G.storage[k],"k",k)
                if isinstance(G.storage[k], list):
                    _DEBUG("G.storage[k]",G.storage[k])
                    ans.insert(0,G.storage[k])
                _DEBUG("ans",ans)
                count = count +1
            m = range(0,count)
            _DEBUG("aaacount",count,"m",m)
            for n in m:
                _DEBUG("aaadirection",G.direction,"num",num[0])
                num1 = "?num" + str(number)
                num2 = "?num" + str(number+1)
                _DEBUG("num1",num1,"num2",num2)
                if G.direction[num[0]] == "up":
                    temp2 = ["more", num1, num2]
                else:
                    temp2 = ["more", num2, num1]
                num[0] = num[0] + 1
                number = number +2
                ans.insert(0,temp2)
            return ans

#R
def changeprecond(precond,actionname,num,lists,action):
    if precond == []:
        return []
    if precond[0] == "and":
        newprecond = changeprecond(precond[1:],actionname,num,lists,action)
        extra = changeprecond1(precond,actionname,num)
        newprecond.extend(extra)
        newprecond.insert(0,precond[0])
#        if debug == True:
#            print "newprecond",newprecond
#        print "aaaaG.storage",G.storage
#        num1 = "?num" + str(num)
#        temp1 = ["count1a1a", G.var1 , var2 , num1]            #%%%%have to fix this for nomys
#        if debug == True:
#            print "temp1",temp1
#        if G.direction[0] == "up":
#            temp2 = ["more", "?num0", "?num1"]
#        else:
#            temp2 = ["more", "?num1", "?num0"]
#        G.direction = G.direction[1:]
#        newprecond.insert(0,temp1)
#        newprecond.insert(0,temp2)
#        newprecond.insert(0,precond[0])
        return newprecond
    first=precond[0]
    newlist = flatten(lists)
    if ((first[0] == G.predicate or (G.NEWPREDICATE == True and first[0] == G.new_predicate)) and (G.TYPING == False or pddl_typing.checkprecond_typing2(precond[0],action,G.typeof))):
        newprecond = changeprecond(precond[1:],actionname,num,lists,action)
        return newprecond
    else:
        newprecond = changeprecond(precond[1:],actionname,num,lists,action)
        newprecond.insert(0,first)
        return newprecond

#def hasmerged(first,lists):
#    print "DDD1first",first
#    if first == []:
#        return False
#    if first[0] in lists:
#        print "DDDfirst",first[0]
#        return True
#    hasmerged(first[1:],lists)

#R
def checkprecond(precond):                                       #! check whether "typeof" (type of variable we merged) is in this precondition "precond"
    _DEBUG("precond",precond)
#    if G.TYPING == False:
    l = range(0,len(precond))
    for i in l:
        if G.typeof in precond[i]:
            return True
    return False
#    else:
#        for i in prob_list2_real:                                                  #! break domain list into important pieces
#    if i[0] == ":objects":
#        objects1 = i

#R
def checkextra(precond2,firstaction,new_predicate):
    _PRINT("checkextraaaa")
    _DEBUG("precond2",precond2)
    _DEBUG("firstaction",firstaction)
    _DEBUG("new_predicate",new_predicate)
    if ((new_predicate in firstaction[5]) or (new_predicate in firstaction[7])):
        _PRINT("YESYES")
        return True
    return False


#R
def checkprecond(precond):                                       #! check whether "typeof" (type of variable we merged) is in this precondition "precond"
    _DEBUG("precond",precond)
    l = range(0,len(precond))
    for i in l:
        if G.typeof in precond[i]:
            return True
    return False

#R
def addgoals(mylist,counts,lists,new_init):                     #! add new goals to the goals description (0s and mores) - never use "lists" do not need

    #global new_goals
    
#    if debug == True:
    _DEBUG("addgoals",mylist,"counts",counts,"new_init",new_init)
    if counts == []:
        return new_init
    _DEBUG("mylistbrrrr",mylist)
    #_DEBUG("counter",counter)
    _DEBUG("counts",counts)
    _DEBUG("lists",lists)
    if 'new_goals' in globals(): _DEBUG("new_init",G.new_goals)
    if mylist == []:
        return []
    elif len(mylist) == 1:
        _DEBUG("mylist",mylist)
###        if len(counter) == 1:
#        print "simpson1",counter
#        if isinstance(counts, list) and isinstance(counts[0],list):
#            counter = counter[0]
#        print "simpson2",counter
        return addgoals1(mylist[0],counts[0],mylist[0],new_init)
#        elif isinstance(counter[0],list):
#            print "really?"
#            return addgoals1(mylist[0],counter[0],counts,mylist[0],new_init)
#        else:
#             return addgoals1(mylist[0],counter,counts,mylist[0],new_init)
    else:
#        if len(counter) == 1:
#            newer_init = addgoals1(mylist[0],counter,counts,mylist[0],new_init)
#            print "newer_init1",newer_init
#            return addgoals(mylist[1:],counter,counts,mylist[1:],newer_init)
#        else:
#        split = split_counter(counter)
#        print "split",split
        newer_init = addgoals1(mylist[0],counts[0],mylist[0],new_init)
        _DEBUG("newer_init2",newer_init)
        return addgoals(mylist[1:],counts[1:],mylist[1:],newer_init)

#R
def split_counter(mylist):                                                #! old function not used
    _DEBUG("mylist",mylist)
    newlist = split_counter1(mylist[0],mylist[1:])
    _DEBUG("newlist",newlist)
    return newlist

#R
def split_counter1(item,mylist):                                           #! old function not used
    if mylist == []:
        return [[item]]
    elif item == mylist[0]:
        new_list.insert(len(mylist[0]),mylist[0])
        _DEBUG("new1",new_list)
        new_list.append(split_counter1(item,mylist[1:]))
        _DEBUG("new2",new_list)
    elif item <> mylist[0]:
        new_list = split_counter1(item,[])
        new_list.extend( split_counter1(mylist[0],mylist[1:]))
        return new_list
#R
def numberinlist(mylist,item):                                             #! old function not used
    _DEBUG("never")
    _DEBUG("list",mylist)
    _DEBUG("item",item)
    count = 0
    for thing in mylist:
        if item == thing:
            count = count + 1
    return count

#R
def addgoals1(list,counts,lists,new_init):                                #! function which really adds goals counts contains list with "value", length = count, lists cotains objects to merge - "list" never used
    _DEBUG("garth",list,"counts",counts)
    _DEBUG("new_init",new_init)
    _DEBUG("length",len(counts))
    #_DEBUG("herman",counter)
    #_DEBUG("counter",counter)
    #_DEBUG("counter[0]", counter[0])
    _DEBUG("counts",counts)
    if counts == []:
        return []
    if len(counts) == 1:
 #1       string = counter[0] + "_count"
#        new_count = len(counts) + 1 alter to handle split gripper domain
#        new_count = numberinlist(counts,counter[0]) + 1
#        print "vampire",new_count
        new_list = ["count1a1a", lists[-1], counts[0], len(counts)]
        _DEBUG("frankin",new_list)
        _DEBUG("new",new_init[1])
        _DEBUG("newlist",new_list)
        temp = new_init[1].append(new_list)
        _DEBUG("temper",temp)
#!        l = range(0,len(counts)+1)
#!        for i in l:
#!            new_temp = ["more", i, i+1]
#!            new_init.append(new_temp)
#!        mytype = pddl_typing.find_type(counter[0],new_init)
#!        if debug == True: "mytype", mytype
#!        mylist = makelist(mytype,counter[0],new_init)
#!        if debug == True: "mylist", mylist
#!        if debug == True: "NEW_INIT",new_init
#!        temper = addzero(mylist,counter,lists[-1],new_init)
        #_DEBUG("DDDDONE",temper)
        _DEBUG("new_init333",new_init)
        return new_init
    else:
#        for each in counter:
#        print "each",each
#        new_count = numberinlist(counts,counter[0]) + 1
#        print "dracula",new_count
        new_list = ["count1a1a", lists[-1], counts[0], len(counts)]
        _DEBUG("stein",new_list)
        temp = new_init[1].append(new_list)
    _DEBUG("new_init444",new_init)
    return new_init
#        print "MUST"
#        if debug == True:
#            print "MUST EXTEND"

#R
def changegoal(myset,init,counter_type,old_vals):                                           #! stopped commenting here%%%%%
    _DEBUG("mymyset",myset,"init",init,"counter_type",counter_type)
    if myset == []:
        return init
    elif len(myset) == 1:
        return changegoal1(myset[0],init,counter_type,old_vals)
    else:
        new_goal = changegoal1(myset[0],init,counter_type,old_vals)
        counter_type.insert(len(counter_type),"merge")
        _DEBUG("NEW",new_goal)
        return changegoal(myset[1:],init,counter_type,old_vals) #! changed new_goal to init...not sure this is right

#R
def changegoal1(myset,init,counter_type,old_vals):
    _DEBUG("myset",myset)
    _DEBUG("init",init)
    _DEBUG("initkk",init)
    _DEBUG("myset",myset)
    if init == []:
        return init
    else:
        if (init[0] == ":goal"):
            _DEBUG("AA")
            newinit=[init[0]]
            temp1=init[1]
            temp2=temp1[0]
            _DEBUG("temp2",temp2)
            temp3 = [temp2]
            temp4 = changegoal1(myset,temp1[1:],counter_type,old_vals)
            _DEBUG("temp4",temp4)
            temp3.extend(temp4)
            _DEBUG("temp3",temp3)
            temp2 = [init[0], temp3]
            _DEBUG("TEMP2",temp2)
            _DEBUG("temp1",temp2)
            return temp2
        elif len(init[0]) == 2:
            _DEBUG("BB")
            temp = init[0]
            _DEBUG("TEMP",temp)
            l = range(0,len(myset)-1)
            for i  in l:
                if myset[i] in temp:
                    return changegoal1(myset,init[1:],counter_type,old_vals)
            newinit=[init[0]]
            _DEBUG("NEWINT",newint)
            newinit.extend(changegoal1(myset,init[1:],counter_type,old_vals))
            _DEBUG("newinit",newinit)
            return newinit
        elif len(init[0]) == 3:
            _DEBUG("Mike",init[0])
            _DEBUG("CC")
            temp = init[0]
            _DEBUG("temp",temp)
            _DEBUG("temp",temp)
#            l = range(0,len(myset)-1)
            l = range(0,len(myset))
            for i  in l:
                _DEBUG("myset[i]",myset[i])
                if myset[i] == temp[1]:
                    _DEBUG("here1",temp[2])
                    _DEBUG("counter_type",counter_type)
#                    counter_type = [counter_type]              ###need to make 2 lists for -pat without destorying original
                    counter_type.insert(len(counter_type),temp[2]) ##change to set
                    _DEBUG("aaaa",counter_type)
                    _DEBUG("counter_type",counter_type)
                    _DEBUG("countera", counter_type)
                    old_vals.insert(0,temp[1])
                elif myset[i] == temp[2]:
                    _DEBUG("here2",temp[1])
#                    counter_type = [counter_type]
                    counter_type.insert(len(counter_type),temp[1])
                    _DEBUG("bbbb",counter_type)
                    _DEBUG("counterb", counter_type)
                    old_vals.insert(0,temp[2])
            _DEBUG("call",init[1:])
#            counter_type = [counter_type]
            return changegoal1(myset,init[1:],counter_type,old_vals)
        elif len(init[0]) > 3:
            _DEBUG("MUST EXTEND")

#R
def semimatch(item,mylist):
    _DEBUG("item",item,"mylist",mylist)
    if mylist == []:
        return False
    matchee = mylist[0]
    _DEBUG("matchee",matchee)
    if len(matchee) > 3 and item[0] == matchee[0] and item[1] == matchee[1] and item[2] == matchee[2]:
        return True
    else:
        return semimatch(item,mylist[1:])

#R
def addzero(mylist,counter,mytype,new_init):
    if len(mylist) == 0:
        return new_init
    l = range(len(mylist))
    for i in l:
        _DEBUG("addzeromylist",mylist,"counter",counter,"mytype",mytype) #,"new_init",new_init
        _DEBUG("new_init",new_init)
        mylist2 = ["count1a1a",mytype, mylist[i] , "0"]
        _DEBUG("checklist",mylist2,"and",new_init)
        if semimatch(mylist2,new_init) == False:
            new_init.append(mylist2)
        _DEBUG("newest",new_init)
    return new_init

#R
def makelist(mytype,counter,new_init):
    _DEBUG("new_initgg",new_init)
    _DEBUG("mytypegg",mytype)
    _DEBUG("counter",counter)
    if new_init == []:
        _DEBUG("AAAAA")
        return []
    elif  new_init[0] == ":init":
        _DEBUG("BBBBB")
        return makelist(mytype,counter,new_init[1:])
    elif len(new_init[0]) == 2:
        _DEBUG("CCCCC")
        temp = new_init[0]
        _DEBUG("temp",temp)
        if temp[0] == mytype:
            if temp[1] <> counter:
                _DEBUG("DDDDD")
                temp3 = makelist(mytype,counter,new_init[1:])
                _DEBUG("temp3",temp3)
                temp3.insert(0,temp[1])
                return temp3
            else:
                _DEBUG("EEEEE")
                return makelist(mytype,counter,new_init[1:])
        else:
            _DEBUG("FFFFF")
            return makelist(mytype,counter,new_init[1:])
    elif len(new_init[0]) >= 3:
        return makelist(mytype,counter,new_init[1:])



#R
def addinit(mylist,counts,lists,new_init,more_list,max_num):     ###must fix to only work with counts and not with counter at all   %%mylist and lists are the same!!!
    _DEBUG("lost",mylist,"counts",counts,"lists",lists,"new_init",new_init,"more_list",more_list)
    if mylist == []:
        return []
    elif len(mylist) == 1:
        _DEBUG("mylist",mylist)
        return addinit1(mylist[0],counts[0],mylist[0],new_init,more_list,max_num)
    else:
        newer_init = addinit1(mylist[0],counts[0],mylist[0],new_init,more_list,max_num)
        return addinit(mylist[1:],counts[1:],mylist[1:],newer_init,more_list,max_num)

#R
def addinit1(list,counts,lists,new_init,more_list,max_num):
    _DEBUG("list",list)
    #_DEBUG("counter",counter)
    _DEBUG("counts",counts)                    #counts are wrong for singletons????? why
    #_DEBUG("counter",counter)
    _DEBUG("lists",lists)
 #   global max_num
    #_DEBUG("counter",counter)
    #_DEBUG("counter[0]", counter[0])
    _DEBUG("counts",counts)
#!    if len(counts) == 1:
 #!       string = counter[0] + "_count"
    _DEBUG("testing")
#    new_count = len(counts)  #! + 1                         %%didn't work for gripper-pat3.pddl
    countlist = pddl_typing.makecounts(counts,lists,[])
    _DEBUG("thecount",countlist)
    new_init.extend(countlist)

    l = range(0,max_num)
    _DEBUG("set max")
#    max_num = len(counts)+2                                  #%dont see why this is right???
    for i in l:
        if not i in more_list:
            new_temp = ["more", i, i+1]
            more_list.insert(0,i)
            new_init.append(new_temp)
    mytype = pddl_typing.find_type(counts[0],new_init)                       #%%%problem with typing
    _DEBUG("mytype", mytype)
    mylist = makelist(mytype,counts[0],new_init)
    _DEBUG("mylist", mylist)
    _DEBUG("NEW_INIT",new_init)
    #_PRINT("mylist", mylist, "counts", counts[0], "lists", lists[-1], "real", lists)
    temper = addzero(mylist,counts[0],lists[-1],new_init)
    #_PRINT("temper", temper)
    _DEBUG("DDDDONE",temper)
    return temper
#else:
    _DEBUG("MUST EXTEND")


#R
def changeinit(myset,init,counter_type,old_vals):
    _DEBUG("called",myset)
    _DEBUG("myset",myset)
    if myset == []:
        return []
    elif len(myset) == 1:
        return changeinit1(myset[0],init,counter_type,old_vals)
    else:
        new_init = changeinit1(myset[0],init,counter_type,old_vals)
        old_counter_type = counter_type
        _DEBUG("old_counter_type1",old_counter_type)
        #        counter_type = []
#        temp = []
        _DEBUG("XXX1", counter_type)
        counter_type.insert(len(counter_type),"merge")
        _DEBUG("XXX2",counter_type)
        ans = changeinit(myset[1:],new_init,counter_type,old_vals)
#        print "temp",temp
#        counter_type.append(temp)
        _DEBUG("old_counter_type2",counter_type,"and",old_counter_type,"old_vlas",old_vals)
#        print "ans",ans
#        temp_counter = [counter_type]
#        counter_type = temp_counter
#        counter_type.append(old_counter_type)
        _DEBUG("old_counter_type3",counter_type,"old_vals",old_vals)
#        print "ans",ans
        return ans

#R
def changeinit1(myset,init,counter_type,old_vals):
    #global savepredicate
    _DEBUG("testcountertest",counter_type,"myset",myset,"init",init)
    _DEBUG("mysetco",myset)
    #global predicate
    #global typeof
    #global save_objects
    _DEBUG("init",init)
    if init == []:
        return init
    else:
        if (init[0] == ":init"):
            newinit=[init[0]]
            _DEBUG("init[0]",init[0],"init[1]",init[1])
            newinit.extend(changeinit1(myset,init[1:],counter_type,old_vals))
            return newinit #was newinit[0:-1]
        elif len(init[0]) == 2:
            temp = init[0]
            _DEBUG("temp12",temp)
            l = range(0,len(myset)-1)                    # change from -1 broke gripper%%%%%
            #_PRINT("typeofbug",myset,"temp",temp)
            for i  in l:
                #_PRINT("myset[i]",myset[i],"temp",temp)
                if myset[i] in temp:
                    #_PRINT("win",temp[0])
                    G.typeof = temp[0]
#                    if debug == True:
                    #_PRINT("typeof",G.typeof)
                    G.save_objects.insert(0,temp[1])
                    #_PRINT("save_objects",G.save_objects)
                    _DEBUG("typeof",G.typeof)
                    return changeinit1(myset,init[1:],counter_type,old_vals)
            newinit=[init[0]]
#            if debug == True:
            _DEBUG("uuuuuuinit[0]2",init[0])
            newinit.extend(changeinit1(myset,init[1:],counter_type,old_vals))
            _DEBUG("newinit",newinit)
            return newinit
        elif len(init[0]) == 3:
            temp = init[0]
            #_PRINT("important",temp)
#            G.predicate = temp[0]
#            print "PRED",G.predicate             ##current bug...need to store list of predicates
            #_DEBUG("predicate1",G.predicate)
            l = range(0,len(myset)) #!changed from l = range(0,len(myset)-1) might break gripper!!!!
            match=False
            insert=[]
            for i  in l:
                #_PRINT("i",i,"l",l)
                #_PRINT("myset",myset[i],"temp",temp[1],"temp",temp[2])
                if myset[i] == temp[1]:
                    G.predicate = temp[0]
                    G.savepredicate = temp[0]
                    #_PRINT("santa",temp[0])       #!maybe can set predicate here
#                    insert = [temp[2]]
#                    counter_type.insert(len(temp[2]),insert)
                    insert.insert(0,temp[2])
                    old_vals.insert(0,temp[1])
                    match=True
                elif myset[i] == temp[2]:
                    insert.insert(0,temp[2])
#                    insert = [temp[1]]
#                    counter_type.insert(len(temp[2]),insert)
                    old_vals.insert(0,temp[2])
                    match=True
            if insert <> []:
                #_PRINT("prob1")
                counter_type.append(insert[0])
            _DEBUG("VVVVV",counter_type)
            _DEBUG("match",match)
            if match == False:               #need to add singles to "lists" so they get turned into counts  **MUST have test first to not transform ALL singletons**
                    temp2 = [init[0]]
                    #_PRINT("hereherehere",temp2)
                    temp2.extend(changeinit1(myset,init[1:],counter_type,old_vals)) #!to fix logistics bug
                    return temp2
            return changeinit1(myset,init[1:],counter_type,old_vals)
        else:
            newinit=[init[0]]
            f = open("trace.txt", "a")
            f.write(str(sys._getframe()))
            f.write("\n\n")
            f.close()
            newinit.extend(changeinit1(myset,init[1:],counter_type,old_vals))
            return newinit
#!1 remove balls
#!2 remove at
#!3 add counter
#!4 add more

#R
def changeobjects(myset,objects): #! creates new object list
    _DEBUG("judy", myset)
    if myset == []:
        return objects
    _DEBUG("test",myset[0])
    _DEBUG("myset0a",myset[0])
    if isinstance(myset[0],list):
        _DEBUG("myset0b",myset[0])
        temp = changeobjects1(myset[0],objects)
        _DEBUG("jetson", temp)
        return changeobjects(myset[1:],temp)
    else:
        return changeobjects1(myset,objects)

#R
def changeobjects1(myset,objects): #! creates new object list
#!    if debug == True:
    _DEBUG("myset",myset)
    if myset == []:
        return objects
    elif len(myset) == 1:
        return objects
    else:
        _DEBUG("elroy",myset[0])
        _DEBUG("objects",objects)
        objects.remove(myset[0])
        return changeobjects1(myset[1:],objects)

#R
def returnsets(mylist,myset,used):
#    myset1 = returnsets1(mylist,myset,used)
    myset1 = returnsetsnew(mylist,myset,used)
    _DEBUG("fudd",myset1)
#    newmyset = returnsets1(mylist,myset1,used)
    newmyset = returnsetsnew(mylist,myset1,used)
    _DEBUG("buggs",newmyset)
    if len(mylist) > 1:
        myset2 = returnsets(mylist[1:],[],used)
        _DEBUG("daffy",myset2)
        if myset2 == []:
            return newmyset
        else:
            temp = [newmyset]
            temp.append(myset2)
            _DEBUG("tweety",temp)
            return temp
    else:
        return []

#R
def returnsetnew(mylist,myset,used):
    finalset = []
    l = range(0,len(mylist))
    for i in l:
#    myset1 = returnsets1(mylist,myset,used)
        myset1 = returnsetsnew(mylist[l:],myset,used)
        _DEBUG("fudd",myset1)
#    newmyset = returnsets1(mylist,myset1,used)
        newmyset = returnsetsnew(mylist[l:],myset1,used)
        _DEBUG("buggs",newmyset)
#    if len(mylist) > 1:
#        myset2 = returnsets(mylist[1:],[],used)
        _DEBUG("daffy",myset2)
#        if myset2 == []:
#            return newmyset
#        else:
#            temp = [newmyset]
#            temp.append(myset2)
#            if debug == True:
#                print "tweety",temp
#            return temp
#    else:
#        return []
        finalset.append(newmyset)
        #_PRINT("finalset",finalset)
    return finalset

#R
def notin(first,second,myset,used):
    #_PRINT("notin",first,second,myset,used)
    if first in used:
        return False
    elif second in used:
        return False
    else:
        l = range(0,len(myset))
        for i in l:
            if first in myset:
                return False
            if second in myset:
                return False
            if first in used:
                return False
            if second in used:
                return False
        return True

#R
def returnsetsnew(mylist,myset,used):
    #global newfound
    l = range(0,len(mylist))
    for i in l:
        firstlist = mylist[i]
        firstitem = firstlist[0]
        seconditem = firstlist[1]
        if myset == [] and firstitem not in used and seconditem not in used:
            myset = firstlist
            used.insert(0,firstitem)
            used.insert(0,seconditem)
        elif firstitem in myset:
            if (seconditem in myset or seconditem in used):
                fred = 4 #this does nothing
            else:
                myset.append(seconditem)
                used.insert(0,seconditem)
        elif (seconditem in myset and firstitem not in used):
            myset.append(firstitem)
            used.insert(0,firstitem)
        elif isinstance(myset[0],list):
            G.newfound = False
            #_PRINT("newfound",G.newfound)
            myset = insertinlist(firstitem,seconditem,myset,used)
            #_PRINT("kkkmyset",myset)
        elif notin(firstitem,seconditem,myset,used):
            if not isinstance(myset[0],list):
                #_PRINT("aaamyset",myset)
                mysetdouble = [myset]
#                mysettriple = [mysetdouble]
                mysetdouble.append([firstitem,seconditem])
                myset = mysetdouble
                #_PRINT("bbbmyset",myset)
            else:
                myset.append([firstitem,seconditem])
#            mysetdouble = [myset]
#            mysetdouble.append([firstitem,seconditem])
#            myset = mysetdouble
            used.insert(0,firstitem)
            used.insert(0,seconditem)
    return myset

#R
def returnsets1(mylist,myset,used):  #! must extend this to handle multiple sets
    _DEBUG("elmer",mylist,myset,used)
    if mylist == []:
        return myset
    _DEBUG("mylist",mylist)
    firstlist = mylist[0]
    _DEBUG("firstlist",firstlist)
    firstitem = firstlist[0]
    seconditem = firstlist[1]
    myset = returnsets1(mylist[1:],myset,used)
    _DEBUG("myset",myset)
    if myset == [] and firstitem not in used and seconditem not in used:
        _DEBUG("AA")
        _DEBUG("list", mylist[0])
        _DEBUG("listagain", firstlist)
        myset = firstlist
        used.insert(0,firstitem)
        used.insert(0,seconditem)
        _DEBUG("myset1",myset)
        return myset
    elif firstitem in myset:
        if (seconditem in myset or seconditem in used):
            _DEBUG("BB")
            _DEBUG("myset2",myset)
            return myset
        else:
            _DEBUG("CC")
            myset.append(seconditem)
            used.insert(0,seconditem)
            _DEBUG("myset3",myset)
            return myset
    elif (seconditem in myset and firstitem not in used):
        _DEBUG("DD")
        myset.append(firstitem)
        used.insert(0,firstitem)
        _DEBUG("myset4",myset)
        return myset
    else:
        _DEBUG("EE")
        _DEBUG("myset5",myset)
        return myset




#-------------------------------------------------------
#   Functions for Testing if Reformulation Required
#-------------------------------------------------------

#TR
def replace(old,new,listing):
#!    if debug == True: "replace", listing, "old", old, "new", new
    if type(listing) is str:
        if listing == old:
            return new
        else:
            return listing
    elif type(listing) is list:
#!        if debug == True: "yes"
        return [replace(old,new,x) for x in listing]
    else:
        return listing

#TR
def compare(list1,list2):
    same = True
    if len(list1) <> len(list2):
        same = False
    for i in range(len(list1)):
        if list1[i] <> list2[i]:
            same = False
    return same

#TR
def fun2(obj,mylist):                                                         #! returns the set of pairs of matching objects
    if mylist == []:
        return
#!    if debug == True: "mylist", mylist
    if obj in mylist:
#!        if debug == True: "HHHEERRREE3",mylist
        return mylist
    k=mylist[0]
#!    if debug == True: "k",k
    #! if debug == True: "list",mylist[1]
    if isinstance(k, (list, tuple)):
#!        if debug == True: "obj",obj
#!        if debug == True: "k", k
        if obj in k:
#!            if debug == True: "HHHEERRREE2",mylist, "list", mylist[1:]
            return [k,mylist[1:]]
#!        if debug == True: "test2", obj,"k",k
        X = fun2(obj,k)
        if X is not None:
            return X
#!    if debug == True: "obj",obj,"mylist",mylist
    return fun2(obj,mylist[1:])

#TR
def fun(obj,mylist):                                                           #! reutrns true if obj occurs in mylist (which is a nexted list structure)
#!    if debug == True: "mylist", mylist
    if obj in mylist:
#!        if debug == True: "HHHEERRREE"
        return True
    for k in mylist:
        if isinstance(k, (list, tuple)):
#!            if debug == True: "obj",obj
#!            if debug == True: "k", k
            if fun(obj,k):
#!               if debug == True: "PPUURRPPLLEE"
               return True

