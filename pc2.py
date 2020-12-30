# This script will serve as the base for the project

# Imports
from subprocess import call, check_call
import yaml
from helpers.helpers import *
import subprocess
from configurations.addServer import *

# Variables
commands = yaml.load(open("data/commands.yaml"), Loader = yaml.FullLoader)

# Scenario set up
def scenarioSetUp():
    list(map(lambda x: subprocess.check_call(x.split(" "), cwd='/mnt/tmp'), commands.get("setUpScenario")))
    list(map(lambda x: subprocess.check_call(x.split(" "), cwd='/mnt/tmp/pc2'), commands.get("prepareScenario")))
def runScenario():
    list(map(lambda x: subprocess.check_call(x.split(" "), cwd='/mnt/tmp/pc2'), commands.get("runScenario")))

def main():
    scenarioSetUp()
    adaptNewServerXML()
    runScenario()

main()