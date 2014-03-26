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
pGNU General Public License for more details.

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

def find_many_unary(myvar,new_init,count):
    new_count = find_many_unary1(myvar,new_init,count)
    if new_count > 1:
        return True
    return False

def find_many_unary1(myvar,new_init,count):
    if new_init <> []:
        new_count = find_many_unary2(myvar,new_init[0],count)
        newer_count = find_many_unary1(myvar,new_init[1:],new_count)
        return newer_count
    return count

def find_many_unary2(myvar,pred,count):
    print "pred", pred
    if myvar in pred and len(pred) == 2:
        print "count",count
        count += 1
        print "count2",count
    return count

def remove_preds(myvar,new_init,preds):
    if new_init == []:
        return new_init
    else:
        new_pred = remove_preds1(myvar,new_init[0],preds)
        new_pred_lists = remove_preds(myvar,new_init[1:],preds)
        if new_pred <> []:
            new_pred_lists.insert(0,new_pred)
            return new_pred_lists
        return new_pred_lists

def remove_preds1(myvar,new_init,preds):
    if myvar in new_init: # and len(new_init) == 2:
        preds.insert(0,new_init)
        return []
    return new_init

def changeunary(lists,new_init,counter_type,old_vals,actions):
    print "lists",lists
    temp = lists[-1]
    myvar = temp[-1]
    print "mymymyvar",myvar
    print "new_init",new_init
    count = 0
    if find_many_unary(myvar,new_init,count):
        print "fred"
        preds = []
        print "new_init"
        new_init = remove_preds(myvar,new_init,preds)
        print "new_init9",new_init
        print "preds",preds
        G.unary_preds = preds
        return new_init
    return new_init

def changepredicates(predicates):
    if predicates == []:
        return []
    ans1 = changepredicates1(predicates[0])
    print "ans1",ans1
    ans2 = changepredicates(predicates[1:])
    print "ans2",ans2
    ans2.insert(0,ans1)
    return ans2

def changepredicates1(changepredicate):
    print "changepredicate",changepredicate
    print "G.savepredicate",G.savepredicate
    print "G.predicate",G.predicate
    print "G.storage",G.storage[1]
    if not isinstance(G.savepredicate,list):
        print "googly"
#        print "predicatescooby",changepredicate,"shaggy",savepredicate,"storage",storage,"predicate",predicate
        if changepredicate[0] == G.savepredicate or changepredicate[0] == G.predicate:
            return G.storage[1]
#            return predicates
        return changepredicate
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
    location = 999
    l = range(0,len(types))
    for i in l:
        print "types[i]",types[i]
        if types[i] == "object":
            location = i
    print "location",location
    if location <> 999:
        types.insert(location-2,"num")
        print "types",types
    else:
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
    print "predicates",predicates
    print "typeof", typeof
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
            print "temp",temp
            if temp[0] <> G.savepredicate:
                _DEBUG("yesssssssssssssss")
                G.NEWPREDICATE = True
                G.new_predicate = temp[0]
                print "valuehere","G.new_predicate",G.new_predicate
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
    print "fmlists",lists
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

def find_biggest_num(new_objects):
    l = range(0,len(new_objects))
    for i in l:
        if isinstance(new_objects[i],int):
            return(new_objects[i],i)

def addobjects_check(new_objects,max_num):
    l = range(0,max_num+1)
    print"new_objects",new_objects
    print "l",l
    big_num, location = find_biggest_num(new_objects)
    for i in l:
        print i
        print "new_objects",new_objects
        if i > big_num:
            new_objects.insert(location,i)
    return new_objects


def addobjectsextra(temp_objects,max_num,predicates,predicate_done):
    print "temp_objectsrrr",temp_objects
    print "max_num",max_num
    print "G.save_unary_predicates",predicates
    if len(predicates) == 1:
        new_temp = addobjectsextra1(temp_objects,max_num,predicates[0],predicate_done)
        return new_temp
    else:
        new_temp = addobjectsextra1(temp_objects,max_num,predicates[0],predicate_done)
        new_temp  = addobjectsextra(new_temp,max_num,predicates[1:],predicate_done)
        return new_temp
    
def extranos(objects):
    print "zzobjects", objects
    print "G.extra_nos",G.extra_nos
    return extranos1(G.extra_nos,objects)

def extranos1(extranos,objects):
    if extranos == []:
        return objects
    new_objects = extranos2(extranos[0],objects)
    return extranos1(extranos[1:],new_objects)

def extranos2(extranos,objects):
    print "extranos",extranos,"objects",objects
    l = range(0,len(objects))
    for i in l:
        print "object[i]",objects[i],"extranos[0]",extranos[0]
        if objects[i] == extranos[0]:
            objects.insert(i-2,extranos[1])
            return objects
    print "objectsz",object
    objects.insert(1,extranos[0])
    objects.insert(1,"-")
    objects.insert(1,extranos[1])
    return objects

def find_predicate(predicates,new_variables):
    if new_variables == []:
        return []
    else:
        first = new_variables[0]
        name = first[0]
        if predicates == name:
            mypair = first[2]
            return (first[1],mypair[0],mypair[1])
        return find_predicate(predicates,new_variables[1:])
    

def addobjectsextra1(temp_objects,max_num,predicates,predicate_done):
    print "tttemp",temp_objects
    print "predicates",predicates
    print "G.new_variables",G.new_variables
    if predicates == []:
        return []
    if predicates[0] in predicate_done:
        return temp_objects
    else:
        predicate_done.insert(0,predicates[0])
        sign_type, val1, val2 = find_predicate(predicates[0],G.new_variables)
#        sign_type = "signtype" + str(sign_count)
        temp_objects.insert(1,sign_type)
        temp_objects.insert(1,"-")
#        pred_name = predicates[0]
#        pred_type = pred_name[:2] + str(sign_count)
        temp_objects.insert(1,val1)
#        no = "no" + str(sign_count)
        temp_objects.insert(1,val2)
#        sign_count = sign_count + 1
        print "temp_objects",temp_objects
        return temp_objects
        

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
    print "calists",lists
    if lists == []:
        return actions
    if isinstance(lists[0],list):
        actions1 = changeactionsa(lists[0],actions,num)
        newactions1 = copy.deepcopy(actions1)
        print "wwgothere",actions1,
        print "lists[0]",lists[0]
        print "lists[1:]",lists[1:]
#        actions1 = add_additional_actions(actions1)
        print "zz?zz",newactions1
        return newactions1
#        return changeactions(lists[1:],actions1,num)              #1/12/14 desperate attempt to fix 
    return changeactionsa(lists,actions,num)

#def add_additional_actions(actions1):
#    print "G.additional_actions",G.additional_actions
#    actions1.extend(G.additional_actions)
#    return actions1
#    dummy()

def changeactionsa(lists,actions,num):
    print "loopylists",lists
    _DEBUG("listsdebug",lists)
    _DEBUG("lists",lists)
    _DEBUG("actions",actions)
    if actions == []:
        return []
    firstaction = actions[0]
    newaction = changeactions1(lists,firstaction,num)
    print "testaz",newaction
    action_messes_up = copy.deepcopy(newaction)
    print "aamesses",action_messes_up
    _DEBUG("newaction",newaction)
    if G.additional_actions <> []:
        print "wcritical",actions
        actions.extend(G.additional_actions)   #1/12/14 critical - changed to extend
        print "zcritical",actions
        G.additional_actions = []
    newactions = changeactionsa(lists,actions[1:],num) #why does this say list and not lists??? afraid to change -- doesn't actually use "lists" anywhere!!! #1/9 added "a"
    print "zzgothere"
    _DEBUG("newactions",newactions)
    print "testazz",newaction

#    newactions.insert(0,newaction)
    print "bbmesses",action_messes_up
    if G.unary_big != []:
        new_action_messes_up = split_in_four(action_messes_up)
        print "zzmesses",new_action_messes_up
    else:
        new_action_messes_up = [action_messes_up]
    newactions.extend(new_action_messes_up)
    newnewactions = copy.deepcopy(newactions)
    _DEBUG("finalactions",newactions)
    _DEBUG("G.storage3a",G.storage3)
    return newnewactions


def split_in_four(action):
    print "action_messes_up",action
    action1 = copy.deepcopy(action)
    action2 = copy.deepcopy(action1) 
    action3 = copy.deepcopy(action1) 
    action4 = copy.deepcopy(action1) 
    action1[1] = action1[1] + "1a"
    action1b, num, othernum, num2 = make_type1(action1)
    action1a = copy.deepcopy(action1b)
    print "action1a",action1a,"znum2",num2
    print "action",action
    if num2 == []:
        return [action]
    else:
        action2[1] = action2[1] + "1b"
        action2 = make_type2(action2,num,othernum)
        action3[1] = action3[1] + "2a"             
        action3 = make_type3(action3,num,num2)        
        action4[1] = action4[1] + "2b"             
        action4 = make_type4(action4,num,othernum,num2)        
        print "action1a",action1a
        print "action2",action2
        print "action3",action3
        print "action4",action4
        return [action1a, action2, action3, action4]
#    dummy()    #2/1/14 add here

def remove_params(mylist,params):
    print "mylist",mylist
    print "params",params
    if mylist == []:
        return params
    params = remove_params1(mylist[0],params)
    print "paramsaa",params
    return remove_params(mylist[1:],params)

def remove_params1(myitem,params):
    print "myitem",myitem
    print "params2",params
    l = range(0,len(params))                                                                           
    for i in l:
        if params[i] == myitem:
            temp = params[0:i]  #changed from i-1
            temp.extend(params[i+1:])
            return temp
    return params
     

def make_type3(action,num,num2):
    predicate = ["noteq1", num]
    print "predicate", predicate
    temp = action[5] 
    temp1, pred = remove_save_predicate(temp[1:],num2) 
    print "temp1",temp1
    print "pred",pred,pred[-1]
    temp1, other_num = remove_more(temp1,pred[-1])
    temp[1:] = temp1
    print "temp",temp
    print "pred",pred
    print "num2",num2,"other_num",other_num
    param = action[3]
    temp3 = [] + [num2] + [other_num]
    param = remove_params(temp3,param)
    print "paramzz",param
    action[3] = param
    print "G.save_objects",G.save_objects
    preds = multiple_pred(pred,len(list(set(G.save_objects)))+2)
    temp.insert(1,predicate)
    for i in preds:
        temp.insert(1,i) 
    print "temp", temp
    action[5] = temp
    print "action",action
    temp = action[7]
    print "aatemp",temp
    print "other_num",other_num
    alter_predicate(temp,other_num)
    print "zzaatemp",temp
    temp = remove_extra_predicate(temp,num,num2,other_num) #remove more with num (but not num from param only other num
    print "zzzztemp",temp
    action[7] = temp
    print "now",temp
    print "endaction",action
    return action

def remove_extra_predicate(temp,num,num2,other_num):
    print "zztempzz",temp,num,num2,other_num
    if temp == []:
        return []
    else:
        mytemp = G.unary_big[0]
        name = mytemp[0]
        temper1 = temp[0]
        if temper1[0] == "not": 
            temper = temper1[1]
            if temper[0] == name and temper[-1] == num2:
                return temp[1:]
            else:
                temper2 = remove_extra_predicate(temp[1:],num,num2,other_num)
                temper2.insert(0,temper1)
                return temper2
        else:
            temper2 = remove_extra_predicate(temp[1:],num,num2,other_num)
            temper2.insert(0,temper1)
            return temper2
    
def remove_more(temp,num):
    print "helptemp",temp
    print "helpnum",num
    if temp == []:
        return ([],[])
    else:
        pred = temp[0]
        if pred[0] == G.big_more[0] and pred[1] == num:
            return (temp[1:], pred[2])
        elif pred[0] == G.big_more[0] and  pred[2] == num:
            return (temp[1:], pred[1])
        else:
            temp, num = remove_more(temp[1:],num)
            temp.insert(0,pred)  #fixed this
            return (temp, num)

def alter_predicate(temp,other_num):
    if temp == []:
        return []
    else:
        pred = temp[0]
        mytemp = G.unary_big[0]
        name = mytemp[0]
        if pred[0] == name and pred[-1] == other_num:
            pred[-1] = 1
            return temp
        return alter_predicate(temp[1:],other_num)
            

def make_type4(action,num, other_num,num2):
    predicate = ["noteq1", num]  
    predicate2 = ["not", predicate]
    temp = action[7]
    temp1 = temp[1:]
    newtemp1 = remove_predicate(temp1,other_num)
    print "newtemp1",newtemp1
    temp[1:] = newtemp1
#    temp.insert(1,predicate2)
    print "aatemp", temp                                                                                    
    action[7] = temp
    temp2 = action[5]
    print "aatemp2",temp2  #has more num4 here
    temp3 = temp2[1:]
    print "temp3",temp3
    temp4, pred = remove_save_predicate(temp3,num2) ###MUST CHANGE THIS EVERYWHERE!!
    print "aatemp4",temp4  #lost more here
    print "pred",pred,pred[-1]
    temp4, other_num = remove_more(temp4,pred[-1])
    print "zztemp4",temp4
    param = action[3]
    temp7 = [] + [num2] + [other_num]
    param = remove_params(temp7,param)
    print "paramzz",param
    action[3] = param
    print "pred",pred
    print "G.save_objects",G.save_objects
    preds = multiple_pred(pred,len(list(set(G.save_objects)))+2)
    temp4.insert(1,predicate2)
    for i in preds:
        temp4.insert(1,i) 
    temp2[1:] = temp4
    action[5] = temp2
    
    temp = action[7]
    print "aatemp",temp
    print "other_num",other_num
    alter_predicate(temp,other_num)
    print "zzaatemp2",temp
    temp = remove_extra_predicate(temp,num,other_num,num2) #switched these around
    print "zzzztemp2",temp
    action[7] = temp
    print "now",temp
    print "action444",action  
    return action


def multiple_pred(pred,num):
    print "num",num
    predlist = []
    l = range(0,num)                                                                           
    for i in l:
        pred1 = copy.deepcopy(pred)
        pred1[-1] = i
        prednew = ["not", pred1]
        predlist.insert(0,prednew)
    return predlist

def make_type2(action,num, other_num):
    predicate = ["noteq1", num]  
    predicate2 = ["not", predicate]
    temp = action[7]
    temp1 = temp[1:]
    newtemp1 = remove_predicate(temp1,other_num)
    print "newtemp1",newtemp1
    temp[1:] = newtemp1
#    temp.insert(1,predicate2) #don't put ( not ( noteq1 ?num3 ) ) in effect
    print "temp", temp                                                                                    
    action[7] = temp
    temp2 = action[5]
    temp2.insert(1,predicate2)
    action[5] = temp2
    print "action",action  
    return action

def remove_save_predicate(temp,other_num):
    print "rptemp",temp
    temp1 = G.unary_big[0]  
    if temp == []:
        return ([], [])
    else:
        pred = temp[0]
        print "pred[0]",pred[0],"temp1[0]",temp1[0]
        print "pred[-1]",pred[-1],"other_num",other_num
        if pred[0] == temp1[0] and pred[-1] == other_num:
            return (remove_predicate(temp[1:],other_num), pred)
        else:
            ans, save_pred =  remove_save_predicate(temp[1:],other_num)  
            ans.insert(0,pred)
            return (ans, save_pred)


def remove_predicate(temp,other_num):
    print "rptemp",temp
    temp1 = G.unary_big[0]  
    if temp == []:
        return []
    else:
        pred = temp[0]
        print "pred[0]",pred[0],"temp1[0]",temp1[0]
        print "pred[-1]",pred[-1],"other_num",other_num
        if pred[0] == temp1[0] and pred[-1] == other_num:
            return remove_predicate(temp[1:],other_num)
        else:
            ans =  remove_predicate(temp[1:],other_num)  
            ans.insert(0,pred)
            return ans
        

def make_type1(action):
    nums = find_num(action)
    print "nums",nums
    num, other_num = going_down(nums,action)
    print "num",num
    if num in nums: nums.remove(num)
    predicate = ["noteq1", num]
    predicate1 = copy.deepcopy(predicate)
    print "predicate", predicate1
    temp = action[5] 
    temp.insert(1,predicate1)
    print "temp", temp
    action[5] = temp
    print "action",action
    if nums <> []:
        return action, num, other_num, nums[0]
    return action, num, other_num, nums


def going_down(nums,action):                                                                          
    temp = action[5] 
    num, other_num = going_down1(nums,temp[1:])  
    return (num, other_num)   

def going_down1(nums,action):
    if action == []:
        return ([], [])
    temp = action[0]
    print "temp0",temp[0]
    print "G.big_more[0]",G.big_more[0]
    if temp[0] == G.big_more[0]:
        if temp[2] in nums:
            return (temp[2], temp[1])
    return going_down1(nums,action[1:])

def find_num(action):
    temp = action[5]
    nums = find_num1(temp[1:])
    return nums

def find_num1(precond):
    if precond == []:
        return []
    else:
        temp = precond[0]
        temp1 = G.unary_big[0]
        if temp[0] == temp1[0]:
            num = temp[-1]
            numlist = find_num1(precond[1:])
            numlist.insert(0,num)
            return numlist
        return find_num1(precond[1:])

#R
def changeactions1(lists,firstaction,num):                         #! alters the action to handle the new predicates, lists - list of objects, firstaction - a single action
    print "critical",lists
    print "firstaction",firstaction
    print "num",num

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
    print "firstaction",firstaction
    print "precond2",precond2
    G.current_precond = precond2
    print "G.typeof",G.typeof
    print "new_predicate",G.new_predicate
    temp = G.bound_variables[0]
    print "num2zzz",G.typeof,temp[0],precond2
    if (G.TYPING == False and checkprecond(precond2)) or (G.TYPING == True and pddl_typing.checkprecond_typing(precond2,firstaction,G.typeof)) or (G.TYPING == True and checkextra(precond2,firstaction,G.new_predicate)) or (G.TYPING == True and pddl_typing.checkprecond_typing(precond2,firstaction,temp[0])):  #this is stopping the change of graspshaker and leaveshaker "with hand"
        print "num1zzz",firstaction,precond2
        G.storage2.insert(0,front2)
        #_PRINT("storage2", storage2)
        _DEBUG("YES")
        _DEBUG("precond2",precond2)
        _DEBUG("effect2",effect2)
        print "storage1",front2
        G.storage.insert(len(G.storage),front2)
        #_PRINT("storagec", storage)
        G.storage3.insert(len(G.storage3),front2)
        #_PRINT("storage3", storage3)
        _DEBUG("param2",param2)
        print "param2",param2
        param3 =  ancillary.fixparam(param2, G.TYPING)                   #!removes typing if needed
        print "param3",param3
        _DEBUG("param3",param3)
        G.storage3.insert(len(G.storage3),param3)
        #_PRINT("storage3", storage3)
        _DEBUG("debguparam3",G.storage3,"param3",param3)
        print "effect2",effect2
        if G.unary_preds <> []:
            neweffect, param2 = changeeffect_unary(effect2,firstaction,param2)
        else:
            neweffect = changeeffect(effect2,0,firstaction)
        print "aaneweffect",neweffect
        _DEBUG("debugG.storage3a",G.storage3)
        _DEBUG("neweffectbbbb",neweffect)
        _DEBUG("neweffect",neweffect)
        print "zzprecond2zz",precond2 #this is the new preconds here.....why?...should be old I think
        if precond2[0] <> "and":
            newprecond2 = ["and"] 
            newprecond2.append(precond2)
            print "newprecond2",newprecond2
            precond2 = newprecond2
        newprecond = changeprecond(precond2,front2,num,lists,firstaction,param2)
        print "zznewprecondzz",newprecond
        _DEBUG("debigstorage3b",G.storage3)
        _DEBUG("aaanewprecond",newprecond)
        new_param2 = copy.deepcopy(param2)
        newparam = changeparam(new_param2) #***use did_split
        _DEBUG("here1")
        _DEBUG("storage3b",G.storage3)
        return [front1,front2,param1,newparam,precond1,newprecond,effect1,neweffect]
#    elif (G.TYPING == True and checkextra(precond2,firstaction,newpredicate))
    _DEBUG("here2")
    return firstaction

def make_list_prednames(pred_list):
    if pred_list == []:
        return []
    else:
        mylist1 = make_list_prednames1(pred_list[0])
        mylist2 = make_list_prednames(pred_list[1:])
        mylist2.insert(0,mylist1)
        return mylist2
        
def make_list_prednames1(pred_list):
    return pred_list[0]

def changeeffect_unary(effect2,firstaction,param):
    G.totalnumber = 0
    G.removed_pred = []
    G.unary_more = []
    G.temporary_bindings = []
    G.newparam = param
    G.num_count = 0
    print "zzeffect2",effect2
    print "param",param
    print "firstaction",firstaction
    print "unary_preds",G.unary_preds
    print "added_goal",G.added_goal
    print "unary_new_preds",G.unary_new_preds
    print "save_unary_predicates",G.save_unary_predicates
    print "total_save_unary_predicates",G.total_save_unary_predicates
    print "all_preds",G.all_preds
    print "thetypes",G.thetypes
    prednames1 = list(set(make_list_prednames(G.total_save_unary_predicates)))                            #make list of predicate names
    prednames2 = list(set(make_list_prednames(G.all_preds)))
    G.removed_prednames = prednames2
    print "prednames1",prednames1
    print "prednames2",prednames2
    prednames2.extend(prednames1)
    prednames2 = list(set(prednames2))
    print "prednames1a",prednames1
    print "prednames2b",prednames2
    G.did_split = False
    if not split_test(param,G.thetypes):    #1) do split of actions
        print "nothere"
        G.did_spilt = True
        print "parambefore",param
        firstaction, param = fix_second_action(firstaction,param)
        print "paramafter",param
        print "G.additional_actions",G.additional_actions
    print "effect2",effect2
    neweffects = remove_bad_effects(prednames2,effect2,param)  #remove all bad ones 
    print "neweffectsa",neweffects
    print "removed",G.removed_pred 
#add code here to say that if removed_pred don't have variable skip add_big second_test
    G.store_big_effects = []
    if secondtest_loop(G.removed_pred,param):
        neweffects = add_big_effects(prednames2,G.removed_pred,neweffects,G.unary_big,G.all_preds,G.new_object_list,G.num_count,param) #2) use big if 1 unary  ***here I am***
#    else:
#        G.big_more = []
    print "neweffectsb",neweffects
#    dummy ()
    print "zzG.newparam",G.newparam
    print "G.temporary_binding1",G.temporary_bindings
    neweffects = add_singleton_effects(neweffects,G.unary_singleton,G.removed_pred,G.unary_singleton_removal,G.num_count ) #3) do mutiple passes (just those 3 passes abvoe)
    print "neweffectsc",neweffects
    print "G.temporary_binding2",G.temporary_bindings
    print "zzG.newparam",G.newparam
#    dummy()
    neweffects = add_goal_counter_effects(G.all_preds,neweffects,G.unary_goal_preds,G.removed_goals,G.removed_pred,G.num_count) #4) if big must also go goal counter
    print "firstaction",firstaction
    print "neweffectsd",neweffects
    G.store_effects = neweffects
    print "neweffects7",neweffects
#    dummy()
#    G.num_count = num_counter
    param = G.newparam
    return (neweffects, param)

def add_goal_counter_effects(all_preds,neweffects,unary_goal_preds,removed_goals,removed_pred,num_count):
    print "z1neweffects",neweffects
    print "z1all_preds",all_preds
    print "z1unary_goal_preds",unary_goal_preds
    print "removed_goals",removed_goals
    print "removed_predszaz",removed_pred
    cheat_goals =[ removed_goals[0]]
    temp = cheat_goals[0]
    G.goal_name = temp[0]
    neweffect = goal_match(unary_goal_preds,removed_pred,cheat_goals,G.num_count) #cheat for the moment only looking at 1 goal
    print "testhere",neweffect
    print "G.goal_more",G.goal_more
    if neweffect == []:
        G.goal_more = []
        return neweffects
    else:
        print "G.temporary_bindings",G.temporary_bindings
        print "wrong",neweffect
    #look in removed_goal and find contains
        goal_pred = removed_goals[0]
        print "goal_pred",goal_pred
    #look in all_preds and find contain
        goal_pred_type = find_pred(goal_pred[0],all_preds)
        print "goal_pred_type",goal_pred_type
        temp = G.unary_goal_preds[0]
        temp2 = [ temp[0] , goal_pred_type[-1]]
        G.unary_params.insert(0, temp2)
    #find 2nd variable type
        vartype = goal_pred_type[6] #should be more complicated than this not always trianry or second variable
    #look through param list and find variable name
        varname = goal_pred_type[4] #should be more complicated than this not always trianry or second variable  
    #look in temprary bindings and find variable
        print "G.temporary_bindings",G.temporary_bindings
#        variable = look_for_bound_variables0(varname,G.temporary_bindings)                1/16/14 removed from here down
#        print "evergood??variable",variable
#        print "varname",varname
#        print "G.patsfavorites",G.pats_favorite
#        print "G.newparam",G.newparam
#        print "G.temporary_bindings",G.temporary_bindings
    #replace in neweffect
    
#    if neweffect == []:
#        return neweffects
#    else:
#        print "neweffect",neweffect
#        term1 = neweffect[0]
#        print "term1",term1
#        term2 = neweffect[1]
#        print "term2",term2
#        if term1[0] == "not":
#            term4 = term1[1]
#            term4[2] = variable
#            term2[2] = variable
#        else:
#            term1[2] = variable
#            term3 = term2[1]
#            print "term3",term3
#            term3[2] = variable
#        neweffects[2] = variable
        print "neweffect",neweffect
#        dummy()
    
        neweffects.extend(neweffect) #changed to extend
        return neweffects

def find_pred(goal_pred,all_preds):
    l = range(0,len(all_preds))
    for i in l:
        temp = all_preds[i]
        if goal_pred == temp[0]:
            return temp
    return []

def goal_match(goal_preds,removed_preds,removed_goals,num_count):
    if removed_preds == []:
        return []
    else:
        effect = goal_match1(goal_preds,removed_preds[0],removed_goals,G.num_count)
        effectlist = goal_match(goal_preds,removed_preds[1:],removed_goals,G.num_count)
        print "effecta",effect
        print "effectlista",effectlist
        print "removed_preds",removed_preds
        if effect == []:
            return effectlist
        elif effectlist== []:
            return effect
        else:
            effectlist.extend(effect)  #changed 1/16/14
            return effectlist

def goal_match1(goal_preds,removed_preds,removed_goals,num_count):
    if removed_goals ==[]:
        return []
    else:
        effect = goal_match2(goal_preds,removed_preds,removed_goals[0],G.num_count)
        effectlist = goal_match1(goal_preds,removed_preds,removed_goals[1:],G.num_count)
        print "effectb",effect
        print "effectlistb",effectlist
        print "removed_preds",removed_preds
        if effect == []:
            return effectlist
        elif effectlist== []:
            return effect
        else:
            effectlist.extend(effect) #changed 1/16/14
            return effectlist

def goal_match2(goal_preds,removed_preds,removed_goals,num_count):
    print "zzgoal_predszz",goal_preds
    print "removed_preds",removed_preds
    print "removed_goals",removed_goals
    if removed_preds == []:
        return []
    elif removed_preds[0] == removed_goals[0]:
        print "zzremoved_preds[0]zz",removed_preds
        print "removed_goals[0]",removed_goals
        goal_temp = removed_preds[0]
#        variable1 = "?"+ "num" + str(G.variable_counter)
#        G.variable_counter = G.variable_counter + 1        
#        variable2 = "?"+ "num" + str(G.variable_counter)
#        G.variable_counter = G.variable_counter + 1        
        variable1 = "?"+ "num" + str(G.num_count)
        G.num_count = G.num_count + 1        
        variable2 = "?"+ "num" + str(G.num_count)
        G.num_count = G.num_count + 1        
        G.totalnumber = G.totalnumber + 2
        temptemp = removed_goals[1]
        print "removed_goals",removed_goals
        temp_more = ["more" + temptemp[:2]]                                #fixed these #fixed this 1/13/14 
        print "moreza",temp_more
        print "temptemp",temptemp
        G.goal_more = temp_more + [variable2] + [variable1]                ##1/16/14 tried switch these
        print "variable13",variable1
        print "goal_preds",goal_preds
        temp_goal_preds = goal_preds[0]
        important_variable = retrieve_from_big(G.store_big_effects,G.all_preds,G.removed_goals)
        print "imortant_variable",important_variable
        print "removed_goals",removed_goals                                  ##moust be same variable from big count ##$$$##    1/13/14???
        neweffect = temp_goal_preds[:2] + [important_variable] + [variable1]    ##must fix below as well
#        neweffect.insert(0,variable1)
#        neweffect.insert(0,removed_goals[2:])
#        neweffect.insert(0,goal_preds[:2])
        print "goal_preds",goal_preds
        print "removed_preds",removed_preds
        neweffect2 = temp_goal_preds[:2] + [important_variable] + [variable2]
#        neweffect2 = temp_goal_preds[:2] + removed_goals[2:] + [variable2]
        neweffect2not = [ "not", neweffect2]
        print "neweffect2is this right1",neweffect,neweffect2not
        return [neweffect, neweffect2not]
    elif removed_preds[0] == "not":
        temp = removed_preds[1]
        if temp[0] == removed_goals[0]:
            goal_temp = temp[0]
#            variable1 = "?"+ "num" + str(G.variable_counter)
#            G.variable_counter = G.variable_counter + 1        
#            variable2 = "?"+ "num" + str(G.variable_counter)
#            G.variable_counter = G.variable_counter + 1
            variable1 = "?"+ "num" + str(G.num_count)
            G.num_count = G.num_count + 1        
            variable2 = "?"+ "num" + str(G.num_count)
            G.num_count = G.num_count + 1
            G.totalnumber = G.totalnumber + 2
            print "removed_goals",removed_goals
            temptemp = removed_goals[1]                               #fixed this 1/13/14
            temp_more = ["more" + temptemp[:2]]
            print "temptemp",temptemp
            print "morezb",temp_more
            G.goal_more = temp_more + [variable2] + [variable1] #1/16/2014 tried switching #to fix empty-shot - try just changing this one 1/29
            print "goal_more_broke",G.goal_more
            print "variable13",variable1
            G.goal_direct ="down"
            G.goal_var = variable1
            print "variable13",variable1
            temp_goal_preds = goal_preds[0]
            important_variable = retrieve_from_big(G.store_big_effects,G.all_preds,G.removed_goals)
            print "imortant_variable",important_variable
            neweffect = temp_goal_preds[:2] + [important_variable] + [variable1]

#            neweffect = []
 #           neweffect.insert(0,variable1)
  #          neweffect.insert(0,removed_goals[2:])
   #         neweffect.insert(0,goal_preds[:2])
#            neweffect2 = goal_preds[:2] + removed_goals[2:] + [variable2]
            print "goal_preds",goal_preds
            print "removed_preds",removed_preds
            neweffect2 = temp_goal_preds[:2] + [important_variable] + [variable2]
            neweffect1not =[ "not",neweffect]
            print "neweffect1is this right2",neweffect1not,neweffect2
            return [neweffect1not, neweffect2]
        return []
    return[]

def retrieve_from_big(store_big_effects,all_preds,removed_goals):
    print "store_big_effects",store_big_effects
    print "all_preds",all_preds
    print "removed_goals",removed_goals
    temp = removed_goals[0]
    predicate = temp[0]
    l = range(0,len(all_preds)-1)
    for i in l:
        temp2 = all_preds[i]
        if predicate == temp2[0]:
            location = i
    print "G.switch",G.switch
    if G.switch == "pos":
        index = 0
    else:
        index = 2
    temp3 = store_big_effects[index]   #changed from 0 to 2 1/31/14
    temp4 = location + 2
    return temp3[temp4]


def add_singleton_effects(neweffects,unary_singleton,removed_pred,unary_singleton_removal,num_count ) :
    print "neweffects",neweffects
    print "unary_singleton",unary_singleton
    print "removed_pred",removed_pred
    print "unary_singleton_removal", unary_singleton_removal
    neweffects1 = add_singleton_effects1(neweffects,unary_singleton,removed_pred,unary_singleton_removal,G.num_count  )
    print "effectseee",neweffects1
    if neweffects1 == []:
        return (neweffects)
    else:
        neweffects.extend(neweffects1)  #1/11/14 changed to extend
        return(neweffects)

def add_singleton_effects1(neweffects,unary_singleton,removed_pred,unary_singleton_removal,num_count ):
    print "unary_singleton_removal",unary_singleton_removal
    if unary_singleton_removal == []:
        return []
    else:
        effect = add_singleton_effects1a(neweffects,unary_singleton[0],removed_pred,unary_singleton_removal[0],G.num_count )
        effectlist = add_singleton_effects1(neweffects,unary_singleton[1:],removed_pred,unary_singleton_removal[1:],G.num_count )
        if effect == []:
            return effectlist
        elif effectlist== []:
            return effect
        else:
            effectlist.append(effect)
            return effectlist
        
def add_singleton_effects1a(neweffects,unary_singleton,removed_pred,unary_singleton_removal,num_count ):
    print "unary_singleton_removal2",unary_singleton_removal
    if removed_pred == []:
        return []
    else:
        effect = add_singleton_effects2(neweffects,unary_singleton,removed_pred[0],unary_singleton_removal,G.num_count )
        effectlist = add_singleton_effects1a(neweffects,unary_singleton,removed_pred[1:],unary_singleton_removal,G.num_count )
        if effect == []:
            return effectlist
        elif effectlist == []:
            return effect
        else:
            effectlist.append(effect)
            return effectlist

def add_singleton_effects2(neweffects,unary_singleton,removed_pred,unary_singleton_removal,num_count ):
    print "unary_singleton3",unary_singleton
    print "unary_singleton_removal3",unary_singleton_removal
    if find_singleton_match(unary_singleton_removal,removed_pred):
#        temp = removed_pred[0]
        temptemp = unary_singleton[1]
#        temptemp = temp[1]
#        print "temp2",temp
#        variable1 = "?"+ "num" + str(G.variable_counter)
#        G.variable_counter = G.variable_counter + 1
        variable1 = "?"+ "num" + str(G.num_count)
        G.num_count = G.num_count + 1
#        variable2 = "?"+ "num" + str(G.variable_counter)
#        G.variable_counter = G.variable_counter + 1
        variable2 = "?"+ "num" + str(G.num_count)
        G.num_count = G.num_count + 1
        G.totalnumber = G.totalnumber + 2
        temp_more = ["more" + temptemp[:2]]                             #fixed 1/12/14
        print "unary_singleton",unary_singleton
        temp = [unary_singleton[0]  , unary_singleton_removal[-1]]
        G.unary_params.insert(0, temp)
        print "temptemp",temptemp
        print "morezc",temp_more
        G.unary_more = temp_more + [variable2] + [variable1]       #switched 1/16/14 to fix grasp #switched back and empty not holding 1/27/14 switch back
        print "G.unary_more",G.unary_more
        print "variable13",variable1
        predicate1 = [unary_singleton[0], unary_singleton_removal[1], variable1]
        print "predicate1",predicate1
        predicate2 = [unary_singleton[0], unary_singleton_removal[1], variable2]
        predicate2not = [ "not", predicate2]
        return [predicate1, predicate2not]
    elif find_singleton_match(unary_singleton_removal,removed_pred[1]):
        temptemp = unary_singleton[1]
#        temptemp = temp[1]
#        tempa = removed_pred[1]
#        temp = tempa[0]
#        print "temp1",temp
#        variable1 = "?"+ "num" + str(G.variable_counter)
#        G.variable_counter = G.variable_counter + 1
#        variable2 = "?"+ "num" + str(G.variable_counter)               #fixed 1/12/14 
#        G.variable_counter = G.variable_counter + 1
        variable1 = "?"+ "num" + str(G.num_count)
        G.num_count = G.num_count + 1
        variable2 = "?"+ "num" + str(G.num_count)               #fixed 1/12/14 
        G.num_count = G.num_count + 1
        G.totalnumber = G.totalnumber + 2
        temp_more = ["more" + temptemp[:2]]
        print "unary_singleton",unary_singleton
        print "temptemp",temptemp
        print "morezd",temp_more
        G.unary_more = temp_more + [variable2] + [variable1] #switched 1/16/14 to fix grasp #switched again above
        print "variable13",variable1
        predicate1 = []
        predicate1.insert(0,variable1)
        predicate1.insert(0,unary_singleton_removal[1])
        predicate1.insert(0,unary_singleton[0])
        predicate2 = [unary_singleton[0], unary_singleton_removal[1], variable2]
        predicate1not = ["not", predicate1]
        print "predicate2",predicate2
#neweffect2 = goal_temp[:2] + removed_goals[2:] + [variable2]
#            neweffect1not =[ "not",neweffect1]
        return [predicate1not, predicate2]
    return []

def find_singleton_match(unary_singleton_removal,removed_pred):
    if unary_singleton_removal[0] == removed_pred[0]:
        return True
    return False

def add_big_effects(prednames2,removed_pred,neweffects,big_unary_pred,big_order,object_list,num_count,param): #**need obejct list already created ** use makehierarcy ontology???? NEED TO KNOW IF SPLIT AND SPECIALISE
    print "prednames2",prednames2
    print "removed_pred", removed_pred
    print "neweffects",neweffects
    print "big_unary_pred",big_unary_pred
    print "big_order",big_order
    print "object_list",object_list

    temp1 = big_unary_pred[0]
    tempname = temp1[1]
    G.big_more = ["more" + tempname[:2]]
    print "G.big_more",G.big_more

    G.direct = []
    predicate1, predicate2 = create_predicate(removed_pred,big_order,param)

    print "predicate1",predicate1
    print "predicate2",predicate2
    predicate1, predicate2, predicate3, predicate4  = add_name_var_numbers(predicate1,predicate2,G.num_count)  #have not done numbers
    print "predicate1",predicate1
    print "predicate2",predicate2
    print "predicate3",predicate3
    print "predicate4",predicate4
    print "G.direct",G.direct
    newlist = [predicate1,predicate2,predicate3,predicate4]
#    dummy()
    neweffects.extend(newlist)
    G.store_big_effects = newlist
    return neweffects
    

def add_name_var_numbers(predicate1,predicate2,num_count):
    temp_list = G.unary_big[0]
    name = temp_list[0]
    var = temp_list[1]
    predicate1.insert(0,var)
    predicate1.insert(0,name)
    predicate2.insert(0,var)
    predicate2.insert(0,name)
#    variable1 = "?"+ "num" + str(G.variable_counter)
#    G.variable_counter = G.variable_counter + 1
    variable1 = "?"+ "num" + str(G.num_count)
    G.num_count = G.num_count + 1
    predicate1 = predicate1 + [variable1]
#    variable2 = "?"+ "num" + str(G.variable_counter)
#    G.variable_counter = G.variable_counter + 1
    variable2 = "?"+ "num" + str(G.num_count)
    G.num_count = G.num_count + 1
    predicate2 = predicate2 + [variable2]
    variable3 = "?"+ "num" + str(G.num_count)
    G.num_count = G.num_count + 1
#    variable3 = "?"+ "num" + str(G.variable_counter)
#    G.variable_counter = G.variable_counter + 1
    predicate3 = predicate1[:-1] + [variable3]
#    variable4 = "?"+ "num" + str(G.variable_counter)
#    G.variable_counter = G.variable_counter + 1
    variable4 = "?"+ "num" + str(G.num_count)
    G.num_count = G.num_count + 1
    G.totalnumber = G.totalnumber + 4
    predicate4 = predicate2[:-1] + [variable4]
    print "zzpredicate1",predicate1
    print "zzpredicate2",predicate2
    print "zzpredicate3",predicate3
    print "zzpredicate4",predicate4
    newpredicate3 = [ "not", predicate3]
    newpredicate4 = [ "not", predicate4]
    return (predicate1,newpredicate3,predicate2,newpredicate4)


def create_predicate(removed_pred,big_order,param):
    print "big_order",big_order
    print "removed_pred", removed_pred
    return create_predicate1(removed_pred,big_order,0,param)
    

def create_predicate1(removed_pred,big_order,var_num,param):
    if big_order == []:
        return ([],[])
    else:
        item, not_item = create_predicate2(removed_pred,big_order[0],var_num,param)
        print "zztesterzz",big_order[0],item,not_item
        var_num = var_num + 1
        item_list, not_item_list = create_predicate1(removed_pred,big_order[1:],var_num,param)
        item_list.insert(0,item)
        not_item_list.insert(0,not_item)
        return (item_list,not_item_list)

def appear(name, removed_pred,param): ##have to check param ?s versus ?d and type from G.thetypes
    print "removed_pred0",removed_pred
    if removed_pred == []:
        return (False, [])
    else:
        print "removed_pred1",removed_pred
        print "name1",name
        appeared, pos_or_neg = appear1(name,removed_pred[0],param)
        print "appeared",appeared
        print "pos_or_neg",pos_or_neg
        if appeared == True:
            return (appeared, pos_or_neg)
        appeared2, pos_or_neg2 = appear(name,removed_pred[1:],param)
        print "appeared2",appeared2
        print "pos_or_neg2",pos_or_neg2
        if appeared2 == True:
            return (appeared2, pos_or_neg2)
        return (False, [])

def appear1(name, removed_pred,param):
    print "appear1"
    print "removed_pred2",removed_pred
    print "name2",name
    print "param",param
    print "G.thetypes",G.thetypes
    temp = secondtest(removed_pred,param)
    print "name",name
    print "special-temp",temp
    if name == removed_pred[0] and secondtest(removed_pred,param): #add test here that type of param is the type of G.thetypes
        return (True, "pos")
    elif removed_pred[0] == "not":
        print "here1",removed_pred[0]
        temp = removed_pred[1]
        print "temp",temp
        temptemp = secondtest(temp,param)
        print "name",name
        print "special-temp2",temptemp
        if name == temp[0]  and secondtest(temp,param):
            print"here2",temp[0]
            return (True, "neg")
        return (False, [])
    return(False, [])

def make_unbound_variable(big_order):
    temp = big_order[0]
    newvariable = "?"+ temp[0] + str(G.variable_counter)
    G.variable_counter = G.variable_counter + 1  
    return newvariable

def type_from_variable_pred_list(big_order,variable_pred_list):
    if variable_pred_list == []:
        return []
    mytype = type_from_variable_pred_list1(big_order,variable_pred_list[0])
    if mytype <> []:
        return mytype
    return type_from_variable_pred_list(big_order,variable_pred_list[1:])

def type_from_variable_pred_list1(big_order,variable_pred_list):
    if big_order == variable_pred_list[1]:
        return variable_pred_list[0]
    return []

def is_singleton(big_order):
    if len(big_order) < 5:
        return True
    return False

def make_new_variable(big_order):
    variable = make_unbound_variable(big_order)
    print "variable",variable
    variable_type = type_from_variable_pred_list(big_order[0],G.variable_pred_list)
    print "variable_type",variable_type
    param = edit_param(G.newparam,variable,variable_type)
    print "param",param
    G.newparam = param
    return variable

def define_singleton_values(effect_pos_or_neg1,precond_pos_or_neg2,val,not_val,big_order):
    print "pos_or_neg1zz",effect_pos_or_neg1
    print "pos_or_neg2zz",precond_pos_or_neg2
    print "val",val
    print "notval",not_val
    if effect_pos_or_neg1 == "pos":
        if precond_pos_or_neg2 == "neg":
            return (val, not_val)
        elif precond_pos_or_neg2 == "pos":
            return (val, val)
        elif precond_pos_or_neg2 == []:
            variable = make_new_variable(big_order)
            return(val,variable)
    elif effect_pos_or_neg1 == "neg":
        if precond_pos_or_neg2 == "neg":
            return (not_val,not_val)
        elif precond_pos_or_neg2 == "pos":
            return (not_val,val)
        elif precond_pos_or_neg2 == []:
            variable = make_new_variable(big_order)
            return(not_val,variable)
    elif effect_pos_or_neg1 == []:
        print "hrlp",val
        if precond_pos_or_neg2 == "neg":
            return (not_val,not_val)
        elif precond_pos_or_neg2 == "pos":
            print "clean-shot",val,val
            return (val,val)
        elif precond_pos_or_neg2 == []:
            variable = make_new_variable(big_order)
            return(variable,variable)
    else:
        print "here1"
        dummy2() #should never get here  
#####making thrid set 

def look_in_predicate_for_variable_name(big_order,variable_type): #last bug 1/16/14
    print "big_orderZZ",big_order
    print "variable_typeZZ",variable_type
    l = range(0,len(big_order))
    for i in l:
        if big_order[i] == variable_type:
            return big_order[i-2]

def create_predicate2(removed_pred,big_order,var_num,param): #need to use ?i if exists
    val, not_val = find_in(removed_pred,big_order[0],var_num,param) #returns us0 and us0 for used in clean-shot should return us0 and no0
    if val == []:
        print "testy",G.current_precond
        val, not_val = find_in(G.current_precond[1:],big_order[0],var_num,param) 
    print "val3",val
    print "not_val3",not_val
    print "Zremoved_pred",removed_pred
    print "Zbig_order",big_order
    print "param",param
    print "G.variable_pred_list",G.variable_pred_list
    print "G.bound_variables",G.bound_variables
    print "G.current_precond",G.current_precond
    effect_appeared1, effect_pos_or_neg1 = appear(big_order[0], removed_pred,param)
    print "big_oder[0]",big_order[0]
    print "G.goal_name",G.goal_name
    if big_order[0] == G.goal_name: 
        G.switch = effect_pos_or_neg1
        print "G.switch1",G.switch
    print "zappeard1z",effect_appeared1,big_order[0],removed_pred,param
    print "pos_or_neg1z",effect_pos_or_neg1
    if G.current_precond[0] == "and":
        precond_appeared2, precond_pos_or_neg2 = appear(big_order[0],G.current_precond[1:],param)
    else:
        precond_appeared2, precond_pos_or_neg2 = appear(big_order[0],[G.current_precond],param)
    print "zappeard2z",precond_appeared2,big_order[0],G.current_precond[1:],param
    print "pos_or_neg2z",precond_pos_or_neg2
    if not effect_appeared1 and not precond_appeared2: ###this is wrong need to pull variable from predicate not make a new one (at least for fill-shot ?i)
        print "freakfreak",big_order,"param",param ##if big_order is not singleton and removed_pred has ?var use that
#        if len(big_order) > 4:
#            variable_type = type_from_variable_pred_list(big_order[0],G.variable_pred_list)
#            print "AA", variable_type
#            variable = look_in_removed_predicate_for_variable_name(big_order,removed_pred,G.newparam,variable_type)
#            print "BB", variable
#        else:
        variable = make_new_variable(big_order)
#        variable = make_unbound_variable(big_order)
#        print "variable",variable
#        variable_type = type_from_variable_pred_list(big_order[0],G.variable_pred_list) 
#        print "variable_type",variable_type
#        param = edit_param(G.newparam,variable,variable_type) 
#        print "param",param
#        G.newparam = param
        print "freakfreakfreak", variable
        return (variable, variable)
    elif is_singleton(big_order):
        return define_singleton_values(effect_pos_or_neg1,precond_pos_or_neg2,val,not_val,big_order)
#        if effect_pos_or_neg1 == "pos":
#            if precond_pos_or_neg2 == "neg":
#                return (val, not_val)
#            elif precond_pos_or_neg2 == "pos":
#                return (val, val)
#            else:
#                variable = make_new_variable(big_order)
#                return(val,variable)
#        elif effect_pos_or_neg1 == "neg":
#            if precond_pos_or_neg2 == "neg":
#                return (not_val,not_val)
#            elif precond_pos_or_neg2 == "pos":
#                return (not_val,val)
#            else:
#                variable = make_new_variable(big_order)
#                return(not_val,variable)
#        else:
#            print "here1"
#            dummy2() #should never get here
    else:
        print "reallyhere2",removed_pred
        print "big_order",big_order
        variable_type = type_from_variable_pred_list(big_order[0],G.variable_pred_list)
        constant = look_for_bound_variables(variable_type,G.bound_variables)
        print "constant",constant
        if constant <> []:
            return define_singleton_values(effect_pos_or_neg1,precond_pos_or_neg2,constant[0],not_val,big_order)
#            if effect_pos_or_neg1 == "pos" and precond_pos_or_neg2 == "neg":
#                return (constant[0], not_val)
#            elif effect_pos_or_neg1 == "neg" and precond_pos_or_neg2 == "pos":
#                return (not_val,constant[0])
#            elif effect_pos_or_neg1 == "neg" and precond_pos_or_neg2 == "neg":
#                return (not_val,not_val)
#            elif effect_pos_or_neg1 == "pos" and precond_pos_or_neg2 == "pos":
#                return (constant[0],constant[0])
#            elif
        print "paramZZ",param
        print "double",G.newparam
        print "removed_pred",removed_pred
#        variable = look_in_predicate_for_variable_name(big_order,variable_type)
        if effect_appeared1 == True and precond_appeared2 == True:
            ###must add code here if pos and neg need no1 for one of them!!
            print "jiggy",effect_pos_or_neg1,precond_pos_or_neg2
            if effect_pos_or_neg1 == "neg" and precond_pos_or_neg2 == "pos":
                variable = look_in_removed_predicate_for_variable_name(big_order,removed_pred,G.newparam,variable_type,not_val) 
                print "jig2",not_val,variable,big_order
                return (not_val,variable) #switched 1/30
            variable = look_in_removed_predicate_for_variable_name(big_order,removed_pred,G.newparam,variable_type,not_val) 
            print "variablevariable1",variable
            return (variable, variable)
        elif precond_appeared2 == True:
            variable = look_in_removed_predicate_for_variable_name(big_order,G.current_precond,G.newparam,variable_type,not_val)
            print "variablevariable2",variable
            return (variable, variable)
        elif effect_appeared1 == True :  #made change 1/28/14
            variable = look_in_removed_predicate_for_variable_name(big_order,removed_pred,G.newparam,variable_type,not_val)   
            print "variablevariable8",variable 
            variable2 = make_new_variable(big_order)
            return (variable, variable2)     
        else:
            variable1 = make_new_variable(big_order)
            variable2 = make_new_variable(big_order)
            print "check this op"
            return (variable1,variable2)
#        if variable <> []:
#            return define_singleton_values(effect_pos_or_neg1,precond_pos_or_neg2,variable,not_val,big_order)            
#        else:
#            dummy3() #this should never happen 


#        dummy1()
        #check param list
#        allreadybound = look_for_bound_variables0(variable,G.temporary_bindings)   #only checks for type needs to check param list

#        variable = make_unbound_variable(big_order)
#        print "variable",variable
#        variable_type = type_from_variable_pred_list(big_order[0],G.variable_pred_list)
#        print "variable_type",variable_type
#        newparam = edit_param(G.newparam,newvariable,variable_type)
#        print "newparam",newparam
#        G.newparam = newparam
        dummy4()
    dummy5()


#    make_unbound_variable
#elif singleton(big_order)
#    if pred_pos(removed_pred):
#        return val
#    return not_val
#else:
#    var = use_param_var(big_order,param,G.bound_variables)
#    if var = []
#    make_unbound_var()
#    edit_param()
#    add_temporary_binding()


#    if val == [] and len(big_order) > 4 and not has_real_variable(big_order):         #must fix here%%
#        print "PATH1"
#        print"G.new_variables",G.new_variables
#        temp = big_order[0]
#        mytypes, myvars = get_types_from_pred(big_order)
#        print "mytypes",mytypes
#        print "myvars",myvars
#        variable = look_for_all_types(mytypes,myvars,big_order,removed_pred,G.bound_variables)
#        print "variable",variable #this should return what is missing
#        #this is semantically wrong
#        variable_type = return_type_of_from_pred(variable,big_order)
#        print "variable_type",variable_type
#        if G.temporary_bindings <> []:
#            allreadybound = look_for_bound_variables0(variable,G.temporary_bindings)
#        else:
#            allreadybound = []
##        allreadybound = []
#        print "allreadybound",allreadybound
##        dummy()
##        variable = look_for_bound_variables(big_order,removed_pred,G.bound_variables)
#        if allreadybound == []:
##must add procedures here to test if should us old variable

## mistake have to use variable name not predicate name

#1 first get types from pred
#2 see if types are bound
#3 if not store ?h in temporary bound
#4 erase after each operator
#            newvariable = "?"+ temp[0] + str(G.variable_counter)
#            print "removed_pred",removed_pred
#            print "big_order",big_order
#            print "var_num",var_num
#            G.newparam = edit_param(G.newparam,newvariable,variable_type)
#            print "param",param
# #            types = get_types_from_pred(big_order)
##            print "types",types
##            onetype = find_missing_type(types,G.bound_variables)
##            print "onetype",onetype
##            dummy()
#            print "bindhere",variable,newvariable
#            print "param",param
#            G.temporary_bindings.insert(0,[variable,newvariable])
#            print "G.temporary_bindings",G.temporary_bindings
#            print "param",param
#            print "big_order",big_order
#            G.variable_counter = G.variable_counter + 1
#            
##            G.bound_variables.insert(0,[big_order[0],variable])
#            return (newvariable, newvariable)
#        print "zwzwgothere", allreadybound
##        dummy()
#        return (allreadybound, allreadybound)    ###return allready bound ???
#    if val == []:
#        temp = big_order[0]
##        mytypes, myvars = get_types_from_pred(big_order)
##        variable = look_for_all_types(mytypes,myvars,big_order,removed_pred,G.bound_variables)
##        variable_type = return_type_of_from_pred(variable,big_order)
#        print "PATH2"
#        newvariable = "?"+ temp[0] + str(G.variable_counter)
#        print "zremoved_pred",removed_pred
#        print "zbig_order",big_order
#        print "zvar_num",var_num
#        temp2 = big_order[:2]
#        print "temp2",temp2
#        variable_type = type_from_pats_favorite(temp2,G.pats_favorite)
#        print "variable_type",variable_type
#        if variable_type <> []: #could use "right" instead of variable   # desperate attend to fix
#            G.newparam = edit_param(G.newparam,newvariable,variable_type)
#            print "param",param
# #            types = get_types_from_pred(big_order)
##            print "types",types
##            onetype = find_missing_type(types,G.bound_variables)
##            print "onetype",onetype
##            dummy()
##        print "bindhere",variable,newvariable
#            print "param",param
#            print "bindhere2",variable_type,newvariable
#            G.temporary_bindings.insert(0,[variable_type,newvariable]) #using type when no vairbale name
#            print "G.temporary_bindings",G.temporary_bindings
#            print "param",param
#            print "big_order",big_order
#        G.variable_counter = G.variable_counter + 1
            
#            G.bound_variables.insert(0,[big_order[0],variable])
#        return (newvariable, newvariable)

#    return (val, not_val)

def look_in_removed_predicate_for_variable_name(big_order,removed_predicate,param,variable_type,not_val):
    if removed_predicate == []:
        return []
    var = look_in_removed_predicate_for_variable_name1(big_order,removed_predicate[0],param,variable_type,not_val)
    if var <> []:
        return var
    return look_in_removed_predicate_for_variable_name(big_order,removed_predicate[1:],param,variable_type,not_val)

def look_in_removed_predicate_for_variable_name1(big_order,removed_predicate,param,variable_type,not_val):
    print "zztzzremoved_predicate",removed_predicate
    print "big_order",big_order
    if removed_predicate[0] == big_order[0]:
        myvars = return_variables(removed_predicate)
        print "myvars",myvars
        print "variable_type1",variable_type
        G.notequalno_type.insert(0,variable_type)
        print "G.notequalno_type",G.notequalno_type
        thevar = return_var_matching_type(myvars,param,variable_type)
        print "variable_type",variable_type
        print "thevar",thevar
        G.store_nots.insert(0,["notequalno",thevar])
        print "storenots1",G.store_nots
        
#        dummy()
        return thevar
    elif removed_predicate[0] == "not":
        temp = removed_predicate[1]
        print "temp",temp
        if temp[0] == big_order[0]:
            myvars = return_variables(removed_predicate[1])
            print "myvars3",myvars
            print "G.notequalno_type",G.notequalno_type 
            G.notequalno_type.insert(0,variable_type)
            print "G.notequalno_type",G.notequalno_type 
            thevar = return_var_matching_type(myvars,param,variable_type)
            print "variable_type",variable_type
            print "thevar4",thevar
#            dummy()
            G.store_nots.insert(0,["notequalno",thevar])   
            print "storenots2",G.store_nots  
            return thevar
    return []

def return_var_matching_type(myvars,param,variable_type):
    print "myvars",myvars
    print "param", param
    print "variable_type",variable_type
    newvar = return_var_matching_type1(myvars,param,variable_type)
    print "newvar1",newvar
    if newvar == []:
         newtypes = go_down_ontology(variable_type)
         print "newtypes",newtypes
         l = range(0,len(newtypes))
         for i in l:
             newvar = return_var_matching_type1(myvars,param,newtypes[i])
             if newvar <> []:
                 return newvar
    return newvar


def go_down_ontology(variable_type):
    l = range(0,len(G.ontology))
    for i in l:
        temp = G.ontology[i]
        print "temp1",temp
        if variable_type == temp[1]:
            return temp[0]

def return_var_matching_type1(myvars,param,newtype): #needs to be the same variable
    print "myvarsW",myvars
    print "paramW", param
    print "variable_typeW",newtype
    l = range(0,len(param))                                                                                                                                                  
    for i in l:
        if param[i] == newtype and param[i-2] in myvars:
            print "param[i]",param[i],param[i-2]
            return param[i-2]
    return []

def return_variables(removed_pred):
    myvars = []
#    l = range(1,len(removed_pred),3)
#    for i in l:
#        myvars.insert(0,removed_pred[i])
    return removed_pred[1:]
#    return myvars

        

def type_from_pats_favorite(val,pats_favorite):
    name = val[0]
    l = range(0,len(pats_favorite))
    for i in l:
        temp = pats_favorite[i]
        print "temp",temp
        temp1 = temp[1]
        print "temp1",temp1
        u = range(0,len(temp1))
        for v in u:
            temp2 = temp1[v]
            print "temp2",temp2
            print "name",name
#            print "temp2[:2]",temp2[:2]
            if not isinstance(temp2,int) and temp2[:2] == name[:2]:
                return temp[0]
    return []

def return_all_types_from_pred(big_order):
    temp = []
    l = range(3,len(big_order),3)
    for i in l:
        temp.insert(0,big_order[i])
    return temp
        
def has_real_variable(big_order):
    print "big_order",big_order
    types = return_all_types_from_pred(big_order)
    l = range(0,len(types))
    for i in l:
        if not found_in_bindings(types[i],G.bound_variables):
            print "False",types[i]
            return False
    print "G.bound_variables",G.bound_variables
    print "big_order",big_order
#    dummy()
    print "True"
    return True

def found_in_bindings(types,bound_variables):
    print "types",types
    print "G.bound_variables",bound_variables
    print "G.newparam",G.newparam
    l = range(0,len(bound_variables))
    for i in l:
        temp = bound_variables[i]
        if types == temp[0]:
            return True
    print    "G.ontology",G.ontology
    print "types",types
    l = range(0,len(G.ontology))
    for i in l:
        temp = G.ontology[i]
        if temp[1] == types:
            print "tempZ",temp
            temp1 = temp[0]
            print "tempW",temp1
            u = range(0,len(temp1))
            for v in u:
                w = range(0,len(bound_variables))
                for z in w:
                    temp2 = bound_variables[z]
                    print "tempU",temp2
                    if temp1[v] == temp2[0]:
                        return True

    print "FAILED",types,G.bound_variables,G.ontology
#    dummy()
    return False


#def edit_param(newparam,newvariable,variable_type): #must fix this
#    print "newparam",newparam
#    print "newvariable",newvariable
#    print "variable_type",variable_type
#    l = range(0,len(newparam))
#    for i in l:
#        if newparam[i] == variable_type:
#            newparam[i-2] = newvariable
#    return newparam

def edit_param(newparam,newvariable,variable_type):
    print "newparam",newparam                                                                                                                                                      
    print "newvariable",newvariable                                                                                                                                                
    print "variable_type",variable_type       
    location = 999
    l = range(0,len(newparam))                                                                                                                                                     
    for i in l:
        if newparam[i] == variable_type:
            location = i
    if location == 999:
        mylist =  [ newvariable] + [ '-'] + [ variable_type] 
        newparam.extend(mylist)
        return newparam
    else:
        newparam.insert(location-2,newvariable)
        return newparam

#    if newparam == []:
#        mylist =  [ newvariable] + [ '-'] + [ variable_type]
#        return mylist
#    if newparam
    

def return_type_of_from_pred(variable,big_order):
    print "variable",variable
    print "big_order",big_order
    l = range(0,len(big_order))
    for i in l:
        if big_order[i] == variable:
            return big_order[i+2]
    return []
                
def look_for_all_types(mytypes,myvars,big_order,removed_pred,bound_variables): #if my types "container" need ontology tpp
    print "mytypes",mytypes
    print "myvars",myvars
    print "bigorder",big_order
    print "removed_pred",removed_pred
    print "bound_variables",bound_variables
    print "bound2",G.bound_variables
    if mytypes == []:
        return []
    variable = look_for_bound_variables(mytypes[0],myvars[0],removed_pred,bound_variables)  #should return [] if not there
    if variable == []:
        return myvars[0]
    return look_for_all_types(mytypes[1:],myvars[1:],removed_pred,bound_variables)  


def go_up_ontology(mytype,bound_variables,ontology):
    if ontology == []:
        return []
    var = go_up_ontology1(mytype,bound_variables,ontology[0])
    if var == []:
        return go_up_ontology(mytype,bound_variables,ontology[1:])
    return var

def go_up_ontology1(mytype,bound_variables,ontology):
    if mytype == ontology[1]:
        return ontology[0]

def find_missing_type(types,bound_variables):
    if types == []:
        return []
    val = find_missing_type1(types[0],bound_variables)
    if val == []:
        new_types = go_up_ontology(types[0],bound_variables,G.ontology)
        return find_missing_ontology(mytype,bound_variables)
    return find_missing_type(types[1:],bound_variables)
        

def find_missing_ontology(mytype,bound_variables):
    if mytype == []:
        return []
    val = find_missing_type1(mytype[0],bound_variables)
    if val == []:
        return mytype
    return find_missing_type(mytype[1:],bound_variables)

def find_missing_type1(types,bound_variables):
    if bound_variables == []:
        return []
    val = find_missing_type2(types,bound_variables[0])
    if val == []:
        return types
    return find_missing_type1(types,bound_variables)

def find_missing_type2(types,bound_variables):
    if types == bound_variables[0]:
        return bound_variables[1]
    return []


def get_types_from_pred(big_order):
    mytypes = []
    myvars = []
    l = range(0,len(big_order))
    for i in l:
        if big_order[i] == '-':
            mytypes.insert(0,big_order[i+1] )
            myvars.insert(0,big_order[i-1] )
    return (mytypes, myvars)
    
def look_for_bound_variables(mytype,bound_variables): #only works for trinary predicates - 1 other variable
#    print "big_order",big_order
#    print "removed_pred",removed_pred
    print "zbound_variables",bound_variables
#    print "G.temporary_variables",G.temporary_variables
    if bound_variables == []:
        return []
    val = look_for_bound_variables01(mytype,bound_variables[0]) 
    if val == []: #have not found it...keep looking
        return look_for_bound_variables(mytype,bound_variables[1:])
    return val

def look_for_bound_variables0(variable,bound_variables): #special for temporary variables
    print "zvariable",variable
    print "bound_variables",bound_variables
    if bound_variables == []:
        return []
    val = look_for_bound_variables01(variable,bound_variables[0])
    print "zval",val
    if val == []: #have not found it...keep looking                                                                                                                                
        return look_for_bound_variables0(variable,bound_variables[1:])
    return val

def look_for_bound_variables01(big_order,bound_variables):
    print "zzbig_order",big_order
    print "zbound_variables",bound_variables
#    if bound_variables == []:
#        return []
    if big_order == bound_variables[0]:
        return bound_variables[1]
    return []

def look_for_bound_variables1(big_order,bound_variables):
    print "zbig_order",big_order
    print "zbound_variables",bound_variables
    if big_order in bound_variables[1]:
        return bound_variables[0]
    return []

def find_in(removed_pred,big_order,var_num,param):
    print "removed_preda",removed_pred    
    print "big_order",big_order
    print "var_num",var_num
    print "zzzparam",param

    if removed_pred == []:
###need to add something here to return em em when there is no value in the effect list...for empty in clean shot....then have to check used again in clean-shot
        return([], [])
    else:
        val, not_val = find_in1(removed_pred[0],big_order,var_num)
        print "val2",val
        print "not_val3",not_val
        if val == []:
            return find_in(removed_pred[1:],big_order,var_num,param)
#        repairparam_list(big_order,param,val,not_val)
        return(val,not_val)

#def repairparam_list(big_order,param,val,not_val):
#    print "big_order",big_order
#    print "zzzzzzparam",param
#    print "val",val
#    print "not_val",not_val
#    l = range(0,len(param))
#    for i in l:
#        if param[i] == 
#        dummy()

def find_in1(removed_pred,big_order,var_num):
    print "finally"
    print "big_order",big_order
    print "removed_pred",removed_pred
#    G.big_more = ["more" + big_order[:2]]
#    print "G.big_more",G.big_more
    print "var_num",var_num
    if big_order == removed_pred[0]:
        G.direct = G.direct + ["up"]
        print "G.direct1",G.direct

        val = big_order[:2] + str(var_num)
        not_val = "no" + str(var_num)
        print "val1",val
        print "notval1",not_val
        return (val, not_val)
    elif removed_pred[0] == "not":
        print "house"
        print "G.direct2",G.direct
        temp = removed_pred[1]
        if big_order == temp[0]:
            G.direct = G.direct + ["down"]
            val = big_order[:2] + str(var_num)
            not_val = "no" + str(var_num)
            print "val1",val
            print "notval1",not_val
#            return ( not_val, val) #desparate fix 1/12/14
            return (val,not_val)
        return([],[])
    print "hod"
#    val = big_order[:2] + str(var_num) #guessing here trying to fix clean-shot 1/29
    return([],[])
                          
                              


def remove_bad_effects(prednames,effect,param):
    print "zeffect23",effect
    print "zprednames",prednames
    print "param",param
    if effect == []:
        return effect
    elif effect[0] == 'and':
        new_effect = remove_bad_effects(prednames,effect[1:],param)
        new_effect.insert(0,effect[0])
        return new_effect
    elif isinstance(effect[0],list): 
        temp_effect1 = effect[0]
        if temp_effect1[0] in prednames and secondtest_diff2(effect[0],param): #must add test here for variable as well  look in G.thetypes and pass "param" if 1 variable not hand or shot then keep
            print "removeremove",effect[0]
            G.removed_pred.insert(0,effect[0])
            return remove_bad_effects(prednames,effect[1:],param)
        else:
            print "temp_effect1zzz",temp_effect1  
            if temp_effect1[0] == 'not' and secondtest_diff2(temp_effect1[1],param): #added second test 1/31/14  #changed both of these to keep holding on shaker 1/31/14
                temp_effect2 = temp_effect1[1]
                if temp_effect2[0] in prednames:
                    G.removed_pred.insert(0,effect[0])
                    return remove_bad_effects(prednames,effect[1:],param)
                else:
                    new_effect = remove_bad_effects(prednames,effect[1:],param)
                    new_effect.insert(0,effect[0])
                    return new_effect
            else:
                new_effect = remove_bad_effects(prednames,effect[1:],param)
                new_effect.insert(0,effect[0])
                return new_effect


def secondtest_loop(preds,param):
    print "preds",preds
    if preds == []:
        return False
    if secondtest_diff(preds[0],param) == True:
        return True
    return secondtest_loop(preds[1:],param)


def secondtest_diff(effect,param):
    print "secondtest"
    print "effect",effect
    print "param",param
    print "G.thetypes",G.thetypes
    found = False
    l = range(0,len(param))
    for i in l:
        if param[i] == "-":
            u = range(0,len(G.thetypes))
            for v in u:
                print "param[i+1]",param[i+1]
                print "found",found
                if param[i+1] in G.thetypes[v] and param[i-1] in effect and param[i+1] == G.typeof:
                    found = True
    print "found",found
    if found == False:
        print "keepkeep",effect
        return False
    return True

def secondtest_diff2(effect,param):
    print "secondtest"
    print "effect",effect
    print "param",param
    print "G.thetypes",G.thetypes
    found = False
    l = range(0,len(param))
    for i in l:
        if param[i] == "-":
            u = range(0,len(G.thetypes))
            for v in u:
                print "param[i+1]",param[i+1]
                print "found",found
                if param[i+1] in G.thetypes[v] and param[i-1] in effect and (param[i+1] == G.typeof or len(effect) == 2):
                    found = True
    print "found",found
    if found == False:
        print "keepkeep",effect
        return False
    return True

#def secondtest(effect,param):
#    print "secondtest"
#    print "effect",effect
#    print "param",param
#    print "G.thetypes",G.thetypes
#    found = False
#    l = range(0,len(param))
#    for i in l:
#        if param[i] == "-":
#            u = range(0,len(G.thetypes))
#            for v in u:
#                print "param[i+1]",param[i+1]
#                print "found",found
#                if param[i+1] in G.thetypes[v] and param[i-1] in effect:
#                    found = True
#    print "found",found
#    if found == False:
#        print "keepkeep",effect
#        return False
#    return True

def secondtest(effect,param):
    print "zzzzeffect",effect
    if effect[0] == "not":
        effect = effect[1]
    l = range(1,len(effect)) 
    for i in l:
        if found_in_param(effect[i],param):
            print "yeseffect",effect
            return True
    print "noeffect",effect
    return False
        
def found_in_param(item,param):  ###do not handle nots
    print "zzitemzz",item
    found = False
    l = range(0,len(param))
    for i in l:
        if param[i] == item:
            print "here1",param[i]
            u = range(i,len(param))
            for v in u:
                if param[v] == "-":
                    print "here2",param[v+1]
#                    w = range(0,len(G.thetypes))
#                    for z in w:   must be in first set
                    print "G.thetypes[z]",G.thetypes[0]
                    if param[v+1] in G.thetypes[0]:
                        return True
                    return False
            return False
    return False

def split_test(param,types):
    action_types = returntypes(param)
    print "action_types",action_types
    print "types",types
    return is_last_loop_outer(action_types,types)

def find_ontology_type(mytype,ontology):
    if ontology == []:
        return []
    if ontology_match(mytype,ontology[0]):
        ontology_temp = ontology[0]
        return ontology_temp[0]
    return find_ontology_type(mytype,ontology[1:])

def ontology_match(mytype,my_onto_list):
    if mytype == my_onto_list[1]:
        return True
    return False

def fix_second_action(first_action,param):
    print "G.ontology",G.ontology
    type_list = find_ontology_type(G.mismatch[0],G.ontology)
    l = range(0,len(type_list)-1)
    for i in l:
        if type_list[i] <> G.mismatch[1]:
            new_first_action = copy.deepcopy(first_action)
            first_action, param = fix_second_action2(type_list[i],first_action,new_first_action,param)
    return (first_action, param)

def replace_param(param):
    l = range(0,len(param))
    for i in l:
        print "i",i,"l",l,"param[i]",param[i],G.mismatch[0],G.mismatch[1]
        if param[i] == G.mismatch[0]:
            param[i] = G.mismatch[1]
    return param

def fix_second_action2(mytype,first_action,new_first_action,param):
        new_first_action[1] = new_first_action[1] + ":" + str(mytype) #3/12/2014 - add ":"
        l = range(0,len(new_first_action))
        for i in l:
            if new_first_action[i] == ":parameters":
                print "anew_first_action[i+1]",new_first_action[i+1]
                print "anew_first_action[i]",new_first_action[i]
                print "afirst_action[i+1]",first_action[i+1]
                print "afirst_action[i]",first_action[i]

                new_first_action[i+1] = first_action_replace_arg_type(mytype,new_first_action[i+1])
                first_action[i+1] = G.mismatch[1]
                print "param",param
                param=replace_param(param)
                print "param",param
                print "#%%#",G.mismatch
#%%# 
#                dummy()
                print "znew_first_action[i+1]",new_first_action[i+1]
                print "znew_first_action[i]",new_first_action[i]
                print "zfirst_action[i+1]",first_action[i+1]
                print "zfirst_action[i]",first_action[i]

                print "new_first_action",new_first_action
                G.additional_actions.insert(0,new_first_action)
        return (first_action, param)
    
def first_action_replace_arg_type(mytype,mylist):
    print "mylist",mylist
    l = range(0,len(mylist))
    for i in l:
        print "G.mismatch[0]",G.mismatch[0], "mylist[i]",mylist[i]
        if G.mismatch[0] == mylist[i]:
            print "G.mismatch[1]",G.mismatch[1], "mylist[i]",mylist[i]
            print "G.ontology",G.ontology
            mylist[i] = mytype
            print "mylist[i]",mylist[i]
            return mylist

        
    

def returntypes(param):
    print "param",param
    if param == []:
        return []
    if param[0] == "-":
        mylists = returntypes(param[1:])
        mylists.insert(0,param[1])
        return mylists
    return returntypes(param[1:])

def is_last_loop_outer(param,types):
    print "help",param,types
    if types == []:
        return True
#    elif not isinstance(types,list):
#        return is_last_loop_outer(param,types)
    elif is_last(param,types[0]):
        return is_last_loop_outer(param,types[1:])
    return False

def is_last(param,types):
    print "param",param,"types",types
    if param == []:
        return True
    elif is_last_loop(param[0],types):
        return is_last(param[1:],types)
    return False

def is_last_loop(param,types):
    print "zzzherezzz",param,types
    if param in types:
        print "here1"
        if param <> types[-1]:
            print "here2",param,types[1]
            G.mismatch = [param,types[-1]]
            print "mismatch",G.mismatch
            return False
        return True
    return True

#R
def changeparam(param):                                                   #! change the parameters on the actions (add ?num1 and ?num2)
    print "??here??"
    print "G.totalnumber",G.totalnumber
    print "G.num_count",G.num_count
    print "param",param
#    if G.totalnumber == 0:                         #1/12/14 change
#        G.totalnumber = G.max_num
    _DEBUG("totalnumber",G.totalnumber)
    if G.totalnumber == 0:
        return param
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
    print "zeffect",effect,"num",num,"action",action
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
    print "G.predicate",G.predicate,"G.new_predicate",G.new_predicate,
    print "first",first
    if ((first[0] == G.predicate or (G.NEWPREDICATE == True and first[0] == G.new_predicate)) and (G.TYPING == False or pddl_typing.checkprecond_typing2(first,action,G.typeof))):        #current bug need to look through list of rpedicates????
        _DEBUG("yesy")
        number = num + 1
        newvar1 = "?num" + str(number)
        if len(first) == 3:                                      #added change for unary predicate 1/5/2014
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
        else:
            temp1 = ["count1a1asingle", first[1] , newvar1] #! changed these
###        G.storage.insert(len(G.storage),first[0])
#        G.storage.insert(len(G.storage),first[1])
#        G.storage.insert(len(G.storage),first[2])
#        stor1 = ["not" ,  temp1]
#        G.storage.insert(len(G.storage),stor1)
            _DEBUG("yea",temp1)
            G.direction.insert(len(G.direction),"up")
            G.var1 = first[1]
#            G.var2 = first[2]
            _DEBUG("var1",G.var1)
            newvar2 = "?num" + str(num)
            temp3 = ["count1a1asingle", first[1] , newvar2]
            temp2 = ["not"]
            #        G.storage.insert(len(G.storage),temp2[0])                                                                                                                        
            #        G.storage.insert(len(G.storage),first[0])                                                                                                                        
            #        G.storage.insert(len(G.storage),first[1])                                                                                                                        
            #        G.storage.insert(len(G.storage),first[2])                                                                                                                        
            print "storage2",temp3
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
            print "temp",temp,"newvar1",newvar1
            print "G.predicate",G.predicate,"G.NEWPREDICATE",G.NEWPREDICATE,G.new_predicate
            if len(temp) == 3:
                temp1 = ["count1a1a", temp[1] , temp[2], newvar1]
                #            G.storage.insert(len(G.storage),temp[0])
                #            G.storage.insert(len(G.storage),temp[1])
                #            G.storage.insert(len(G.storage),temp[2])
                stor2 = [ "not" , temp1]
            #            G.storage.insert(len(G.storage),stor2)
                G.direction.insert(len(G.direction),"down")
                G.var1 = temp[1]
#                G.var2 = temp[2]
#                _DEBUG("var",G.var1,G.var2)
                newvar2 = "?num" + str(num)
                temp3 = ["count1a1a", temp[1], temp[2], newvar2]
                temp2 = ["not"]
                #            G.storage.insert(len(G.storage),temp2[0])
                #            G.storage.insert(len(G.storage),temp[0])
                #            G.storage.insert(len(G.storage),temp[1])
                #            G.storage.insert(len(G.storage),temp[2])
                print "storage3",temp3
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
            else:                                                     #added branch for unary predicates 1/5/2014
                temp1 = ["count1a1asingle", temp[1] , newvar1]
                #            G.storage.insert(len(G.storage),temp[0])                                                                                                                 
                #            G.storage.insert(len(G.storage),temp[1])                                                                                                                 
                #            G.storage.insert(len(G.storage),temp[2])                                                                                                                 
                stor2 = [ "not" , temp1]
            #            G.storage.insert(len(G.storage),stor2)                                                                                                                       
                G.direction.insert(len(G.direction),"down")
                G.var1 = temp[1]
#                G.var2 = temp[2]
#                _DEBUG("var",G.var1,G.var2)
                newvar2 = "?num" + str(num)
                temp3 = ["count1a1asingle", temp[1], newvar2]
                temp2 = ["not"]
                #            G.storage.insert(len(G.storage),temp2[0])                                                                                                                
                #            G.storage.insert(len(G.storage),temp[0])                                                                                                                 
                #            G.storage.insert(len(G.storage),temp[1])                                                                                                                 
                #            G.storage.insert(len(G.storage),temp[2])                                                                                                                 
                print "storage4",temp3
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
def changeprecond1(precond,action,num,more):                                                        #! change precondition of the action by replacing old predicate with new predicate
    _DEBUG("num",num)
    number = 0
    #global direction
    _DEBUG("aaaprecond",precond,"direction",G.direction)
    ans = []
    _DEBUG("precond",precond)
    if precond == []:
        return []
    print "G.storage",G.storage
    l = range(0,len(G.storage))
    _DEBUG("DDDG.storage",G.storage,"l",l,"action",action)
    for i in l:
        _DEBUG("i",i,"G.storage[i]",G.storage[i],"action",action,"l",l)
        if G.storage[i] == action:
            print "wahoo",action,more
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
                    temp2 = [more, num1, num2]
                else:
                    temp2 = [more, num2, num1]
                num[0] = num[0] + 1
                number = number +2
                ans.insert(0,temp2)
            return ans


#**erk
def  changeunaryprecond(newprecond,removed_pred,precond,param):  #preconds messed up!! and try G.more_big again 2/1/14
    print "zznewprecond1",newprecond
    print "zzremoved_pred",removed_pred
    print "G.sotre_effects",G.store_effects
    print "G.remove_prednames",G.removed_prednames
    print "G.store_big_effects",G.store_big_effects
    newprecond = remove_bad_effects(G.removed_prednames,newprecond,param)
    print "zznewprecond2",newprecond
    if not G.store_effects == []:
        effects = addunaryprecond(newprecond,G.store_effects)
    if effects <> []:
        newprecond.extend(effects)
    print "zznewprecond3",newprecond,effects,G.store_effects
    newprecond = addbigmores(newprecond,G.store_big_effects)
    print "zznewprecond4",newprecond
    newprecond = addgoalmores(newprecond,G.unary_goal_preds,G.goal_more,G.removed_pred)
    print "zznewprecond5",newprecond
    newprecond = addunarymores(newprecond,G.unary_singleton,G.unary_singleton_removal,precond)
    print "zznewprecond6",newprecond
    if G.store_nots <> []:
        newprecond.insert(0,G.store_nots[0])
    print "zznewprecond7",newprecond
    G.store_nots = []
#    newprecond = dummy()
    return newprecond

def addunarymores(newprecond,unary_singleton,unary_singleton_removal,precond):
    print "zbnewprecond",newprecond
    print "unary_singleton",unary_singleton
    print "unary_singleton_removal",unary_singleton_removal
    print "recond",precond
    print " G.unary_more", G.unary_more
    print "G.goal_more",G.goal_more
    if G.unary_more <> []:
        newprecond.insert(0, G.unary_more)
        return newprecond                                            ##must add not equal
    else:                                                            ####in the precond and not the effect!!! (handempty)
        test = find_unary_precond(G.unary_singleton_removal,precond) ###always returns [] ???
        print "zbtest",test
        if test == True:
            print "hahahaha"
        ##add <>0 predicates for all nums and add count num3 num <> 0
        # is if not count 0
#            variable1 = "?"+ "num" + str(G.variable_counter)
#            G.variable_counter = G.variable_counter + 1
            variable1 = "?"+ "num" + str(G.num_count)
            G.num_count = G.num_count + 1
            G.totalnumber = G.totalnumber + 1
            temp = unary_singleton[0]
            print "temp",temp
            print "len(temp)",len(temp)
            temp[len(temp)-1] = variable1
            G.notequal = True
            G.notequalvar = variable1
            print "zztempzz",temp
            temp2 = ["notequal0"] + [variable1]
            temp3 = [temp] + [temp2]
            newprecond.extend(temp3) #changed to extend 1/12/14
            return newprecond
#            return temp3
        elif test == False:  ###not in the precondition not in the effect (not (handempty))  #wrong for empty shot!!!
            print "fred34" #think should do nothing here                removed 1/16/14
#            temp = unary_singleton[0]
#            print "temp",temp
#            print "len(temp)",len(temp)
#            temp[len(temp)-1] = 0
#            print "temp",temp
#            return [temp]
#                #not = add 0
#            newprecond.append(temp) #changed to append 1/12/14
            return newprecond
        return newprecond
        
def find_unary_precond(unary_singleton_removal,precond):
    print "unary_singleton_removal",unary_singleton_removal
    print "recond",precond
    if precond == []:
        return False
    elif precond[0] == "and":
        return find_unary_precond(unary_singleton_removal,precond[1:])
    elif find_unary_precond1(unary_singleton_removal,precond[0]):
        return True
    return find_unary_precond(unary_singleton_removal,precond[1:])

def find_unary_precond1(unary_singleton_removal,precond):
    print "zcunary_singleton_removal",unary_singleton_removal
    temp1 = unary_singleton_removal[0]
    print "zcprecond",precond
    if temp1[0] == precond[0]:
        return True
    temp = precond[0]
    if temp1[0] == temp[0]:
        return False
    return []

def addgoalmores(newprecond,unary_goal_preds,goal_more,removed_pred):
    print "newprecond",newprecond
    print "unary_goal_preds",unary_goal_preds
    print "goal_more",goal_more
    print "removed_pred",removed_pred
    if G.goal_more <> []:
        newprecond.insert(0, G.goal_more)
        return newprecond
    return newprecond

#***how get 1 and 0??? how mind numbers???

#*add (<> 1 0)
#* blrag >0
#* not blarg = 0

    


def addbigmores(newprecond,store_big_effects):
    print "newprecond",newprecond
    print "storeeffects",store_big_effects
    print "G.direct",G.direct
    print "G.big_more",G.big_more
    if store_big_effects == []:
        return newprecond
    predicate1 = store_big_effects[0]
    print "predicate1",predicate1
    predicate2 = store_big_effects[1]
    predicate3 = store_big_effects[2]
    predicate4 = store_big_effects[3]
    num1 = predicate1[-1]
    print "num1",num1
    temp = predicate2[1]
    num2 = temp[-1]
    print "num2",num2
    num3 = predicate3[-1]
    print "num3",num3
    temp1 = predicate4[1]
    num4 = temp1[-1]
    print "num4",num4
    newmore = G.big_more +[ num2] + [ num1] #switched these to be right for grasp 1/16/14
    newprecond = newprecond + [newmore]
    newmore = G.big_more +[ num3] + [ num4] #switched these to be right for grasp 1/16/14   
    newprecond = newprecond + [newmore]
    return newprecond
#    dummy()
#    num = len(store_big_effects)/2
#    l = range(0,num)
#    addition = 0
#    for i in l:
#       temp1 = store_big_effects[addition]
#       print "temp1",temp1
#       if temp1[0] <> "not":
#           num1 = temp1[-1]
#       else:
#           temp3 = temp1[1]
#           num1 = temp3[-1]
#       print "num1",num1
#       temp_num = addition+1
##       temp2 = store_big_effects[temp_num]
##       print "temp2",temp2
##       if temp2[0] <> "not":
#           num2 = temp2[-1]
#       else:
 #          temp4 = temp2[1]
 #          num2 = temp4[-1]
 #      print "num2",num2
 #      if G.direct[i] == "up":
 #          newmore = G.big_more +[ num2] + [ num1] #switched
 #          print "newmore",newmore
#           newprecond = newprecond + [newmore]
#       else:
#           newmore = G.big_more +[ num1] + [ num2] #swirched
#           print "newmore",newmore
#           newprecond = newprecond + [newmore]
##       G.direct_count = G.direct_count + 1
#       addition = addition +2
#    return newprecond
    
            
    
    
    

def addunaryprecond(newprecond,store_effects):
    print "store_effectsz",store_effects
    if store_effects == []:
        return []
    else:
        effect = addunaryprecond1(newprecond,store_effects[0])
        effectlist = addunaryprecond(newprecond,store_effects[1:])
        print "effectz",effect
        print "effectlistz",effectlist

        if effect == []:
            return effectlist
        elif effectlist== []:
            if not check_if_in(effect,newprecond):                                                          
                return [effect]
            return []
        else:
            print "zzeffect",effect,newprecond
            if not check_if_in(effect,newprecond):
                effectlist.append(effect)
            return effectlist

def addunaryprecond1(newprecond,store_effects):
    
    if store_effects[0] == "not":
        return store_effects[1]
    return []

def check_if_in(mylist,listoflists):
    print "mylist",mylist,"listoflists",listoflists
    if listoflists == []:
        return False
    elif mylist == listoflists[0]:
        return True
    return check_if_in(mylist,listoflists[1:])

#def removeunaryprecond(newprecond,removed_pred):
    

#R
def changeprecond(precond,actionname,num,lists,action,param):
    if precond == []:
        return []
#    if len(precond) == 1:      #added 1/16/14
#        newprecond = ["and"] + [precond]
#        print "hubbanewprecond", newprecond
#        return changeprecond(newprecond,actionname,num,lists,action)
    if precond[0] == "and":
        print "before",precond[1:]
        newprecond = changeprecond(precond[1:],actionname,num,lists,action,param)
        print "kookylists",lists
        print "after",newprecond
        print "G.unary_preds",G.unary_preds
        if G.unary_preds:
            newprecond  = changeunaryprecond(newprecond,G.removed_pred,precond,param)
        print "after2",newprecond
        temp1 = lists[0]
        temp2 = temp1[0]
        print "G.more",G.more,temp2
        if G.more == [] or temp2 in G.more:
            more = "more"
            G.more.insert(0,temp2)
        else: 
            more = "more1"
            print "kooky2",actionname
            G.more.insert(0,temp2)
        extra = changeprecond1(precond,actionname,num,more)
        print "extra",extra
        newprecond.extend(extra)
        newprecond.insert(0,precond[0])
        print "after3",newprecond
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
    print "precond",precond
    first=precond[0]
    newlist = flatten(lists)
    print "zzfirst[0]zz",first
    if ((first[0] == G.predicate or (G.NEWPREDICATE == True and first[0] == G.new_predicate)) and (G.TYPING == False or pddl_typing.checkprecond_typing2(precond[0],action,G.typeof))):
        newprecond = changeprecond(precond[1:],actionname,num,lists,action,param)
        return newprecond
    else:
        newprecond = changeprecond(precond[1:],actionname,num,lists,action,param)
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
def addgoals_outer(myvar,mylist,counts,lists,new_init):                     #! add new goals to the goals description (0s and mores) - never use "lists" do not need
    if G.direction <> "backward":
        return addgoals(mylist,counts,lists,new_init)
    else:
        print "mylist3",mylist,"counts",counts,"lists",lists,"new_init",new_init,"G.direction",G.direction
        name = G.count_name + str(G.count_count)
#        G.goal_more = name
        G.count_count = G.count_count +1
        return addgoals_backward(myvar,mylist,counts[0],lists,new_init,name)


def addgoals_backward(myvar,mylist,counts,lists,new_init,name):
    print "backtop",mylist,"counts",counts,"lists",lists,"new_init",new_init
    if counts == []:
        return new_init
    if mylist == []:
        return []
    elif len(mylist) == 1:
        return addgoals_backward1(myvar,mylist[0],counts[0],mylist[0],new_init,name)
    else:
        print "gothereeee"
        newer_init = addgoals_backward1(myvar,mylist[0],counts[0],mylist[0],new_init,name)
        print "halfway",newer_init
        _DEBUG("newer_init2",newer_init)
        return addgoals_backward(myvar,mylist[1:],counts[1:],mylist[1:],newer_init,name)

def addgoals_backward1(myvar,mylist,counts,lists,new_init,name):
    print "countsback",counts,"lists",lists,"new_init",new_init
    if counts == []:
        return []
#    if len(counts) == 1:
#        new_list = ["count1a1a", lists, counts, 1]
#        temp = new_init[1].append(new_list)
#        return new_init
#    else:
    new_list = [name, myvar, counts, 1]
    if G.added_goal == False:
        print "zznew_listzz", new_list
        G.unary_new_preds.insert(0,new_list)
        G.unary_goal_preds.insert(0,new_list)
        G.added_goal = True
#    new_list = ["count1a1agoals", lists, counts, 1]
    temp = new_init[1].append(new_list)
    print "new_init",new_init
    return new_init



def addgoals(mylist,counts,lists,new_init):
#def addgoals(mylist,counts,lists,new_init):                     #! add new goals to the goals description (0s and mores) - never use "lists" do not need
#    print "mylist3",mylist,"counts",counts,"lists",lists,"new_init",new_init
    #global new_goals
    
#    if debug == True:
    _DEBUG("addgoals",mylist,"counts",counts,"new_init",new_init)
    if counts == []:
        return new_init
    _DEBUG("mylistbrrrr",mylist)
    #_DEBUG("counter",counter)
    _DEBUG("counts",counts)
    _DEBUG("lists",lists)
    print "gethere1"
    if 'new_goals' in globals(): _DEBUG("new_init",G.new_goals)
    print "gethere2",len(mylist)
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
        print "gothereeee"
        newer_init = addgoals1(mylist[0],counts[0],mylist[0],new_init)
        print "halfway",newer_init
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
    print "counts",counts,"lists",lists,"new_init",new_init
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
    print "new_init",new_init
    return new_init
#        print "MUST"
#        if debug == True:
#            print "MUST EXTEND"

#R

def changegoalbackward(myset,init,counter_type,old_vals,object_type) :
    if myset == []:
        return init
    elif len(myset) == 1:
        return changegoalbackward1(myset[0],init,counter_type,old_vals,object_type)
    else:
        new_goal = changegoalbackward(myset[0],init,counter_type,old_vals,object_type)
        print "new_goal_back",new_goal                                                                                                                                         
#        counter_type.insert(len(counter_type),"merge")
        _DEBUG("NEW",new_goal)
        new_goal2 = changegoal(myset[1:],init,counter_type,old_vals,object_type)
        print "new_goal2",new_goal2

#def changegoal(myset,init,counter_type,old_vals,object_type):                         
#    changegoal2(myset,init,counter_type,old_vals,object_type)
#    if G.direction <> "backward":
#        print "hereforward"
#        changegoal2(myset,init,counter_type,old_vals,object_type)
#    else:
#        changegoalbackward(myset,init,counter_type,old_vals,object_type) 


def changegoal(myset,init,counter_type,old_vals,object_type):                                           #! stopped commenting here%%%%%
    _DEBUG("mymyset",myset,"init",init,"counter_type",counter_type)
    print "mymyset",myset,"init",init,"counter_type",counter_type
    if myset == []:
        return init
    elif len(myset) == 1:
        return changegoal1(myset[0],init,counter_type,old_vals,object_type)
    else:
        new_goal = changegoal1(myset[0],init,counter_type,old_vals,object_type)
        print "new_goal",new_goal
        counter_type.insert(len(counter_type),"merge")
        _DEBUG("NEW",new_goal)
        return changegoal(myset[1:],init,counter_type,old_vals,object_type) #! changed new_goal to init...not sure this is right

#R
def changegoal1(myset,init,counter_type,old_vals,object_type):
    print "goalgoal",init
    print "old_vals",old_vals
    print "mymymyset",myset
    _DEBUG("myset",myset)
    _DEBUG("init",init)
    _DEBUG("initkk",init)
    _DEBUG("myset",myset)
    if init == []:
        return init
    else:
        if (init[0] == ":goal"):
            print "here1"
            _DEBUG("AA")
            newinit=[init[0]]
            temp1=init[1]
            temp2=temp1[0]
            _DEBUG("temp2",temp2)
            temp3 = [temp2]
            temp4 = changegoal1(myset,temp1[1:],counter_type,old_vals,object_type)
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
                    return changegoal1(myset,init[1:],counter_type,old_vals,object_type)
            newinit=[init[0]]
            _DEBUG("NEWINT",newint)
            newinit.extend(changegoal1(myset,init[1:],counter_type,old_vals,object_type))
            _DEBUG("newinit",newinit)
            return newinit
        elif len(init[0]) == 3:
            print "here2zaz",init[0]
            _DEBUG("Mike",init[0])
            _DEBUG("CC")
            temp = init[0]
#            print "temp",temp
            _DEBUG("temp",temp)
            _DEBUG("temp",temp)
#            l = range(0,len(myset)-1)
            l = range(0,len(myset))
            for i  in l:
                _DEBUG("myset[i]",myset[i])
                print "myset[i]",myset[i],"temp",temp
                if myset[i] == temp[1]:
                    print "gotherez",myset[i],temp[1]
                    _DEBUG("here1",temp[2])
                    _DEBUG("counter_type",counter_type)
#                    counter_type = [counter_type]              ###need to make 2 lists for -pat without destorying original
                    counter_type.insert(len(counter_type),temp[2]) ##change to set
                    object_type.insert(len(counter_type),temp[1])
                    _DEBUG("aaaa",counter_type)
                    _DEBUG("counter_type",counter_type)
                    _DEBUG("countera", counter_type)
                    old_vals.insert(0,temp[1])
                elif myset[i] == temp[2]:
                    _DEBUG("here2",temp[1])
#                    counter_type = [counter_type]
                    counter_type.insert(len(counter_type),temp[1])
                    object_type.insert(len(object_type),temp[2])
                    _DEBUG("bbbb",counter_type)
                    _DEBUG("counterb", counter_type)
                    print "hereneedtosave2", myset[i],temp[2]
                    old_vals.insert(0,temp[2])
            _DEBUG("call",init[1:])
#            counter_type = [counter_type]
#            print "counter_type",counter_type,"old_vals",old_vals
            print "needtosave",init[0]
            G.removed_goals.insert(0,init[0])
            return changegoal1(myset,init[1:],counter_type,old_vals,object_type)
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
    print "tempermylist",mylist,"counts",counts,"lists",lists,new_init
    temper = addzero(mylist,counts[0],lists[-1],new_init)
    #_PRINT("temper", temper)
    _DEBUG("DDDDONE",temper)
    return temper
#else:
    _DEBUG("MUST EXTEND")


#R
def changeinit(myset,init,counter_type,old_vals):
    temp = myset[0]
    G.temporary_variables.insert(0,temp[-1])
#    print "cimyset",myset
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
#    print "ci1myset",myset
#    print "counter_type",counter_type
#    print"init",init
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
#            print "mysettt",myset,"l",l

            #_PRINT("typeofbug",myset,"temp",temp)
            for i  in l:
#                print "i",i,"l",l,"init[0]",init[0]
                #_PRINT("myset[i]",myset[i],"temp",temp)
#                print "mysett[i]",myset[1],temp,l
                if myset[i] in temp:
                    #_PRINT("win",temp[0])
                    G.typeof = temp[0]
#                    if debug == True:
                    #_PRINT("typeof",G.typeof)
#                    print "temp1",temp[1]
                    G.save_objects.insert(0,temp[1])
#                    print "saveobjects",G.save_objects
                    G.save_unary_predicates.insert(0,temp)
                    G.total_save_unary_predicates.insert(0,temp)
#                    print "total_save_unary_predicates",G.total_save_unary_predicates
#                    print "saveunarypredicates",G.save_unary_predicates
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
            print "temphere",temp
            #_PRINT("important",temp)
#            G.predicate = temp[0]
#            print "PRED",G.predicate             ##current bug...need to store list of predicates
            #_DEBUG("predicate1",G.predicate)
            l = range(0,len(myset)) #!changed from l = range(0,len(myset)-1) might break gripper!!!!
#            print "init[0]",init[0]
#            print "myset",myset
            match=False
            insert=[]
#            print "fixl",l
            for i  in l:
#                print "fixi",i
#                print "myset[i]",myset[i]
#                print "temp[1]",temp[1]
#                print "temp[2]",temp[2]
                #_PRINT("i",i,"l",l)
                #_PRINT("myset",myset[i],"temp",temp[1],"temp",temp[2])
                if myset[i] == temp[1]:
                    print "mysethere",myset[i]
                    G.predicate = temp[0]
                    G.savepredicate = temp[0]
#                    print "santa",temp
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
                print "counter_typec",counter_type
                counter_type.append(insert[0])
                print "counter_typed",counter_type
            _DEBUG("VVVVV",counter_type)
            _DEBUG("match",match)
            if match == False:               #need to add singles to "lists" so they get turned into counts  **MUST have test first to not transform ALL singletons**
                    temp2 = [init[0]]
                    #_PRINT("hereherehere",temp2)
                    temp2.extend(changeinit1(myset,init[1:],counter_type,old_vals)) #!to fix logistics bug
#                    print"temp2kkk",temp2
                    return temp2
            return changeinit1(myset,init[1:],counter_type,old_vals)
        else:
#            print "helphelp",init[0]
#            print "help",init
            newinit=[init[0]]
#            f = open("trace.txt", "a")
#            f.write(str(sys._getframe()))
#            f.write("\n\n")
#            f.close()
            newinit.extend(changeinit1(myset,init[1:],counter_type,old_vals))
#            print "init[0]",init
#            print "newinit",newinit
#            print "isitherea",newinit
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

