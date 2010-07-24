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

import os
import sys
from optparse import OptionParser
from architecture import Architecture
from assembler import Assembler
from context import Context

def main():
    parser = OptionParser("usage: %prog [options] src_file [src_file...]")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="Verbose output.")
    parser.add_option("-l", "--log", dest="logLevel", default=0, help="Print detailed log information.")
    parser.add_option("-t", "--test", action="store_true", dest="test", default=False, help="Run assembler test code.")
    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.error("At least one source file must be supplied!")
        sys.exit(1)

    sources = []
    for arg in args:
        sources.append(arg)
        if not os.path.isfile(arg):
            parser.error("File \"%s\" does not exist" % arg)
            sys.exit(1)

    listfile = open(args[0].split('.')[0] + ".lst", 'w')
    symtabfile = open(args[0].split('.')[0] + ".symtab", 'w')
    binfile = open(args[0] + ".bin", 'wb')
    logfile = open(args[0].split('.')[0] + ".log", 'w')

    context = Context(Architecture.AGC4_B2, listfile, binfile, options.verbose, int(options.logLevel), logfile)
    assembler = Assembler(context)
    context.assembler = assembler
    
    assembler.info("Simple AGC Assembler, v0.1", source=False)
    assembler.info("", source=False)

    for arg in args:
        assembler.assemble(arg)

    assembler.info("Resolving symbols...", source=False)
    assembler.resolve()
    
    assembler.info("Writing listing...", source=False)
    print >>listfile 
    print >>listfile, "Listing"
    print >>listfile, "-------"
    for record in assembler.context.records:
        print >>listfile, record

    assembler.info("Writing symbol table...", source=False)
    print >>symtabfile 
    print >>symtabfile, "Symbol Table"
    print >>symtabfile, "------------"
    assembler.context.symtab.printTable(symtabfile)
    
    assembler.info("%d errors, %d warnings" % (context.errors, context.warnings), source=False)
    
    if options.test:
        # FIXME: Temporary hack 
        # Check generated symbols against the symtab generated by yaYUL.
        
        assembler.info("Checking symbol table against yaYUL version...", source=False)
        from artemis072_symbols import ARTEMIS_SYMBOLS
        from memory import MemoryType
        
        nsyms = assembler.context.symtab.getNumSymbols()
        check_nsyms = len(ARTEMIS_SYMBOLS.keys())
        assembler.info("Number of symbols: yaYUL=%d pyagc=%d" % (check_nsyms, nsyms), source=False)
    
        my_syms = []
        other_syms = []
        common_syms = []
        
        for sym in assembler.context.symtab.keys():
            if sym in ARTEMIS_SYMBOLS.keys():
                common_syms.append(sym)
            else:
                if sym != "FIXED":
                    my_syms.append(sym)
                
        for sym in ARTEMIS_SYMBOLS.keys():
            if sym not in assembler.context.symtab.keys():
                if not sym.startswith('$') and sym != "'":
                    other_syms.append(sym)

        if len(my_syms) != 0 or len(other_syms) != 0:
            assembler.error("incorrect number of symbols, expected %d, got %d" % (check_nsyms, nsyms), source=False)
    
        if len(my_syms) > 0:
            assembler.error("symbols defined that should not be defined: %s" % my_syms, source=False)
    
        if len(other_syms) > 0:
            assembler.error("symbols not defined that should be defined: %s" % other_syms, source=False)
    
        errcount = 0
        bad_syms = {}
        
        for sym in common_syms:
            entry = assembler.context.symtab.lookup(sym)
            if entry == None:
                assembler.error("symbol %-8s not defined" % entry, source=False)
            pa = entry.value
            aval = ARTEMIS_SYMBOLS[sym]
            if ',' in aval:
                bank = aval.split(',')[0]
                type = MemoryType.FIXED
                if bank.startswith('E'):
                    bank = bank[1:]
                    type = MemoryType.ERASABLE
                bank = int(bank, 8)
                offset = int(aval.split(',')[1], 8)
                check_pa = context.memmap.segmentedToPseudo(type, bank, offset, absolute=True)
            else:
                check_pa = int(aval, 8)
            if pa != check_pa:
                errcount += 1
                bad_syms[pa] = (sym, check_pa)
    
        if errcount > 0:
            bad_addrs = bad_syms.keys()
            bad_addrs.sort()
            for pa in bad_addrs:
                sym = bad_syms[pa][0]
                check_pa = bad_syms[pa][1]
                assembler.error("symbol %-8s defined as %06o %s, expected %06o %s" % (sym, pa, context.memmap.pseudoToSegmentedString(pa), check_pa, context.memmap.pseudoToSegmentedString(check_pa)), source=False)
            assembler.error("%d/%d symbols incorrectly defined" % (errcount, len(common_syms)), source=False)
        
        # FIXME: End of temporary hack
    
    assembler.info("Writing binary output...", source=False)
    
    assembler.info("Done.", source=False)
    print "Done."

if __name__=="__main__":
    sys.exit(main())
