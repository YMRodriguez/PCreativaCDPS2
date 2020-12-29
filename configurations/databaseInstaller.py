# This module is in charge of installing MariaDB in the corresponding VM
import sys
import yaml

sys.path.insert(0, "/home/yamil.mateo.rodriguez/CDPS/PCreativaCDPS/helpers/")
#from PCreativaCDPS2.helpers.helpers import *
from subprocess import call

def ExecuteEach(listCommands, offset = ""):
    list(map(lambda x: call(offset + x, shell= True) , listCommands))
    
    
commands = yaml.load(open("../data/commands.yaml"), Loader = yaml.FullLoader)

def dbInstaller(commands):
    stri = commands.get("baseCLIforVM")[0] + ' bbdd -- '
    ExecuteEach(commands.get("installDB"), stri)
    
dbInstaller(commands)
    
    