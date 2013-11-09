#!/usr/bin/python
from Token import Token

class SQueue( ):
    """
      A Toy queue suitable for use with the Dijkstra 
      implementation in question.
        @self.queue   manages the order
        @self.states  manages membership
    """
    def __init__( self ):
        self.queue  = []
        self.states = {}

    def __contains__( self, key ):
        if isinstance(key,int):
            return key in self.states
        return key.state in self.states

    def __repr__( self ):
        return self.queue.__repr__()

    def add( self, tok ):
        self.states[tok.state] = tok
        self.queue.append(tok)
        self.queue.sort()

    def head( self ):
        """
         Just return the top element, but
         do not pop/delete it.
        """
        return self.queue[-1]

    def pop( self ):
        tok = self.queue.pop( )
        self.states.pop(tok.state)
        return tok

    def remove( self, state ):
        tok = self.states.pop(state)
        self.queue.remove(tok)
        return

