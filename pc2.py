# This script will serve as the base for the project

# Imports
from subprocess import call
import yaml
from helpers.helpers import *

# Variables
commands = yaml.load(open("data/commands.yaml"), Loader = yaml.FullLoader)

# Scenario set up
def scenarioSetUp():
    ExecuteEach(commands.get("setUpScenario"))
scenarioSetUp()