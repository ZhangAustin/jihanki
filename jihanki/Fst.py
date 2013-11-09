#!/usr/bin/env python
import sys, re

class SymbolTable( ):
    def __init__( self, symbols_list=[], eps="<eps>" ):
        self.eps          = eps
        self.syms_to_ints = {eps:0}
        self.ints_to_syms = {0:eps}
        self._load_symbols( symbols_list )

    def _load_symbols( self, symbols_list ):
        for i,symbol in enumerate(symbols_list):
            if symbol not in self.syms_to_ints \
               and i+1 not in self.ints_to_syms:
                self._syms_to_ints[symbol] = i+1
                self._ints_to_syms[i+1]    = symbol
            else:
                print >> sys.stderr, "Duplicate symbol: {0}->{1}".format(symbol,i+1)
        return

    def ReadText( self, symbolfile ):
        for line in open(symbolfile,"r"):
            symbol, sid = re.split(r"\s+",line.strip())
            if symbol not in self._syms_to_ints:
                self._syms_to_ints[symbol]   = int(sid)
                self._ints_to_syms[int(sid)] = symbol
            if int(sid)==0:
                self.eps = symbol
        return

    def NumSymbols( self ):
        return len(self._syms_to_ints.keys())

    def AddSymbol( self, symbol, sid=None ):
        if symbol in self._syms_to_ints:
            return self._syms_to_ints[symbol]
        #Note: this assumes that symbol integers are not
        # scattered willy-nilly.
        sid = self.NumSymbols()
        self._syms_to_ints[symbol] = sid
        self._ints_to_syms[sid]    = symbol
        return sid

    def FindSID( self, sid ):
        if isinstance(sid, int):
            if sid in self._ints_to_syms:
                return self._ints_to_syms[sid]
            else:
                return ""
        else:
            return ValueError, "Predicate not an integer."
    
    def FindSym( self, symbol ):
        if isinstance(symbol,str):
            if symbol in self._syms_to_ints:
                return self._syms_to_ints[symbol]
            else:
                return -1
        else:
            return ValueError, "Predicate not a string."

class State( ):
    """
      WFST state representation.
      Basic feature is simply an integer description.
      Filter state may be useful for composition.
      Additional arguments supported for symbol 
      manipulation or more complex filters.
    """
    def __init__( self, state, filter_state=None, **kwargs ):
        self._state       = state
        self.filter_state = meta
        self.kwargs       = kwargs
    
    def __repr__( self ):
        return str(self._state)

class Arc( ):
    def __init__( self, ilabel, olabel, weight, nstate, **kwargs ):
        self.ilabel = ilabel
        self.olabel = olabel
        self.weight = weight
        self.nstate = nstate
        self.kwargs = kwargs

class Fst( ):

    def __init__( self, isyms=None, osyms=None, ssyms=None, arctype="standard" ):
        self.isyms = self._init_symbol_table(isyms)
        self.osyms = self._init_symbol_table(osyms)
        self.ssyms = self._init_symbol_table(ssyms)
        self.arctype = arctype
        self._state_list = []
        self._state_hash = {}
        self._start      = None
        self._finals     = {}

    def _init_symbol_table( self, syms=None ):
        if syms:
            return syms

        return SymbolTable()

    def NumStates( self ):
        return len(self._state_list);

    def NumArcs( self, state ):
        return len(self._state_hash[state])

    def SetStart( self, state ):
        if state in self._state_hash:
            self._start = state
        else:
            raise KeyError, "State: {0} does not exist!".format(state)
        return state

    def Start( self ):
        return self._start

    def AddState( self, state=None ):
        if not state == None:
            if state not in self._state_hash:
                self._state_hash[state] = []
                self._state_list.append(state)
            return state

        return self.AddState( state=self.NumStates() )

    def AddArc( self, state, arc ):
        if state not in self._state_hash:
            raise KeyError, "State: {0} does not exist!".format(state)
        self._state_hash[state].append(arc)

    def IsFinal( self, sid ):
        if sid in self._finals:
            return self._finals[sid]
        else:
            return float("inf")

    def SetFinal( self, sid, weight=1.0 ):
        self._finals[sid] = weight
        return weight
            
    def ReadText( self, infile, acceptor=False ):
        if acceptor==True:
            return self._read_acceptor( infile )
        return self._read_transducer( infile )
            
    def _read_acceptor( self, infile ):
        for i,line in enumerate(open(infile,"r")):
            parts = re.split("\s+", line.strip())
            if len(parts) not in [1,2,3,4]:
                raise ValueError, "Bad line: {0}".format(line)
            self.AddState(int(parts[0]))

            if len(parts)>2:
                self.AddState(int(parts[1]))
                if i==0:
                    self.SetStart(int(parts[0]))
                if len(parts)==3:
                    self.AddArc( 
                        int(parts[0]), 
                        Arc(
                            ilabel=parts[2], 
                            olabel=parts[2], 
                            weight=1.0, 
                            nstate=int(parts[1]) 
                        )
                    )
                elif len(parts)==4:
                    self.AddArc(
                        int(parts[0]),
                        Arc(
                            ilabel=parts[2], 
                            olabel=parts[2], 
                            weight=float(parts[3]),
                            nstate=int(parts[1]) 
                        )
                    )
            elif len(parts)==2:
                self.SetFinal(int(parts[0]), float(parts[1]))
            else:
                self.SetFinal(int(parts[0]), 1.0 )
        return self.Start()

    def _read_transducer( self, infile ):
        for i,line in enumerate(open(infile,"r")):
            parts = re.split("\s+", line.strip())
            if len(parts) not in [1,2,4,5]:
                raise ValueError, "Bad line: {0}".format(line)
            self.AddState(int(parts[0]))

            if len(parts)>2:
                self.AddState(int(parts[1]))
                if i==0:
                    self.SetStart(int(parts[0]))
                if len(parts)==4:
                    self.AddArc( 
                        int(parts[0]), 
                        Arc(
                            ilabel=parts[2], 
                            olabel=parts[3], 
                            weight=1.0, 
                            nstate=int(parts[1]) 
                        )
                    )
                else:
                    self.AddArc(
                        int(parts[0]),
                        Arc(
                            ilabel=parts[2], 
                            olabel=parts[3], 
                            weight=float(parts[4]),
                            nstate=int(parts[1]) 
                        )
                    )
            elif len(parts)==2:
                self.SetFinal(int(parts[0]), float(parts[1]))
            else:
                self.SetFinal(int(parts[0]), 1.0 )
        return self.Start()

    def WriteText( self, ofile ):
        ofp = open(ofile,"w")
        for state in self._state_list:
            for arc in self._state_hash[state]:
                ofp.write( "{0} {1} {2} {3} {4}\n".\
                           format(
                               state, arc.nstate, 
                               arc.ilabel, arc.olabel, 
                               arc.weight)
                           )
            if self.IsFinal(state) != float("inf"):
                if self._finals[state]==1.0:
                    ofp.write("{0}\n".format(state))
                else:
                    ofp.write("{0} {1}\n".format(state,self._finals[state]))
        ofp.close()
        return
