'''
PDDL Merge and Translator - Typing Module

Author: Dr. Patricia Riddle @ 2013

Functions used in handling typing during translation

'''
from pddl_debug import _DEBUG, _D
from pddl_debug import _PRINT, _P
import pddl_globals as G


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

def addinit_typing1(mylist,counter_type,new_init,more_list,original_objects,typing,max_num):
    #_PRINT("mylist",mylist)
    _DEBUG("testing")
#    new_count = len(counter_type)  #! + 1
#    print "new_vampire", new_count
#    new_list = ["count1a1a", mylist[-1], counter_type[0], new_count]
#    print "chocula",new_list
    countlist = makecounts(counter_type,mylist,[])
#    if debug == True:
    #_PRINT("countlist",countlist)
    new_init.extend(countlist)
    l = range(0,max_num)
    _DEBUG("set max")
#    max_num = len(counter_type)+2                             #why + 2 ????
    for i in l:
        if not i in more_list:
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
    _DEBUG("chocchocmylist",mylist,"counter_type",counter_type)
    temper = addzero_typing(mylist,counter_type,mylist[-1],new_init,original_objects,typing)
#    print "temper",temper
    _DEBUG("DDDDONE",temper)
    return temper
#else:
    _DEBUG("MUST EXTEND")

def addinit_typing(mylist,counter_type,new_init,more_list,original_objects,typing,max_num):
    #_PRINT("mylist1",mylist)
    _DEBUG("typinglists",mylist,"counter_type",counter_type)
    if mylist == []:
        return []
    elif len(mylist) == 1:
        _DEBUG("mylist",mylist)
        return addinit_typing1(mylist[0],counter_type[0],new_init,more_list,original_objects,typing,max_num)
    else:
        newer_init = addinit_typing1(mylist[0],counter_type[0],new_init,more_list,original_objects,typing,max_num)
        return addinit_typing(mylist[1:],counter_type[1:],newer_init,more_list,original_objects,typing,max_num)

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

def checkprecond_typing(precond,action,typeof):
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
#    if debug == True:
    _DEBUG("addzerotyping",objects,"locations",locations,"theobjects",theobject) #,"new_init",new_init
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
                new_init.append(newzero)
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
