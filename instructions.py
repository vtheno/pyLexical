#coding=utf-8
from datatype import *
from types import CodeType
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
class Instruction(metaclass=TypeMeta):
    def __init__(self,name=''):
        self.argcount = 0
        self.kwonlyargcount = 0
        self.nlocals = 0
        self.stacksize = 0
        self.flags = 0 #int( bytes([0] * 9) )
        self.code = [ ]
        self.consts = set( [None] ) # LOAD_CONST 
        self.names = set(  ) # LOAD_NAME,STORE_NAME
        # LOAD_GLOBAL,STORE_GLOBAL
        self.varnames = set(  ) # LOAD_FAST,STORE_FAST
        self.filename = '<Inst>'
        self.name = name
        self.firstlineno = 1
        self.lnotab = b''
        self.freevars = set() # need __closure__ ,LOAD_ClOSURE
        self.cellvars = set() # LOAD_DEREF, STORE_DEREF

    def makeCode(self):
        self.converts()
        self.getIndexs()
        self.LabelConvert()
        self.nlocals = len(self.varnames)
        # varnames is local variable names and function arguments
        self.code += [opmap["RETURN_VALUE"],0]
        #print( self.code )
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
            if i == len(code):
                break
            if op in jumps and type(args) != int:
                #print( " op in jumps ")
                name,source = args
                if name == 'goto':
                    index = self.code.index(source)
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
                name,source = args
                if op is opmap["LOAD_CONST"] and name == 'consts':
                    result += [ self.consts.index(source) ]
                elif op is opmap["LOAD_NAME"] and name == 'L_NAME':
                    result += [ self.names.index(source) ]
                elif op is opmap["STORE_NAME"] and name == 'S_NAME':
                    result += [ self.names.index(source) ]
                elif op is opmap["LOAD_DEREF"] and name == 'L_REF':
                    if len(self.cellvars) > 0:
                        if source in self.cellvars:
                            result += [ self.cellvars.index(source) ]
                        else:
                            result += [ self.freevars.index(source) ]
                    else:
                        result += [ self.freevars.index(source) ]
                elif op is opmap["STORE_DEREF"] and name == 'S_REF':
                    if len(self.cellvars) > 0:
                        if source in self.cellvars:
                            result += [ self.cellvars.index(source) ]
                        else:
                            result += [ self.freevars.index(source) ]
                    else:
                        result += [ self.freevars.index(source) ]
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
        self.flags = 65 # NOFREE OPTIMZED
        self.code = [opmap["LOAD_CONST"],('consts',num)]
class SymInst(Instruction):
    def __init__(self,sym):
        super(SymInst,self).__init__()
        self.stacksize = 1
        self.varnames.update( sym )
        self.flags = 65 # NOFREE optimzed
        """
        self.code = [opmap["LOAD_FAST"],('L_FAST',sym),
                     opmap["NOP"],0]
        """
        self.code = [opmap["LOAD_DEREF"],('L_REF',sym)]

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
        self.flags = 65 # NOFREE OPTIMZED
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
        self.flags = 65 # NOFREE and OPTIMZED
        jump_label = makeLabel()
        self.code = cond.code + \
                    [opmap["POP_JUMP_IF_FALSE"],('goto',jump_label)] + \
                    true.code + \
                    [opmap["JUMP_FORWARD"],len(false.code) + 2] + \
                    [jump_label,0 ] + \
                    false.code


class LetInst(Instruction):
    def __init__(self,sym,val,body):
        super(LetInst,self).__init__()
        self.cellvars = set( [ sym ] )
        self.freevars = set( [ ] )
        self.stacksize = body.stacksize
        self.consts.update( val.consts , body.consts )
        self.cellvars.update( body.cellvars )

        self.flags = 65 # OPTIMZED
        self.code = val.code + \
                    [ opmap["STORE_DEREF"],('S_REF',sym), ] + \
                    body.code 
        """
                      #opmap["DUP_TOP"],0,    # debug
                      #opmap["PRINT_EXPR"],0, # debug
                      opmap["LOAD_CLOSURE"],0,
                      opmap["BUILD_TUPLE"],1,
                      #opmap["DUP_TOP"],0,    # debug
                      #opmap["PRINT_EXPR"],0, # debug
                      opmap["LOAD_CONST"],('consts',_body),
                      opmap["LOAD_CONST"],('consts','<body>'),
                      opmap["MAKE_FUNCTION"],8, # 0x8 -> cellvars and closure
                      opmap["CALL_FUNCTION"],0,
                    ]
        """
class MainInst(Instruction):
    def __init__(self,code):
        super(MainInst,self).__init__()
        self.consts.add(code)
        self.consts.add('code')
        self.names.add('main')
        self.code = [opmap["LOAD_CONST"],('consts',code),
                     opmap["LOAD_CONST"],('consts','code'),
                     opmap["MAKE_FUNCTION"],0,
                     opmap["STORE_NAME"],('S_NAME','main'),
                     opmap["LOAD_NAME"],("L_NAME","main") ]
__all__ = ["SymInst","NumInst",
           "LetInst",
           "BinopInst","IfInst",
           "MainInst",
           "Instruction"]

