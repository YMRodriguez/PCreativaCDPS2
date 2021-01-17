# This module contains the methods to install and configure the firewall virtual machine
# It allows ICMP and HTTP traffic to the LAN2 load balancer IP - 20.20.2.2/24

from subprocess import call, check_call
import yaml


#commands = yaml.load(open("./data/commands.yaml"), Loader=yaml.FullLoader)

def firewallInstallation(cm):
    preStr = cm.get("baseCLIforVM")[0]
    call( preStr + " fw -- " + cm.get("firewall")[0], shell = True)
    call("sudo /lab/cdps/bin/cp2lxc ./data/fw.fw /var/lib/lxc/fw/rootfs/etc/fw", shell = True)
    call( preStr + " fw -- " + cm.get("firewall")[1], shell = True)

#firewallInstallation(commands)