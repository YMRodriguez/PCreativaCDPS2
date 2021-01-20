# This module is in charge of replicating the main database

from lxml import etree
import xml.etree.ElementTree as ET
from xml.sax.saxutils import unescape
import copy

commands = yaml.load(open("./data/commands.yaml"), Loader=yaml.FullLoader)

# This method creates the slave replication VM
def adaptSlaveDatabaseXML():
    # Define the parser
    parser = etree.XMLParser(remove_blank_text=True)
    # Define the files
    globalfile = ET.parse("/mnt/tmp/pc2/pc2.xml")
    
    bbdd = globalfile.find('.//*[@name="bbdd"]')
    slave = copy.deepcopy(bbdd)
    slave.set('name', 'sbbdd')
    slave.find('./if/ipv4').text = '20.20.4.32/24'
    
    globalfile.getroot().insert(14, slave)
    globalfile.write("/mnt/tmp/pc2/pc2.xml")
    globalFile2 = etree.parse("/mnt/tmp/pc2/pc2.xml", parser)
    globalFile2.write("/mnt/tmp/pc2/pc2.xml", pretty_print= True)
    pc2_str = unescape(open("/mnt/tmp/pc2/pc2.xml", "r+").read())
    a = open("/mnt/tmp/pc2/pc2.xml", "w+")
    a.write(pc2_str)
    a.close()    

# This method install MariaDB into the slave   
def installMDB():
    call("sudo lxc-attach --clear-env -n bbdd -- apt update", shell = True)
    call("sudo lxc-attach --clear-env -n bbdd -- apt -y install mariadb-server", shell = True)
    call("sudo lxc-attach --clear-env -n bbdd -- sed -i -e 's/bind-address.*/bind-address=0.0.0.0/' -e 's/utf8mb4/utf8/' /etc/mysql/mariadb.conf.d/50-server.cnf", shell = True)
    call("sudo lxc-attach --clear-env -n bbdd -- systemctl restart mysql", shell = True)

# This method is in charge of creating the master logic into bbdd original VM   
def createMaster(cm):
    preStr = cm.get("baseCLIforVM")[0]
    call("sudo /lab/cdps/bin/cp2lxc ./data/dbReplication/master/50-server.cnf /var/lib/lxc/lb/rootfs/etc/mysql/mariadb.conf.d", shell = True)
    call(preStr + " bbdd -- " + cm.get("restartMDB")[0], shell = True) 
    call("sudo lxc-attach --clear-env -n bbdd -- mysql -u root --password='xxxx' -e \"CREATE USER 'replication'@'%' IDENTIFIED BY 'xxxx';\"", shell = True)
    call("sudo lxc-attach --clear-env -n bbdd -- mysql -u root --password='xxxx' -e \"GRANT REPLICATION SLAVE ON *.* TO 'replication'@'%';\"", shell = True)
    call("sudo lxc-attach --clear-env -n bbdd -- mysql -u root --password='xxxx' -e \"FLUSH PRIVILEGES;\"", shell = True)

# This method is in charge of creating the slave logic into the slave VM
def createSlave(cm):
    preStr = cm.get("baseCLIforVM")[0]
    call("sudo /lab/cdps/bin/cp2lxc ./data/dbReplication/slave/50-server.cnf /var/lib/lxc/lb/rootfs/etc/mysql/mariadb.conf.d", shell = True)
    call(preStr + " sbbdd -- " + cm.get("restartMDB")[0], shell = True) 
    call("sudo lxc-attach --clear-env -n bbdd -- mysql -u root --password='xxxx' -e \"stop slave;\"", shell = True)
    call("sudo lxc-attach --clear-env -n bbdd -- mysql -u root --password='xxxx' -e \"CHANGE MASTER TO MASTER_HOST = '20.20.4.31', MASTER_USER = 'replication', MASTER_PASSWORD = 'xxxx', MASTER_LOG_FILE = 'mysql-bin.000001', MASTER_LOG_POS = 313;\"", shell = True)
    call("sudo lxc-attach --clear-env -n bbdd -- mysql -u root --password='xxxx' -e \"start slave;\"", shell = True)

