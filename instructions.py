#coding=utf-8
from datatype import *
from types import CodeType
from types import FunctionType
from opcode import opmap,opname
import dis
class Label(object):
    def __init__(self):
        self.labels = [ ]
        self.label_count = 0
    def newLableNumber(self):
        self.label_count += 1
        return self.label_count
    def makeLabel(self):
        label = "label_" + str(self.newLableNumber())
        self.labels += [ label ]
        return label
LABEL = Label()
makeLabel = LABEL.makeLabel
jumps = [opmap["POP_JUMP_IF_FALSE"],
         opmap["POP_JUMP_IF_TRUE"],
         opmap["JUMP_IF_TRUE_OR_POP"],
         opmap["JUMP_IF_FALSE_OR_POP"],
         opmap["JUMP_ABSOLUTE"]]
jump_forward = opmap["JUMP_FORWARD"]
def makefunc(code,env):
    return FunctionType(code,env)
class Instruction(metaclass=TypeMeta):
    def __init__(self,name=''):
        self.argcount = 0
        self.kwonlyargcount = 0
        self.nlocals = 0
        self.stacksize = 0
        self.flags = 0 #int( bytes([0] * 9) )
        self.code = [ ]
        self.consts = set( [None] )
        self.names = set( ["DUMMY"] )
        self.varnames = set( )
        self.filename = '<Inst>'
        self.name = name
        self.firstlineno = 0
        self.lnotab = b''
        self.freevars = ()
        self.cellvars = ()
    def makeCode(self):
        self.converts()
        self.getIndexs()
        self.LabelConvert()
        self.code += [opmap["RETURN_VALUE"],0]
        #print( 'makeCode:',self.code,len(self.code) )
        #print( self.consts,self.names,
        #       self.varnames,self.freevars,self.cellvars )
        code = CodeType(self.argcount,       # argcount
                        self.kwonlyargcount, # kwonlyargcount
                        self.nlocals,        # nlocals
                        self.stacksize,      # stacksize
                        self.flags,          # flags
                        bytes(self.code),    # codestring
                        self.consts,         # consts
                        self.names,          # names
                        self.varnames,       # varnames
                        self.filename,       # filename
                        self.name,           # name
                        self.firstlineno,    # firstlineno
                        self.lnotab,         # lnotab
                        self.freevars,       # freevars
                        self.cellvars,       # cellvars
                    )
        return code

    def LabelConvert(self):
        code = self.code
        length = len(code)
        i = 0
        while i < length:
            op,args = code[i],code[i+1]
            if op in jumps and type(args) != int:
                #print( " op in jumps ")
                index = args(self.code)
                code[i+1] = index
                code[index] = opmap["NOP"]
            i+=2
        self.code = code
    def converts(self):
        self.consts = tuple(self.consts)
        self.names = tuple(self.names)
        self.varnames = tuple(self.varnames)
        self.freevars = tuple(self.freevars)
        self.cellvars = tuple(self.cellvars)
    def getIndexs(self):
        result = [ ]
        code = self.code
        i,length = 0,len(code)
        while i < length:
            op,args = code[i],code[i+1]
            result += [op]
            if type(args) != int:
                if op is opmap["LOAD_CONST"]:
                    result += [ args(self.consts) ]
                elif op is opmap["LOAD_GLOBAL"]:
                    result += [ args(self.names) ]
                elif op is opmap["STORE_GLOBAL"]:
                    result += [ args(self.names) ]
                else:
                    result += [args]
            else:
                result += [args]
            i += 2
        self.code = result
class NumInst(Instruction):
    def __init__(self,num):
        super(NumInst,self).__init__()
        self.stacksize = 1
        self.consts = (num,)
        def numIndex(consts):
            return consts.index(num)
        self.code = [opmap["LOAD_CONST"],numIndex,
                     opmap["NOP"],opmap["NOP"]]
class SymInst(Instruction):
    def __init__(self,sym):
        super(SymInst,self).__init__()
        self.stacksize = 1
        self.names.update( sym )
        def symIndex(names):
            if sym in names:
                return names.index(sym)
            else:
                print( ' undefine variable ')
                return names.index('DUMMY')
        self.code = [opmap["LOAD_GLOBAL"],symIndex,
                     opmap["NOP"],opmap["NOP"]]
class BinopInst(Instruction):
    tables = {
        '+':opmap["BINARY_ADD"],
        '-':opmap["BINARY_SUBTRACT"],
        '*':opmap["BINARY_MULTIPLY"],
    }
    def __init__(self,left,right,opname):
        super(BinopInst,self).__init__()
        self.stacksize = max(left.stacksize,right.stacksize)
        self.consts.update ( left.consts ,right.consts )
        self.names.update ( left.names, right.names )
        self.varnames.update ( left.varnames,right.varnames )
        self.code = left.code + \
                    right.code + \
                    [self.tables[opname],0] 
class IfInst(Instruction):
    def __init__(self,cond,true,false):
        super(IfInst,self).__init__()
        self.stacksize = max(cond.stacksize,true.stacksize,false.stacksize)
        self.consts.update( cond.consts,
                            true.consts,
                            false.consts)
        self.names.update( cond.names,
                           true.names,
                           false.names )
        self.varnames.update( cond.varnames,
                              true.varnames,
                              false.varnames)
        '''
        <cond_code>,
        POP_JUMP_IF_FALSE,<false_code>,
        <true_code>,
        <false_code>,
        '''
        false_label = makeLabel()
        def falseLabel(code):
            return code.index(false_label)
        self.code = cond.code + \
                    [opmap["POP_JUMP_IF_FALSE"],falseLabel,
                     opmap["NOP"],opmap["NOP"] ] + \
                    true.code + \
                    [opmap["JUMP_FORWARD"],len(false.code) + 2] + \
                    [false_label,opmap["NOP"] ] + \
                    false.code

class ValInst(Instruction):
    def __init__(self,sym,val):
        super(ValInst,self).__init__()
        self.consts = val.consts
        self.freevars = val.freevars
        self.cellvars = val.freevars
        self.stacksize = 2
        self.names = val.names
        self.names.add(sym)
        def symIndex(names):
            return names.index(sym)
        self.code = val.code + \
                    [ opmap["DUP_TOP"],0,
                      opmap["STORE_GLOBAL"],symIndex,
                      opmap["LOAD_GLOBAL"],symIndex ]
__all__ = ["SymInst","NumInst",
           "ValInst",
           "BinopInst","IfInst",
           "Instruction",
           "makefunc"]