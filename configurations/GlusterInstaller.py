# This module is in charge of making up the cluster

from subprocess import call
import yaml

#commands = yaml.load(open("./data/commands.yaml"), Loader = yaml.FullLoader)

# This function creates the disk server cluster from nas1
def NASconf(nNAS, lc):
    nasIDS = list(range(1, nNAS +1 ))
    preStr = lc.get("baseCLIforVM")[0]
    list(map(lambda x: call(preStr + " nas1 -- "+ lc.get("addServerToGluster")[0] + str(x), shell= True), nasIDS))
    call(preStr + " nas1 -- gluster volume create nas replica 3 20.20.4.2"+ str(nasIDS[0]) +":/nas/ 20.20.4.2"+str(nasIDS[1])+":/nas/ 20.20.4.2"+str(nasIDS[2])+":/nas/ force", shell = True)

# This function configures the nas from the web servers
def MountNas(nServ, lc):
    servIDS = list(range(1, nServ +1 ))
    preStr = lc.get("baseCLIforVM")[0]
    list(map(lambda x: call(preStr + " nas1 -- "+ x, shell = True), lc.get("createAndRunVolumes")))
    for i in servIDS:
        call(preStr + " s"+ str(i) + " -- " + lc.get("mountNAS")[0], shell = True)
        call(preStr + " s"+ str(i) + " -- " + lc.get("mountNAS")[1], shell = True)

#NASconf(3, commands)
#MountNas(4, commands)




