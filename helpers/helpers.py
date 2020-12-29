'''
Created on 27 dic. 2020

@author: yamil.mateo.rodriguez
'''
from subprocess import call

def ExecuteEach( listCommands, offset = ""):
    list(map(lambda x: call((offset + x ).split(" ")), listCommands))
    