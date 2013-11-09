#!/usr/bin/env python
from Token import Token
import random

class MaxHeap( ):
    """
     [13, 9, 5, 12, 8, 7, 4, 0, 6, 2, 1]
    """
    def __init__( self ):
        self.heap = [ 
            Token( 11, 1,  1 ),
            Token( 0, 15, 15 ),
            Token( 5, 13, 13 ),
            Token( 1,  9,  9 ),
            Token( 2,  5, 12 ),
            Token( 3,  8,  8 ),
            Token( 4,  7,  7 ),
            Token( 6,  4,  4 ),
            Token( 7,  0,  0 ),
            Token( 8,  6,  6 ),
            Token( 9,  2,  2 ),
            Token(10,  1,  1 ),
            ]

    def __contains__( self, key ):
        for i,token in enumerate(self.heap):
            if token.state == key:
                return i
        return -1

    def parent( self, i ):
        return ((i+1)/2) - 1

    def leftchild( self, i ):
        return i*2 + 1

    def rightchild( self, i ):
        return i*2 + 2

    def heapify( self, i ):
        lc_i = self.leftchild( i )
        rc_i = self.rightchild( i )

        largest = i
        if lc_i < len(self.heap) and self.heap[largest] < self.heap[lc_i]:
            largest = lc_i
        if rc_i < len(self.heap) and self.heap[largest] < self.heap[rc_i]:
            largest = rc_i

        if not largest == i:
            self.heap[largest], self.heap[i] = self.heap[i], self.heap[largest]
            self.heapify(largest)
        
    def max_heapify( self ):
        for i in xrange( (len(self.heap)/2)-1, -1, -1 ):
            self.heapify( i )

    def heap_sort( self ):
        sorted_heap = []

        while len(self.heap)>0:
            self.max_heapify()
            sorted_heap.append(self.heap.pop(0))
            
        self.heap = sorted_heap

    def add_to_heap( self, token ):
        self.heap.append( token )
        self.max_heapify()

    def get_depth( self, i, depth=0 ):
        if self.parent(i)==-1:
            return depth

        return self.get_depth( self.parent(i), depth+1 )

    def print_tree( self ):
        rows = []
        for i,token in enumerate(self.heap):
            depth = self.get_depth(i, 0)
            if len(rows) <= depth:
                rows.append([token])
            else:
                rows[depth].append(token)
        for row in rows:
            print row

    def pop( self ):
        """
          Pop the root and re-heapify
        """
        max_token = self.heap.pop(0)
        self.max_heapify()
        return max_token

    def update( self, state, heur, cost ):
        i = state in self
        print i
        if i==-1:
            raise ValueError, "No token for requested state!"

        self.heap[i].heur = heur
        self.heap[i].cost = cost
        self.max_heapify()
        
if __name__=="__main__":

    m = MaxHeap()
    print m.heap
    m.heapify(0)
    print m.heap
    m.max_heapify()
    print m.heap
    m.heap_sort()
    print m.heap
    print "Add 3"
    m.add_to_heap( Token(15,3,3) )
    print m.heap
    print "3 ->", m.parent(len(m.heap)-1)
    m.heap_sort()
    print m.heap
    print "Add 26"
    m.add_to_heap( Token(16,26,26) )
    print m.heap
    print "26 ->", m.parent(len(m.heap)-1)
    m.heap_sort()
    print m.heap
    print ""
    m.print_tree()
    print ""
    print 16 in m
    print m.pop()
    print 16 in m
    m.print_tree()
    print ""
    m.update(7,5,18)
    print m.heap
    m.print_tree()
    #print ""
    #for i in range(5):
    #    random.shuffle(m.heap)
    #    print m.heap
    #    m.heap_sort()
    #    print m.heap
    #    print ""
    #print ""
    #random.shuffle(m.heap)
    #m.print_tree()
    #print ""
    #m.max_heapify()
    #m.print_tree()
    #print ""
    #m.heap_sort()
    #m.print_tree()
