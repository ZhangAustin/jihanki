#!/usr/bin/python
import re

class SymTable( ):
    def __init__( self ):
        self.s2i = {}
        self.i2s = {}

    def Find( self, item ):
        if isinstance(item,int):
            if item in self.i2s:
                return self.i2s[item]
            else:
                return False
        elif isinstance(item,str):
            if item in self.s2i:
                return self.s2i[item]
            else:
                return False
        else:
            raise KeyError, "Item should be Int or String."

    def AddSymbol( self, sym, i=None ):
        if i==None:
            if not sym in self.s2i:
                self.s2i[sym] = len(self.s2i.keys())
                self.i2s[self.s2i[sym]] = sym
            return self.s2i[sym]
        else:
            if not isinstance(i, int):
                raise TypeError, "i is not an Int!"
            if i in self.i2s:
                raise ValueError, "i is already present!"
            if not sym in self.s2i:
                self.s2i[sym] = i
                self.i2s[i] = sym
            return self.s2i[sym]
            

    def WriteText( self, ofile ):
        ofp = open(ofile,"w")
        for i in sorted(self.i2s.keys()):
            print >> ofp, "{0}\t{1}".format(self.i2s[i],i)
        ofp.close()
        return

    def ReadText( self, ifile ):
        for line in open(ifile,"r"):
            sym, i = re.split(r"\s+", line.strip())
            self.s2i[sym] = int(i)
            self.i2s[int(i)] = sym
        return

class Arc( ):
    def __init__( self, ilabel, olabel, weight, nstate ):
        self.ilabel = ilabel
        self.olabel = olabel
        self.weight = weight
        self.nstate = nstate

class State( ):
    def __init__( self, sid, weight=-99 ):
        self.sid = sid
        self.weight = weight
        self.arcs = []

class WFST( ):

    def __init__( self, ssyms=SymTable(), isyms=SymTable(), osyms=SymTable(), 
                  states={}, finals=[], start=None ):
        self.ssyms  = ssyms
        self.isyms  = isyms
        self.osyms  = osyms
        self.states = states
        self.start  = start
        self.finals = finals

    def SetStart( self, state ):
        """
          There should be only one start state.
        """
        self.start = state
        return self.start

    def SetFinal( self, state, weight ):
        if not state in self.states:
            raise ValueError, "State: {0} doesn't exist!".format(state)
        self.states[state].weight = weight

        return self.states[state]

    def Final( self, state ):
        if not state in self.states:
            raise ValueError, "State: {0} doesn't exist!".format(state)

        if self.states[state].weight<=-99:
            return -99
        else:
            return self.states[state].weight

    def AddArc( self, istate, arc ):
        if not istate in self.states:
            raise ValueError, "State: {0} doesn't exist!".format(istate)

        self.states[istate].arcs.append(arc)
        if arc.nstate not in self.states:
            self.AddState(sid=arc.nstate)

        return

    def AddState( self, **kwargs ):
        if "sid" in kwargs:
            nstate = kwargs["sid"]
            if nstate not in self.states:
                self.states[nstate] = State(nstate)
            return self.states[nstate]
        else:
            nstate = len(self.states.keys())
            self.states[nstate] = State(nstate)
            return self.states[nstate]

    def ReadText( self, ifst, fst=True ):
        for i,line in enumerate(open(ifst,"r")):
            parts = re.split(r"\s+",line.strip())
            #Final state
            if len(parts)==2:
                self.AddState(sid=parts[0])
                self.SetFinal(parts[0], parts[1])
            elif len(parts)==1:
                self.AddState(sid=parts[0])
                self.SetFinal(parts[0], 1)

            elif fst==True and len(parts)>3:
                self.AddState(int(parts[0]))
                ilabel = self.isyms.AddSymbol(parts[2]) 
                olabel = self.osyms.AddSymbol(parts[2])
                weight = 1.0
                if len(parts)==5:
                    weight = float(parts[4])
                self.AddArc(
                    int(parts[0]), 
                    Arc( ilabel, olabel, weight, int(parts[1]) )
                )
            elif fst==False and len(parts)<5:
                self.AddState(int(parts[0]))
                ilabel = self.isyms.AddSymbol(parts[2])
                weight = 1.0
                if len(parts)==4:
                    weight = float(parts[3])
                self.AddArc(
                    int(parts[0]),
                    Arc( ilabel, ilabel, weight, int(parts[1]) )
                )
            else:
                raise SyntaxError, "Bad line: {0}".format(line)

    def WriteText( self, ofile ):
        ofp = open(ofile,"w")
        for state in self.states:
            for arc in self.states[state].arcs:
                print >> ofp, "{0}\t{1}\t{2}\t{3}\t{4}".format(
                    state, arc.nstate, arc.ilabel, arc.olabel, arc.weight
                    )
            if self.Final(state)>-99:
                print >> ofp, "{0}\t{1}".format( state, self.Final(state) )
        ofp.close()

if __name__=="__main__":
    pass
