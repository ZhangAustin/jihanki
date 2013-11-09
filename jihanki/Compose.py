#!/usr/bin/python
from Fst import *
import re


class ComposeSimple( ):
    """
      Vanilla composition with no special support
      for epsilon transitions or other goodies.
    """
      
    def __init__( self, fst1, fst2 ):
        self.fst1   = fst1
        self.fst2   = fst2
        self.result = Fst( )
        self.queue  = [ ]

class Compose( ):
    """
      Normal composition.  Handles epsilons using 
      the standard epsilon filter Fst.
    """
    def __init__( self, fst1, fst2 ):
        pass

class ComposeFst(Fst):
    """
      Lazy composition.  Same process as 'Compose',
      but only expands arc and states on-demand.
    """
    def __init__( self, fst1, fst2 ):
        pass

class ThreeWayComposeSimple( ):
    """
      Three-way composition as described in Allauzen 2012.
      This version uses dualing epsilon filters.
    """
    def __init__( self, fst1, fst2, fst3 ):
        pass

class ThreeWayCompose( ):
    """
      Three-way composition as described in Allauzen 2012.
      This version uses the more complex 3D filter.
    """
    def __init__( self, fst1, fst2, fst3 ):
        pass

class ThreeWayComposeFst(Fst):
    """
      Lazy three-way composition.  This uses 3D filter 
      approach from ThreeWayCompose, but arcs and states
      are only expanded 'on-demand'.
    """
    def __init__( self, fst1, fst2, fst3 ):
        pass
