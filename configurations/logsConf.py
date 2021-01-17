from subprocess import call
import yaml
from lxml import etree
import xml.etree.ElementTree as ET
from xml.sax.saxutils import unescape

#commands = yaml.load(open("./data/commands.yaml"), Loader = yaml.FullLoader)

def adaptLogsServerXML(newName = "logs"):
    # Define the parser
    parser = etree.XMLParser(remove_blank_text=True)
    
    #Edit the logs.xml file 
    call("cp /mnt/tmp/pc2/s4.xml /mnt/tmp/pc2/logs.xml", shell= True)
    baseServerFile = ET.parse("/mnt/tmp/pc2/logs.xml")
    baseServerFile.getroot().attrib['name'] = 'logs'
    baseServerFile.getroot().findall('./if/ipv4')[0].text = '20.20.3.15/24'
    baseServerFile.getroot().findall('./if/ipv4')[1].text = '20.20.4.15/24'
    baseServerFile.write("/mnt/tmp/pc2/logs.xml")
    print(baseServerFile.getroot().attrib['name'])
    
    # Second adaptation
    baseServerFile = etree.parse("/mnt/tmp/pc2/logs.xml", parser)
    etree.cleanup_namespaces(baseServerFile)
    baseServerFile.write("/mnt/tmp/pc2/logs.xml", pretty_print= True)
    
    # Add server to scenario definition
    globalFile = ET.parse("/mnt/tmp/pc2/pc2.xml")
    baseServerFile = ET.parse("/mnt/tmp/pc2/logs.xml")
    globalFile.getroot().insert(14, baseServerFile.getroot())
    globalFile.write("/mnt/tmp/pc2/pc2.xml")
    globalFile2 = etree.parse("/mnt/tmp/pc2/pc2.xml", parser)
    globalFile2.write("/mnt/tmp/pc2/pc2.xml", pretty_print= True)
    pc2_str = unescape(open("/mnt/tmp/pc2/pc2.xml", "r+").read())
    a = open("/mnt/tmp/pc2/pc2.xml", "w+")
    a.write(pc2_str)
    a.close()    
    


def installLogs(cm):
    for server in ["s1","s2","s3","s4"]:
        order = cm.get("baseCLIforVM")[0] + server + " -- "
        list(map(lambda x: call(order + x, shell = True), cm.get("installRsyslog")))
        
def rsyslogServer(cm):
    #Create .conf file in rsyslog server
    order = cm.get("baseCLIforVM")[0] + " logs -- "
    call(order + "cd /etc/rsyslog.d", shell=True)
    call(order + "sudo touch 01-server.conf", shell=True)
    
    #Edit .conf file part to complete
    
    #Restart rsyslog in server
    call(order + "sudo systemctl restart rsyslog", shell=True)
    
def rsyslogClient(cm):
    #Create .conf file in rsyslog client
    order = cm.get("baseCLIforVM")[0] + " logs -- "
    call(order + "cd /etc/rsyslog.d", shell=True)
    call(order + "sudo vi 01-client.conf", shell=True)
    
    #Edit .conf file part to complete 
    
    #Restart rsyslog in client and send logs to server
    call(order + "sudo systemctl restart rsyslog", shell=True)
    call(order + "journalctl -f -u rsyslog", shell=True)
    
     