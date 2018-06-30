#coding=utf-8
import marshal
import struct
import time
import imp
import sys

def genFile(filename,code):
    magic_number = imp.get_magic()
    gen_time     = struct.pack('i',int(time.time()))
    padding      = bytes( [65,0,0,0] ) # 65 0 0 0
    #code = MainInst(code).makeCode()
    data         = marshal.dumps(code)
    with open(filename,'wb') as f:
        f.write(magic_number)
        f.write(gen_time)
        f.write(padding)
        f.write(data)
    print( 'finshed.')
