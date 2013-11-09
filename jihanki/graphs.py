#!/usr/bin/python
class Arc( ):
    def __init__( self, nextstate, score, isfinal ):
        self.nextstate = nextstate
        self.score = score
        self.isfinal = isfinal

wiki_graph_dijkstra = { 
    0 : [ Arc(1,7,False),  Arc(2,9,False), Arc(5,14,False) ],
    1 : [ Arc(3,15,False), Arc(2,10,False) ],
    2 : [ Arc(3,11,False), Arc(5,2,False) ],
    3 : [ Arc(4,6,False) ],
    4 : [ Arc(6,2,False) ],
    5 : [ Arc(4,9,False) ],
    'F' : set([4])
}
