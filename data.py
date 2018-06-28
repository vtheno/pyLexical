#coding=utf-8
from datatype import *
class Expr(metaclass=TypeMeta): pass
class SYM(Expr):
    def __init__(self,sym):
        self.sym = sym
    def __repr__(self):
        return "({} {})".format(self.__name__,repr(self.sym))
class NUM(Expr):
    def __init__(self,num):
        self.num = num
    def __repr__(self):
        return "({} {})".format(self.__name__,repr(self.num))
    @prop
    def singleStepEval(self):
        return self.num
class BINOP(Expr):
    def __init__(self,l,opname,r):
        self.left = l
        self.opname = opname
        self.right = r
    def __repr__(self):
        return "({} {} {})".format(self.left,self.opname,self.right)
    @prop
    def singleStepEval(self):
        tables = {'+':lambda a,b:a+b,
                  '-':lambda a,b:a-b,
                  '*':lambda a,b:a*b,
                  '/':lambda a,b:a/b,
                  '==':lambda a,b:1 if a==b else 0,}
        if isinstance(self.left,NUM) and isinstance(self.right,NUM):
            return NUM( tables[self.opname](self.left.singleStepEval,
                                            self.right.singleStepEval) \
                        )
        elif isinstance(self.left,NUM):
            return BINOP(self.left.singleStepEval,
                         self.opname,
                         singleStepEval(self.right))
        else:
            return BINOP(singleStepEval(self.left),
                         self.opname,
                         self.right)
class IF(Expr):
    def __init__(self,e1,e2,e3):
        self.cond = e1
        self.true = e2
        self.false = e3
    def __repr__(self):
        return "({} {} {} {})".format(self.__name__,self.cond,self.true,self.false)
    @prop
    def singleStepEval(self):
        if isinstance(self.cond,NUM):
            return self.true if self.cond.num else self.false
        else: # if isinstance(self.cond,Expr):
            return IF(singleStepEval(self.cond),self.true,self.false)
def singleStepEval( expr ):
    print( "singleStepEval:",expr )
    if isinstance(expr,IF):
        return expr.singleStepEval
    elif isinstance(expr,BINOP):
        return expr.singleStepEval
    elif isinstance(expr,NUM):
        return expr.singleStepEval
    else:
        raise RuntimeError
def multStepEval( expr ):
    print( "multStepEval:",expr )
    if isinstance(expr,NUM):
        return expr
    else:
        return multStepEval( singleStepEval(expr) )
__all__ = ["Expr",
           "BINOP",
           "SYM","NUM",
           "IF",
           "singleStepEval","multStepEval"
       ]
