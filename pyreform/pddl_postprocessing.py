'''
PDDL Merge and Translator - Post Processing Module

Author: Dr. Patricia Riddle @ 2013
Contact: pat@cs.auckland.ac.nz

Translates PDDL files using an automated planner in order to improve performance

This module contain functions used in the post processing of the planner output file after reformulation

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

import pddl_typing
from pddl_debug import _DEBUG, _D
from pddl_debug import _PRINT, _P
import pddl_ancillary as ancillary
import pddl_globals as G
import pddl_reformulation as reform
import pddl_core as core

#PP
def checkmove(move):
    _DEBUG("G.storage2",G.storage2,"move",move)
    print "movename",move
    print "G.storage2",G.storage2
    l = range(0,len(G.storage2))
    for i in l:
        if move[0].lower() == G.storage2[i].lower() or move[0][0:-2].lower() == G.storage2[i].lower():
            _DEBUG("yeaa",move[0],G.storage2[i])
            return True
    return False




#PP
def testmove(newmove,state,actions, TYPING):                           #!checks to see if move can be applied, returns new state
#    if debug == True:
    print "statestate",state
    print "newmove",newmove
    _DEBUG("newmove",newmove,"state",state,"actions",actions)
    _DEBUG("newmove",newmove)
    _DEBUG("state", state)
    realstate = state[1:]
    _DEBUG("actions",actions)
    matches = []
    for i in actions:
        _DEBUG("debugging")
        _DEBUG("action",i)
        _DEBUG("i",i)
        param = i[3]
        if TYPING == True:
            param = ancillary.fixparam(param, TYPING)
#        if debug == True:
        _DEBUG("param",i[3])
        _DEBUG("newmove[0]",newmove[0],"i[1]",i[1])
        if newmove[0].lower() == i[1].lower():
            print "i[5]",i[5]
            precond1 = i[5]
            if precond1[0] == "and": #3/20/2014
                precond2 = precond1[1:]
            else:
                precond2 = [precond1]
            print "precond2",precond2
            _DEBUG("debugi",i,"precond1",precond1,"precond2",precond2)
            _DEBUG("precond2",precond2)
#!            for k in precond2:                #!make matches list
#!                match1 = False
#!                for j in realstate:
#!                    print "matches",matches
#!                    print "i",i
#!                    print "j",j
#!                    print "k",k
#!                    if k == "and":
#!                        match1=True
#!                    if k[0] == j[0] or k == "and":
#!                        if len(k) == 2:
#!                            matches.insert(0,[j[1],k[1]])
#!                        if len(k) == 3:
#!                            matches.insert(0,[j[1],k[1]])
#!                            matches.insert(0,[j[2],k[2]])
#!                        match1=True
#!                print "precon",k
#!                print "match1",match1
#!                if match1 <> True:
#!                    return False
#!            newmatches = remove_duplicates(matches)    #!remove duplicates in matches list
            for k in precond2:                #!check instantiated preconditions
                print "kkk",k
                _DEBUG("debugk",k,"precond2",precond2)
                match1 = False
                if k == "and":
                    match1=True
                else:
#                    if debug == True:
                    _DEBUG("instantiate",k,"newmove",newmove,"param",param)
                    newk = instantiate(k,newmove,param)
#                    if debug == True:
                    _DEBUG("newk",newk)
                    _DEBUG("realstate",realstate)
                    print "k",k
                    for j in realstate:
                        print "j",j,"newk",newk
                        _DEBUG("realstate",realstate)
                        _DEBUG("matches",matches)
                        _DEBUG("i",i)
                        _DEBUG("j",j)
                        _DEBUG("k",k)
                        _DEBUG("newked",newk)
                        _DEBUG("j",j)
                        if newk == j or k == "and":
                            match1=True
                        _DEBUG("preconkkk",k)
                        _DEBUG("match1",match1)
                    print "match1",match1
                    if match1 <> True:
                        return False
            _DEBUG("here?") #,newmatches
            _DEBUG("newmove",newmove)
            _DEBUG("state",state)
            effect1 = i[7]
            _DEBUG("effect1",effect1)
#            effect1 = effect1[1]
#            print "effect2",effect2
            effect = effect1[1:]
            _DEBUG("effect3",effect)
            for temp in effect:
                print "temp",temp
                _DEBUG("debugtemp",temp,"effect",effect)
                _DEBUG("effect",temp)
#                temp = m[0]
                _DEBUG("temp[0]",temp[0])
                if temp[0] <> "not":
                    _DEBUG("again")
                    _DEBUG("temp",temp)
                    newtemp = instantiate(temp,newmove,param)
                    _DEBUG("newtemp",newtemp)
                    state.insert(1,newtemp)
                    _DEBUG("newstate1",state)
                else:
                    _DEBUG("hoowa",temp[1])
                    _DEBUG("newmove",newmove)
#!                    print "newmatches",newmatches
                    newtemp = instantiate(temp[1],newmove,param)
                    for n in state:
                        _DEBUG("temp1",temp[1])
                        _DEBUG("newtemp2",newtemp)
                        _DEBUG("state",state)
                        _DEBUG("newtemp",newtemp)
                        _DEBUG("n",n)
                        if newtemp == n:
                            _DEBUG("wahoo",newtemp)
                            state.remove(n)
                        _DEBUG("newstate2",state)
            _DEBUG("newstate",state)
            return state


#PP
def instantiate(term,move,param):                                            #! two problems (road ?l ?l) returns (road city..) and needs to backtrack...need to move test inside of instantiate!!!!!
#! not sure this only uses elements in the same list "[ball1 balls]" should check this ...will make it faster
#    if debug == True:
    print "ttterm1",term
    print "move",move
    print "param",param
    _DEBUG("seven")
    _DEBUG("term",term)
    _DEBUG("move",move)
    _DEBUG("param",param)
#    print "matches", matches
    newterm=[]
    for i in term:
        print "iii",i
#        if debug == True:
        _DEBUG("i",i)
        if len(str(i)) > 1 and i[0] == "?":
 #!           for j in matches:     #!change this part to use param
 #!               print "j",j
 #!               print "j1",j[1]
 #!               print "i0",i[0]
 #!               if j[1] == i:
 #!                   print "almost", j
 #!                   print "move",move
 #!                   if j[0] in move:
 #!                       print "gothere",j
 #!                       newterm.insert(len(newterm),j[0])
            l = range(0,(len(param)))        #-1 or not???
#            if debug == True:
            _DEBUG("l", l)
            for j in l:
                print "jjj",j,param[j]
#                if debug == True:
                _DEBUG("i",i,"param[j]",param[j])
                if i == param[j]:
                    newterm.insert(len(newterm),move[j+1])
                    _DEBUG("pazazz",newterm)
#                    return newterm
        else:
            newterm.insert(len(newterm),i)
            _DEBUG("newterm",newterm)
    print "ttterm2",newterm
    return newterm


def testmove_backward(newmove,state,actions, TYPING):                           #!checks to see if move can be applied, returns new state
    print "newmove99",newmove
    print "actions",actions
#    alternate_name = newmove[0]
#    alternate_name = alternate_name[:-2]  #will not work for grasp_shaker
    for i in actions:
        print "i",i
        param = i[3]
        if TYPING == True:
            print "old_param",param
            new_param = ancillary.fixparam(param, TYPING)
            print "newparam",new_param
        print "newmove[0]",newmove[0]
        print "i[1]",i[1]
        if newmove[0].lower() == i[1].lower(): #or alternate_name.lower() == i[1].lower():
            print "i2",i
            effects1 = i[7]
            print "effects1",effects1
            effects2 = effects1[1:]
            print "effects2",effects2
            new_state = state
            
#            repairmove(newmove, ,
            for j in effects2:
                print "effectjjj",j
                new_state = test_effect(newmove,j,new_state,newmove[1:],new_param)
                if new_state == False:
#                    dummy3()
                    return new_state
            preconditions1 = i[5]
            print "preconditions111",preconditions1
            preconditions2 = preconditions1[1:]
            for k in preconditions2:
                print "kkk",k
                new_state = test_precond(newmove,k,new_state,newmove[1:],new_param)  
                if new_state == False:
                    dummy4()
                    return new_state
            return new_state

def remove_from_state(neweffect,state): ####seriously broken 3/12/2014
    print "state777",state
    print "neweffect",neweffect
    newstate = []
    for i in state:
        if i != neweffect:
            newstate += [i]
    print "newstate777",newstate
    return newstate

def test_precond(newmove,precond,state,param,op_param):  
    if precond[0] == "not":
        temp = precond[1]
        newprecond = instantiate(temp,newmove,op_param)   
        if newprecond in state:
            dummy6()
            newstate = False
        elif not_is_in_state(newprecond,state):
            newstate = state
        else:
            newstate = state
            newstate += [["not",newprecond]]
    else:
        newprecond = instantiate(precond,newmove,op_param)
        if newprecond in state:
            newstate = state
        elif not_is_in_state(newprecond,state):
            dummy7()
            newstate = False
        else:
            newstate = state
            newstate += [newprecond]
    return newstate

def test_effect(newmove,effect,state,param,op_param):
    print "effect",effect
    print "state",state
    print "param",param
    print "op_param",op_param
    if effect[0] == "not":
        temp = effect[1]
        neweffect = instantiate(temp,newmove,op_param) 
        print "neweffect",neweffect
        if neweffect in state:
            newstate = False
        elif not_is_in_state(neweffect,state):
            print "state22",state
            newstate = remove_from_state(neweffect,state)
            print "newstate33",newstate
        else:
            newstate = state
#        l = range(0,len(state))
#        for i in l:
#            temp2 = state[i]
#            if temp[0] == temp2[0]:
#                dummy2(0)
        
    else:
        neweffect = instantiate(effect,newmove,op_param)
        print "neweffect",neweffect
        if neweffect in state:
            print "one"
            newstate = remove_from_state(neweffect,state)
        elif not_is_in_state(neweffect,state):
            print "two"
            newstate = False
        else:
            print "three"
            newstate = state
    return newstate

def not_is_in_state(effect,state):
    neweffect = ["not", effect]
    if neweffect in state:
        return True
    return False

#def fixsolutionnew_backward(plan_list,lists,init,actions, TYPING, goals,new_actions):
#    temp = goals[1]
#    temp2 = temp[1:]
#    print "temp2",temp2
#    return fixsolutionnew_backward1(plan_list,lists,init,[],actions, TYPING,temp2,new_actions)

def fixsolutionnew_backward(plan_list,lists,init,actions, TYPING, goals,new_actions):
    temp = goals[1]
    temp2 = temp[1:]
#    print "temp2",temp2
    G.new_actions = new_actions
#    for i in lists:
#     G.locations_in_list.insert(0,0)
#     G.locations_max = G.locations_max + [len(i)]
#    print "G.locations_in_list",G.locations_in_list
#    print "G.locations_max",G.locations_max
    newplan = fixsolutionnew(plan_list,lists,init,actions, TYPING)
#    return fixsolutionnew_backward1(plan_list,lists,init,[],actions, TYPING,temp2,new_actions)
    print "newplan",newplan
    if check_goals(goals,G.final_state):
        return newplan
    else:
        return replace_goals(goals[1][1:],G.final_state,newplan,lists)
    ##add part here to fix variables against goals 20/3/2014
    dummy88()

def replace_goals(goals,final_state,newplan,lists):
    match = []
    for i in goals:
        print "i",i
        for j in final_state:
            nomatch = False   
            print "j",j
            if i[0] == j[0]:
                l = range(1,len(i))
                for h in l:
                    for list1 in lists:
#                        if i[h] <> j[h] and i[h] in list1 and j[h] in list1:
                        if i[h] in list1 and j[h] in list1:
                            z = range(h+1,len(i))
                            for w in z:
                                if i[w] <> j[w]:
                                    nomatch = True
                            print "goal",i
                            print "state",j
                            if nomatch == False:
                                match.append([i[h],j[h]])
    print "matchlist",match
    match1,match2 = extend_match(match,lists)
    return replace_in_plan(newplan,match1,match2)

def extend_match(match,lists):
    print "oldmatch",match
    num = 0
    match1 = []
    match2 = []
    new_list = []
    old_list = []
    for list1 in lists:
        if match[0][0] in list1:
            correctlist = list1
    for i in match:
        if i[0] <> i[1]:
            match1.append([i[1],"v"+str(num)])
            match2.append([i[0],"v"+str(num)])
            num = num + 1
        new_list.insert(0,i[0])
        old_list.insert(0,i[1])
    print "new_list",new_list
    print "old_list",old_list
    for i in new_list:
        if i not in old_list:
            for j in correctlist:
                if j not in new_list:
                    match1.append([i,"v"+str(num)])
                    match2.append([j,"v"+str(num)])
                    num = num+1
    print "match1",match1
    print "match2",match2
    return (match1,match2)
                    

def replace_in_plan(plan,match1,match2):
    print "oldplan",plan
    for i in plan:
        print "planstep",i
        Found = False
        for j in match1:
            print "matchstep",j
            l = range(1,len(i)) 
            for z in l:
                if i[z] == j[0] and Found == False:
                    print "match",i[z]
                    i[z] = j[1]
                    Found = True
        Found = False
        for j in match2:
            print "matchstep",j
            l = range(1,len(i)) 
            for z in l:
                if i[z] == j[1] and Found == False:
                    print "match",i[z]
                    i[z] = j[0]
                    Found = True
    print "newplan",plan
    return plan


def check_goals(goals,final_state):
    print "goals",goals
    print "final_state",final_state
    print "goals2",goals[1][1:]
    for i in goals[1][1:]:
        if i not in final_state:
            return False
    return True
                    

def fixsolutionnew_backward1(plan_list,lists,init,new_plan, actions, TYPING, goals,new_actions):
    print "actions",actions
    print "new_actions",new_actions
    print "plan_list",plan_list
    if plan_list == []:
        return []
    else:
        move = plan_list[-1]
        print "move",move
#        print "G.storage2",G.storage2
#        if checkmove(move) or checkmove(move[:-2]):
#            print "helper"
#            x=2
#        else:
        state = goals
        print "state",state
        for i in lists:
            for j in i:
                print "move1",move
                print "j",j
                print "i",i
                newmove = repairmove_complex(move,j,i,actions,new_actions)
#need to make a new repairmove (using the old move and the new move)
                print "newmove88",newmove
                print "state",state
                newstate = testmove_backward(newmove,state,actions, TYPING)            #changed to new_actions 3/11
                print "newstate2",newstate  ###gets this far...in pour_shaker_to_shot2b ....must add preconditions to testmove_backward  3/12/2014
                if newstate <> False:
                    new_plan.append(newmove)
                    temp2 = fixsolutionnew_backward1(plan_list[0:-1],lists,init,new_plan,actions, TYPING, newstate,new_actions) 
                else:
                    temp2 = False
                print "i",i
                print "j",j
                print "newstate444",newstate
                print "temp2",temp2
                print "G.recurse",G.recurse
                if G.recurse <> 0:
                    new_plan = new_plan[0:-(len(plan_list)-1)]
                    G.recurse = 0
                print "new_plan",new_plan
                print "plan_list",plan_list
                print "plan_list[0:-1]",plan_list[0:-1]
                print "temp2",temp2
                if temp2 <> False:
                    temp2.insert(0,newmove)
                    return temp2
#                else: 
#                    print "new_plan1",new_plan
#                    new_plan = new_plan[0:-1]
#                    print "new_plan2",new_plan
        new_plan = new_plan[0:-1]
        G.recurse = G.recurse + 1
        return False
    _PRINT("really??")




def shorten(name):
    l = range(0,len(name))
    for i in l:
        if name[i] == ":":
            return name[0:i]
    return name
        

def repairmove_complex1(move,myobject_lists,actions,new_actions): #switched myobject and lists 17/3/2014
    print "move",move
    name = move[0]
    print "name",name
    oldname = []
    if ":" in name:
        oldname = shorten(name)
    print "name22",name
    for i in new_actions:
        print "i",i
        if name == i[1]:
            myaction = i
    print "myaction",myaction
    temp = myaction[3]
    new_param = ancillary.fixparam(temp, True)  
    print "new_param",new_param
    print "mistake"
    for  i in actions:
        print "ieyei",i,"i[1]",i[1],"name[-2]",name[-2],"name",name
        if (((name[-2] == "1" or name[-2] == "2") and name[0:(len(name)-2)] == i[1]) or (name[-2] != "1" and name[-2] != "2" and name == i[1]) or (oldname != [] and i[1] == oldname)):
            myoldaction = i
    print "myoldaction",myoldaction
    temp = myoldaction[3]
    old_param = ancillary.fixparam(temp, True)  
    print "old_param",old_param
    newmove = [myoldaction[1]]
    for i in old_param:
        l = range(0,len(new_param))
        for j in l:
            if i == new_param[j]:
                newmove.extend([move[j+1]])
    l = range(1,(len(newmove))) 
    for i in l:
        for j in myobject_lists:
            type1 = core.find_type_of(newmove[i],G.pats_favorite)  
            type2 = core.find_type_of(j[-1],G.pats_favorite)
            if type1 == type2:
                print "test",type1,type2,newmove[i]
                G.locations_in_list.insert(0,0)
                G.which.insert(0,[i,j])
                print "G.locations", G.locations_in_list
                print "G.which",G.which
#     G.locations_max = G.locations_max + [len(i)]
    print "G.locations_in_list",G.locations_in_list
    print "G.which",G.which
    for i in G.which:
        G.locations_max = G.locations_max + [len(i[1])]
#    dummy()
    return [newmove,temp]
#    for i in old_param:
#        for j in lists:        
#     G.locations_in_list.insert(0,0)
#     G.locations_max = G.locations_max + [len(i)]
#    print "G.locations_in_list",G.locations_in_list
#    print "G.locations_max",G.locations_max

def repairmove_complex2(newmove,myobject_lists,temp): #switched myobject and lists 17/3/2014
     print "newnewmove",newmove
     newnewmove = replaceinmove2(newmove,temp,myobject_lists)
     print "newnewnewmove",newnewmove
     return newnewmove

#PP
def fixsolutionnew(plan_list,lists,init,actions, TYPING):                           #!attempts to find solution to old representation
#    print "init",init
    _DEBUG("fix",plan_list)
    #global recurse
    _DEBUG("plan_list",plan_list)
    _DEBUG("lists",lists)
    G.recurse = 0
    plan = fixsolutionnew1(plan_list,lists,init,[],actions, TYPING)
    _DEBUG("plan",plan)
    _DEBUG("planzzz",plan)
    return plan

#PP
def fixsolutionnew1(plan_list,lists,state,new_plan,actions, TYPING):               #!attempts to find solution to old representation - using new_plan for backtracking
    print "fix1",lists
    _PRINT("debugstate",state)
    _DEBUG("fix1",plan_list)
    #global recurse
    _DEBUG("new_plan",new_plan)
    _DEBUG("plan_list",plan_list)
    if plan_list == []:
#!        suceed = planner.runvalidation(new_plan)
#!        if debug == True:
#!            print "suceed",suceed
#!        if suceed <> False:
        _DEBUG("new_plan1111",new_plan)
#        return new_plan                 this was the bug
        return []
#!        else:
#!            return False
    move = plan_list[0]
    _DEBUG("move",move)
#    if len(move) == 6:
    _DEBUG("checkmove",move,checkmove(move))
    if checkmove(move):
        _DEBUG("checkmove",move)
        _DEBUG("here1")
        if notsametype(lists):
            return double_loop(plan_list,lists,state,new_plan,actions, TYPING)
        for i in lists: ### this this works if two sets of balls not a set of balls and a set of trucks
            _DEBUG("i",i)
            _DEBUG("lists",lists)
            for j in i:
                _DEBUG("debug",j,"i",i)
                _DEBUG("here2")
                _DEBUG("j",j)
                _DEBUG("i",i)
                _DEBUG("debugmove",move)
                if G.unary_big == []:
                    new_move = repairmove(move,j,i)
                else:
                    new_actions = G.new_actions
                    new_move = repairmove_complex(move,j,i,actions,new_actions) 
                _DEBUG("debugnewmove",new_move)
#                if debug == True:
                _DEBUG("newmovezzz",new_move)
                newstate = testmove(new_move,state,actions, TYPING) #must write this
#                if debug == True:
                _DEBUG("newstate",newstate)
                _DEBUG("newstatezzz",newstate)
                _DEBUG("new_move",new_move)
                _DEBUG("newmove",new_move)
                if newstate <> False:
                    new_plan.append(new_move)
                    _DEBUG("newplan1",new_plan)
                    temp = fixsolutionnew1(plan_list[1:],lists,newstate,new_plan,actions, TYPING)
                    _DEBUG("newplan9",new_plan)
                else:
                    _DEBUG("scary")
                    temp = False
                if G.recurse <> 0:
#                    if debug == True:
                    _DEBUG("recurseb")
                    new_plan = new_plan[0:-(len(plan_list)-1)] #changed from -recurse
                    _DEBUG("newplan2",new_plan) # never happens
                    G.recurse = 0
                    _DEBUG("tempa",temp)
                if temp <> False:
                    _DEBUG("here3")
                    temp.insert(0,new_move)
                    _DEBUG("temp",temp)
                    return temp
                else:
                    _DEBUG("before",new_plan)
                    new_plan = new_plan[0:-1]
                    _DEBUG("newplan3",new_plan)
                    _DEBUG("ohnoc",new_plan)
#                    return False
        new_plan = new_plan[0:-1] #not sure this does anything
        _DEBUG("newplan4",new_plan) #never happens
        _DEBUG("ohnoa",new_plan)
        G.recurse = G.recurse + 1
        _DEBUG("recurse", G.recurse)
        return False
#    if len(move) < 6:
    else:
        _DEBUG("here4")
        _DEBUG("here4")
        _DEBUG("move",move)
        _DEBUG("state",state)
        print "state88",state
        newstate = testmove(move,state,actions, TYPING)
#        if debug == True:
        _DEBUG("newstatevvv",newstate)
        if newstate == False:
            _PRINT("recurse2")
            new_plan = new_plan[0:-1]
            _PRINT("newplan5",new_plan) #never happens
            G.recurse = G.recurse + 1
        new_plan.append(move)
        _DEBUG("newplan6",new_plan)
        temp2 = fixsolutionnew1(plan_list[1:],lists,newstate,new_plan,actions, TYPING)
        _DEBUG("new_plan8",new_plan)
        _DEBUG("temp2",temp2)
        if temp2 <> False:
            _DEBUG("here5")
            temp2.insert(0,move)
            _DEBUG("temp2",temp2)
            return temp2
        else:
            new_plan = new_plan[0:-1]
            _DEBUG("newplan7",new_plan) #never happens
            _DEBUG("ohnob",new_plan)
            G.recurse = G.recurse + 2
            _DEBUG("recursec",G.recurse)
            return False
    _PRINT("really??")

def notsametype(lists):
     l = range(1,(len(lists)))
     for i in l:
         temp1 = lists[i-1][-1]
         temp2 = lists[i][-1]
         type1 = core.find_type_of(temp1,G.pats_favorite)
         type2 = core.find_type_of(temp2,G.pats_favorite)
         if reform.checktypeof(type1,type2,G.ontology) == False:
             print "falsefalse",type1,type2,temp1,temp2
             print "save_objects",G.save_objects
             print "G.pats_favourite",G.pats_favorite
             if type1 == type2:
                 return False
             return True
     return False
        

def choose_one_from_each(lists):
    print "lists",lists
    temp = []
    l = range(0,(len(lists)))
    print "G.locations_in_list",G.locations_in_list
    for i in l:
        temp.insert(0,[lists[i][-1],lists[i][G.locations_in_list[i]]])
        G.locations_in_list[i] = G.locations_in_list[i]
    print "GGG.locations",G.locations_in_list
    print "GGG.max",G.locations_max
    increment1()
    print "GGGG.locations",G.locations_in_list 
    print "tempnew",temp
    print "locations_in_list",G.locations_in_list
    return temp

def increment1():
    print "fred",G.locations_in_list,G.locations_max
    l = range(0,(len(G.locations_in_list))) 
    print "l",l
    for i in reversed(l):  #once it makes the second go to the end "1" it does not go through all the number in the last one again goes from 010 to 100 instead of 011
        if G.locations_in_list[i] == G.locations_max[i]-1 and i < len(G.locations_in_list)-1 and G.locations_in_list[i+1] < G.locations_max[i+1]-1: 
            print "pp1"
            G.locations_in_list[-1] = G.locations_in_list[-1] + 1 
            return
        if G.locations_in_list[i] == G.locations_max[i]-1 and G.locations_in_list[i-1] < G.locations_max[i-1]-1:
            z = range(i,(len(G.locations_in_list)))
            for v in z:
                G.locations_in_list[v] = 0 #add a loop that goes through i+1 and makes 0
            G.locations_in_list[i-1] = G.locations_in_list[i-1] + 1
            print "here99"
            print "pp2"
            return
    print "here2"
    print "pp3"
    G.locations_in_list[-1] = G.locations_in_list[-1] + 1
    print "G.locations_in_list",G.locations_in_list
    
#write choose_one_from_each
#fix repairmove_complex
#write same_type

def reset_locations_in_list():
    l = range(0,(len(G.locations_in_list)))
    for i in l:
        G.locations_in_list[i] = 0

def double_loop(plan_list,lists,state,new_plan,actions, TYPING):
    print "double loop warning"
    if plan_list == []:
        G.final_state = state
        return []
    else:
        move = plan_list[0]  #need to fix this to allow multiple ones from each list depending on param list
        newstate = False
        G.which = []
        G.locations_in_list = []
        G.locations_max = []
        print "movemove",move
        new_actions = G.new_actions
        new_move, temp = repairmove_complex1(move,lists,actions,new_actions)   
        while (newstate == False):
#        new_params = choose_one_from_each(lists)
#        print "new_params",new_params

            if G.unary_big == []:
                new_move = repairmove(move,j,i) ###need to fix this
            else:
                new_move = repairmove_complex2(new_move,lists,temp) 
            newstate = testmove(new_move,state,actions, TYPING) #must write this
        new_plan.append(new_move)
        reset_locations_in_list()
        temp = double_loop(plan_list[1:],lists,newstate,new_plan,actions, TYPING)
        if G.recurse <> 0:
            new_plan = new_plan[0:-(len(plan_list)-1)] #changed from -recurse
            G.recurse = 0
        if temp <> False:
            temp.insert(0,new_move)
            return temp
        else:
            new_plan = new_plan[0:-1]
    

'''        for i in lists: ### this this works if two sets of balls not a set of balls and a set of trucks
            for j in i:
                if G.unary_big == []:
                    new_move = repairmove(move,j,i)
                else:
                    new_actions = G.new_actions
                    new_move = repairmove_complex(move,j,i,actions,new_actions) 
                newstate = testmove(new_move,state,actions, TYPING) #must write this
                if newstate <> False:
                    new_plan.append(new_move)
                    temp = fixsolutionnew1(plan_list[1:],lists,newstate,new_plan,actions, TYPING)
                else:
                    temp = False
                if G.recurse <> 0:
                    new_plan = new_plan[0:-(len(plan_list)-1)] #changed from -recurse
                    G.recurse = 0
                if temp <> False:
                    temp.insert(0,new_move)
                    return temp
                else:
                    new_plan = new_plan[0:-1]
'''

#O
def fixsolution(plan_list,lists):                                       #! old code that is not currently used (see new version above) ... this tried all options and ran the validator....too solve
    #global recurse
    _DEBUG("plan_list",plan_list)
    _DEBUG("lists",lists)
    G.recurse = 0
    plan = fixsolution1(plan_list,lists,[])
    return plan

#O
def fixsolution1(plan_list,lists,new_plan):                              #! old code not currently used ........second fixsolution routine which includes new_plan where we build the plan so we can backtrack
    #global recurse
    _DEBUG("new_plan",new_plan)
    _DEBUG("plan_list",plan_list)
    if plan_list == []:
        suceed = planner.runvalidation(new_plan)
        _DEBUG("suceed",suceed)
        if suceed <> False:
            return new_plan
        else:
            return False
    move = plan_list[0]
    _DEBUG("move",move)
#    if len(move) == 6:
    if checkmove(move):
        _DEBUG("here1")
        for i in lists:
            _DEBUG("i",i)
            _DEBUG("lists",lists)
            for j in i:
                _DEBUG("here2")
                _DEBUG("j",j)
                _DEBUG("i",i)
                new_move = repairmove(move,j,i)
                _DEBUG("new_move",new_move)
                new_plan.append(new_move)
                temp = fixsolution1(plan_list[1:],lists,new_plan)
                if G.recurse <> 0:
                    _DEBUG("recurseb", G.recurse,len(plan_list),len(new_plan))
                    new_plan = new_plan[0:-(len(plan_list)-1)] #changed from -recurse
                    G.recurse = 0
                    _DEBUG("tempa",temp)
                if temp <> False:
                    _DEBUG("here3")
                    temp.insert(0,new_move)
                    _DEBUG("temp",temp)
                    return temp
                else:
                    _DEBUG("before",new_plan)
                    new_plan = new_plan[0:-1]
                    _DEBUG("ohnoc",new_plan)
#                    return False
        new_plan = new_plan[0:-1] #not sure this does anything
        _DEBUG("ohnoa",new_plan)
        G.recurse = G.recurse + 1
        _DEBUG("recurse", G.recurse)
        return False
    if len(move) < 6:
        _DEBUG("here4")
        new_plan.append(move)
        temp2 = fixsolution1(plan_list[1:],lists,new_plan)
        _DEBUG("temp2",temp2)
        if temp2 <> False:
            _DEBUG("here5")
            temp2.insert(0,move)
            _DEBUG("temp2",temp2)
            return temp2
        else:
            new_plan = new_plan[0:-1]
            _DEBUG("ohnob",new_plan)
            G.recurse = G.recurse + 2
            _DEBUG("recursec",G.recurse)
            return False
    _PRINT("really??")

#O PP
def repairmove(move,i,lists):                                          #! repairs the move call to the correct form for the original representation
    _DEBUG("debugmove1",move,"i",i)
    _DEBUG("move",move)
    _DEBUG("i",i)
    print "move",move
    print "i",i
    print "lists",lists
    new_move = [move[0]]
#    new_move.insert(1,i)
    _DEBUG("new_move",new_move)
    _DEBUG("G.storage3",G.storage3)
    new_move = findparam(new_move,move)
    print "new_move1",new_move
    _DEBUG("new_move",new_move)
    _DEBUG("i",i,"lists",lists)
    print "i",i,"lists",lists
    new_move = replaceinmove(new_move,i,lists)
    print "new_move2",new_move
#    new_move.extend(move[4:6])
    _DEBUG("new_move2",new_move)
    return new_move

#O PP
def replaceinmove(new_move,replace,lists):
    _DEBUG("new_move",new_move,"replace",replace,"lists",lists)
    l = range(0,len(new_move))
    for i in l:
        if new_move[i] == lists[len(lists)-1]:
            new_move[i] = replace
    return new_move

def return_type_list(temp):
    ans = []
    l = range(0,len(temp)) 
    for i in l:
        if temp[i] == "-":
            ans = ans + [temp[i+1]]
    print "ans",ans
    return ans

def replaceinmove2(new_move,params,replace_lists):
    _DEBUG("new_move",new_move,"replace_lists",replace_lists)
    types = return_type_list(params)
    print "types",types
    l = range(1,len(new_move))
    print "new_move",new_move
    print "l",l
    t = range(0,len(G.locations_in_list))
    for j in t:  #make G.which a pair which says which entry in newmove[1, [shot4..]]
        for i in l:
            print "here111",j,i,new_move[i],G.which[j][1][-1]
            type_newmove = core.find_type_of(new_move[i],G.pats_favorite)  
            print "type_newmove",type_newmove
#        for p in replace_lists:
#            print "p1",p[0]
            type_which = core.find_type_of(G.which[j][1][-1],G.pats_favorite) 
            print "type_p1",type_which
            print "i",i,G.which[j]
            print "new_move[i]",new_move[i]
            if i == G.which[j][0] and (new_move[i] == G.which[j][1][-1] or type_which == type_newmove or new_move[i] in G.which[j][1]):
#                temp_list - G.which[t]
                print "here222"
                print "new_move[i]",new_move[i]
                print "G.locations_in_list[j]",G.locations_in_list[j]
                print "G.which[j]",G.which[j]
                new_move[i] = G.which[j][1][G.locations_in_list[j]-1]
    print "new_move",new_move
    print "GG.locations_in_list",G.locations_in_list 
    increment1()
    print "GGGG.locations_in_list",G.locations_in_list
    return new_move

#O PP
def findparam(new_move,move):
    l = range(0,len(G.storage3))
    for i in l:
        _DEBUG("new_move[0]",new_move[0],"G.storage3[i]",G.storage3[i],len(move),len(G.storage3[i+1]),G.storage3)
        if isinstance(G.storage3[i],str) and new_move[0].lower() == G.storage3[i].lower():
            start = len(move)-len(G.storage3[i+1])
            end = start + len(G.storage3[i+1])
            _DEBUG("start",start)
            _DEBUG("end",end)
            new_move.extend(move[start:end])
            _DEBUG("new+movedebug",new_move)
            return new_move
