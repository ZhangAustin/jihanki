#!/usr/bin/python

arcs = [
    ("0","0","1"),
    ("0","1","0"),
    ("0","1","1"),
    ("1","0","0"),
    ("1","0","1"),
    ("1","1","0"),
    ("1","1","1"),
    ("x","x","0"),
    ("x","x","1"),
    ("0","x","x"),
    ("1","x","x"),
    ("x","x","x"),
]

def rule1( a1, a2 ):
    """
      For two consecutive arcs:
        a1 0 for index 0 or 2 means
        a2 1 for same index is illegal
    """
    if a1[0]=="0" and a2[0]=="1":
        return False
    if a1[1]=="0" and a2[1]=="1":
        return False
    if a1[2]=="0" and a2[2]=="1":
        return False
    return True

def rule2( a1, a2 ):
    """
     2 0s in adjacent transducers: T1 & T2 or T2 & T3
    cannot both become Xs unless all components become 
    Xs.
    """
    if a1[0]=="0" and a1[1]=="0":
        if a2[0]=="x":
            if a2[1]=="x" and a2[2]=="x":
                return True
            elif a2[1]!="x":
                return True
            else:
                return False
        elif a2[1]=="x":
            if a2[0]=="x" and a2[2]=="x":
                return True
            elif a2[0]!="x":
                return True
            else:
                return False

    if a1[1]=="0" and a1[2]=="0":
        if a2[1]=="x":
            if a2[0]=="x" and a2[2]=="x":
                return True
            elif a2[2]!="x":
                return True
            else:
                return False
        elif a2[2]=="x":
            if a2[0]=="x" and a2[1]=="x":
                return True
            elif a2[1]!="x":
                return True
            else:
                return False
    return True

st = 1
ist = 1
f = set([])
for a1 in arcs:
    print 0, ist, ",".join(a1)
    st = ist+1
    for a2 in arcs:
        if rule1(a1,a2)==False or \
           rule2(a1,a2)==False:
            print ist, st, ",".join(a2)
            f.add(st)
            st += 1
        else:
            pass
    ist = st
#for i in xrange(0,ist):
#    print i
for fs in f:
    print fs
#print "<eps> 0"
#for i,arc in enumerate(arcs):
#    print ",".join(arc), i
    
