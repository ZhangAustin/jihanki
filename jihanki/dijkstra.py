#!/usr/bin/python
from Token  import Token
from Queues import SQueue

class Dijkstra( ):
    """
      A simple implementation of the Dijkstra shortest
      path algorithm.  No queue optimization.  No checking
      the closed queue for better options.
    """
    def __init__( self, graph ):
        self.graph     = graph
        self.o_queue   = SQueue()

    def dijkstra_path( self ):
        #Initialize the open queue with the start state
        #Note: assumes start state is part of a valid path
        self.o_queue.add( Token(0,0.,0.,None) )

        #Repeatedly check the queue
        while self.o_queue.head().state not in self.graph['F']:
            current = self.o_queue.pop( )

            for arc in self.graph[current.state]:
                score = current.score + arc.score

                if arc.nextstate in self.o_queue and \
                   score < self.o_queue.states[arc.nextstate].score:
                    self.o_queue.remove(arc.nextstate)

                if arc.nextstate not in self.o_queue:
                    heur = score #For a-star this would be different
                    self.o_queue.add(
                        Token(arc.nextstate, score, heur, current) 
                    )

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
    import sys, argparse

    example = "{0}".format(sys.argv[0])
    parser  = argparse.ArgumentParser( description=example )
    parser.add_argument( "--verbose", "-v", help="Verbose mode.", default=False, action="store_true" )
    args = parser.parse_args( )

    #Instantiate a searcher, and run search, compute traceback
    searcher  = Dijkstra( graph, defaultHeuristic )
    searcher.dijkstra_path( )
    traceback = searcher.compute_traceback( )
    for tok in traceback:
        print tok.state, tok.score

