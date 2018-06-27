#coding=utf-8
from vtype import *
from Lexical import Lex,SpecTab
help(Lex)
print( Lex(SpecTab,"<> >< ") )
class ParseError(Exception): pass
def strip( tok : str ,toks : List(str) ) -> List(str) :
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
operators = [ ]
keywords = ["if","then","else"]
def IsVariable( s : str ) -> bool:
    return s not in keywords and s not in operators
def parseAtom( toks : List(str) ) -> Tuple(Tuple(str,object),List(str)) :
    t,rest = unpack(toks)
    if IsVariable(t):
        return ( ("Sym",t),rest )
    elif t == "if":
        e1,rest1 = parseExpr(rest)
        e2,rest2 = parseExpr( strip("then",rest1) )
        e3,rest3 = parseExpr( strip("else",rest2) )
        return ( ('if',e1,e2,e3),rest3 )
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
    if x == "+":
        exp2,rest = parseExpr(xs)
        return ( ("PLUS",exp1,exp2) , rest)
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
inp = """
if a 
then b + a
else c + a
"""
print( read(inp) )

#print( isinstance(SYM("A"),SYM) )
#print( isinstance(SYM("A"),IF) )
#print( isinstance(SYM("A"),Expr) )
#c = SYM("x")
