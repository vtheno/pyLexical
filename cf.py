#coding=utf-8
# this is cellvars and freevars in python
# 
import dis
from opcode import opmap,opname
from types import CodeType,FunctionType
def func(x,y):
    x = x + 1
    def out(z):
        z = x + y
        return z
    return out
# func has cellvars ('x','y')
# out has freevars ('x','y')
out = func(1,2)
#dis.dis(func)
#dis.show_code(func)
#dis.dis(out)
#dis.show_code(out)
class Instruction(object):
    def __init__(self,name='<Instruction>'):
        self.argcount = 0
        self.kwonlyargcount = 0
        self.nlocals = 0
        self.stacksize = 1
        self.flags = 0
        self.code = [ ]
        self.name = name
        self.filename = "<string>"
        self.firstlineno = 1
        self.lnotab = b''
        self.consts = set( [None] )
        self.names = set( [ ] )
        self.varnames = set( [ ] ) # nlocals ,local variable and cellvars and arguments
        self.freevars = set( [ ] ) # LOAD_DEREF STORE_DREF
        self.cellvars = set( [ ] ) # LOAD_CLOSURE and LOAD_FAST 

    def converts(self):
        self.consts = tuple(self.consts)
        self.names = tuple(self.names)
        self.varnames = tuple(self.varnames)
        self.freevars = tuple(self.freevars)
        self.cellvars = tuple(self.cellvars)
    def build(self):
        # let x = let a = 1 in a + a in x * x
        # (lambda x : x * x )( (lambda a: a + a) (1) )
        #self.consts.add( 1 )
        #self.varnames.add( 'x' )
        #self.freevars.add( 'a' ) 
        self.converts()
        self.flags = 65 # NOFREE + OPTIMZED
        self.code += [opmap["RETURN_VALUE"],0]
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


co = Instruction()
co.consts = (2,None)
co.code = [opmap["LOAD_CONST"],0]
co = co.build()
dis.dis(co) 
dis.show_code(co)   

co1 = Instruction()
co1.consts = (co,'<lambda>')
co1.code = [opmap["LOAD_CONST"],0,
            opmap["LOAD_CONST"],1,
            opmap["MAKE_FUNCTION"],0,
            opmap["CALL_FUNCTION"],0]
co1 = co1.build()
dis.dis(co1)
dis.show_code(co1)
a = eval(co1)
print( a )
