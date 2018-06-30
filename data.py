#coding=utf-8
from datatype import *
#from instructions import *
class Expr(metaclass=TypeMeta): pass
class ApplyEnvError(Exception): pass
class Environment(metaclass=TypeMeta): pass
class Empty(Environment): pass
class Extend(Environment):
    def __init__(self,sym,val,env):
        self.sym = sym
        self.val = val
        self.env = env
    def __repr__(self):
        return "[ {} , {} , {} , {} ]".format(self.__name__,self.sym,self.val,repr(self.env))
class Env(object):
    def __init__(self,init=Empty()):
        self.env = init
    def __repr__(self):
        return repr(self.env)
    def extendEnv(self,sym,val):
        return Env( Extend(sym,val,self.env) )
    def assginEnv(self,sym,val):
        self.env = self.extendEnv(sym,val)
    def applyEnv(self,sym):
        temp = self.env
        while not isinstance(temp,Empty):
            if isinstance(temp,Env):
                temp = temp.env
            if isinstance(temp,Extend):
                ss,vv,temp = temp.sym,temp.val,temp.env
                if sym == ss:
                    return vv
        else:
            raise ApplyEnvError( "no bound variable {}, {} ".format(sym,self.env) )

class EvalERROR(Exception): pass
def Eval( expr, env ):
    print( "Step:",expr,env )
    if isinstance(expr,SYM):
        return env.applyEnv(expr.sym)
    elif isinstance(expr,NUM):
        return expr
    elif isinstance(expr,FUN):
        return expr
    elif isinstance(expr,BINOP):
        return expr.next(env)
    elif isinstance(expr,IF):
        return expr.next(env)
    elif isinstance(expr,LET):
        return expr.next(env)
    elif isinstance(expr,DEF):
        return expr.next(env)
    elif isinstance(expr,APP):
        return expr.next(env)
    else:
        raise EvalERROR('expr is not buildin type: {} , {}'.format(expr,type(expr)))
class SYM(Expr):
    def __init__(self,sym):
        self.sym = sym
    def __repr__(self):
        return "{}".format(self.sym)
class NUM(Expr):
    def __init__(self,num):
        self.num = num
    def __repr__(self):
        return "{}".format(repr(self.num))
    def singleStepEval(self,env):
        return self
class BINOP(Expr):
    tables = {'+':lambda a,b:NUM(a.num+b.num),
              '-':lambda a,b:NUM(a.num-b.num),
              '*':lambda a,b:NUM(a.num*b.num),
              '/':lambda a,b:NUM(a.num/b.num),
            '==':lambda a,b:NUM(1 if a.num==b.num else 0),}
    def __init__(self,l,opname,r):
        self.left = l
        self.opname = opname
        self.right = r
    def __repr__(self):
        return "({} {} {})".format(self.left,self.opname,self.right)
    def next(self,env):
        l = Eval(self.left,env)
        r = Eval(self.right,env)
        if isinstance(l,NUM) and isinstance(r,NUM):
            return self.tables[self.opname](l,r)
        else:
            raise TypeError( "{} need type int * int ,but {} * {}".format(self.opname,type(l),type(r)))
    
class IF(Expr):
    def __init__(self,e1,e2,e3):
        self.cond = e1
        self.true = e2
        self.false = e3
    def __repr__(self):
        return "({} {} {} {})".format(self.__name__,self.cond,self.true,self.false)
    def next(self,env):
        test = Eval(self.cond,env)
        if test:
            return Eval(self.true,env)
        return Eval(self.false,env)
class LET(Expr):
    def __init__(self,sym,val,body):
        self.sym = sym # str
        self.val = val # Expr
        self.body = body # Expr
    def __repr__(self):
        return "({} {}={} in {})".format(self.__name__,self.sym,self.val,self.body)
    def next(self,env):
        val = Eval(self.val,env)
        newEnv = env.extendEnv(self.sym,val)
        return Eval(self.body,newEnv)
class DEF(Expr):
    def __init__(self,sym,val):
        self.sym = sym
        self.val = val
    def __repr__(self):
        return "({} {} {})".format(self.__name__,self.sym,self.val)
    def next(self,env):
        val = Eval(self.val,env)
        env.assginEnv(self.sym,val)
        return val
class FUN(Expr):
    def __init__(self,sym,body):
        self.sym = sym
        self.body = body
    def __repr__(self):
        return "({} {} {})".format(self.__name__,self.sym,self.body)

class APPLYERROR(Exception): pass
class APP(Expr):
    def __init__(self,e1,e2):
        self.e1 = e1
        self.e2 = e2
    def __repr__(self):
        return "({} {} {})".format(self.__name__,repr(self.e1),repr(self.e2))
    def next(self,env):
        val = Eval(self.e2,env)
        fun = Eval(self.e1,env)
        return Eval(fun.body,env.extendEnv(fun.sym,val))
__all__ = ["Expr",
           "BINOP",
           "SYM","NUM",
           "IF",
           "LET","DEF","FUN",
           "APP",
           "Env",
           "Eval",
       ]
