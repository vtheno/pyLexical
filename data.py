#coding=utf-8
from datatype import *
#from instructions import *
class Expr(metaclass=TypeMeta): pass
empty = "empty"
extend = "extend"
def emptyEnv():
    return [empty]
emptyEnv = [empty]
def extendEnv(sym,val,env):
    return [extend,sym,val,env]
class ApplyEnvError(Exception): pass
def applyEnv(sym,env):
    temp = env
    while temp != emptyEnv:
        if extend == temp[0]:
            ss,vv = temp[1],temp[2]
            temp = temp[3]
            if sym == ss:
                return vv
    else:
        raise ApplyEnvError( "no bound variable {} {} ".format(sym,env) )
    
class SYM(Expr):
    def __init__(self,sym):
        self.sym = sym
    def __repr__(self):
        return "{}".format(self.sym)
    def singleStepEval(self,env):
        return applyEnv(self.sym,env)
class NUM(Expr):
    def __init__(self,num):
        self.num = num
    def __repr__(self):
        return "{}".format(repr(self.num))
    def singleStepEval(self,env):
        return self.num
class BINOP(Expr):
    tables = {'+':lambda a,b:a+b,
              '-':lambda a,b:a-b,
              '*':lambda a,b:a*b,
              '/':lambda a,b:a/b,
            '==':lambda a,b:1 if a==b else 0,}
    def __init__(self,l,opname,r):
        self.left = l
        self.opname = opname
        self.right = r
    def __repr__(self):
        return "({} {} {})".format(self.left,self.opname,self.right)
    def singleStepEval(self,env):
        if isinstance(self.left,NUM) and isinstance(self.right,NUM):
            return NUM( self.tables[self.opname](self.left.singleStepEval(env),
                                                 self.right.singleStepEval(env)) )
        elif isinstance(self.left,NUM):
            return BINOP(self.left,
                         self.opname,
                         singleStepEval(self.right,env))
        else:
            return BINOP(singleStepEval(self.left,env),
                         self.opname,
                         self.right)
class IF(Expr):
    def __init__(self,e1,e2,e3):
        self.cond = e1
        self.true = e2
        self.false = e3
    def __repr__(self):
        return "({} {} {} {})".format(self.__name__,self.cond,self.true,self.false)
    def singleStepEval(self,env):
        if isinstance(self.cond,NUM):
            return self.true if self.cond.num else self.false
        else: # if isinstance(self.cond,Expr):
            return IF(singleStepEval(self.cond,env),self.true,self.false)
class LET(Expr):
    def __init__(self,sym,val,body):
        self.sym = sym # str
        self.val = val # Expr
        self.body = body # Expr
    def __repr__(self):
        return "({} {}={} in {})".format(self.__name__,self.sym,self.val,self.body)
    def singleStepEval(self,env):
        newEnv = extendEnv(self.sym,self.val,env)
        return multStepEval(self.body,newEnv)

def singleStepEval( expr , env):
    print( "singleStepEval:",expr )
    if isinstance(expr,IF):
        return expr.singleStepEval(env)
    elif isinstance(expr,BINOP):
        return expr.singleStepEval(env)
    elif isinstance(expr,LET):
        return expr.singleStepEval(env)
    elif isinstance(expr,NUM):
        return expr.singleStepEval(env)
    elif isinstance(expr,SYM):
        return expr.singleStepEval(env)
    else:
        raise RuntimeError( "{} ".format(repr(expr)) )

def multStepEval( expr ,env ):
    #print( "multStepEval:",expr )
    if isinstance(expr,SYM):
        return expr.singleStepEval(env)
    elif isinstance(expr,NUM):
        return expr
    else:
        return multStepEval( singleStepEval(expr,env) ,env)
__all__ = ["Expr",
           "BINOP",
           "SYM","NUM",
           "IF",
           "LET",
           "singleStepEval","multStepEval"
       ]
