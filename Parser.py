#coding=utf-8
from vtype import *
from Lexical import *
#Lex,SpecTab,IsSeparator,IsDigit,IsLetter
from data import *
#help(Lex)
#print( Lex(SpecTab,"<> >< ") )
class ParseError(Exception): pass
def strip( tok : str ,toks : List(str) ) -> List(str) :
    #print( "strip:",tok,toks)
    if toks == [ ]:
        raise ParseError("strip error ,rest is nil \n tok: {} rest: {}".format(repr(tok),toks))
    else:
        x,xs = toks[0],toks[1:]
        if tok == x:
            return xs
        else:
            raise ParseError("strip no match tok ,{} , {}".format(repr(tok),toks))
def unpack(lst):
    assert lst != [ ] ,"unpack (nil)"
    return lst[0],lst[1:]
binops = [ "+","-","*",'/']
operators = [ "=",'(',')','=>' ] + binops
keywords = ["if","then","else","let","in","def"]
#,"val"]
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
    elif t == "let":
        sym,rest1 = parseSym( rest )
        val,rest2 = parseExpr( strip("=",rest1) )
        body,rest3 = parseExpr( strip("in",rest2) )
        return ( LET(sym,val,body),rest3 )
    elif t == "def": # def a 1
        sym,rest1 = parseSym( rest )
        val,rest2 = parseExpr( rest1 )
        return ( DEF(sym,val),rest2 )
    elif t == '(':
        val,rest1 = parseExpr( rest )
        if isinstance(val,SYM):
            sym = val.sym
            x,xs = unpack(rest1)
            if x != ')':
                e2,last = parseExpr( rest1 )
                return ( APP(val,e2),strip(')',last) )
            else:
                body,last = parseExpr ( strip('=>',strip(')',rest1)))
                return ( FUN(sym,body),last )
        else:
            x,xs = unpack(rest1)
            if x != ')':
                e2,last = parseExpr( rest1 )
                return ( APP(val,e2),strip(')',last) )
            else:
                return ( val, strip(')',rest1) )
    elif IsVariable(t):
        return ( SYM(t),rest )
    elif IsNumber(t):
        return ( NUM(int(t)),rest )
    else:
        raise ParseError ("ParseAtomError: no match {} , {}".format(repr(t),rest))
def parseExpr( toks ):
    #exp1,rest1 = parseAtom( toks )
    #return parseRest(exp1,rest1)
    exp1,rest1 = parseT( toks )
    return parseEopt(exp1,rest1)
def parseEopt( exp1,toks ):
    if toks == [ ]: 
        return (exp1,toks)
    x,xs = unpack(toks)
    if x in ['+','-','==']:
        exp2,rest = parseT(xs)
        return parseEopt( BINOP(exp1,x,exp2) , rest)
    else:
        return (exp1,toks)
def parseT( toks ):
    exp1,rest1 = parseAtom(toks) #parseAtom( toks )
    return parseTopt(exp1,rest1)
def parseTopt( exp1,toks ):
    if toks == [ ]:
        return (exp1,toks)
    x,xs = unpack(toks)
    if x in ['*','/']:#binops
        exp2,rest = parseAtom (xs)
        return parseTopt( BINOP(exp1,x,exp2) , rest)
    else:
        return (exp1,toks)

"""
E = E binops E  ; binops ['+','-','*','/']
  | Atom
Atom = Num | SYM | FUN 
------------------ |
E = T Eopt
Eopt = '+' T Eopt | '-' T Eopt
T = Atom Topt
Topt = '*' Atom Topt | '/' Atom Topt
Atom = Num ... 
"""
def parse(inp):
    return parseExpr( Lex(SpecTab,inp) )
def read(inps):
    result,rest = parse(inps)
    if rest == [ ]:
        return result
    else:
        out = implode(rest)
        raise ParseError( "readError:\nno parse all ,error in there: \n {} \n index: {}, {}".format(repr(inps),
                                                                                        len(inps) - len(out),
                                                                                        out) )
#print( isinstance(SYM("A"),SYM) )
#print( isinstance(SYM("A"),IF) )
#print( isinstance(SYM("A"),Expr) )
#c = SYM("x")
__all__ = ["read","parse"]
