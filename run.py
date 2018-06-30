#coding=utf-8
from Parser import *
from data import Eval,Env
def repl():
    env = Env()
    while 1:
        inputStr = input('>> ')
        if inputStr == ':q':
            print( '(quit)')
            break
        try:
            expr = read(inputStr)
            print( '=>',Eval(expr,env) )
            print( ';;',env )
        except Exception as e:
            print( '\033[0;31;43m',e,'\033[0m' )
            continue
if __name__ == '__main__':
    repl()
