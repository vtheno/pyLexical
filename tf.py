#coding=utf-8
from opcode import opmap
import dis

def f():
    a = 233
    def g():
        return a 
    return g

g = f()
dis.dis(f)
print( f.__closure__,g.__closure__)
