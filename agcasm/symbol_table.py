#!/usr/bin/env python

# Copyright 2010 Jim Lawton <jim dot lawton at gmail dot com>
# 
# This file is part of pyagc. 
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import sys

class SymbolTableEntry:
    
    def __init__(self, context, name, symbolic=None, value=None):
        self.context = context              # Assembler context.
        self.name = name                    # Symbol name.
        self.symbolic = symbolic            # Symbolic value (expression).
        self.value = value                  # Actual value.
        self.recordIndex = None             # Index of the parser record containing the definition of this symbol.
        self.references = []                # TODO: List of references.
        self.refType = None                 # Reference type: None, forward or reverse 

    def isComplete(self):
        return (self.value != None)

    def addReference(self, ref):
        self.references.append(ref)

    def getReferences(self):
        return self.references

    def __str__(self):
        text = "%-8s "  % (self.name)
        if self.refType != None:
            text += "%-4s " % self.refType
        else:
            text += 4 * ' ' 
        if self.value == None:
            text += "%-20s" % "******"
        else:
            text += "%-10s" % self.context.memmap.pseudoToString(self.value)
            text += "%s " % self.context.memmap.pseudoToSegmentedString(self.value)
        if self.symbolic:
            text += "%-32s " % (' '.join(self.symbolic))
        else:
            text += 33 * ' '
        if self.recordIndex != None:
            text += " %s" % (self.context.records[self.recordIndex].srcline)
        return text

class SymbolTable:
    def __init__(self, context):
        self.symbols = {}
        self.undefs = []
        self.context = context
        
    def add(self, name=None, symbolic=None, value=None):
        if name != None:
            if name in self.symbols.keys():
                self.context.error("symbol \"%s\" already defined!" % (name))
            else:
                self.symbols[name] = SymbolTableEntry(self.context, name, symbolic, value) 
                self.symbols[name].recordIndex = self.context.global_linenum - 1
                if value == None:
                    self.undefs.append(name)
                    self.symbols[name].refType = "FWD"
                    self.context.log("[%05d] added undefined symbol %-8s" % (len(self.symbols), name))
                else:
                    self.symbols[name].refType = "REV"
                    self.context.log("[%05d] added   defined symbol %-8s %s" % (len(self.symbols), name, self.context.memmap.pseudoToSegmentedString(value)))

    def update(self, name=None, symbolic=None, value=None):
        if name != None:
            if name not in self.symbols.keys():
                self.context.error("symbol \"%s\" not defined!" % (name))
            else:
                entry = self.symbols[name]
                entry.value = value
                self.symbols[name] = entry
                self.context.log("updated symbol %-8s %s" % (name, self.context.memmap.pseudoToSegmentedString(value)))

    def resolve(self, maxPasses=10):
        self.context.log("resolving symbols...")
        nPrevUndefs = nUndefs = len(self.undefs)
        for i in range(maxPasses):
            self.context.log("pass %d: %d undefined symbols" % (i, nUndefs))
            if nUndefs == 0:
                self.context.log("all symbols resolved")
                break
            for symbol in self.undefs:
                self.context.assembler.reparse(self.symbols[symbol].recordIndex)
            self.pruneUndefines()
            nUndefs = len(self.undefs)
            if nUndefs == nPrevUndefs:
                self.context.error("aborting, no progress in resolving symbols")
                break
            nPrevUndefs = nUndefs

    def pruneUndefines(self):
        # Prune the undefs list.
        self.context.log("[%05d] pruning undefined symbols list" % len(self.undefs))
        tmpUndefs =[]
        for symbol in self.undefs:
            record = self.context.records[self.symbols[symbol].recordIndex]
            if not record.complete:
                tmpUndefs.append(symbol)
            else:
                self.context.log("[%05d] removing %s from undefined symbols list" % (len(self.undefs), symbol))
        self.undefs = tmpUndefs
        
    def keys(self):
        return self.symbols.keys()

    def lookup(self, name):
        entry = None
        if name in self.symbols:
            entry = self.symbols[name]
        return entry

    def printTable(self, outfile=None):
        if outfile == None:
            out = sys.stdout
        else:
            out = outfile
        symbols = self.symbols.keys()
        symbols.sort()
        for symbol in symbols:
            print >>out, self.symbols[symbol]

        for symbol in self.undefs:
            print >>out, self.symbols[symbol]
