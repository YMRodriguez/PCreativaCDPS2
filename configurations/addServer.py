# This module is in charge of adding new servers to the front-end

from lxml import etree
import xml.etree.ElementTree as ET
from xml.sax.saxutils import unescape

def adaptNewServerXML(newName = "s4", extraServers = 0):
    # Define the parser
    parser = etree.XMLParser(remove_blank_text=True)
    # Define the files
    globalFile = ET.parse("/mnt/tmp/pc2/pc2.xml")
    baseServerFile = ET.parse("/mnt/tmp/pc2/s4.xml")
    # Clean new server xml
    baseServerFile._setroot(baseServerFile.find('/vm'))    
    # Add needed exec and filetree
    baseServerFile.getroot().append(globalFile.findall('.//*[@name="s1"]/exec')[1])
    baseServerFile.getroot().append(globalFile.findall('.//*[@name="s1"]/filetree')[0])
    baseServerFile.write("/mnt/tmp/pc2/s4.xml")
    
    # Second adaptation
    baseServerFile = etree.parse("/mnt/tmp/pc2/s4.xml", parser)
    etree.cleanup_namespaces(baseServerFile)
    baseServerFile.write("/mnt/tmp/pc2/s4.xml", pretty_print= True)
    
    # Add server to scenario definition
    baseServerFile = ET.parse("/mnt/tmp/pc2/s4.xml")
    globalFile.getroot().insert(13, baseServerFile.getroot())
    globalFile.write("/mnt/tmp/pc2/pc2.xml")
    globalFile2 = etree.parse("/mnt/tmp/pc2/pc2.xml", parser)
    globalFile2.write("/mnt/tmp/pc2/pc2.xml", pretty_print= True)
    pc2_str = unescape(open("/mnt/tmp/pc2/pc2.xml", "r+").read())
    a = open("/mnt/tmp/pc2/pc2.xml", "w+")
    a.write(pc2_str)
    a.close()    