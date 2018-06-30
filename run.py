#coding=utf-8
from Parser import *
from data import multStepEval,emptyEnv
def repl():
    env = emptyEnv
    while 1:
        inputStr = input('>> ')
        if inputStr == ':q':
            print( '(quit)')
            break
        try:
            expr = read(inputStr)
            print( '=>',multStepEval(expr,env) )
            print( ';;',env )
        except Exception as e:
            print( '\033[0;31;43m',e,'\033[0m' )
            continue
if __name__ == '__main__':
    repl()
