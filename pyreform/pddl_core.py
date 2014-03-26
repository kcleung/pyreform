'''
PDDL Merge and Translator - Main Module

Author: Dr. Patricia Riddle @ 2013
Contact: pat@cs.auckland.ac.nz

Translates PDDL files using an automated planner in order to improve performance

Core functions called directly from main code

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

#**goal is wrong in barman - DONE
#fix objects ** (need to get no numbers created in init global vairalble fix in addobjectsextra1 - DONE
#need to had other nos to other object types (new method - global variable) - DONE
#remove old handempty - DOME
#**no zeros are created in barman - DONE
#*fix on 0s to have beverage work correctly -DONE
#*fix actions stopped at bug in -- DONE
#File "/home/prid013/googlecode/opt/pddl/bin/pyreform/pddl_reformulation.py", line 1107, in is_last_loop_outer
#    return is_last_loop_outer(param,types[1])
#IndexError: string index out of range
#are mores in initial state??? -DONE
#mores in inital state are based on object mores and moreh
#mores in operators are based on predicates moreha and moreon  !!!! need both to be objects
#plus check to make sure add # for goals like fill-shot n1 and n2 - DONE
#add notequas in initial state -DONE
#fix param lists of actions (preconditions only not fixed) - DONE
#add code for add additonal actions (shaker) and for specialising the type on the shot version!!! - DONE
##**need obejct list already created ** use makehierarcy ontology???? NEED TO KNOW IF SPLIT AND SPECIALISE = DONE

#* fix binding variables - almost done (must use ontology)

#* make_large_counter1 change to avoid "right" or "shot" being a variable or a "no3"

#**type hierarchy is wrong (fix addnum in reformulate.py)

#** 3 new predicate must be added handempty count1a1a and count1a1agoal



#solution path transform


#remove prints
#test other domains

#from itertools import product
import copy
import shlex
import re
import sys
import itertools
#import traceback
from pyparsing import nestedExpr

import pddl_globals as G
from pddl_debug import _DEBUG, _D
from pddl_debug import _PRINT, _P
import pddl_ancillary as ancillary
from pddl_preprocess import remove_comments
import pddl_typing
import pddl_reformulation as reform
import pddl_postprocessing as post
import pddl_planner as planner


def remove_from_list(myset,actions,ontology,objects):
    print "mysetrepeat",myset
    if myset == []:
        return []
    first = test_operator(myset[0],actions,ontology,objects)
    print "first",first
    rest = remove_from_list(myset[1:],actions,ontology,objects)
    print "rest",rest
    if first <> []:
        rest.insert(0,first)
        return rest
    else:
        return rest

def find_more_type(mytype,ontology):
    print "mytype",mytype,"onotlogy",ontology
    if ontology == []:
        return []
    firstlist = ontology[0]
    if mytype in firstlist[0]:
        firsttype = firstlist[1]
        resttype = find_more_type(firsttype,ontology[1:])
        resttype.insert(0,firsttype)
        return resttype
    else:
        return find_more_type(mytype,ontology[1:])

def find_type(myset,objects,ontology):
    mytype = find_first_type(myset[0],objects)
    print "mytype",mytype
    moretypes = find_more_type(mytype,ontology)
    moretypes.append(mytype)
    return moretypes

def find_first_type(myobj,objectlist):
    if myobj == objectlist[0]:
        return  find_dash(objectlist[1:])
    else:
        return find_first_type(myobj,objectlist[1:])

def find_dash(objectlist):
    if objectlist[0] == "-":
        return objectlist[1]
    else:
        return find_dash(objectlist[1:])
    
def type_match(mytypes,parameters):
    print "mytypes",mytypes
    print "parameters",parameters
    if mytypes == []:
        return (False,[])
    if mytypes[0] in parameters:
        myvars1 = find_variables(mytypes[0],parameters)
        match, myvars2 = type_match(mytypes[1:],parameters)
        print "myvars2",myvars2,myvars1
        myvars2.append(myvars1)
        return (True, myvars2)
    else:
        return type_match(mytypes[1:],parameters)
    
def find_variables(mytype,parameters):
    print "parameters",parameters
    if parameters == []:
        return []
    elif parameters[-1] == mytype:
            myvar = goback_until_dash(parameters[0:-1])
            return myvar
    else:
        return find_variables(mytype,parameters[0:-1])
    
def goback_until_dash(parameters):
    if parameters[-1] == "-":
        temp = parameters[0:-1]
        return temp[-1]

def get_parameters(action):
    if action[0] == ":parameters":
        return action[1]
    else:
        return get_parameters(action[1:])

def get_preconditions(action):
    print "action",action
    if action[0] == ":precondition":
        temp = action[1]
        if temp[0] <> "and":
            temp2 = []
            temp2.insert(0,action[1])
            return temp2
        return action[1]
    else:
        return get_preconditions(action[1:])

def test_type_oneoperator(mytypes,action):
    print "mytypes",mytypes
    print "myactions",action
    parameters = get_parameters(action)
    print "parameters", parameters
    matched, myvars = type_match(mytypes,parameters)
    if matched == True:
        print "myvars",myvars
        matched, preconditions = test_precondition(myvars,action)
        print "preconditions2", preconditions
        if matched == True:
            if test_effects_vars(myvars,action,preconditions):
                print "gothere",preconditions,"mytypes",mytypes
                return True
            print "failed",preconditions,"types",mytypes
            return False
    return True

def test_effects_vars(myvars,action,preconditions):
    if myvars == []:
        return True
    elif test_effects(myvars[0],action,preconditions):
        return test_effects_vars(myvars[1:],action,preconditions)


def test_effects(myvar,action,preconditions):
    print "freaky",preconditions
    if preconditions == []:
        return True
    elif len(preconditions[0]) == 2:
        print "testing",preconditions[1:]
        return test_effects(myvar,action,preconditions[1:])
    elif test_effect(myvar,action,preconditions[0]):
        return test_effects(myvar,action,preconditions[1:])

def found_predicates(myvar,precondition,effect):
    print "gothere5", precondition
    if precondition == []:
        return True
    elif no_not_predicate(precondition,effect) and found_other_predicate(myvar,precondition,effect):
        print "yeloow"
        return False
    print "black"
    return True

def no_not_predicate(precondition,effect):
#        found_predicates(myvar,precondition,effect[1:])
    new_precondition = [ 'not' ]
    new_precondition.insert(1,precondition)
    print "new_precondition",new_precondition
    print "effect", effect
    if new_precondition in effect:
        print "gothere2"
        return False
    print "fail1",new_precondition,"effect",effect
    return True

def found_other_predicate(myvar,precondition,effect):
    print "gethere3",myvar,precondition,effect
    if effect == []:
        return False  #switched last
    elif found_other_predicate1(myvar,precondition,effect[0]):
        return found_other_predicate(myvar,precondition,effect[1:])
    return True

def found_other_predicate1(myvar,precondition,effect):
    print "mushy",myvar,precondition,effect
    if precondition[0] == effect[0]:
        if match_variable(myvar,precondition[1:],effect[1:]):
            print "pink"
            return True
        print "blue"
        return False
    return True  #last change

def match_variable(myvar,precondition,effect):
    print "husky",myvar,precondition,effect
    if precondition[0] == effect[0]:
        if precondition[0] == myvar:
            if match_other_vars(precondition[1:],effect[1:]):
                return True  #switched both
            return False
        return match_variable(myvar,precondition[1:],effect[1:])
    if match_other_vars(precondition[1:],effect[1:]):
        print "purple"
        return False
    return True

def match_other_vars(list1,list2):
    print "list1",list1,list2
    if list1 == []:
        return True
    if list1[0] == list2[0]:
        return match_other_vars(list1[1:],list2[1:])
    return False
        


def test_effect(myvar,action,precondition):
    print "testingprecond",precondition
    if precondition == []:
        return True
    effect = get_effects(action)
    if found_predicates(myvar,precondition,effect) <> True:
        return False
    return True
        
def get_effects(action):
    print "action",action
    if action[0] == ":effect":
        return action[1]
    else:
        return get_effects(action[1:])

def vars_preconditions(myvars,precondition):
    print "preconditions4", precondition
    if myvars == []:
        return (True, [])
    found, important_precond = var_preconditions(myvars[0],precondition)
    print "important1",important_precond
    if found == True:
        found2, important_precond_list = vars_preconditions(myvars[1:],precondition)
        print "important2",important_precond_list
        print "found2",found2
        if found2 == True:
            if isinstance(important_precond[0],list) and important_precond_list == []:
                print "important4",important_precond
                return (True,important_precond)
            else:
                important_precond_list.insert(0,important_precond)
                print "important3",important_precond_list
                return (True, important_precond_list)
        return (True, important_precond)
    return (False, [])

def var_preconditions(myvar,precondition):
    print "precondition3",precondition
    if precondition == []:
        return (False, [])
    else:
        if myvar in precondition[0]:
            found1 , precond1 = var_preconditions(myvar,precondition[1:])
            if found1 == True:
                print "precond1",precond1
                if isinstance(precond1[0],list):
                    precond1.insert(0,precondition[0])
                    print "precond2",precond1
                    return (True, precond1)
                else:
                    print "precond1[0]",precond1[0]
                    print "precond1",precond1,"precondition[0]",precondition[0]
                    temp = []
                    temp.insert(0,precond1)
                    temp.insert(0,precondition[0])
                    print "precond3",temp
                    return (True, temp)
            else:
#                print 
#                temp =[]
#                temp.insert(0,precondition[0])
                return (True,precondition[0])
        else:
            found1 , precond1 = var_preconditions(myvar,precondition[1:])
            if found1 == True:
                return (True,precond1)
            return (False,[])
                                                 
    
    

    

def test_precondition(myvars,action):
    preconditions = get_preconditions(action)
    print "myvars",myvars
    print "preconditions",preconditions
    matched, preconditions = vars_preconditions(myvars,preconditions)
    print "preconditionsfailed",preconditions
    if matched == True:
        return (matched, preconditions)
    return (False, [])

def test_type_operator(mytypes,actions):
    if actions == []:
        return True
    if test_type_oneoperator(mytypes,actions[0]):
        print "yeah"
        return test_type_operator(mytypes,actions[1:])
    else:
        return False

def test_operator(myset,actions,ontology,objects):
    print "ontology",ontology
    print "objects", objects
    print "myset",myset
    mytypes = find_type(myset,objects,ontology)
    print "mytypes",mytypes
#    G.append
    if test_type_operator(mytypes,actions):
        print "yesy",myset
        return myset
    else:
        return []


def check_both_ways(j,j_list,k,k_list):
    if same_pred_lists(j,j_list,k,k_list) and same_pred_lists(k,k_list,j,j_list):
        return True
    return False

def same_pred_lists(j,j_list,k,k_list):
    print "call",j,j_list,k,k_list
    if j_list == []:
        print "match", j_list
        return True;
    l = j_list[0]
    for m in k_list:
        if l[0] == m[0]:
            print "check",l,m
            if same_pred(j,l,k,m):
                print "free",k,m
                return same_pred_lists(j,j_list[1:],k,k_list)
    return False
             
def same_pred(j,list1,k,list2):
    print "bird",list1,list2,j,k
    if list1 == []:
        return True
    if list1[0] == list2[0] or (list1[0] == j and list2[0] == k):
        return same_pred(j,list1[1:],k,list2[1:])
    else: 
        return False
        

def find_subset(myvar,mylist):
    for k in mylist:
        print "k",k
        if k[0] == myvar:
            print "list",k
            return k[1]

def make_init_subsets(objects,init):
    superset = []
    for k in objects:
        myset = []
        for j in init:
            if reform.fun(k,j):
                myset.append(j)
        print "k",k
        l = [k]
        print "l",l
        print "myset",myset
        mylist = [myset]
        mylist.insert(0,k)
        print "real",mylist
        superset.append(mylist)
    return(superset)


def read_input(domain_file, problem_file):
    '''
    Read in the two input files
    '''

    domain = remove_comments(domain_file)
    prob = remove_comments(problem_file)
    #! if debug == True: sys.argv
    #myfiledomain = open(sys.argv[1])           #! open domain file               #remove 2
    #!open("/Users/prid013/Documents/IPCdomains/benchmarks3/blocks/domain.pddl")
    #myfileprob = open(sys.argv[2])             #! open problem file              #remove 4
    #!probfileName, probfileExtension = os.path.splitext(myfileprob)
    #!open("benchmarks3/blocks/probBLOCKS-4-0.pddl", "r")
    #!myfile3 = open("benchmarks3/blocks/domain-pat-auto.pddl", "w")
    #!myfile4 = open("benchmarks3/blocks/p01-pat-auto.pddl", "w")

    #! regex = re.compile('(:objects.*?)',re.DOTALL)
    #! regex2 = re.compile('(:requirements.*?)')
    #prob = myfileprob.read()                   #! read in problem file           #remove 1
    #print "bugbug",prob
    #! matches = re.search(regex,prob)

    #! if debug == True: matches.group(0)
    #! string1 = str(matches.group(0))
    #! string2 = string1[9:-2]
    #! if debug == True: "string1", string1, "string2",string2
    #!string3 = string2.replace(" ",",")

    #! objects1 = string2.split()
    #! if debug == True: "mike", objects1    

    return (domain, prob)

def parse_domain(domain):
    '''
    Parse the domain input file
    '''

    num = domain.find("(")
    #!if debug == True: num
    num2=len(domain)
    #!if debug == True: num2
    domain2 = domain[num:num2]
    #!if debug == True: domain2
    domain_list1 = nestedExpr('(',')').parseString(domain2).asList()         #!turn domain string into list
    #!if debug == True: domain_list1
    domain_list1_temp = domain_list1[0]
    domain_list1_real = domain_list1_temp[1:]
    #!if debug == True: "domain_list1_real", domain_list1_real
    actions = []
    requirements = []
    types = 0
    predicates = []
    for i in domain_list1_real:                                               #! break domain list into important pieces
        if i[0] == ":requirements":
            G.HASREQUIREMENTS = True
            requirements = i
        if i[0] == ":predicates":
            predicates = i
        if i[0] == ":types":
            types = i
        if i[0] == ":functions":
            G.HAVEFUNCTIONS = True
            G.functions = i
        if i[0] == ":action":
            actions.append(i)

    return (domain2, requirements, predicates, types, actions, domain_list1_real, domain_list1_temp)

def parse_problem(prob):
    '''
    Parse the problem input file
    '''

    num3 = prob.find("(")
    _DEBUG(num3)
    num4=len(prob)
    _DEBUG(num4)
    front = prob[0:num3-1]
    prob2 = prob[num3:num4]
    _DEBUG(prob2)
    prob_list2 = nestedExpr('(',')').parseString(prob2).asList()               #! turn prob string into list
    _DEBUG(prob_list2)
    _DEBUG("tester", prob_list2[0])
    prob_list2_temp = prob_list2[0]
    prob_list2_real = prob_list2_temp[1:]
    _DEBUG("prob_list2_real", prob_list2_real)
    #! text_file = open("Output.txt", "w")

    #! text_file.write("Purchase Amount: " 'TotalAmount')

    #!text_file.close()

    objects1 = []
    goals = []
    init = []

    for i in prob_list2_real:                                                  #! break domain list into important pieces
        if i[0] == ":objects":
            objects1 = i
        if i[0] == ":goal":
            goals = i
        if i[0] == ":init":
            init = i
        if i[0] == ":metric":
            G.HASMETRIC = True
            G.metric = i


    #! object_index = prob_list2.index(":objects")
    #! if debug == True: "object_index", object_index

    return (prob2, objects1, goals, init, prob_list2_real, prob_list2_temp)    

def process_typing(requirements, types, objects1):
    '''
    Process any typing if applicable
    '''

    #global TYPING
    #domain = myfiledomain.read()              #! read in domain file    #remove 3
    #!regex2 = re.compile("(:action .*)" )
    #!matches2 = re.search(regex2,domain)
    #!if debug == True: matches2.group(0)
    G.TYPING = False
    #! matches2 = re.search(regex2,domain)
    #! string4 = str(matches2.group(0))
    #! string5 = string4[14:-2]
    #! if debug == True: "string4", string4, "string5",string5
    #! requirements = string5.split()
    #! if debug == True: "require", requirements
    #! if ":typing" in requirements:
    #!     objects = []
    #!     G.typeof = []
    #!     G.TYPING = True
    #!     l = range(0,len(objects1)/3)
    #!    for i in l:
    #!        j = i*3
    #!        objects.append(objects1[j])
    #!        G.typeof.append(objects1[j+2])
    #!    if debug == True: "objects",objects
    #!    if debug == True: "typeof",G.typeof
    #! else:
    #!    objects = objects1

    G.TYPING = False
    #global typeof
    G.typeof = None
    
    #! if G.TYPING == true:
    #!    actions = domain_list1[0][6:]
    #!else:
    #!    actions = domain_list1[0][4:]
    SOKOBAN = False
    G.ontology = []
    typing = []
    
    if requirements <> []:                                                      #! this is the typing code that currently does not work
        if ":typing" in requirements:
            G.TYPING = True
            G.ontology = pddl_typing.maketypehierarchy(types)
            objects = pddl_typing.dotyping(objects1[1:],typing)                             #%%%%have to put objects1[0] back on...have to add types back on later
    #        print "objects", objects, "typing", typing, len(objects), len(typing)
    #! put the object typing stuff in here
    #        G.TYPING = True
    #        objects = []
    #        G.typeof = []
    #        l = range(1,(len(objects1)/3)+1)
    #        for i in l:
    #            j = (i*3)-2
    #            objects.append(objects1[j])
    #            G.typeof.append(objects1[j+2])
    #            if debug == True:
    #                print "objects",objects
    #            if debug == True:
    #                print "typeof",G.typeof
        else:
            objects=objects1
    else:
        objects = objects1

    return (G.ontology, typing, objects, G.typeof, SOKOBAN)    


def test_reformulate(newdirection,objects, actions, goals, prob2, init, ontology, objects1):
    print "objects",objects
    print "objects1",objects1
    '''
    Check if reformulation is required/applicable
    '''

    myset = []
    #global TYPING

    #!goals = prob_list2[0][5:]
    _DEBUG("actions",actions)
    _DEBUG("goals",goals)
    REFORMULATE=True
    FOUND=False
    for k in objects:
     for j in actions:
      _DEBUG(j)
      _DEBUG(k)
      if reform.fun(k,j):                                            #! test to make sure object not mentioned in action
          _DEBUG("test1")
          REFORMULATE=False
    for k in objects:
        _DEBUG("repeat",k)
        #! for j in goals:
    #!    j=goals[0]
        j=goals
        _DEBUG("jaz",j,"cam")
        if reform.fun(k,j):                                         #! test to see if object mentioned in goal
            for k2 in objects:                               #!test to check which objects go together
    #!            if debug == True: "k",k,"type",G.typeof[objects.index(k)]
    #!            if debug == True: "k2",k2,"type",G.typeof[objects.index(k2)]
                if k <> k2: #and (G.TYPING == False or G.typeof[objects.index(k)] == G.typeof[objects.index(k2)]):            #got rid of extra things becuase adding typing
                    _DEBUG("k",k)
                    _DEBUG("k2",k2)
    #!                goals1 = goals[0]
    #!                goals2 = goals1[1]
    #!                goals3 = goals2[1:]
                    goals1 = goals[1]
                    goals3 = goals1[1:]
                    _DEBUG("goals3",goals3)
                    list1 = reform.fun2(k,goals3)                   #! must try all goals with k not just first
                    _DEBUG("list1",list1)

                    pred1=list1[0]
                    rest1=list1[1]
                    _DEBUG("pred1",pred1)
                    _DEBUG("rest1",rest1)
                    while goals3 <> []:                       #! iterates through the set of goals
                        _DEBUG("abby",goals3,"k2",k2)
                        list2 = reform.fun2(k2,goals3)               #! returns the pairs of objects that should be merged
                        _DEBUG("DEBUG",list2)
                        _DEBUG("cccccccbug",list2)
                        _DEBUG("bug",list2)
                        if list2 <> None:
                            pred2 = list2[0]
                            rest2 = list2[1]
                            _DEBUG("list2",list2)
                            _DEBUG("pred2",pred2)
                            _DEBUG("rest2",rest2)
                            _DEBUG("NO0")
                            if pred1 <> None and pred2 <> None and pred1[0] == pred2[0] and reform.compare(pred1,pred2) == False and (len(pred1) == 2 or len(pred2) == 2): #this branch is sobokan specific (will also be called with micon) I can't figure out how to comment out one branch without messing up the indent......just ignore this branch
                                #_PRINT("TRIPLEHELP")
                                _DEBUG("YES1")
                                _DEBUG("k", k)
                                _DEBUG("k2",k2)
                                _DEBUG("spencer")
                                myset.append([k,k2])
                                print "myset1",myset
                                _DEBUG("garth")
    #!                            mytype.append([G.typeof[objects.index(k)],G.typeof[objects.index(k2)]])
                                _DEBUG("test5",myset)
                                FOUND = True
    #! 1) add search for action that achieves "list2"
    #! 2) find something else in that action that has "k2" in it
    #! 3) make sure it is a predicate with 2 variables
    #! 4) add this to goal twice once with k and once with k2
    #1 5) add that values are not equal
                                for i in actions: #!look through all actions
                                    _DEBUG("i")
                                    parameters=i[3]
                                    temp_effects1=i[7]
                                    _DEBUG("temp_effects1",temp_effects1)
                                    effects=temp_effects1[1:]
                                    _DEBUG("parameters",parameters)
                                    _DEBUG("effects",effects)
    #!                                if debug == True: "type",G.typeof[objects.index(k2)]
                                    if G.TYPING == False or (G.TYPING == True and G.typeof[objects.index(k2)] in parameters): #make sure action uses type of variable
                                        if G.TYPING == True :
                                            parameter_index = parameters.index(G.typeof[objects.index(k2)])
                                            _DEBUG("parameter_index", parameter_index)
                                            variable = parameters[parameter_index-2]
                                            _DEBUG("variable",variable)
                                        SOKOBAN = True
                                        for m in effects:   #!look through effects for effect on this variable
                                            _DEBUG("m",m)
                                            if m[0] <> "not":
                                                _DEBUG("m[0]",m[0])
                                                if variable in m:  #! make sure variable is in add

                                                    _DEBUG("important",len(m))
                                                    if len(m) > 2:
                                                        effects_index = m.index(variable)
                                                        _DEBUG("effects_index", effects_index)
                                                        effect_variable = m[effects_index]
                                                        _DEBUG("effect_variable",effect_variable)
                                                        effect = m
                                                        _DEBUG("effect",effect)
                                                        new_goal = reform.replace(variable,k2,effect)
                                                        if new_goal.index(k2) == 1:
                                                            newer_goal1 = reform.replace(new_goal[2],"?x1",new_goal)
                                                            newer_goal2 = reform.replace(new_goal[2],"?x2",new_goal)
                                                            newer_goal3 = ["not", ["=", "?x1", "?x2"]]
                                                        else:
                                                            newer_goal1 = reform.replace(new_goal[1],"?x1",new_goal)
                                                            newer_goal2 = reform.replace(new_goal[1],"?x2",new_goal)
                                                            newer_goal3 = ["not", ["=", "?x1", "?x2"]]

                                                        _DEBUG("new_goal", new_goal)
                                                        _DEBUG("goals",goals)
                                                        temp_goal = goals[1]
                                                        _DEBUG("temp_goal",temp_goal)
                                                        temp_goal2 = temp_goal[1:]
                                                        _DEBUG("temp_goal2",temp_goal2)
                                                        temp_goal2.append(newer_goal1)
                                                        _DEBUG("temp_goal2",temp_goal2)
                                                        temp_goal2.append(newer_goal2)
                                                        temp_goal2.append(newer_goal3)
                                                        _DEBUG("temp_goal2",temp_goal2)
                                                        temp_goal2.insert(0,temp_goal[0])
                                                        _DEBUG("temp_goal2",temp_goal2)
    #!                                                    temp_goal2.insert(0,goals[0])
                                                        G.new_goals = [goals[0],temp_goal2]
                                                        _DEBUG("new_goals", G.new_goals)
                                                        #!if debug == True: "string_old_goals",''.join(goals)
                                                        #!new_prob = prob2.replace(''.join(goals),''.join(G.new_goals))
    #!new_prob = replace(goals,G.new_goals,prob)
    #!                                                    new_goals_string = tostring(G.new_goals)
      #!                                                  if debug == True: "new_goals_string",new_goals_string
                                             #!           old_goals_string = tostring(goals)
                                             #!           if debug == True: "old_goals_string",old_goals_string
                                             #!           new_prob = prob2.replace(old_goals_string,new_goals_string)
                                                        _DEBUG("brown", prob_list2)
                                                        temp_prob = prob_list2[0]
                                                        _DEBUG("blue", temp_prob[0:5])
                                                        temptemp = temp_prob[0:5] #!removed brackets
                                                        _DEBUG("temptemp", temptemp)
                                                        _DEBUG("new_goals",G.new_goals)
                                                        newnew_goals = G.new_goals
                                                        temptemp.append(newnew_goals)
                                                        _DEBUG("orange", temptemp)
                                                        _DEBUG("yellow", temp_prob[6])
                                                        temptemp.append(temp_prob[6])
                                                        _DEBUG("green", temptemp)
    #!                                                    new_prob_list = [].append(new_prob_list_temp)
                                                        new_prob = ancillary.tostring(temptemp)
                                                        _DEBUG("new_prob", new_prob)


                                                   #!if effect[8] == "yellow":
                                                    #!if effect[8] == "yellow":
                                                    #!    goals.append(new_goal)
                                                    #!    goals.append(new_goal)
                                                    #!    if effect[1] == variable:
                                                     #!       goals.append(effect

    #!                                for j in i:
    #!                                    if debug == True: "j",j
    #!                                    if debug == True: "j[0]",j[0]
    #!                                    if j[0] == ":effect":
    #!                                        if debug == True:"echo"
    #!                            REFORMULATE = True
                            elif pred1 <> None and pred2 <> None and pred1[0] == pred2[0] and reform.compare(pred1,pred2) == False and (pred1[2] == pred2[2] or pred1[1] == pred2[1]) and ((pred1[1] == k and pred2[1] == k2) or (pred1[2] == k and pred2[2] == k2)):                                                                 #! need last test to stop ball1 mapping to rooma with no typing???
                                _DEBUG("YES2")
                                _DEBUG("k", k)
                                _DEBUG("k2",k2)
                                _DEBUG("pred1", pred1[0])
                                _DEBUG("pred2", pred2[0])
                                _DEBUG("a1",pred1[1])
                                _DEBUG("b1",pred2[1])
                                _DEBUG("a2",pred1[2])
                                _DEBUG("b2",pred2[2])
                                myset.append([k,k2])
                                print "myset2",myset
                                _DEBUG("test6",myset)
                                new_prob = prob2
                                FOUND = True
                                direction = "forward"
    #                            REFORMULATE = True                                                           #! yes we have determined we should reformulate

                            goals3=rest2                                                                      #! look through the rest of the goal list
                            _DEBUG("goals",goals3)
                        else:
                            _DEBUG("help")
                            _DEBUG("k", k)
                            _DEBUG("k2",k2)
                            goals3 = []
    #!
    #!
    #!add third test to say and there is no other talk of K or K2 glue together if goal predicate the same
                _DEBUG("test4")
    #!            REFORMULATE=False

#    if myset == []:   #barman test
    if newdirection == "backward":
        myset = []
        x = 4
        subsets = make_init_subsets(objects,init)  #make subset of intital predicates for each object
        print "subsets",subsets
        myset2 = []
        for j in objects:
            for k in objects:
                if j <> k:
                    x= 4   
                    print "x",x
                    j_list = find_subset(j,subsets)
                    print "j",j,"jlist",j_list
                    k_list = find_subset(k,subsets)
                    print "k",k,"klist",k_list
                    if check_both_ways(j,j_list,k,k_list):
                        myset2.append([j,k])
                        print "myset3",myset2
        print "myset done", myset2
        print "objects1 again",objects1
        myset2 = remove_from_list(myset2,actions,ontology,objects1)
        print "myset again", myset2
        G.direction = "backward"
        direction = "backward"
        if myset2 <> []:
            FOUND = True
            myset = myset2
        #return with myset2 and transform type 2

#loop through object pairs
#make myset2
#make counts from predicate sets
#change ops etc
    return (REFORMULATE, myset, FOUND, newdirection)    #must return which type of reform  #changed direction => newdirection 2/26/2014

def output_prob_file(prob_list2_real,new_objects,new_init,new_goals,prob_list2_temp):
    '''
    Write the reformulated problem file out to a new file
    '''
    print "magic_new_goals", new_goals
    print "new_inti",new_init
    _DEBUG("new_goals",new_goals)
    _DEBUG("new_goals",new_goals)
    new_prob_list=prob_list2_real[0:2]                                                                  #!start putting the new problem list together
    _DEBUG("new_prob_list1",new_prob_list)
    new_prob_list.append(new_objects)
    new_prob_list.append(new_init)
    _DEBUG("new_prob_list2",new_prob_list)
    new_prob_list.append(new_goals)
    if G.HASMETRIC:
        new_prob_list.append(G.metric)
    _DEBUG("new_prob_list3",new_prob_list)
    new_prob_listend=[prob_list2_temp[0]]
    new_prob_listend.extend(new_prob_list)
    _DEBUG("new_prob_list4",new_prob_listend)
    new_prob_done = ancillary.tostring(new_prob_listend)                                                          #!putting the new problem list into a string
    _DEBUG("new_prob_done",new_prob_done)
    new_file_name = "newprob.pddl"
    _DEBUG("new_prob_done",new_prob_done)
    text_file = open(new_file_name, "w")                                                                #!write prob string into a file
    text_file.write(new_prob_done)
    text_file.close()


def reformulate_loop(new_objects,original_objects,lists,myset, domain2, requirements, predicates, types, actions, domain_list1_real, domain_list1_temp, prob2, objects1, goals, init, prob_list2_real, prob_list2_temp, ontology, typing, objects, SOKOBAN, direction,realobjects):
    print "kooky",lists
#    G.all_lists = lists
    print "before",G.all_lists
    if len(lists) == 1:
        G.all_lists.insert(0,lists[0])###why is this only lists[0] instead of lists 3/25/2014
    elif G.all_lists == []:
        G.all_lists =  copy.deepcopy(lists)     ##should probably make this a sublist when rewrite post processing code
    print "after",G.all_lists
    
#    G.all_lists.insert(0,lists)###why is this only lists[0] instead of lists 3/25/2014
    print "objects",objects
    print"init", init
    if G.TYPING == False:
        extra_list = reform.completesets(lists,objects,init)                                                    #! this creates the singleton objects to add to the list
        extra_list = reform.removeduplicates(lists,extra_list)
        extra_list = reform.remove_duplicates(extra_list)
        extra_list = reform.make_listoflist(extra_list)
            #_PRINT("RRRRRRealextra",extra_list)
    else:
        extra_list = pddl_typing.completeset_typing(lists,original_objects,typing)                              #! this adds the singleton objects to the list
        extra_list = reform.removeduplicates(lists,extra_list)
        extra_list = reform.remove_duplicates(extra_list)
            #_PRINT("EEExtra",extra_list)
    _DEBUG("testextra",extra_list)
    print "extra",extra_list
    if extra_list <> []:
        if isinstance(extra_list[0],list):
            lists.extend(extra_list)
        else:
            print "lists",lists
            lists.append(extra_list)
            print "lists2",lists
        #_PRINT("dave_list",lists)
#        if debug == True:
        #_PRINT("stewart_lists",lists)
        #_PRINT("new_objects",new_objects)
    _DEBUG("new_objects",new_objects)
    _DEBUG("init",init)
    counter_type = []
    old_vals = []
    G.save_objects = []
#        if debug == True:
    _DEBUG("testlists4",lists)
    print "init8",init
    print "lists",lists
    new_init = reform.changeinit(lists,init,counter_type,old_vals)                                         #! this changes the init state to the new init state
    print "init9",new_init
    print "counter_typeb",counter_type
    new_init = reform.changeunary(lists,new_init,counter_type,old_vals,actions)
    print "newinit10",new_init
    print "counter_typea",counter_type
#        if debug == True:
    _DEBUG("testlists3",lists)
                #!old_vals was never used #chnages initial state #changes init state by removing stuff you don't want
#        if debug == True:
    _DEBUG("bugbugbugnew_init",new_init)
    _DEBUG("old counter type",counter_type)
    new_counter_type = pddl_typing.fix_counter_type(counter_type)                                               #! this changes [rooma romma merge romma romma] to [[rooma rooma][rooma rooma]]
    newcounter_type = reform.remove_empty(new_counter_type)
                #!stupid code to fix counter_type list becuase I hate python
    counter_type = new_counter_type
    print "countertype",counter_type
        #_PRINT("new counter type",new_counter_type)
        #_PRINT("old_vals",old_vals)
#        print "new_init1111",new_init
        #_PRINT("counter_type",counter_type)
    _DEBUG("save_objects",G.save_objects)
    _DEBUG("old_vals",old_vals)
    _DEBUG("new_init4",new_init)
    _DEBUG("counter_type",counter_type)
    _DEBUG("lista",lists)
    _DEBUG("lists",lists)
    _DEBUG("counter_type",counter_type)
    _DEBUG("init",init)
    _DEBUG("new_init",new_init)
    if G.TYPING == False:
        max_num = reform.findmax(lists)
        _DEBUG("testlists2",lists)
        print "stuckstuck1"
        new_init = reform.addinit(lists,counter_type,lists,new_init,[],max_num)                                        #!adds in new predicates for new init state "the zero counts" and the "mores & and all the counts"
        print "new_init2",new_init
            #_PRINT("bugger",new_init)
        print "newobjsggg",new_objects
        temp_objects = new_objects[1:]
        temp2_objects = new_objects[0]
        temp_objects = reform.addobjects(temp_objects,max_num)
        temp_objects.insert(0,temp2_objects)
        new_objects = temp_objects
        print "newobjskkk",new_objects
            #_PRINT("debugnewobjects",new_objects)
    else:
        _DEBUG("testlists2",lists)
        print "lists",lists
        print "counter_type",counter_type
#            if len(lists) > 1:
#            if isinstance(lists[0],list):   #*****have to add loop here and else for doing once
#                for i in lists:
#                    print "i",i
#                    max_num = reform.findmax(i) #this is wrong!! adds hands and shots together-fixed
#                    max_num = len(i)
#                    print "max_numa",max_num
#                    _DEBUG("testlists",lists)
#                    max_num = len(li
#                    temp = []
#                    temp.insert(0,i)
#                    print "stuck1",temp,counter_type,new_init,original_objects,typing,max_num
#                    new_init = pddl_typing.addinit_typing(temp,counter_type,new_init,[],original_objects,typing,max_num)
#                    print "new_inita",new_init
#                    #_PRINT("bugger2",new_init)
#                    new_objects = reform.addobjects(new_objects,max_num)
#                print "new_initb",new_init
#            else:
        max_num = reform.findmax(lists) #this is wrong!! adds hands and shots together
        print "max_numb",max_num
        _DEBUG("testlists",lists)
        print "stuck",lists,counter_type,original_objects,typing,max_num,new_init
        new_init = pddl_typing.addinit_typing(lists,counter_type,new_init,[],original_objects,typing,max_num,init,predicates,realobjects)
                #_PRINT("bugger2",new_init)
        print "kkknew_initkkk",new_init
        print "newobjskkk",new_objects
        print "G.multiple_reforms",G.multiple_reforms
        print "max_num",max_num
        print "G.second_time",G.second_time

        print "zzsave_unary_predicates",G.save_unary_predicates
        if G.save_unary_predicates <> []:
#            sign_count = 0
            predicate_done = []
            new_objects = reform.addobjectsextra(new_objects,max_num,G.save_unary_predicates,[])
            new_objects = reform.extranos(new_objects)
        print "newobjobjobj",new_objects
        if G.multiple_reforms and G.second_time:
            print "here???"
            new_objects = reform.addobjects_check(new_objects,max_num)
        else:
            new_objects = reform.addobjects(new_objects,max_num) #first fix of objects
        print "newobjslll", new_objects

    _DEBUG("countertypeeee",counter_type)
    _DEBUG("bbbbbnewinit",new_init)
                                                              #!adds in new objects like numbers
    if G.TYPING == True:
        _PRINT("new_objects",new_objects)
        print "kkknew_objects",new_objects
        if not G.second_time:
            G.second_time = True
            new_objects = reform.addbacktypes(new_objects,original_objects,typing) #fixes objects
            print "kkknew_objectskkk",new_objects
            new_objects.insert(0,objects1[0])
        print "new_objects",new_objects
        #_PRINT("ddddnewobjects",new_objects,objects1[0])
    _DEBUG("new_init",new_init)
    _DEBUG("listb",lists)
    counter_type2 = []
    old_vals2 = []
        #_PRINT("lists",lists)
    print "gethere??",goals
    object_type = []
    G.new_goals = reform.changegoal(lists,goals,counter_type2,old_vals2,object_type)                                    #!removes the goal description for new objects
    print "counter_type2zzzz6",counter_type2
    print "object_type",object_type
    print "G.new_goals",G.new_goals
    if G.TYPING == True:
        G.typeof = reform.maketype(lists,original_objects,typing)     #what uses this later???
            #_PRINT("typeoftyping",G.typeof)
        #_PRINT("counter_type2",counter_type2,"new_goals",G.new_goals)
    new_counter_type2 = pddl_typing.fix_counter_type(counter_type2)                                             #! this changes [rooma romma merge romma romma] to [[rooma rooma][rooma rooma]]
    print "counter_type2zzzz5",new_counter_type2
    new_counter_type2 = reform.remove_empty(new_counter_type2)
    print "counter_type2zzzz4",new_counter_type2
        #_PRINT("brr2",new_counter_type2)
    if len(new_counter_type2) == 1:
        counter_type                  #!what does this do????
    counter_type2 = new_counter_type2
    print "counter_type2zzzz",counter_type2, "G.save_unday_predicates",G.save_unary_predicates
    print "lists",lists
    print "new_counter_typ2",new_counter_type2
    print "original_objects",original_objects
    print "typing",typing
    print "predicates",predicates
    print "objects1",objects1
#    if G.TYPING == True and G.save_unary_predicates <> []:       #changed 1/8/2014
    if G.TYPING == True and G.DOUBLE_LOOP == False:# and G.save_unary_predicates <> []:       #changed 1/8/2014 [changed 2/25/2014] check and fix BARMAN!!!  #must fix this at some point so can loop and add extra!!!
        myextralist = reform.return_places(G.typeof,lists,new_counter_type2,original_objects,typing,predicates,objects1)   #added to init list
        print "extralistkkk",myextralist
#            if debug == True:
        _DEBUG("myextralist",myextralist)
        new_init.extend(myextralist)
        _DEBUG("new_init",new_init)
    _DEBUG("newgoals",G.new_goals)
    _DEBUG("new_goals",G.new_goals)
    _DEBUG("new_goals1",G.new_goals)
    _DEBUG("listc",lists)
    _PRINT("counter_typehoho",counter_type2)
    print "counter_type2zzz",counter_type2
    if not isinstance(counter_type2,list):  #probably never is true
        print "counter_type2z",counter_type2
        counter_type2 = list(set(counter_type2))
        print "counter_type2zz",counter_type2
        #_PRINT("counter_type2really",counter_type2)
        #_PRINT("lists",lists)
#        if len(lists) == 1:
#            counter_type2 = [counter_type2[0]]
#            lists = lists[0]
#        counter_type2 = [counter_type2]
#        if isinstance(counter_type2[0],list):
#            p = range(0,len(counter_type2))
#            counter_singleton = []
#            for i in p:
#                counter_singleton.append(list(set(counter_type2[i])))
#        else:
#            counter_singleton = list(set(counter_type2))
##    print "counter_type2",counter_type2,lists,G.new_goals
##    G.new_goals = reform.addgoals(lists,counter_type2,lists,G.new_goals)                                           #!add the goal description for new objects
##    print "finally",G.new_goals
##    num = [0]
##    new_actions = reform.changeactions(lists,actions,num)                                                          #!change the actions
    return (object_type, counter_type2, new_init, new_objects)

def is_same_type(lists,types,ontology,typing,objects,realobjects):
    print "lists",lists
    print "types",types
    print "ontology",ontology
    print "typing",typing
    print "objects",objects
    print "G.pats_favorite",G.pats_favorite
    print "realobjects",realobjects
    j = range(0,len(lists)-1) 
    for i in j:
        temp1 = lists[i]
        print "temp1",temp1
        p = range(0,len(objects)) 
        for s in p:
            print "temp1[1]",temp1[1],"objects[s]",objects[s]
            if temp1[-1] == objects[s]:   #should also be -1
                type1 = return_type(objects[s],realobjects)
                print "list[i]",lists[i]
                r = range(0,len(objects))
                for t in r:
                    temp2 = lists[i+1]
                    print "temp2",temp2
                    if temp2[-1] == objects[t]:   #1 => -1
                        type2 = return_type(objects[t],realobjects)
                        print "lists[i+1]",lists[i+1],
                        print "objects[s}",objects[s]
                        print "objects[t]",objects[t]
                        print "typing[s]",typing[s]
                        print "typing[t]",typing[t]
                        print "type1",type1
                        print "type2",type2
                        if type1 == type2:
                            return True
    return False

def return_type(myobject,objects):
    print "myobject",myobject
    print "objects",objects
    j = range(0,len(objects)) 
    for i in j:
        if myobject == objects[i]:
            mycount = i+1
            while mycount < len(objects):
                if objects[mycount] == "-":
                    return objects[mycount+1]
                mycount = mycount + 1
    dummy()

def reformulate(myset, domain2, requirements, predicates, types, actions, domain_list1_real, domain_list1_temp, prob2, objects1, goals, init, prob_list2_real, prob_list2_temp, ontology, typing, objects, SOKOBAN, direction,realobjects):
    '''
    Perform a reformulation of the input domain and problem files
    '''
    print "aobjects",objects
    print "testerinit",init
    print "zzmysetzz",myset
    G.more = []
    #global TYPING
    print "test"
    _DEBUG("sassy")
    if SOKOBAN == False:                                                                                  #! not in painful sokoban case
#        if debug == True:
        _DEBUG("how", len(myset))
        _DEBUG("myset",myset)
        lists = reform.returnsetsnew(myset,[],[])                                                                #! merge the pairs into a list of arbitrary lists
        print "lists",lists
        #_PRINT("lists",lists)
        _DEBUG("ddddddlists",lists)
        print "lists[0]",lists[0]
        if not isinstance(lists[0],list):          #!should not need this anymore!!!
            temp = [lists] #!temporary fix!!!!
            lists = temp   #!temporary fix!!!!  cheat for only one set of variables must fix when fix for 2 sets
#        if debug == True:
        print "lists2",lists
        _DEBUG("lists2", lists)
        _DEBUG("sylvlists", lists)  #!need to retest for actions....some groups not compatable...before changeobjects
        original_objects = copy.deepcopy(objects)
        print "original_objects",original_objects
        #_PRINT("original_objects",original_objects)
        new_objects = reform.changeobjects(lists,objects)                                                       #! this returns the new object list for the new prob file
        print "newobjs",new_objects
        #_PRINT("new_objects",new_objects)
        #_PRINT("original_objects2",original_objects)
        G.savepredicate = []     # 1/5/2014
#loop starts here
#        new_actions = []
        if len(lists) == 1 or is_same_type(lists,types,ontology,typing,objects,realobjects): 
            print "help1"
            object_type, counter_type2, new_init, new_objects = reformulate_loop(new_objects,original_objects,lists,myset, domain2, requirements, predicates, types, actions, domain_list1_real, domain_list1_temp, prob2, objects1, goals, init, prob_list2_real, prob_list2_temp, ontology, typing, objects, SOKOBAN, direction,realobjects)
            print "new_init_save",new_init
            print "zznew_objects2",new_objects
        else:
            G.DOUBLE_LOOP = True
            print "help2"
            G.multiple_reforms = True
            print "HELP"
            tempa = lists
            new_init = init
            for i in tempa:
                print "outloop",i,tempa
                print "outinit",new_init
                temp = []
                temp.insert(0,i)
                lists = temp
                object_type, counter_type2, new_init, new_objects = reformulate_loop(new_objects,original_objects,lists,myset, domain2, requirements, predicates, types, actions, domain_list1_real, domain_list1_temp, prob2, objects1, goals, new_init, prob_list2_real, prob_list2_temp, ontology, typing, objects, SOKOBAN, direction,realobjects)
#                actions = new_actions
                print "new_init_broke",new_init
                print "zznew_objects1",new_objects
#                print "loop_new_actions",new_actions
#            lists = tempa
#stopped here
#        if G.TYPING == False:
#            extra_list = reform.completesets(lists,objects,init)                                                    #! this creates the singleton objects to add to the list
#            extra_list = reform.removeduplicates(lists,extra_list)
#            extra_list = reform.remove_duplicates(extra_list)
#            extra_list = reform.make_listoflist(extra_list)
#            #_PRINT("RRRRRRealextra",extra_list)
#        else:
#            extra_list = pddl_typing.completeset_typing(lists,original_objects,typing)                              #! this adds the singleton objects to the list
#            extra_list = reform.removeduplicates(lists,extra_list)
#            extra_list = reform.remove_duplicates(extra_list)
#            #_PRINT("EEExtra",extra_list)
#        _DEBUG("testextra",extra_list)
#        print "extra",extra_list
#        if extra_list <> []:
#            if isinstance(extra_list[0],list):
#                lists.extend(extra_list)
#            else:
#                lists.append(extra_list)
#        #_PRINT("dave_list",lists)
##        if debug == True:
#        #_PRINT("stewart_lists",lists)
#        #_PRINT("new_objects",new_objects)
#        _DEBUG("new_objects",new_objects)
#        _DEBUG("init",init)
#        counter_type = []
#        old_vals = []
#        G.save_objects = []
##        if debug == True:
#        _DEBUG("testlists4",lists)
#        new_init = reform.changeinit(lists,init,counter_type,old_vals)                                         #! this changes the init state to the new init state
#        print "newinit",new_init
#        print "counter_typea",counter_type
##        if debug == True:
#        _DEBUG("testlists3",lists)
#                #!old_vals was never used #chnages initial state #changes init state by removing stuff you don't want
##        if debug == True:
#        _DEBUG("bugbugbugnew_init",new_init)
#        _DEBUG("old counter type",counter_type)
#        new_counter_type = pddl_typing.fix_counter_type(counter_type)                                               #! this changes [rooma romma merge romma romma] to [[rooma rooma][rooma rooma]]
#        newcounter_type = reform.remove_empty(new_counter_type)
#                #!stupid code to fix counter_type list becuase I hate python
#        counter_type = new_counter_type
#        print "countertype",counter_type
#        #_PRINT("new counter type",new_counter_type)
#        #_PRINT("old_vals",old_vals)
#        print "new_init1111",new_init
#        #_PRINT("counter_type",counter_type)
#        _DEBUG("save_objects",G.save_objects)
#        _DEBUG("old_vals",old_vals)
#        _DEBUG("new_init4",new_init)
#        _DEBUG("counter_type",counter_type)
#        _DEBUG("lista",lists)
#        _DEBUG("lists",lists)
#        _DEBUG("counter_type",counter_type)
#        _DEBUG("init",init)
#        _DEBUG("new_init",new_init)
#        if G.TYPING == False:
#            max_num = reform.findmax(lists)
#            _DEBUG("testlists2",lists)
#            new_init = reform.addinit(lists,counter_type,lists,new_init,[],max_num)                                        #!adds in new predicates for new init state "the zero counts" and the "mores"
#            print "new_init2",new_init
#            #_PRINT("bugger",new_init)
#            temp_objects = new_objects[1:]
#            temp2_objects = new_objects[0]
#            temp_objects = reform.addobjects(temp_objects,max_num)
#            temp_objects.insert(0,temp2_objects)
#            new_objects = temp_objects
#            #_PRINT("debugnewobjects",new_objects)
#        else:
#            _DEBUG("testlists2",lists)
#            print "lists",lists
#            print "counter_type",counter_type
##            if len(lists) > 1:
##            if isinstance(lists[0],list):   #*****have to add loop here and else for doing once
##                for i in lists:
##                    print "i",i
##                    max_num = reform.findmax(i) #this is wrong!! adds hands and shots together-fixed
##                    max_num = len(i)
##                    print "max_numa",max_num
##                    _DEBUG("testlists",lists)
##                    max_num = len(li
##                    temp = []
##                    temp.insert(0,i)
##                    print "stuck1",temp,counter_type,new_init,original_objects,typing,max_num
##                    new_init = pddl_typing.addinit_typing(temp,counter_type,new_init,[],original_objects,typing,max_num)
##                    print "new_inita",new_init
##                    #_PRINT("bugger2",new_init)
##                    new_objects = reform.addobjects(new_objects,max_num)
##                print "new_initb",new_init
##            else:
#            max_num = reform.findmax(lists) #this is wrong!! adds hands and shots together
#            print "max_numb",max_num
#            _DEBUG("testlists",lists)
#            print "stuck"
#            new_init = pddl_typing.addinit_typing(lists,counter_type,new_init,[],original_objects,typing,max_num)
#                #_PRINT("bugger2",new_init) 
#           new_objects = reform.addobjects(new_objects,max_num)
#
#        _DEBUG("countertypeeee",counter_type)
#        _DEBUG("bbbbbnewinit",new_init)
#                                                              #!adds in new objects like numbers
#        if G.TYPING == True:
#            _PRINT("new_objects",new_objects)
#            new_objects = reform.addbacktypes(new_objects,original_objects,typing)
#            new_objects.insert(0,objects1[0])
#        #_PRINT("ddddnewobjects",new_objects,objects1[0])
#        _DEBUG("new_init",new_init)
#        _DEBUG("listb",lists)
#        counter_type2 = []
#        old_vals2 = []
#        #_PRINT("lists",lists)
#        G.new_goals = reform.changegoal(lists,goals,counter_type2,old_vals2)                                    #!removes the goal description for new objects
#        if G.TYPING == True:
#            G.typeof = reform.maketype(lists,original_objects,typing)
#            #_PRINT("typeoftyping",G.typeof)
#        #_PRINT("counter_type2",counter_type2,"new_goals",G.new_goals)
#        new_counter_type2 = pddl_typing.fix_counter_type(counter_type2)                                             #! this changes [rooma romma merge romma romma] to [[rooma rooma][rooma rooma]]
#        new_counter_type2 = reform.remove_empty(new_counter_type2)
#        #_PRINT("brr2",new_counter_type2)
#        if len(new_counter_type2) == 1:
#            counter_type                  #!what does this do????
#        counter_type2 = new_counter_type2
#        if G.TYPING == True:
#            myextralist = reform.return_places(G.typeof,lists,new_counter_type2,original_objects,typing,predicates,objects1)
##            if debug == True:
#            _DEBUG("myextralist",myextralist)
#            new_init.extend(myextralist)
#            _DEBUG("new_init",new_init)
#        _DEBUG("newgoals",G.new_goals)
#        _DEBUG("new_goals",G.new_goals)
#        _DEBUG("new_goals1",G.new_goals)
#        _DEBUG("listc",lists)
#        _PRINT("counter_typehoho",counter_type2)
#        if not isinstance(counter_type2,list):  #probably never is true
#            counter_type2 = list(set(counter_type2))
#        #_PRINT("counter_type2really",counter_type2)
#        #_PRINT("lists",lists)
#        if len(lists) == 1:
#            counter_type2 = [counter_type2[0]]
#            lists = lists[0]
#        counter_type2 = [counter_type2]
#        if isinstance(counter_type2[0],list):
#            p = range(0,len(counter_type2))
#            counter_singleton = []
#            for i in p:
#                counter_singleton.append(list(set(counter_type2[i])))
#        else:
#            counter_singleton = list(set(counter_type2))
#        G.new_goals = reform.addgoals(lists,counter_type2,lists,G.new_goals)                                           #!add the goal description for new objects
#        output_prob_file(prob_list2_real,new_objects,new_init,G.new_goals,prob_list2_temp)
#        #_PRINT("counter_type2",counter_type2)
#        #_PRINT("newgoals2",G.new_goals)
#        _DEBUG("new_goals",G.new_goals)
#        _DEBUG("new_goals",G.new_goals)
#        _DEBUG("flinstones",lists,actions)
#        num = [0]
#        new_actions = reform.changeactions(lists,actions,num)                                                          #!change the actions
#loop ends here
        print "counter_type222",counter_type2
        print "lists",lists
#        print "newgoals",G.new_goals
#        new_list = []
#        list1 = [lists[1]]
#        print "list1",list1
#        new_list.insert(0,[lists[1]])
#        new_list.insert(0,[lists[0]])
#        print "new_list",new_list
#        new_list = [['package-1'],[ 'package-2']]   ###*****fix number 1
#        new_counter_type2 = [['city-loc-5'],[ 'city-loc-2']]

#        new_counter_type2 = [counter_type2[0],counter_type2[1]]
#        G.new_goals = reform.addgoals(new_list,new_counter_type2,new_list,G.new_goals)                                           #!add the goal description for new objects              #        G.new_goals = reform.addgoals(lists,counter_type2,lists,G.new_goals)                                           #!add the goal description for new objects    

        print "finally",object_type,counter_type2
        print "zznew_objects3",new_objects
        print "lists",lists
        first_list = lists[0]
        last_var = first_list[-1]

        if G.direction <> "backward":
            
            G.new_goals = reform.addgoals_outer(last_var,lists,counter_type2,lists,G.new_goals)     
        else:
            G.new_goals = reform.addgoals_outer(last_var,object_type,counter_type2,object_type,G.new_goals)                                           #!add the goal description for new objects                   
        print "finallyfinally",G.new_goals
        print "finallynew_init",new_init     #stopped here looking for bug
        print "unary_preds",G.unary_new_preds
        print "new_objects",new_objects
        temp_objects = new_objects[1:]
        print "temp_objects",temp_objects
        object_list = make_object_list(temp_objects)
        G.pats_favorite = object_list
        fix_bound_variables(G.pats_favorite,G.temporary_variables,G.bound_variables)
#        if G.unary_new_preds <> []:
#            new_init = make_big_zeros(new_init,object_list,G.unary_new_preds)
            #remove original from this list to avoid a 4 and a 0
        num = [0]
        print "zzz"
        print "new_init",new_init
        print "zzz"
        total_list = G.all_lists
        print "total_list",total_list
        print "znew_objectsa",new_objects
        G.new_object_list = new_objects
        new_actions = reform.changeactions(total_list,actions,num)                #!change the actions    
        print "zznewactions",new_actions
       # if G.new_object_list <> == []:        #%
       #     new_objects = G.new_object_list
        print "zzazobject_list",object_list
        if G.unary_new_preds <> []:
            new_init = make_big_zeros(new_init,object_list,G.unary_new_preds)
            #remove original from this list to avoid a 4 and a 0
        if G.notequal == True:
            new_init = addnotequal(new_init,new_objects)
        print "znew_objectsb",new_objects
        print "prob_list2_real",prob_list2_real
        print "new_objects",new_objects  #OK here 2/7/14
        print "zzzzznew_init",new_init
#        print "G.new_goals",new_goals
        print "prob_list2_temp",prob_list2_temp
        output_prob_file(prob_list2_real,new_objects,new_init,G.new_goals,prob_list2_temp)
        #_PRINT("counter_type2",counter_type2)
        #_PRINT("newgoals2",G.new_goals)
        _DEBUG("new_goals",G.new_goals)
        _DEBUG("new_goals",G.new_goals)
        _DEBUG("flinstones",lists,actions)
        print("done_new_actions",new_actions)
        _PRINT("debugstorage",G.storage)
        _PRINT("debugstorage2",G.storage2)
        #_PRINT("debugstorage3",G.storage3)
        #_PRINT("reallyreally", new_actions)
        _DEBUG("scooby",new_actions)
        print "critica;G.HASREQUIREMENTS",G.HASREQUIREMENTS
        print "domain_list1_real[0:2]",domain_list1_real[0:2]
        if G.HASREQUIREMENTS:
            new_domain_list = domain_list1_real[0:2]
        else:                                         #added else to make abrman work 1/16/2014
            new_domain_list = domain_list1_real[0:1]
        print "new_domain_list",new_domain_list
        _PRINT("new_domain_list", new_domain_list)
        if G.TYPING == True:
            new_types = reform.addnum(types)
            if G.unary_preds <> []:
                new_types = add_types(new_types)
            new_domain_list.append(new_types)
        #! new_domain = reform.changepredicates(lists, domain2)  not sure I need this
        newpredicates = reform.changepredicates(predicates)  #changed Oct 22
        if G.unary_preds <> []:
            print "panda"
            print "big-more",G.big_more
            print "unary_more",G.unary_more
            print "goal_more",G.goal_more
            print "unary_big",G.unary_big
            print "unary_singleton", G.unary_singleton
            print "added_gaol",G.added_goal
#            dummy()
        #_PRINT("brandnew", newpredicates)
        new_domain_list.append(newpredicates)
        print "predicates",predicates
        print "newpredicates",newpredicates
        if G.HAVEFUNCTIONS:
            #_PRINT("waaahooo")
            new_domain_list.append(G.functions)
        _DEBUG("josie",new_domain_list)
        print "new_actions",new_actions
        new_domain_list.extend(new_actions)
        _DEBUG("new_domain_list",new_domain_list)
        new_domain_listend=[domain_list1_temp[0]]
        new_domain_listend.extend(new_domain_list)
        #_PRINT("new_domain_list",new_domain_list)
        print "new_domain_listend",new_domain_listend
        new_domain_done = ancillary.tostring(new_domain_listend)
        #_PRINT("new_domain_done",new_domain_done)
        new_file_name2 = "newdomain.pddl"
        text_file = open(new_file_name2, "w")
        text_file.write(new_domain_done)
        text_file.close()


### run lmcut

### read in file

### run validatir

#    for k1 in objects:
#        for k2 in objects:
#            if k1 <> k2:
#                if debug == True: "fred"
#!test type and then glue together
    else:
        _DEBUG("myset", myset)
#!remove duplicates from myset
        l = range(0,len(myset)-1)  #! this is a cheat should be -1
        _DEBUG("l",l)
        for i in l:
            a = myset[i]
            _DEBUG("a",a)
            temp = myset[i]
            first = temp[0]
            _DEBUG("first",first)
            _DEBUG("new_prob", new_prob)
            _DEBUG("b", new_prob.index(first))
            prob2new = new_prob.replace(temp[0],temp[1])
            _DEBUG("new", prob2new)

#!        if debug == True: "prob_list2",prob_list2
#!        prob_list2[prob_list2.index(myset[i])] = myset[0]
#!        new_prob_list2 = replace(myset[i],myset[0],prob_list2)
#!        if debug == True: "list1again",new_prob_list2
            prob2final = front + prob2new
            _DEBUG("newest", prob2final)

    return ((lists), new_actions)

def add_types(mytypes):
    print "mytypes",mytypes
    mysignlist = ["-", "signtype"]
    l = range(0,len(G.pats_favorite))
    for i in l:
        temp = G.pats_favorite[i]
        print "temp",temp
        temp1 = temp[0]
        print "temp1",temp1
        print "temp1[:8]",temp1[:8]
        if temp1[:8] == "signtype":
            mysignlist.insert(0,temp1)
    print "mysigntype",mysignlist
    mytypes.extend(mysignlist)
    print "newtypes",mytypes
    return mytypes


def fix_bound_variables(pats_favorite,temporary_variables,bound_variables):
    print "G.pats_favorite",pats_favorite
    print "temporary_variables",temporary_variables
    print "bound_variables",bound_variables
    bound_variables = bind_temporary_variables(bound_variables,temporary_variables,pats_favorite)
    print "abound_variables",bound_variables
    G.bound_variables = bound_variables

def bind_temporary_variables(bound_variables,temporary_variables,pats_favorite):
    if temporary_variables == []:
        return []
    bound_variables = bind_temporary_variables1(bound_variables,temporary_variables[0],pats_favorite)
    bound_variables_list = bind_temporary_variables(bound_variables,temporary_variables[1:],pats_favorite)
    if bound_variables == []:
        return bound_variables_list
    elif bound_variables_list == []:
        return bound_variables
    else:
        bound_variables_list.extend(bound_variables)
        return bound_variables_list


def bind_temporary_variables1(bound_variables,temporary_variables,pats_favorite):
    mytype = find_type_of(temporary_variables,pats_favorite)
    temp = [mytype,[temporary_variables]]
    print "zzztempzzz",temp
    return [temp]

def find_type_of(temporary_variables,pats_favorite):
    if pats_favorite == []:
        return []
    val = find_type_of1(temporary_variables,pats_favorite[0])
    if val <> []:
        return val
    return find_type_of(temporary_variables,pats_favorite[1:])

def find_type_of1(temporary_variables,pats_favorite):
    print "temporary_variables",temporary_variables,pats_favorite
    if temporary_variables in pats_favorite[1]:
        return pats_favorite[0]
    return []

def addnotequal(new_init,new_objects):
    print "new_init",new_init
    print "new_objects",new_objects
    print "G.max_num",G.max_num
    l = range(0,G.max_num)
    for i in l:
        num = i + 1
        new_term = ["notequal0"] + [num]
        print "new_term",new_term
        new_init.insert(1,new_term)
    new_term = ["noteq1", 0]
    new_init.insert(1,new_term)
    l = range(1,G.max_num)
    for i in l:
        num = i + 1
        new_term = ["noteq1"] + [num]
        print "new_term",new_term
        new_init.insert(1,new_term)
    totallist = []
    print "zG.notequalno_type",G.notequalno_type
    for mytype in list(set(G.notequalno_type)):
        print "mytype",mytype
        for mylist in G.complete_object_list:
            print "mylist",mylist
            if mylist[0] == mytype:
                print "Here"
                totallist.extend(mylist[1])
    print "totallist",totallist
    new_total_list = list(set(totallist))
    print "new_total_list",new_total_list
###wrong stuff in this list 2/4/2013
    for item in new_total_list:
        print "item",item, item[0:2]
        if item[0:2] <> "no":
            new_term = ["notequalno"] + [item]                                                                                                      
            print "zznew_term",new_term                                                                                                  
            new_init.insert(1,new_term)
    print "zzznew_init",new_init
    return new_init

def  make_big_zeros(new_init,object_list,unary_new_preds):
    if unary_new_preds == []:
        return new_init
    print "zznew_initz",new_init
    print "object_list",object_list
#*****add in here to add cockatials and ingredients    
    print "unary_new_preds", unary_new_preds
    new_init = make_big_zeros1(new_init,object_list,unary_new_preds[0])
    print "newinithere",new_init
    return make_big_zeros(new_init,object_list,unary_new_preds[1:])

def find_pred_lists(unary_new_pred,object_list,unary_param_list,predicate):
    print "zzunary",unary_new_pred
    print "zzobject_list",object_list           #this is that great daat structure I liek [type[values]][type[values]]
    print "object_list",object_list
    my_object_list = copy.deepcopy(object_list) #shot in the dark
    complete_object_list =  add_extras(my_object_list,G.ontology)
    print "complete_object_list",complete_object_list
    G.complete_object_list = complete_object_list
    return find_pred_lists1(unary_new_pred,complete_object_list,1,unary_param_list,predicate)

def return_extras1(mytype,ontology):
    print "mytype",mytype
    print "ontology",ontology
    if mytype == ontology[1]:
        return ontology[0]
    return []

def return_extras(mytype,ontology):
    if ontology == []:
        return []
    else:
        extras = return_extras1(mytype,ontology[0])
        extra_list = return_extras(mytype,ontology[1:])
        if extras == []:
            return extra_list
        elif extra_list == []:
            return extras
        else:
            extra_list.append(extras)
            return extra_list

def add_extras(object_list,ontology):
    print "object_list",object_list
    print "ontology",ontology
    l = range(0,len(object_list))
    for i in l:
        temp = object_list[i]
        extras =  return_extras(temp[0],ontology)
        u = range(0,len(extras))
        save_extras = []
        print "extras",extras
        for v in u:
            real_extras = return_objects_outer(extras,object_list)
            print "real_extras",real_extras
            print "save_extras",save_extras
            save_extras.extend(real_extras)   #made extend??
            print "save_extras",save_extras
        if save_extras <> []:
            print "tempzz",temp
            print "object_list",object_list
            new_save_extras = list(set(save_extras))
            temp[1].extend(new_save_extras)       #made extend 2
            object_list[i] = temp
    return object_list

def return_objects_outer(extras,object_list):
    if extras == []:
        return []
    else:
        temp = return_objects(extras[0],object_list)
        templist = return_objects_outer(extras[1:],object_list)
        if temp == []:
            return templist
        elif templist == []:
            return temp
        else:
            templist.extend(temp)
            return templist


def return_objects(extras,object_list):
    if object_list == []:
        return []
    temp = return_objects1(extras,object_list[0])
    if temp <> []:
        return temp
    return return_objects(extras,object_list[1:])

#def return_objects1(extras,object_list):

def return_objects1(extras,object_list):
    print "extras",extras
    print "object_list",object_list
    if extras == object_list[0]:
        myreturn = copy.deepcopy(object_list[1])
        return myreturn
    return []

def find_pred_lists1(unary_new_pred,object_list,i,unary_param_list,predicate):
    print "i",i,"unary_new_pred",unary_new_pred,len(unary_new_pred)
    if i == len(unary_new_pred):
        return []
    else:
        list1 = find_pred_lists2(unary_new_pred[i],object_list,unary_param_list,predicate)
        i = i + 1
        list2 = find_pred_lists1(unary_new_pred,object_list,i,unary_param_list,predicate)
        list2.insert(0,list1)
        return list2

def find_pred_lists2(myvar,object_list,unary_param_list,predicate):
    print "zmyvarz",myvar,"object_list",object_list
    print "unary_param_list",unary_param_list
    print "predicate", predicate
    mytype = find_type_param(predicate,myvar,unary_param_list)
    print "mytype",mytype
    l = range(0,len(object_list))
    for i in l:
        myvarlist = object_list[i]
        if mytype == myvarlist[0]:
            return myvarlist[1]
#        if myvar in myvarlist[1]:
#            return myvarlist[1]

def  find_type_param(predicate,myvar,unary_param_list) :
    print "zzpredicate",predicate
    for pred in G.bound_variables:
        print "pred",pred
        if myvar in pred[1]:
            return pred[0]
    for pred in unary_param_list:
        if pred[0] == predicate:
            return pred[1] 

def make_big_zeros1(new_init,object_list,unary_new_pred):
    print "zczcnew_init",new_init
    print "object_list",object_list
    print "unary_new_preds", unary_new_pred
    new_replacement = find_pred_lists(unary_new_pred, object_list,G.unary_params,unary_new_pred[0])
    print "new_replacement",new_replacement
    better_replacement = new_replacement[0:-1]
    print "better_replacement",better_replacement
#must replace better_replacement with something based on print "G.unary_params",G.unary_params
    

    if len(unary_new_pred) < 5:
        addition = make_big_zeros_second(new_init,better_replacement,unary_new_pred) # changed 2/1/14
        print "additionZ",addition
##    print "len(newadditions)Z",len(addition)
##    new_addition = remove_unecessary_zeros(addition,G.unary_big)                                                                                                               
##    print "addition",addition                                                                                                                                                        
##    print "len(new_addition)Z",len(new_addition)
##    print "len(new_additions2)",len(new_additions2)     

        new_init.extend(addition)
    print "new_initzaz",new_init
    return new_init

def make_big_zeros_second(new_init,new_replacement,unary_new_pred):  ###bug is here!!! 2/7/14
    print "new_replacement",new_replacement,"unary_new_pred",unary_new_pred
    first_addition = []
    first_addition.insert(0,unary_new_pred[0])
#    first_addition.insert(-1,[0])
    print "first_addition",first_addition
    print "G.unary_params",G.unary_params
    addition = make_big_zeros_second1(new_init,first_addition,new_replacement,unary_new_pred,0)
    ###here is where you remove extras 1/16/14
    return addition


def remove_unecessary_zeros(addition,unary_big):
    myunary_big = unary_big[0]
    print "crazy"
    new_addition = []
    l = range(0,len(addition))
    for i in l:
        temp = addition[i]
        print "tempff1",temp
        print "len(temp)",len(temp)
        print "myunary_big",myunary_big
        print "len(myunary_big)",len(myunary_big)
        if len(temp) < len(myunary_big):
            return addition
        elif remove_unecessary_zeros2(temp,myunary_big,addition[i]) <> []:
            new_addition.insert(0,addition[i])
    return new_addition

def remove_unecessary_zeros2(temp,myunary_big,addition):
    u = range(0,len(myunary_big)-1)
    for v in u:
        if temp[v] <> myunary_big[v]:
            return(addition)
    return []


def make_big_zeros_second1(new_init,addition,new_replacement,unary_new_pred,i):
    print "zzaddition",addition
    print "zznew_replacement",new_replacement
    print "zzunary_mew_pred",unary_new_pred
    name = unary_new_pred[0]
    name_list = [name]
    print "new_replacement_final",new_replacement
    new_replacement.insert(0,name_list)
    new_replacement.append([0])
    print "new_replacement_finaller",new_replacement
    additions = list(itertools.product(*new_replacement))
#map(list, product(
#    additions = map(list product(new_replacement))
    print "additionsW",additions   ##correct this far
    real_additions = map(list,additions)
    print "real additions1",real_additions  ##correct here
    new_additions = remove_duplicate_new(new_init,real_additions)
#    new_additions = remove_duplicate(unary_new_pred,real_additions)
#    new_additions = real_additions
    print "real additions",new_additions ##incorrect here
    print "len(newadditions)",len(new_additions)
    new_additions2 = remove_unecessary_zeros(new_additions,G.unary_big)    #not currently used but works
    print "addition",new_additions2
    print "len(new_additions2)",len(new_additions2)
    return new_additions

def remove_duplicate_new(init,additions):
    if additions == []:
        return []
    new_addition = remove_duplicate_new1(init,additions[0])
    if new_addition == []:
        return remove_duplicate_new(init,additions[1:])
    else:
        addition_list =  remove_duplicate_new(init,additions[1:])
        addition_list.insert(0,new_addition)
        return addition_list

def remove_duplicate_new1(init,addition):
    print "zzinit",init
    for item in init:
        if item[0:-1] == addition[0:-1]:
            return []
    return addition

def remove_duplicate(unary_new_pred,additions):  ###this is removing 
    print "zunary",unary_new_pred,"zadd",additions
    l = range(0,len(additions))
    for i in l:
        temp = additions[i]
        print "unary[0:-1]",unary_new_pred[0:-1],temp[0:-1]
        print "unary",unary_new_pred,temp
#        print "i",i,"l",l,"temp",temp,len(unary_new_pred)
#        print "unary_new_pred[0:-1]",unary_new_pred[0:-1],"temp[0:-1]",temp[0:-1]
#        if unary_new_pred[0:len(unary_new_pred)-1] == temp[0:len(unary_new_pred)-1]:
#        if unary_new_pred[0:len(unary_new_pred)] == temp[0:len(unary_new_pred)]:
        if unary_new_pred[0:-1] == temp[0:-1]:   ##problem here 2/7/14
           
            print "yeazzz",i
            if i == 0:
                return additions[1:]
            elif i == len(additions)-1:
                print "one"
                return additions
            else:
                print "two",additions
                first_part = additions[0:i-1]    ###this is the problem I think!!!!!
                print "firstpart",first_part
                last_part = additions[i+1:]
                print "lastpart",last_part
                first_part.extend(last_part)
                print "first_pat",first_part
                return first_part


def  make_object_list(new_objects):
    print "new_objects", new_objects
#    l = range(0,len(new_objects)) 
#    for i in reversed(l):
#        print "i",i,"new_objects[i]",new_objects[i]
    i = 0
    vals = []
    object_list = []
    print "i",i
    while i < len(new_objects):
        if new_objects[i] == "-":
            mytype = new_objects[i+1]
            mypair = [mytype,vals]
            print "mypair",mypair
            object_list.insert(0,mypair)
            print "object_list",object_list
            i = i + 2
            vals = []
        else:
            print "i",i
            vals.insert(0,new_objects[i])
            i = i + 1
            print "object_list",object_list
    return(object_list)

def postprocess_plan(plan, lists, init, old_actions, goals, direction,new_actions):
    '''
    After running the reformulated input files through the planner
    post process the output sas plan file and save
    '''
    
    newplan = "(" + plan + ")"
    print "PPPlan",newplan
    _DEBUG(newplan)
    tmp_plan_list = nestedExpr('(',')').parseString(newplan).asList()
    plan_list = tmp_plan_list[0]
    #_PRINT("plan_list",plan_list)
    _DEBUG(plan_list)

    _DEBUG(lists)
    _DEBUG("help",old_actions)
    _PRINT("DEBUGGING",init)
    print "helplists",lists
    if direction == "forward":
        return post.fixsolutionnew(plan_list,lists,init,old_actions, G.TYPING)
    return post.fixsolutionnew_backward(plan_list,lists,init,old_actions, G.TYPING, goals,new_actions)

def writeout_solution(solution):
    '''
    Write the solution/sas plan out to a new file
    '''
    print "solution",solution
    solutionstring = ancillary.tostring(solution)
    solution_file = open("sas_plan_new", "w")
    solution_file.write(solutionstring[1:-1])
    solution_file.close()

    #!l = range(0,len(plan_list))
    #!for i in l:
    #!          move = planlist[i]
    #!          if len(move) == 6:
    #!              k = range(0,len(lists)-1)
    #!              for j in k:
    #!                  myvars = list[i]
    #!                  return replace(move,myvars)
    #!          else:
    #!              return move
    #run validator

    #add typing for ipc11
    

