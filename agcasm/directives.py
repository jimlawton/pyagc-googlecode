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
#

import sys
from architecture import *
from number import *
from memory import *
from symbol_table import *

# NOTE: Must be a new-style class.
class Directive(object):
    
    def __init__(self, name, mnemonic=None):
        if mnemonic:
            self.mnemonic = mnemonic
        else:
            self.mnemonic = name
        self.name = name
        
    def process(self, context, symbol, operands):
        self.__getattribute__("process_" + self.name)(context, symbol, operands)

    def ignore(self, context):
        context.info("ignoring directive \"%s\"" % self.mnemonic)

    def process_Minus1_DNADR(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def process_Minus2_CADR(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def process_Minus2_DNADR(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def process_Minus3_DNADR(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def process_Minus4_DNADR(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def process_Minus5_DNADR(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def process_Minus6_DNADR(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def process_Minus_DNCHAN(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def process_Minus_DNPTR(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def process_Minus_GENADR(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def process_1DNADR(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def process_2BCADR(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def process_2CADR(self, context, symbol, operands):
        word1 = word2 = None
        if operands:
            bank = None
            op = Number(operands[0])
            if op.isValid():
                word1 = op.value
            else:
                entry = context.symtab.lookup(operands[0])
                if entry:
                    (bank, offset) = context.memmap.pseudoToSegmented(entry.value)
                else:
                    context.error("undefined symbol \"%s\"" % operands[0])
                if bank:
                    word1 = offset
            if len(operands) > 1:
                context.error("operand expressions not supported yet!")
            if context.memmap.isFixed(word1):
                word2 = 0
                # Bits 15-11 of the 2nd generated word contain the bank number.
                word2 |= ((context.fbank & 037) << 10) 
                # Bits 10-8 and 4 are zero. 
                # Bits 7-5 are 000 if F-Bank < 030, 011 if F-Bank is 030-037, or 100 if F-Bank is 040-043.
                if 030 <= context.fbank <= 037:
                    word2 |= (3 << 4)
                elif 040 <= context.fbank <= 043:
                    word2 |= (4 << 4)
                # Bits 3-1 equals the current EBANK= code.
                word2 != (context.ebank & 07)
            else:
                word2 = context.memmap.getBankNumber(word1)
        else:
            context.error("invalid syntax")

    
    def process_2DEC(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def process_2DNADR(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def process_2FCADR(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def process_2OCT(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def process_3DNADR(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def process_4DNADR(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def process_5DNADR(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def process_6DNADR(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def process_Equals_Sign(self, context, symbol, operands):
        if symbol:
            if operands:
                op = Number(operands[0])
                if op.isValid():
                    context.symtab.add(symbol, operands[0], op.value)
                else:
                    context.symtab.add(symbol, operands[0])
            else:
                context.symtab.add(symbol, operands[0], context.loc)
    
    def process_Equals_ECADR(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def process_Equals_MINUS(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def process_ADRES(self, context, symbol, operands):
        if operands:
            op = Number(operands[0])
            if op.isValid():
                aval = op.value
            else:
                entry = context.symtab.lookup(operands[0])
                if entry:
                    (bank, offset) = context.memmap.convertPAToBank(entry.value)
                else:
                    context.error("undefined symbol \"%s\"" % operands[0])
                if bank and (bank == context.fbank or bank == context.ebank):
                    aval = offset
        else:
            context.error("invalid syntax")
    
    def process_BANK(self, context, symbol, operands):
        if operands:
            op = Number(operands[0])
            if op.isValid():
                context.fbank = op.value
                context.loc = context.memmap.segmentedToPseudo(MemoryType.FIXED, op.value, context.bankloc[op.value])
            else:
                context.error("invalid syntax, \"%s\"" % operand)
        else:
            context.loc = context.memmap.segmentedToPseudo(MemoryType.FIXED, context.fbank, context.bankloc[context.fbank])
    
    def process_BBCON(self, context, symbol, operands):
        if operands:
            fbank = None
            op = Number(operands[0])
            if op.isValid():
                fbank = op.value
            else:
                entry = context.symtab.lookup(operands[0])
                if entry:
                    (fbank, offset) = context.memmap.pseudoToSegmented(entry.value)
                else:
                    context.error("undefined symbol \"%s\"" % operands[0])
            if fbank:
                bbval = 0
                # Bits 15-11 of the generated word contain the bank number.
                bbval |= ((fbank & 037) << 10) 
                # Bits 10-8 and 4 are zero. 
                # Bits 7-5 are 000 if F-Bank < 030, 011 if F-Bank is 030-037, or 100 if F-Bank is 040-043.
                if 030 <= fbank <= 037:
                    bbval |= (3 << 4)
                elif 040 <= fbank <= 043:
                    bbval |= (4 << 4)
                # Bits 3-1 equals the current EBANK= code.
                bbval != (context.ebank & 07)
                # TODO: emit bbval to code stream.
        else:
            context.error("invalid syntax")
        
    
    def process_BLOCK(self, context, symbol, operands):
        if operands:
            op = Number(operands[0])
            if op.isValid():
                bank = op.value
                if bank == 0:
                    context.ebank = bank
                    context.loc = context.memmap.convertBankToPA(MemoryType.ERASABLE, bank, context.bankloc[bank])
                else:
                    context.fbank = bank
                    context.loc = context.memmap.segmentedToPseudo(MemoryType.FIXED, bank, context.bankloc[bank])
            else:
                context.error("invalid syntax")
        else:
            context.error("invalid syntax")
    
    def process_BNKSUM(self, context, symbol, operands):
        self.ignore(context)
    
    def process_CADR(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def process_CHECK_Equals(self, context, symbol, operands):
        if operands:
            fields = operands[0].split()
            defn = context.symtab.lookup(fields[0])
            if not defn:
                # Add to checklist and check at the end.
                context.checklist.append(SymbolTableEntry(context, symbol, operands[0]))
            else:
                pa = defn.value
                if len(fields) > 1:
                    op = Number(fields[1].strip())
                    if op.isValid():
                        pa += op.value
                    else:
                        context.error("invalid expression, \"%s\"" % operand)
    
    def process_COUNT(self, context, symbol, operands):
        self.ignore(context)
    
    def process_DEC(self, context, symbol, operands):
        if operands:
            op = Number(operands[0], Number.DECIMAL)
            if op.isValid():
                if symbol:
                    context.symtab.add(symbol, operands[0], op.value)
                context.loc += 1
            else:
                context.error("syntax error: %s %s" % (self.mnemonic, operands[0]))
        else:
            context.error("syntax error: %s %s" % (self.mnemonic, operands[0]))
    
    def process_DNCHAN(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def process_DNPTR(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def process_EBANK_Equals(self, context, symbol, operands):
        # TODO: handle one-shot EBANK=.
        if operands:
            op = Number(operands[0])
            if op.isValid():
                context.ebank = op.value
            else:
                entry = context.symtab.lookup(operands[0])
                if entry:
                    bank = context.memmap.pseudoToSegmented(entry.value)
                else:
                    context.error("undefined symbol \"%s\"" % operands[0])
        else:
            context.error("invalid syntax, \"%s\"" % operands[0])
    
    def process_ECADR(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def process_EQUALS(self, context, symbol, operands):
        if symbol:
            if operands:
                if operands[0].isdigit():
                    context.symtab.add(symbol, operands[0], int(operands[0], 8))
                else:
                    context.symtab.add(symbol, operands[0])
            else:
                context.symtab.add(symbol, None, context.loc)
    
    def process_ERASE(self, context, symbol, operands):
        size = 0
        if not operands:
            size = 1
            operand = None
            op = Number("1")
        else:
            operand = operands[0]
            if '-' in operands[0]:
                op = Number(operands[0].strip())
                if op.isValid():
                    size = op.value
            else:
                op = Number(operands[0])
                if op.isValid():
                    size = op.value + 1
        if symbol and op.isValid():
            context.symtab.add(symbol, operand, op.value)
        context.loc += size
        
    def process_FCADR(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def process_GENADR(self, context, symbol, operands):
        if operands:
            op = Number(operands[0])
            if op.isValid():
                aval = op.value
            else:
                entry = context.symtab.lookup(operands[0])
                if entry:
                    (bank, offset) = context.memmap.convertPAToBank(entry.value)
                else:
                    context.error("undefined symbol \"%s\"" % operands[0])
                if bank:
                    aval = offset
        else:
            context.error("invalid syntax")
    
    def process_MEMORY(self, context, symbol, operands):
        if '-' in operands:
            op1 = int(operands[0], 8)
            if symbol:
                context.symtab.add(symbol, operands[0], op1)
        else:
            context.error("syntax error: %s %s" % (self.mnemonic, operand))
    
    def process_MM(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def process_NV(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def process_OCT(self, context, symbol, operands):
        if operands:
            op = Number(operands[0], Number.OCTAL)
            if op.isValid():
                if symbol:
                    context.symtab.add(symbol, operands[0], op.value)
                context.loc += 1
            else:
                context.error("syntax error: %s %s" % (self.mnemonic, operands[0]))
        else:
            context.error("syntax error: %s %s" % (self.mnemonic, operands[0]))
            
    def process_OCTAL(self, context, symbol, operands):
        self.process_OCT(context, symbol, operands)
    
    def process_REMADR(self, context, symbol, operands):
        if operands:
            op = Number(operands[0])
            if op.isValid():
                aval = op.value
            else:
                entry = context.symtab.lookup(operands[0])
                if entry:
                    (bank, offset) = context.memmap.convertPAToBank(entry.value)
                else:
                    context.error("undefined symbol \"%s\"" % operands[0])
                if bank and (bank != context.fbank and bank != context.ebank):
                    aval = offset
        else:
            context.error("invalid syntax")
    
    def process_SBANK_Equals(self, context, symbol, operands):
        context.warn("unsupported directive: %s %s" % (self.mnemonic, operands))
    
    def process_SETLOC(self, context, symbol, operands):
        if operands:
            if operands[0].isdigit():
                context.loc = int(operands[0], 8)
            else:
                if context.symtab.lookup(operands[0]):
                    context.loc = context.symtab.lookup(operands[0])
        else:
            context.error("invalid syntax")
    
    def process_SUBRO(self, context, symbol, operands):
        self.ignore(context)
    
    def process_VN(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()


DIRECTIVES = {
    Architecture.AGC4_B2 : {
        "-1DNADR":  Directive("Minus1_DNADR", "-1DNADR"),
        "-2CADR":   Directive("Minus2_CADR",  "-2CADR"),
        "-2DNADR":  Directive("Minus2_DNADR", "-2DNADR"),
        "-3DNADR":  Directive("Minus3_DNADR", "-3DNADR"),
        "-4DNADR":  Directive("Minus4_DNADR", "-4DNADR"),
        "-5DNADR":  Directive("Minus5_DNADR", "-5DNADR"),
        "-6DNADR":  Directive("Minus6_DNADR", "-6DNADR"),
        "-DNCHAN":  Directive("Minus_DNCHAN", "-DNCHAN"),
        "-DNPTR":   Directive("Minus_DNPTR",  "-DNPTR"),
        "-GENADR":  Directive("Minus_GENADR", "-GENADR"),
        "1DNADR":   Directive("1DNADR"),
        "2BCADR":   Directive("2BCADR"),
        "2CADR":    Directive("2CADR"),
        "2DEC":     Directive("2DEC"),
        "2DEC*":    Directive("2DEC",         "2DEC*"),
        "2DNADR":   Directive("2DNADR"),
        "2FCADR":   Directive("2FCADR"), 
        "2OCT":     Directive("2OCT"),
        "3DNADR":   Directive("3DNADR"),
        "4DNADR":   Directive("4DNADR"),
        "5DNADR":   Directive("5DNADR"),
        "6DNADR":   Directive("6DNADR"),
        "=":        Directive("Equals_Sign",  "="),
        "=ECADR":   Directive("Equals_ECADR", "=ECADR"),
        "=MINUS":   Directive("Equals_MINUS"  "=MINUS"),
        "ADRES":    Directive("ADRES"),
        "BANK":     Directive("BANK"),
        "BBCON":    Directive("BBCON"),
        "BBCON*":   Directive("BBCON",        "BBCON*"),
        "BLOCK":    Directive("BLOCK"),
        "BNKSUM":   Directive("BNKSUM"),
        "CADR":     Directive("CADR"),
        "CHECK=":   Directive("CHECK_Equals", "CHECK="),
        "COUNT":    Directive("COUNT"),
        "COUNT*":   Directive("COUNT",        "COUNT*"),
        "DEC":      Directive("DEC"),
        "DEC*":     Directive("DEC",          "DEC*"),
        "DNCHAN":   Directive("DNCHAN"),
        "DNPTR":    Directive("DNPTR"),
        "EBANK=":   Directive("EBANK_Equals", "EBANK="),
        "ECADR":    Directive("ECADR"),
        "EQUALS":   Directive("EQUALS"),
        "ERASE":    Directive("ERASE"),
        "FCADR":    Directive("FCADR"),
        "GENADR":   Directive("GENADR"),
        "MEMORY":   Directive("MEMORY"),
        "MM":       Directive("MM"),
        "NV":       Directive("NV"),
        "OCT":      Directive("OCT"),
        "OCTAL":    Directive("OCTAL"),
        "REMADR":   Directive("REMADR"),
        "SBANK=":   Directive("SBANK_Equals", "SBANK="),
        "SETLOC":   Directive("SETLOC"),
        "SUBRO":    Directive("SUBRO"),
        "VN":       Directive("VN")
    }
}

