import os
import subprocess
from collections import OrderedDict
os.environ["GISRC"] = "/home/epinux/.grass7/rc"
import grass.script.core as grass
import re

removable = ['r.mapcalc', 'g.gui', 'g.gui.animation',
             'g.gui.dbmgr', 'g.gui.gcp', 'g.gui.gmodeler',
             'g.gui.iclass', 'g.gui.mapswipe', 'g.gui.psmap',
             'g.gui.rlisetup', 'g.gui.timeline', 'g.gui.vdigit',
             'wxpyimgview', 'ximgview', 'g.mapsets_picker.py', 'g.parser']

def getCommands(removable=removable):
    cmd = grass.get_commands()[0]
    for i in removable:
        cmd.remove(i)
    commands = {}
    for i in cmd:
        command = ("%s --interface-description" % i).split()
        uidescription = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]
        commands[str(i)] = uidescription
    commands = OrderedDict(sorted(commands.items(), key=lambda t: t[0]))
    return commands


def getRasterList():
    rasterlist = re.findall(r"[\w']+", re.sub(' + ', ' ', grass.read_command("g.list", type='rast').strip()))[6:]
    return rasterlist


def getVectorList():
    vectorlist = re.findall(r"[\w']+", re.sub(' +', ' ', grass.read_command("g.list", type='vect').strip()))[6:]
    return vectorlist

def getLayerInfo(layer, ltype):
    #print layer, ltype
    if ltype == "raster":
        info = grass.read_command('r.info', map=layer)
    if ltype == "vector":
        info = grass.read_command('v.info', map=layer)
    return info
