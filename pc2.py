# This script will serve as the base for the project

# Imports
from subprocess import call, check_call
import yaml
from helpers.helpers import *
import subprocess
from configurations.addServer import *
from configurations.GlusterInstaller import *
from configurations.databaseInstaller import *
from configurations.firewallConf import *
from configurations.LBinstaller import *
from configurations.serverQuizConf import *
from configurations.logsConf import *
from configurations.databaseReplication import *

# Variables
commands = yaml.load(open("data/commands.yaml"), Loader = yaml.FullLoader)
nNAS=3
nServ=4
# Scenario set up
def scenarioSetUp(cm):
    list(map(lambda x: subprocess.check_call(x.split(" "), cwd='/mnt/tmp'), commands.get("setUpScenario")))
    list(map(lambda x: subprocess.check_call(x.split(" "), cwd='/mnt/tmp/pc2'), commands.get("prepareScenario")))
def runScenario(cm):
    list(map(lambda x: subprocess.check_call(x.split(" "), cwd='/mnt/tmp/pc2'), commands.get("runScenario")))

def main(cm, nNAS, nServ):
    scenarioSetUp(cm)
    adaptNewServerXML()
    adaptLogsServerXML()
    adaptSlaveDatabaseXML()
    runScenario(cm)
    NASconf(nNAS, cm)
    MountNas(nServ, cm)
    dbInstaller()
    installHAProxy(cm)
    createHAProxy(nServ, cm)
    firewallInstallation(cm)
    serverQuiz(cm)
    installLogs(cm)
    rsyslogServer(cm)
    rsyslogClient(cm)

main(commands, nNAS, nServ)
