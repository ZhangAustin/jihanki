#!/usr/bin/python

class Token( ):
    def __init__( self, state, score=0.0, heur=0.0, parent=None, label=None ):
        self.score  = float(score) #actual score
        self.heur   = float(heur)  #heuristic score in Dijkstra: score==heur
        self.state  = state
        self.label  = label
        self.parent = parent

    def __repr__( self ):
        string = str(self.heur)
        return string

    #def __repr__( self ):
    #    string = str(self.state)+":"+str(self.score)+":"+str(self.heur)+":"
    #    if self.parent:
    #        string += str(self.parent.state)
    #    else:
    #        string += str(None)
    #    return string

    def __cmp__( self, other ):
        if self.heur   > other.heur:
            return 1
        elif self.heur == other.heur:
            return 0
        elif self.heur < other.heur:
            return -1

if __name__=="__main__":
    import sys, argparse
    from random import random

    tokens = []
    for i in xrange(65,75):
        tok = Token(0, i*random())
        tok.label = chr(i)
        tokens.append(tok)

    print tokens
    tokens.sort()
    print tokens
    
