#coding=utf-8
from vtype import *
from Lexical import *
#Lex,SpecTab,IsSeparator,IsDigit,IsLetter
from data import *
help(Lex)
print( Lex(SpecTab,"<> >< ") )
class ParseError(Exception): pass
def strip( tok : str ,toks : List(str) ) -> List(str) :
    #print( "strip:",tok,toks)
    if toks == [ ]:
        raise ParseError("strip nil ,{}".format(toks))
    else:
        x,xs = toks[0],toks[1:]
        if tok == x:
            return xs
        else:
            raise ParseError("strip no match tok ,{} , {}".format(repr(tok),toks))
def unpack(lst):
    assert lst != [ ] ,"unpack (nil)"
    return lst[0],lst[1:]
binops = [ "+","-","*","=" ]
operators = [ ] + binops
keywords = ["if","then","else","val"]
def IsDigits( lst : List(str) ) -> bool:
    flag = True
    temp = lst
    if temp == [ ]:
        return not flag
    while temp:
        x,temp = temp[0],temp[1:]
        flag = IsDigit(x) and flag
    return flag
def IsAlpha( lst : List(str) ) -> bool :
    flag = True
    temp = lst
    if temp == [ ]:
        return not flag
    x,temp = temp[0],temp[1:]
    if IsLetter(x):
        while temp:
            x,temp = temp[0],temp[1:]
            flag = flag and ( IsDigit(x) or IsLetter(x) )
        return flag
    else:
        return False
def IsVariable( s : str ) -> bool:
    return s not in keywords and s not in operators and IsAlpha(list(s) )
def IsNumber( s : str ) -> bool:
    return IsDigits(list(s))
def parseSym( toks ):
    t,rest = unpack(toks)
    if IsVariable(t):
        return t,rest
    else:
        raise ParseError( "ParseSym: {} , {}".format(t,rest) )
def parseAtom( toks : List(str) ) -> Tuple(Tuple(str,object),List(str)) :
    t,rest = unpack(toks)
    if t == "if":
        e1,rest1 = parseExpr(rest)
        e2,rest2 = parseExpr( strip("then",rest1) )
        e3,rest3 = parseExpr( strip("else",rest2) )
        return ( IF(e1,e2,e3),rest3 )
    elif t == "val":
        sym,rest1 = parseSym( rest )
        val,rest2 = parseExpr( strip("=",rest1) )
        return ( VAL(sym,val),rest2 )
    elif IsVariable(t):
        return ( SYM(t),rest )
    elif IsNumber(t):
        return ( NUM(int(t)),rest )
    else:
        raise ParseError ("ParseAtom: {} , {}".format(t,rest))
def parseExpr( toks ):
    exp1,rest1 = parseAtom( toks )
    return parseRest(exp1,rest1)
def parseRest( exp1,toks ):
    # if xx 
    # else =>
    if toks == [ ]:
        return (exp1,toks)
    x,xs = unpack(toks)
    if x in binops:
        exp2,rest = parseAtom(xs)
        return parseRest( BINOP(exp1,x,exp2) , rest)
    else:
        return (exp1,toks)
def parse(inp):
    return parseExpr( Lex(SpecTab,inp) )
def read(inps):
    result,rest = parse(inps)
    if rest == [ ]:
        return result
    else:
        raise ParseError( "no parse all: {}".format(implode(rest)) )

"""
inp = 
if 1
then 1 + 2 + 3
else 1 - 2 - 3

out = read(inp)
print( out,"\noutput:",multStepEval(out) )
p = read( " 1 + 2 - 3 " )
print( p,"\noutput:",multStepEval(p) )
"""
from instructions import makefunc
p = read("""
if val a = 1
then val b = a + 2 
else val c = b + 3
""")
o = multStepEval(p)
print( p ,"\noutput:",o )
env = {}#{'a':True,'b':1,'c':2}
import dis
code = o.makeCode()
dis.show_code(code)
ff = makefunc(code,env)
print( ff() )
def genFile(filename,code):
    import marshal
    import struct
    import time
    import imp
    import sys
    magic_number = imp.get_magic()
    gen_time     = struct.pack('i',int(time.time()))
    padding      = bytes( [65,0,0,0] ) # 65 0 0 0
    data         = marshal.dumps(code)
    with open(filename,'wb') as f:
        f.write(magic_number)
        f.write(gen_time)
        f.write(padding)
        f.write(data)
genFile('mylang.pyc',ff.__code__)
#print( isinstance(SYM("A"),SYM) )
#print( isinstance(SYM("A"),IF) )
#print( isinstance(SYM("A"),Expr) )
#c = SYM("x")
