#coding=utf-8
from Parser import *
from instructions import MainInst
from GenFile import *
from data import multStepEval
string = """
let a = 2 + 1
in let c = if a then a - 1 else a + 1
   in 1 +  2
"""
#p = read("""2 + 1 * 2""")
p = read(string)
# output will is 13 ,it's a mistake,
# fix dispose precedence of operator
o = multStepEval(p)
#print( p ,"\noutput:",o )
import dis
code = o.makeCode()
dis.dis(code)
#dis.show_code(code)
print( code.co_cellvars,code.co_freevars )
print( eval(code) )
genFile('mylang.pyc',MainInst(code).makeCode() )
