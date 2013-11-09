#!/usr/bin/python
from Fst import *

if __name__=="__main__":
    import sys
    
    wfst = Fst()
    wfst.ReadText(sys.argv[1], acceptor=True)
    wfst.WriteText(sys.argv[2])
