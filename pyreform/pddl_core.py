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

import copy
import shlex
import re
import sys
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


def test_reformulate(objects, actions, goals, prob2):
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
                                    if debug == True:
                                        _PRINT("i",i)
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
                                _DEBUG("test6",myset)
                                new_prob = prob2
                                FOUND = True
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

    return (REFORMULATE, myset, FOUND)    


def output_prob_file(prob_list2_real,new_objects,new_init,new_goals,prob_list2_temp):
    '''
    Write the reformulated problem file out to a new file
    '''
    
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


def reformulate(myset, domain2, requirements, predicates, types, actions, domain_list1_real, domain_list1_temp, prob2, objects1, goals, init, prob_list2_real, prob_list2_temp, ontology, typing, objects, SOKOBAN):
    '''
    Perform a reformulation of the input domain and problem files
    '''

    #global TYPING
    
    _DEBUG("sassy")
    if SOKOBAN == False:                                                                                  #! not in painful sokoban case
#        if debug == True:
        _DEBUG("how", len(myset))
        _DEBUG("myset",myset)
        lists = reform.returnsetsnew(myset,[],[])                                                                #! merge the pairs into a list of arbitrary lists
        #_PRINT("lists",lists)
        _DEBUG("ddddddlists",lists)
        if not isinstance(lists[0],list):          #!should not need this anymore!!!
            temp = [lists] #!temporary fix!!!!
            lists = temp   #!temporary fix!!!!  cheat for only one set of variables must fix when fix for 2 sets
#        if debug == True:
        _DEBUG("lists2", lists)
        _DEBUG("sylvlists", lists)  #!need to retest for actions....some groups not compatable...before changeobjects
        original_objects = copy.deepcopy(objects)
        #_PRINT("original_objects",original_objects)
        new_objects = reform.changeobjects(lists,objects)                                                       #! this returns the new object list for the new prob file
        #_PRINT("new_objects",new_objects)
        #_PRINT("original_objects2",original_objects)
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
        if extra_list <> []:
            if isinstance(extra_list[0],list):
                lists.extend(extra_list)
            else:
                lists.append(extra_list)
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
        new_init = reform.changeinit(lists,init,counter_type,old_vals)                                         #! this changes the init state to the new init state
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
            new_init = reform.addinit(lists,counter_type,lists,new_init,[],max_num)                                        #!adds in new predicates for new init state "the zero counts" and the "mores"
            #_PRINT("bugger",new_init)
            temp_objects = new_objects[1:]
            temp2_objects = new_objects[0]
            temp_objects = reform.addobjects(temp_objects,max_num)
            temp_objects.insert(0,temp2_objects)
            new_objects = temp_objects
            #_PRINT("debugnewobjects",new_objects)
        else:
            _DEBUG("testlists2",lists)
            max_num = reform.findmax(lists)
            _DEBUG("testlists",lists)
            new_init = pddl_typing.addinit_typing(lists,counter_type,new_init,[],original_objects,typing,max_num)
            #_PRINT("bugger2",new_init)
            new_objects = reform.addobjects(new_objects,max_num)
        _DEBUG("countertypeeee",counter_type)
        _DEBUG("bbbbbnewinit",new_init)
                                                              #!adds in new objects like numbers
        if G.TYPING == True:
            _PRINT("new_objects",new_objects)
            new_objects = reform.addbacktypes(new_objects,original_objects,typing)
            new_objects.insert(0,objects1[0])
        #_PRINT("ddddnewobjects",new_objects,objects1[0])
        _DEBUG("new_init",new_init)
        _DEBUG("listb",lists)
        counter_type2 = []
        old_vals2 = []
        #_PRINT("lists",lists)
        G.new_goals = reform.changegoal(lists,goals,counter_type2,old_vals2)                                    #!removes the goal description for new objects
        if G.TYPING == True:
            G.typeof = reform.maketype(lists,original_objects,typing)
            #_PRINT("typeoftyping",G.typeof)
        #_PRINT("counter_type2",counter_type2,"new_goals",G.new_goals)
        new_counter_type2 = pddl_typing.fix_counter_type(counter_type2)                                             #! this changes [rooma romma merge romma romma] to [[rooma rooma][rooma rooma]]
        new_counter_type2 = reform.remove_empty(new_counter_type2)
        #_PRINT("brr2",new_counter_type2)
        if len(new_counter_type2) == 1:
            counter_type                  #!what does this do????
        counter_type2 = new_counter_type2
        if G.TYPING == True:
            myextralist = reform.return_places(G.typeof,lists,new_counter_type2,original_objects,typing,predicates,objects1)
#            if debug == True:
            _DEBUG("myextralist",myextralist)
            new_init.extend(myextralist)
            _DEBUG("new_init",new_init)
        _DEBUG("newgoals",G.new_goals)
        _DEBUG("new_goals",G.new_goals)
        _DEBUG("new_goals1",G.new_goals)
        _DEBUG("listc",lists)
        _PRINT("counter_typehoho",counter_type2)
        if not isinstance(counter_type2,list):  #probably never is true
            counter_type2 = list(set(counter_type2))
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
        G.new_goals = reform.addgoals(lists,counter_type2,lists,G.new_goals)                                           #!add the goal description for new objects
        output_prob_file(prob_list2_real,new_objects,new_init,G.new_goals,prob_list2_temp)
        #_PRINT("counter_type2",counter_type2)
        #_PRINT("newgoals2",G.new_goals)
        _DEBUG("new_goals",G.new_goals)
        _DEBUG("new_goals",G.new_goals)
        _DEBUG("flinstones",lists,actions)
        num = [0]
        new_actions = reform.changeactions(lists,actions,num)                                                          #!change the actions
        _PRINT("debugstorage",G.storage)
        _PRINT("debugstorage2",G.storage2)
        #_PRINT("debugstorage3",G.storage3)
        #_PRINT("reallyreally", new_actions)
        _DEBUG("scooby",new_actions)
        if G.HASREQUIREMENTS:
            new_domain_list = domain_list1_real[0:2]
        new_domain_list = domain_list1_real[0:1]
        _PRINT("new_domain_list", new_domain_list)
        if G.TYPING == True:
            new_types = reform.addnum(types)
            new_domain_list.append(new_types)
        #! new_domain = reform.changepredicates(lists, domain2)  not sure I need this
        newpredicates = reform.changepredicates(predicates)  #changed Oct 22
        #_PRINT("brandnew", newpredicates)
        new_domain_list.append(newpredicates)
        if G.HAVEFUNCTIONS:
            #_PRINT("waaahooo")
            new_domain_list.append(G.functions)
        _DEBUG("josie",new_domain_list)
        new_domain_list.extend(new_actions)
        _DEBUG("new_domain_list",new_domain_list)
        new_domain_listend=[domain_list1_temp[0]]
        new_domain_listend.extend(new_domain_list)
        #_PRINT("new_domain_list",new_domain_list)
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

    return (lists)

def postprocess_plan(plan, lists, init, old_actions):
    '''
    After running the reformulated input files through the planner
    post process the output sas plan file and save
    '''
    
    newplan = "(" + plan + ")"
    _DEBUG(newplan)
    tmp_plan_list = nestedExpr('(',')').parseString(newplan).asList()
    plan_list = tmp_plan_list[0]
    #_PRINT("plan_list",plan_list)
    _DEBUG(plan_list)

    _DEBUG(lists)
    _DEBUG("help",old_actions)
    _PRINT("DEBUGGING",init)
    solution = post.fixsolutionnew(plan_list,lists,init,old_actions, G.TYPING)

    return solution

def writeout_solution(solution):
    '''
    Write the solution/sas plan out to a new file
    '''

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
    

