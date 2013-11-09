#!/usr/bin/python
from Token  import Token
from Queues import SQueue

def defaultHeuristic( token, arc ):
    """
      Default heuristic = 0.
      Equivalent to Dijkstra.
    """

    return 0.

class Dijkstra( ):
    """
      A simple implementation of the Dijkstra shortest
      path algorithm.  No queue optimization.  No checking
      the closed queue for better options.
    """
    def __init__( self, graph, heuristic ):
        self.graph     = graph
        self.heuristic = heuristic
        self.o_queue   = SQueue()

    def dijkstra_path( self ):
        #Initialize the open queue with the start state
        #Note: assumes start state is part of a valid path
        self.o_queue.add( Token(0,0.,0.+self.heuristic(None,None),None) )

        #Repeatedly check the queue
        states_searched = 0
        arcs_searched   = 0
        while self.o_queue.head().state not in self.graph['F']:
            states_searched += 1
            current = self.o_queue.pop( )

            for arc in self.graph[current.state]:
                arcs_searched += 1
                score = current.score + arc.score

                if arc.nextstate in self.o_queue and \
                   score < self.o_queue.states[arc.nextstate].score:
                    self.o_queue.remove(arc.nextstate)

                if arc.nextstate not in self.o_queue:
                    heur = score + self.heuristic(current, arc)
                    self.o_queue.add(
                        Token(arc.nextstate, score, heur, current) 
                    )
        print "Total states searched:", states_searched
        print "Total arcs searched:", arcs_searched
        return 

    def compute_traceback( self ):
        """
          Reconstruct the traceback, yielding
          the actual shortest path, in order.
        """
        head = self.o_queue.head()

        traceback = [head]
        while head.parent:
            head = head.parent
            traceback.append(head)
        traceback.reverse()

        return traceback



if __name__=="__main__":
    from graphs import wiki_graph_dijkstra as graph
    import sys

    searcher  = Dijkstra( graph, defaultHeuristic )
    searcher.dijkstra_path( )
    traceback = searcher.compute_traceback( )
    for tok in traceback:
        print tok.state, tok.score

