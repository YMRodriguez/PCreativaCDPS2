# This module contains all the methods to install and run the load balancer virtual machine

from subprocess import call, check_call
import subprocess
import yaml

#commands = yaml.load(open("./data/commands.yaml"), Loader=yaml.FullLoader)

# This method installs HAProxy software in lb virtual machine
def installHAProxy(cm):
    preStr = cm.get("baseCLIforVM")[0]
    list(map(lambda x: call(preStr + " lb -- " + x, shell=True), cm.get("installHAProxy")))

# This method modifies the haproxy file and adds it to lb virtual machine
def createHAProxy(nServ, cm):
    servIDS = list(range(1, nServ + 1))
    preStr = cm.get("baseCLIforVM")[0]
    weights = {"s1": 35, "s2": 25, "s3":20, "s4": 20}
    
    # For the host the statistics page is in http://20.20.2.2:8001
    file = open("./data/haproxy.cfg", "a")
    file.write("\nfrontend lb \n")
    file.write("\tbind *:80\n")
    file.write("\tmode http\n")
    file.write("\tdefault_backend webservers\n")
    file.write("\n")
    file.write("backend webservers\n")
    file.write("\tmode http\n")
    file.write("\tbalance roundrobin\n")
    file.close()
    for i in servIDS:
        file = open("./data/haproxy.cfg", "a")
        file.write("\tserver " + "s" + str(i) + " 20.20.3.1" + str(i) + ":3000 weight " + str(weights["s" + str(i)]) +" check\n")
        file.close()
    file = open("./data/haproxy.cfg", "a")
    file.write("listen stats\n")
    file.write("\tbind *:8001\n")
    file.write("\tstats enable\n")
    file.write("\tstats uri /\n")
    file.write("\tstats hide-version\n")
    file.write("\tstats auth admin:cdps\n")
    file.close()
    call("sudo /lab/cdps/bin/cp2lxc ./data/haproxy.cfg /var/lib/lxc/lb/rootfs/etc/haproxy", shell = True)
    call(preStr + " lb -- " + cm.get("restartHAProxy")[0], shell = True) 
 