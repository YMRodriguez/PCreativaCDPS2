# This module is in charge of installing MariaDB in the corresponding VM
import sys
import yaml
from xml.sax.saxutils import unescape
sys.path.insert(0, "/home/yamil.mateo.rodriguez/CDPS/PCreativaCDPS/helpers/")
#from PCreativaCDPS2.helpers.helpers import *
from subprocess import call

def ExecuteEach(listCommands, offset = ""):
    list(map(lambda x: call((offset + x), shell = True), listCommands))
    
commands = yaml.load(open("../data/commands.yaml"), Loader = yaml.FullLoader)

def dbInstaller(commands):
    stri = commands.get("baseCLIforVM")[0] + ' bbdd -- '
    ExecuteEach(commands.get("installDB"), stri)
    
#dbInstaller(commands)

def dbFullInstaller():
    cmd_line = "sudo lxc-attach --clear-env -n bbdd -- apt update"
    call (cmd_line, shell=True)
    cmd_line = "sudo lxc-attach --clear-env -n bbdd -- apt -y install mariadb-server"
    call (cmd_line, shell=True)
    cmd_line = "sudo lxc-attach --clear-env -n bbdd -- sed -i -e 's/bind-address.*/bind-address=0.0.0.0/' -e 's/utf8mb4/utf8/' /etc/mysql/mariadb.conf.d/50-server.cnf"
    call (cmd_line, shell=True)
    cmd_line = "sudo lxc-attach --clear-env -n bbdd -- systemctl restart mysql"
    call (cmd_line, shell=True)
    cmd_line = "sudo lxc-attach --clear-env -n bbdd -- mysqladmin -u root password xxxx"
    call (cmd_line, shell=True)
    cmd_line = "sudo lxc-attach --clear-env -n bbdd -- mysql -u root --password='xxxx' -e \"CREATE USER 'quiz' IDENTIFIED BY 'xxxx';\""
    call (cmd_line, shell=True)
    cmd_line = "sudo lxc-attach --clear-env -n bbdd -- mysql -u root --password='xxxx' -e \"CREATE DATABASE quiz;\""
    call (cmd_line, shell=True)
    cmd_line = "sudo lxc-attach --clear-env -n bbdd -- mysql -u root --password='xxxx' -e \"GRANT ALL PRIVILEGES ON quiz.* to 'quiz'@'localhost' IDENTIFIED by 'xxxx';\""
    call (cmd_line, shell=True)
    cmd_line = "sudo lxc-attach --clear-env -n bbdd -- mysql -u root --password='xxxx' -e \"GRANT ALL PRIVILEGES ON quiz.* to 'quiz'@'%' IDENTIFIED by 'xxxx';\""
    call (cmd_line, shell=True)
    cmd_line = "sudo lxc-attach --clear-env -n bbdd -- mysql -u root --password='xxxx' -e \"FLUSH PRIVILEGES;\""
    call (cmd_line, shell=True)
    
dbFullInstaller()



    
    