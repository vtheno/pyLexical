from datatype import *
class Expr(metaclass=TypeMeta):pass
class SYM(Expr):
    def __init__(self,name):
        self.name = name
class IF(Expr):
    def __init__(self,e1,e2,e3):
        self.e1 = e1
        self.e2 = e2
        self.e3 = e3
def test1():
    a = SYM('a')
    b = IF(a,a,a)
    print( Expr.__subs__ )
    assert isinstance(Expr,Expr) is False
    assert isinstance(SYM,Expr) is True
    assert isinstance(IF,Expr) is True
    
    assert isinstance(SYM,IF) is False
    assert isinstance(IF,SYM) is False
    
    assert isinstance(b,IF) is True
    assert isinstance(b,SYM) is False
    
    assert isinstance(a,IF) is False
    assert isinstance(a,SYM) is True
    
    assert isinstance(a,Expr) is True
    assert isinstance(b,Expr) is True
    print( a, b)
test1()
class Nat(metaclass=TypeMeta): pass
class Zero(Nat):
    @class_prop
    def eval(cls):
        return 0

class Succ(Nat):
    def __init__(self,o):
        self.o = o
    @prop
    def eval(self):
        return 1 + self.o.eval
    def __repr__(self):
        return "{} {}".format(self.__name__,self.o)

one = Succ(Zero)
two = Succ(one)
three = Succ(Succ(Succ(Zero)))
print( Zero )
assert isinstance(Zero,Nat) is True
assert isinstance(one,Nat) is True
assert isinstance(one,Succ) is True
assert isinstance(Zero,Succ) is False
assert isinstance(one,Zero) is False
assert isinstance(Zero,Zero) is False
print( Nat.__subs__ )
print( one.eval )
print( two.eval )
print( three.eval )
print( dir(Nat) )
