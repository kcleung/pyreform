'''
PDDL Merge and Translator - Typing Module

Author: Dr. Patricia Riddle @ 2013
Contact: pat@cs.auckland.ac.nz

Functions used in handling typing during translation

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
from pddl_debug import _DEBUG, _D
from pddl_debug import _PRINT, _P
import pddl_globals as G
import copy
import pddl_core as core
import pddl_utils as utils

#PT
def maketypehierarchy(types):
    _PRINT(len(types))
    mark = False
    store = []
    l=range(0,len(types))
    for i in l:
        if types[i] == ":types":
            fred = 3 #do nothing
        elif types[i] == "-":
            mark = True
        elif mark == True:
            G.ontology.insert(0,[store,types[i]])
            store =[]
            mark = False
        else:
            store.insert(0,types[i])
    #_PRINT("ontology",G.ontology)
    return G.ontology

def countsame(match,mylist):
    count = 0
    l = range(0,len(mylist))
    for i in l:
        if match == mylist[i]:
            count = count + 1
    return count

def makecounts(counts,lists,used):
    #_PRINT("makecounts",counts,"list",lists)
    if counts == []:
        return []
    if counts[0] in used:
        new_list = makecounts(counts[1:],lists[1:],used)
    else:
        new_count = countsame(counts[0],counts)
#    if debug == True:
        #_PRINT("new_vampire", new_count, counts)
        new_list = ["count1a1a", lists[-1], counts[0], new_count]
        used.insert(0,counts[0])
#    if debug == True:
        #_PRINT("chocula",new_list)
        if new_count <> len(counts):
            more_list = makecounts(counts[1:],lists[1:],used)
            new_list = [new_list]
            new_list.extend(more_list)
    if new_list == []:
        return new_list
    elif isinstance(new_list[0],list):
        return new_list
    else:
        return [new_list]


def makecounts_type(newcounts,setofobjects):
    #_PRINT("newcounts1",newcounts,"setofobjects",setofobjects)
    returnlist = []
    if setofobjects == []:
        return returnlist
    elif not isinstance(setofobjects,list):
         l = range(0,len(newcounts))
         for i in l:
             count = ["count1a1a",newcounts[i],setofobjects,0]
             returnlist.append(count)
         #_PRINT("returnlist",returnlist)
         return returnlist
    else:
        list1 = makecounts_type(newcounts,setofobjects[0])
        list2 = makecounts_type(newcounts,setofobjects[1:])
        list1.extend(list2)
        #_PRINT("list1",list1)
        return list1

def test_original_init(predicates,new_init,max_num,init,num):
    if new_init == []:
        return (0, [])
    else:
        num1, remove1 = test_original_init1(predicates,new_init[0],max_num,init,num)
        num2, remove2 = test_original_init(predicates,new_init[1:],max_num,init,num)
        num = num1 + num2
        remove1.extend(remove2)
        return (num, remove1)

def  test_original_init1(predicates,new_init,max_num,init,num):
    print "predicatenew",predicates,num,new_init
    if predicates[0] == new_init[0]:
        num = num + 1
        mylist = []
        mylist.insert(0,new_init)
        return (num, mylist)
    return (0 , [])
    

def makeunarycounts(myvar,save_unary_predicates,new_init,max_num,init,predicates,objects):
    print "save_unary",save_unary_predicates
    myset = []
    myset.insert(0,myvar)
    ontology = G.ontology
    mytypes = core.find_type(myset,objects,ontology)
    G.thetypes.insert(0,mytypes)
    print "typing",mytypes
    if len(save_unary_predicates) == 1:
        num = 0
        print "new_initttt",new_init
        num, removal = test_original_init(save_unary_predicates[0],new_init,max_num,init,num)
        print "num",num,"removal",removal
        num = num + len(save_unary_predicates)
        temp = copy.deepcopy(removal)
        temp2 = []
        temp2.insert(0,num)
        print "temp",temp
        print "temp2",temp2
        temp4 = temp[0]
        temp4.extend(temp2)
        print "temp",temp4
        name = G.count_name + str(G.count_count) #count1a1a
        temp4[0] = name
        G.unary_new_preds.insert(0,temp4)
        G.unary_singleton.insert(0,temp4)
        G.unary_singleton_removal.insert(0,removal[0])
        G.count_count = G.count_count + 1
        temp_list = []
        temp5 = copy.deepcopy(temp4)
        temp_list.insert(0,temp5)
        print "temp_list",temp_list
        print "tada",temp_list,removal
        G.save_unary_predicates = []
        return (temp_list, removal)
    else:
#        myset = []
#        myset.insert(0,myvar)
#        ontology = G.ontology
#        mytypes = core.find_type(myset,objects,ontology)
#        G.thetypes.insert(0,mytypes)
#        print "typing",mytypes
        all_preds = find_all_preds(mytypes,predicates)
        G.all_preds = all_preds
        print "new_init",new_init
        print "allpreds",all_preds
        count = 0
        counts1, removal1 = make_large_counter(all_preds,count,mytypes,myvar,init)
#        all_objects =find_all_objects()
# if some are not unary
        #loop for each object
             #make count

        #loop test_original_init
        #find all preds 
        #make count

#                (holding ?h - hand ?c - container) 
#(contains ?c - container ?b - beverage)  
#  (used ?c - container ?b - beverage)  no in initial state
        #make empty emp no1
        #make clean cl no2
        #make ontable on no3 (do I need hand here??????)

#        temp1 = []
#        temp0 = save_unary_predicates[0]
#        temp1.insert(0,temp0)
#        temp2 = save_unary_predicates[1:]
#        counts1, removal1 = makeunarycounts(myvar,temp1,max_num,init)
#        counts2, removal2 = makeunarycounts(myvar,temp2,max_num,init)
#        counts1.append(counts2)
#        removal1.append(removal2)
        return (counts1, removal1)
        
def make_init_list(myvar,variable_list,all_preds,init):
    print "fudd",myvar
    print "list",variable_list
    print "all_preds",all_preds
    print "init",init
    set_objects = G.save_objects
    print "set_objects", set_objects
    test = list(set(set_objects))
    print "tttest",test,myvar
    pred_list = return_predicates(myvar,init)
    print "pred_list",pred_list
    counter = makecounter(pred_list,variable_list)
    counter.insert(0,myvar)
    name = G.count_name + str(G.count_count)
    counter.insert(0,name)
    print "addunary",counter
    G.unary_new_preds.insert(0,counter)
    G.unary_big.insert(0,counter)
    print "unary_big",G.unary_big
    G.count_count = G.count_count +1
#    counter.insert(0,"count1a1a")
    counter.extend([1])
    print "kookycounter",counter
    counter_list = [counter]
    print "beginbegin",counter_list
    return makecounter_loop(test,counter_list,init,variable_list)
    
def makecounter_loop(myvars,counter_list,init,variable_list):
    if myvars == []:
        return counter_list
    new_counter_list = makecounter_loop1(myvars[0],counter_list,init,variable_list)
    return makecounter_loop(myvars[1:],new_counter_list,init,variable_list)

def makecounter_loop1(myvar, counter_list,init,variable_list):
    print "myvarrrr",myvar
    pred_list = return_predicates(myvar,init)
    print "pred_list",pred_list
    counter = makecounter(pred_list,variable_list)
    print "begin",counter_list
    found, new_counter = check_duplicate_increment(counter,counter_list)
    print "new_counterkook",new_counter
    if found:
        return new_counter
    counter.insert(0,myvar)
    name = G.count_name + str(G.count_count)
    counter.insert(0,name)
    G.unary_new_preds.insert(0,counter)
    print "addunary2",counter
    G.count_count = G.count_count +1
    counter.insert(0,name)
#    counter.insert(0,"count1a1a")
    counter.extend([1])
    print "kookycounter",counter
    new_counter_list.insert(0,counter)
    return new_counter_list

def check_duplicate_increment(counter,counter_list):
    print "ccounter",counter,"ccounter_list",counter_list
    if counter_list == []:
        return (False, counter_list)
    found, new_counter_list = check_duplicate_increment1(counter,counter_list[0])
    if found:
        return (found, [new_counter_list])
    return check_duplicate_increment(counter,counter_list[1:])

def check_duplicate_increment1(counter,counter_list):
    print "len(counter)",len(counter),counter_list
    l = range(0,len(counter))
    for i in l:
        print "kooki",i,counter[i],counter_list[i+1]
        if counter[i] <> counter_list[i+2]:
            return (False,counter_list)
    print "len(counter)+2", len(counter)+2
#    print "counter_list[len(counter)+1]" , counter_list[len(counter)+1]  
    location = len(counter) + 2
    print "location", location
    counter_list[location] = counter_list[location] + 1
    print "newcounterlist",counter_list
    return (True, counter_list)


def makecounter(pred_list,variable_list): #pred list and variable list
    if variable_list == []:
        return []
    mylist = makecounter1(pred_list,variable_list[0])
    mylist2 = makecounter(pred_list,variable_list[1:])
    mylist2.insert(0,mylist)
    return mylist2
    
def makecounter1(pred_list,variable_list): #pred list and single variable
    print "pred_listb",pred_list,"variable_list",variable_list
    if pred_list == []:
        print "variable_list",variable_list
        mylist = variable_list[2]
        return mylist[-1]
    print "sad",pred_list[0],variable_list
    found, value = makecounter2(pred_list[0],variable_list)
    print "really", found,value
    if found == True:
        return value
    print "loop",pred_list[1:]
    return makecounter1(pred_list[1:],variable_list)

def makecounter2(pred_list,variable_list): #pred variable and single variable
    print "pred_lista",pred_list,variable_list
    if pred_list[0] == variable_list[1]:
#        mylist = variable_list[1]
        temp=variable_list[2]
        print "temptemp",temp
        return (True, temp[0])
    return (False, [])
        
        

def return_predicates1(myvar,init):
    if myvar in init:
        return init
    return []
    
def return_predicates(myvar,init):
    if init == []:
        return []
    list1 = return_predicates1(myvar,init[0])
    list2 = return_predicates(myvar,init[1:])
    if list1 == []:
        return list2
    elif list2 == []:
        return [list1]
    else:
        list2.insert(0,list1)
        return list2

def make_large_counter(all_preds,count,mytypes,myvar,init):
    variable_list = make_large_counter0(all_preds,count,mytypes)
    print "variable_list",variable_list
    G.variable_pred_list = variable_list
    counts = make_init_list(myvar,variable_list,all_preds,init)
    print "kookylist",counts
    return (counts,[])

def make_large_counter0(all_preds,count,mytypes):
    print "all_pred",all_preds
    if all_preds == []:
        return ([])
    else:
        print "elmo"
        variable_value_list1 = make_large_counter1(all_preds[0],count,mytypes)
        print "variable_value_list1",variable_value_list1
        new_count = count + 1
        variable_value_list2  = make_large_counter0(all_preds[1:],new_count,mytypes)
        variable_value_list2.insert(0,variable_value_list1)
        print "variable_value_list2",variable_value_list1
        return variable_value_list2

def make_large_counter1(predicate,count,mytypes):   ##must add test for bound variables temp = right or shot!!!
    print "bert",predicate,count
    if len(predicate) == 4:
        temp = str(predicate[0])
        val1 = temp[:2] + str(count)
        val2 = "no" + str(count)
        value_list = [val1,val2]
        print value_list
        mytype = "signtype" + str(count)
        G.new_variables.insert(0,[temp,mytype,value_list])
        temp = []
#        G.new_variables.insert(0,[temp,val1,val2])
        temp.insert(0, value_list)
        temp.insert(0,mytype)
        temp.insert(-1,predicate[0])
        print "tempppp", temp
        return temp
    elif len(predicate) == 7:
        print "mytypes",mytypes,"pred4",predicate[3],"whole",predicate
        if predicate[3] in mytypes:
            val1 = "no" + str(count)
            G.extra_nos.insert(0,[predicate[6],val1])
            value_list = [val1]
            temp = []
            temp.insert(0, value_list)
            temp.insert(0,predicate[6])
            temp.insert(-1,predicate[0])
            print "tempppp1", temp
            return temp
        else:
            val1 = "no" + str(count)
            G.extra_nos.insert(0,[predicate[3],val1])
            value_list = [val1]
            temp = []
            temp.insert(0, value_list)
            temp.insert(0,predicate[3])
            temp.insert(-1,predicate[0])
            print "tempppp1", temp
            return temp

        
        

    
    
    #add objects ro prob file reform.addobjects(temp_objects,max_num) called in core
    #apredicate to domain file reform.changepredicates(predicates) called in core
    #fix init in prob file addinit_typing
    #fix goal in prob file reform.changegoal(lists,goals,counter_type2,old_vals2) and reform.addgoals(lists,counter_type2,lists,G.new_goals)
    #fix actions reform.changeactions(lists,actions,num) 
    #fix typing
    
    #new_objs no1 - beverage (us)
    #         cl no2 - sign1
    #         co no1 - beverage
    #         em no3 - sign2
    #         no4 -hand (ho)
    #         on no5 - sign3
    #         1 2 3 4 - num

    #count1a1a(shot2 no1 cl no3 em no5 on) 
    #predicate make_predicate =
    


def find_all_preds(mytypes,predicates):
    print "mytypes",mytypes
    print "predicates",predicates
    if predicates == []:
        return []
    elif predicates[0] == ":predicates":
        return find_all_preds(mytypes,predicates[1:])
    elif not isinstance(predicates[0],list):
        if matches(mytypes,predicates):
            return predicates
        return []
    else:
        list1 = find_all_preds(mytypes,predicates[0])
        print "list1",list1
        if list1 == []:
            return find_all_preds(mytypes,predicates[1:])
        else:
            list2 = find_all_preds(mytypes,predicates[1:])
            print "list2a",list2
            if list2 == []:
                temp = []
                temp.insert(0,list1)
                return temp
            else:
                list2.append(list1)
                print "list2b",list2
                return list2

def matches(mytypes,predicate):
    print "mytpes",mytypes,predicate
    if mytypes == []:
        return False
    else:
        if mytypes[0] in predicate:
            return True
        return matches(mytypes[1:],predicate)

    

def remove_unary(new_init,removal_list):
    print "remove1",new_init,"removal",removal_list
    if new_init == []:
        return []
    else:
        temp1 = remove_unary1(new_init[0],removal_list)
        temp2 = remove_unary(new_init[1:],removal_list)
        temp2.insert(0,temp1)
        return temp2

def remove_unary1(new_init,removal_list):
    print "remove2",new_init,"removal2",removal_list
    if removal_list == []:
        return new_init
    else:
        temp1 = remove_unary2(new_init,removal_list[0])
        temp2 = remove_unary1(new_init,removal_list[1:])
        print "temp1",temp1,"temp2",temp2
        if temp1 == []:
            return []
        else:
            return temp2

def remove_unary2(new_init,removal_list):
    print "new_init",new_init,removal_list
    if new_init == removal_list:
        return []
    return new_init

    

#def makeunarycounts(save_unary_predicates):
#    temp = save_unary_predicates
#    return temp

def addinit_typing1(mylist,counter_type,new_init,more_list,original_objects,typing,max_num,init,predicates,objects):
    print "mylsit",mylist
    print "counter_type", counter_type
    print "new_init",new_init
    print "more_list",more_list
    print "original_objects",original_objects
    print "typing",typing
    print "max_num",max_num
    countlist1 = []

    #_PRINT("mylist",mylist)
    _DEBUG("testing")
#    new_count = len(counter_type)  #! + 1
#    print "new_vampire", new_count
#    new_list = ["count1a1a", mylist[-1], counter_type[0], new_count]
#    print "chocula",new_list
    print "G.predicate",G.predicate
    print "G.savepredicate",G.savepredicate
    print "G.save_objects",G.save_objects
    print "G.save_unary_predicates", G.save_unary_predicates ###add makecount for unary**1**

####must add in predicates from predicates list (holding ?h - hand ?c - container) (contains ?c - container ?b - beverage) (used ?c - container ?b - beverage)
#(must have stored all predicates from initial state not just left and shot1) - so can get counts

#why handempty seperate handempty ontable shot => holding shot => handempty ontable shot
#(count hand enmpy shot)
    if counter_type == [] and G.save_unary_predicates <> []:
        countlist1, removallist = makeunarycounts(mylist[-1],G.save_unary_predicates,new_init,max_num,init,predicates,objects)
    countlist = makecounts(counter_type,mylist,[])    #this is where count predicates are made
#    print "removallist",removallist
    if countlist == []:
        countlist = countlist1
    elif countlist1 <> []:
        countlist.append(countlist1)
    print "countlist",countlist
    print "counter_type",counter_type,"G.save_unary_predicates",G.save_unary_predicates,"G.multiple_reforms",G.multiple_reforms,
#    if debug == True:
    #_PRINT("countlist",countlist)
#    if counter_type == [] and G.multiple_reforms <> []:  #for barman but not nomystery  2/26/2014
    if counter_type == [] and G.save_unary_predicates <> []:
        new_init = remove_unary(new_init,removallist)   #****fix removal here****
    if G.max_num < max_num:
        G.max_num = max_num
    print "remove",new_init       
    new_init.extend(countlist)
    print "aaded",new_init
    l = range(0,max_num)
    _DEBUG("set max")
#    max_num = len(counter_type)+2                             #why + 2 ????
    myvar = mylist[-1]
#    myletter = myvar[0]
    myletter = myvar[:2]
    print "myvar??",myvar
    print "myletter",myletter
    print "zzmore_list",more_list
    mymore = "more" + myletter          #changed back I hope 1/12/14
    for i in l:
        if not i in more_list:
            print "KKKKK",mylist[-1]
            if G.multiple_reforms:
                new_temp = [mymore, i, i+1]          #1/8/2014 change
                more_list.insert(0,i)
                new_init.append(new_temp)
            else:
                new_temp = ["more", i, i+1]
                more_list.insert(0,i)
                new_init.append(new_temp)
#    print "new_init",new_init
#    myextralist = return_places(counts[0],counter_type[0],original_list,typing)           #%%%%put this back to handle ""ins"" (must fix changeaction too)
#mytype = find_type(counts[0],new_init)                       #%%%problem with typing
#    if debug == True: 
#        print "mytype", mytype
#    mylist = makelist(mytype,counts[0],new_init)
#    if debug == True: 
#        print "mylist", mylist
#    if debug == True: 
#        print "NEW_INIT",new_init
    print "new_initkoo",new_init
    _DEBUG("chocchocmylist",mylist,"counter_type",counter_type)
    print "temper2mylist",mylist,counter_type,mylist[-1],new_init,original_objects,typing
    temper = addzero_typing(mylist,counter_type,mylist[-1],new_init,original_objects,typing) #need to fix more to moreh***
    print "temper",temper
    _DEBUG("DDDDONE",temper)
    return temper
#else:
    _DEBUG("MUST EXTEND")

def addinit_typing(mylist,counter_type,new_init,more_list,original_objects,typing,max_num,init,predicates,objects):
    print "josie",mylist,len(mylist)
    print "counter_type",counter_type
    #_PRINT("mylist1",mylist)
    _DEBUG("typinglists",mylist,"counter_type",counter_type)
    if mylist == []:
        return []
    elif len(mylist) == 1:
        _DEBUG("mylist",mylist)
        return addinit_typing1(mylist[0],counter_type[0],new_init,more_list,original_objects,typing,max_num,init,predicates,objects)
    else:
        newer_init = addinit_typing1(mylist[0],counter_type[0],new_init,more_list,original_objects,typing,max_num,init,predicates,objects)
        return addinit_typing(mylist[1:],counter_type[1:],newer_init,more_list,original_objects,typing,max_num,init,predicates,objects)

def completeset_typing(lists,objects,typing):
    _DEBUG("listslistslists",lists)
    _DEBUG("objects",objects)
    _DEBUG("typing",typing)
    if lists == []:
        return []
    extra = completeset_typing1(lists[0],objects,typing)
    #_PRINT("extrareal",extra)
    extra2 = completeset_typing(lists[1:],objects,typing)
    #_PRINT("extrareal",extra)
    #_PRINT("extrareal2",extra2)
    extra.extend(extra2)
    return extra
#    final = []
#    l = range(0,len(extra))
#    m = range(0,len(extra2))
#    for i in l:
#        for j in m:
#            print "extra(i)",extra(i),"extra2(j)",extra2(j)
#            if extra(i) == extra2(j):
#                final.insert(0,extra(i))
#    print "final",final
#    return final

def completeset_typing1(lists,objects,typing):
    _DEBUG("lists",lists,"lists[len(lists)]",lists[len(lists)-1],"objects",objects,"typing",typing)
    extra = []
    l = range(0,len(objects))
    for i in l:
        if lists[len(lists)-1] == objects[i]:
            mytype = typing[i]
    for i in l:
        if typing[i] == mytype:
            MISSING = True
            k = range(0,len(lists))
            for m in k:
                if objects[i] == lists[m]:
                    MISSING = False
            if MISSING == True:
                extra.insert(0,[objects[i]])
    return extra

def dotyping(objects,typing):
    _DEBUG("objects",objects,"typing",typing)
    if objects == []:
        return []
    leftover=[]
    count = [0]
    new_objects = dotyping1(objects,typing,leftover,count)
    leftover2 = []
    _DEBUG("count",count)
    new_type = dotyping2(leftover,typing,leftover2,count)
#    typing.insert(len(typing),new_type)
    newer_objects = dotyping(leftover2,typing)
    new_objects.extend(newer_objects)
    return new_objects

def dotyping1(objects,typing,leftover,count):
    _DEBUG("objects1",objects,"typing",typing,"leftover",leftover,"count",count)
    if objects[0] == "-":
        leftover += objects[1:]
        return []
    else:
        nextobj = dotyping1(objects[1:],typing,leftover,count)
        nextobj.insert(0,objects[0])
        count[0] = count[0] + 1 
        return nextobj

def dotyping2(objects,typing,leftover,count):
    _DEBUG("objects2",objects,"typing",typing,"leftover",leftover,"count",count)
#    if count[0] == 1:
#        typing.insert(len(typing),objects[0])
#    else:
    l = range(0,(count[0]))
    for i in l:
        typing.insert(len(typing), objects[0])
    leftover += objects[1:]
    

def fix_counter_type(counter_type):                                            #! this is the stupid code that changes [rooma rooma merge rooma rooma] to [[rooma rooma][rooma rooma]
    temp = []
    return fix_counter_type1(counter_type,temp)

def fix_counter_type1(counter_type,temp):                                      #! this is the second routine called from ebfore that has the "temp" variable we are building up
    _DEBUG("c",counter_type,"t",temp)
    if counter_type == []:
        return [temp]
    if counter_type[0] == "merge" and counter_type[1:] == []:
        return temp
    if counter_type[0] == "merge":
        temp2 = []
        reallist = fix_counter_type1(counter_type[1:],temp2)
        _DEBUG("temp2", temp2, "temp", temp)
        temp = [temp]
        temp.extend(reallist)
        _DEBUG("realtemp", temp)
        return temp
    temp.append(counter_type[0])
    return fix_counter_type1(counter_type[1:],temp)

def returntypes(typeof,thetypes):
    print "typeof",typeof
    print "thetypes",thetypes
    if thetypes == []:
        return []
    else:
        first = returntypes1(typeof,thetypes[0])
        if first <> []:
            return first
        else:
            second = returntypes(typeof,thetypes[1:])
            return second

def returntypes1(typeof,thetypes):
    if typeof in thetypes:
        return thetypes
    return []

def checkprecond_typing(precond,action,typeof):
# if not checkprecond_typing_part1(precond,action,typeof):
    print "thetypes",G.thetypes
    checkset = returntypes(typeof,G.thetypes)
#     return checkprecond_typing_part2(precond,action,checkset)
# 
#def checkprecond_typing_part2(precond,action,thetypes)
#
#def checkprecond_typing_part1(precond,action,typeof):
    print "typeof",typeof
    print"action",action
    print "checkset",checkset
    found = False
    _DEBUG("action",action,"precond",precond)
    l = range(0,len(action))
    for i in l:                                                  #! break domain list into important pieces
        if action[i] == ":parameters":
            myobject = action[i+1]
            _DEBUG("objects1",myobject)
    j = 0
#    while j+2 < len(myobject):
#        _DEBUG("myobject",myobject[j+2],"typeof",typeof)
#        print "checkseta",checkset,"myobject[j+2]",myobject[j+2],"typeof",typeof 
#        if myobject[j+2] == typeof or myobject[j+2] in checkset:
#            print "checksetb",checkset,"myobject[j+2]",myobject[j+2],"typeof",typeof
#            realtype = myobject[j]
#            found = True
#        j = j+3
#    return found 
    while j < len(myobject):
        _DEBUG("myobject",myobject[j],"typeof",typeof)
        print "checkseta",checkset,"myobject[j+2]",myobject[j],"typeof",typeof 
        if myobject[j] == typeof or myobject[j] in checkset:
            print "checksetb",checkset,"myobject[j+2]",myobject[j],"typeof",typeof
            realtype = myobject[j]
            found = True
        j = j+1
    return found 
#    print "realtype",realtype
#    l = range(0,len(precond))
#    for i in l:
#        if realtype in precond[i]:
#            return True
#    return False

def checkprecond_typing2(precond,action,typeof):
    found = False
    _DEBUG("action",action,"precond",precond)
    l = range(0,len(action))
    for i in l:                                                  #! break domain list into important pieces
        if action[i] == ":parameters":
            myobject = action[i+1]
            _DEBUG("objects1",myobject)
    j = 0
    while j+2 < len(myobject):
        _DEBUG("myobject",myobject[j+2],"typeof",typeof)
        if myobject[j+2] == typeof:
            realtype = myobject[j]
            found = True
        j = j+3
    l = range(0,len(precond))
    _DEBUG("realtype1",realtype,"precond",precond)
    for i in l:
        if  isinstance(precond[i], list):
            k = range(0,len(precond[i]))
            temp = precond[i]
            for j in k:
                _DEBUG("realtype3",realtype,"temp",temp[j])
                if realtype == temp[j]:
                    return True
        else: 
            _DEBUG("realtype2",realtype,"precond",precond[i])
            if realtype == precond[i]:
                return True
    return False 

def addzero_typing(objects,locations,theobject,new_init,original_objects,typing):
    print "00objects",objects,"locations",locations,"theobject",theobject,"new_init",new_init,"original_objects",original_objects,"typing",typing
#    if debug == True:
    _DEBUG("addzerotyping",objects,"locations",locations,"theobjects",theobject) #,"new_init",new_init
    if locations == []:
#        newzero = ["count1a1a",theobject, original_objects[i] , "0"]
        print "newzero"
#        new_init.append(newzero)
    else:
        thelocation = locations[0]
        l = range(0,len(original_objects))
        for i in l:
            if thelocation == original_objects[i]:
                theindex = i
        thetype = typing[theindex]
        for i in l:
            if typing[i] == thetype:
                if not original_objects[i] in locations:
                    newzero = ["count1a1a",theobject, original_objects[i] , "0"]       
                    _DEBUG("newzero",newzero)
                    print "newzero",newzero
                    new_init.append(newzero)
    print "new_init",new_init
    return new_init
#    if debug == True: 
#        print "new_init",new_init
#    mylist2 = ["count1a1a",mytype, mylist[0] , "0"]
#    if debug == True: 
#    print "checklist",mylist2,"and",new_init
#    if semimatch(mylist2,new_init) == False:
#        new_init.append(mylist2)
#    if debug == True: 
#        print "newest",new_init
#    return new_init

def find_type(counter,new_init):
    _DEBUG("ft_counter",counter)
    _DEBUG("new_init",new_init)
    if new_init == []:
        _DEBUG("AAA")
        return "NONE"
    elif len(new_init[0]) == 1:
        _DEBUG("BBB")
        return find_type(counter,new_init[1:])
    elif len(new_init[0]) == 2:
        _DEBUG("CCC")
        temp = new_init[0]
        _DEBUG("temp",temp)
        _DEBUG("temp1",temp[1])
        if temp[1] == counter:
            return temp[0]
        else:
            _DEBUG("DDD")
           
            return find_type(counter,new_init[1:])
    else:
                 _DEBUG("EEE")
                 _DEBUG("len",len(new_init[0]))
                 _DEBUG("new",new_init[0])
                 return find_type(counter,new_init[1:])
