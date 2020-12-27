'''
Created on 27 dic. 2020

@author: yamil.mateo.rodriguez
'''
from subprocess import call

def ExecuteEach(listCommands):
    map(lambda x: call(x.split(" ")), listCommands)