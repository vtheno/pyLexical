#coding=utf-8
from vtype import *
def Mem (x : str ,lst :List(Tuple(str,List(str))) ) -> bool :
    #print( "Mem(",repr(x),lst,")")
    temp = lst
    while temp:
        t,temp = temp[0],temp[1:]
        if t == x:
            #print( "Mem true")
            return True
    #print( "Mem false")
    return False
def Get( x : str, lst : List(Tuple(str,List(str))) ) -> List(str):
    result = [ ]
    temp = lst
    while temp:
        (t,c),temp = temp[0],temp[1:]
        if x == t:
            #print( "GetResult:",c)
            return c
    #print( "GetResult:",result )
    return result
def IsDigit( x :str ) -> bool:
    return "0" <= x <= "9"
def IsLetter( x : str ) -> bool:
    return "a" <= x <= "z" or "A" <= x <= "Z"
def IsLetterOrDigit( x : str ) -> bool:
    return ("a" <= x <= "z" or "A" <= x <= "Z") or "0" <= x <= "9"
def IsSeparator( x : str ) -> bool:
    # \\n \\t
    return x == " " or x == "\n" or x == "\t" 
explode = list
def implode( lst : List(str) ) -> str:
    return ''.join(lst)
def GetSymbol ( spectab , tok, lst ):
    temp = lst
    while temp:
        x,temp = temp[0],temp[1:]
        l = [x] + temp
        if Mem(x,Get(tok,spectab)):
            tok += x
        else:
            return (tok,l)
    return (tok,[ ])
def GetTail(p , buf ,lst ):
    #print( "GetTail",p,buf,lst)
    result = buf
    temp = lst
    while temp :
        x,temp = temp[0],temp[1:]
        if p(x):
            result = [x] + result
            continue
        else:
            temp = [x] + temp # fix a miss tok
            return ( ''.join(list(reversed(result))),temp )
    return ( ''.join(list(reversed(result))),temp )
class GetNextTokenErr(Exception) : pass
def GetNextToken(spectab,lst):
    #print( "GetNextToken:",lst)
    temp = lst
    if len(temp) < 1:
        raise GetNextTokenErr("{} length < 1 !".format(temp))
    elif len(temp) == 1:
        return (temp[0],[ ])
    else:
        x,l = temp[0],temp[1:]
        c,cs = l[0],l[1:]
        if IsLetter(x):
            #print( "IsLetter" )
            return GetTail (IsLetterOrDigit,[x],l)
        elif IsDigit(x):
            #print( "IsDigit")
            return GetTail (IsDigit,[x],l)
        elif Mem(c,Get(x,spectab)):
            #print( "Mem" )
            return GetSymbol( spectab,implode([x,c]),cs)
        else:
            #print( "otherwise")
            return (x,l)
def Tokenise( spectab : List(Tuple(str,List(str))) , lst : List(str) ) -> List(str) :
    temp = lst
    result = [ ]
    while temp:
        x,l1 = temp[0],temp[1:]
        l = [x] + l1
        #print( "now =>",x,temp)
        if IsSeparator(x):
            #print( "IsSeparator(x)",repr(x),temp )
            temp = l1
        else:
            t,l2 = GetNextToken(spectab,l)
            temp = l2
            result = result + [ t ]
    return result

SpecTab = [ ("=",["<",">","="]),
            (">",["<",">"]),
            ("<",["<",">"]),
            ("==",[">"])]
def Lex(spectab,inp):
    """ spectab example:
    SpecTab = [ ("=",["<",">","="]),
                (">",["<",">"]),
                ("<",["<",">"]),
                ("==",[">"]) ]
    => =< == , >< >> ,<< <> ,==>
    """
    inps = explode(inp)
    return Tokenise(spectab,inps )
#print( Mem("=",SpecTab) )
#print( Get("=",SpecTab) )
#print( IsAlpha("abc1") )
#t = ["=",">"]
#print( GetSymbol( SpecTab,"=",t) )
#print( GetTail( IsLetter,[ ],list("abcDef") ) )
#inp = "abc => def"
#x,l = inp[0],inp[1:]
#print( GetTail (lambda a: IsLetter(a) or IsDigit(a),[x],l) )
#print( Lex(inp) )
__all__ = ["Lex","Tokenise",
           "GetNextToken","GetTail","GetSymbol",
           "IsSeparator","IsDigit","IsLetter","IsLetterOrDigit",
           "explode","implode",
           "Mem","Get","SpecTab","GetNextTokenErr"]

