'''
PDDL Merge and Translator - Post Processing Module

Author: Dr. Patricia Riddle @ 2013

Translates PDDL files using an automated planner in order to improve performance

This module contain functions used in the post processing of the planner output file after reformulation
'''

import pddl_typing
from pddl_debug import _DEBUG, _D
from pddl_debug import _PRINT, _P
import pddl_ancillary as ancillary
import pddl_globals as G

#PP
def checkmove(move):
    _DEBUG("G.storage2",G.storage2,"move",move)
    l = range(0,len(G.storage2))
    for i in l:
        if move[0].lower() == G.storage2[i].lower():
            _DEBUG("yeaa",move[0],G.storage2[i])
            return True
    return False




#PP
def testmove(newmove,state,actions, TYPING):                           #!checks to see if move can be applied, returns new state
#    if debug == True:
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
            precond1 = i[5]
            precond2 = precond1[1:]
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
                    for j in realstate:
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
    _DEBUG("seven")
    _DEBUG("term",term)
    _DEBUG("move",move)
    _DEBUG("param",param)
#    print "matches", matches
    newterm=[]
    for i in term:
#        if debug == True:
        _DEBUG("i",i)
        if i[0] == "?":
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
#                if debug == True:
                _DEBUG("i",i,"param[j]",param[j])
                if i == param[j]:
                    newterm.insert(len(newterm),move[j+1])
                    _DEBUG("pazazz",newterm)
#                    return newterm
        else:
            newterm.insert(len(newterm),i)
            _DEBUG("newterm",newterm)
    return newterm

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
        for i in lists:
            _DEBUG("i",i)
            _DEBUG("lists",lists)
            for j in i:
                _DEBUG("debug",j,"i",i)
                _DEBUG("here2")
                _DEBUG("j",j)
                _DEBUG("i",i)
                _DEBUG("debugmove",move)
                new_move = repairmove(move,j,i)
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
    new_move = [move[0]]
#    new_move.insert(1,i)
    _DEBUG("new_move",new_move)
    _DEBUG("G.storage3",G.storage3)
    new_move = findparam(new_move,move)
    _DEBUG("new_move",new_move)
    _DEBUG("i",i,"lists",lists)
    new_move = replaceinmove(new_move,i,lists)
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
