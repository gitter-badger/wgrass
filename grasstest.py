


import sys
import Wt
import WtHttp
from Wt import *
import os
from grass_cmd import getCommands, getRasterList, getVectorList, getLayerInfo

os.environ["GISRC"] = "/home/epinux/.grass7/rc"

removable = ['r.mapcalc', 'g.gui', 'g.gui.animation',
             'g.gui.dbmgr', 'g.gui.gcp', 'g.gui.gmodeler',
             'g.gui.iclass', 'g.gui.mapswipe', 'g.gui.psmap',
             'g.gui.rlisetup', 'g.gui.timeline', 'g.gui.vdigit',
             'wxpyimgview', 'ximgview', 'g.mapsets_picker.py', 'g.parser']

gcommands = getCommands(removable=removable)


def addEntry(model, value):
    model.insertRows(model.rowCount(), 1)
    model.setData(model.rowCount()-1, 0, value)


class MyApplication(Wt.WApplication):
    def __init__(self, env):
        Wt.WApplication.__init__(self, env)
        self.setTitle("experimental")
        #
        Wt.WText("Populate a combo box with a list of available grass commands and parse the User Interface of each command, this action requires few seconds to be executed and is just an example on how to parse and capture the user interface xml description", Wt.PlainText, self.root())
        Wt.WBreak(self.root())

        container = Wt.WContainerWidget(self.root())
        #container.resize(100, 100)
        grid = Wt.WGridLayout(container)
        #for c in range(0, 22):
        #    grid.setColumnStretch(c, 0)
        #    grid.setRowStretch(c, 0)
        #grid.setHorizontalSpacing(0)
        #grid.setColumnResizable(0)
        container.setLayout(grid)

        self.cmdescbutton = Wt.WPushButton("get command list", self.root())
        grid.addWidget(self.cmdescbutton, 0, 0)

        self.cmdComboBox = WComboBox(self.root())
        grid.addWidget(self.cmdComboBox, 0, 1)

        self.printDescbutton = Wt.WPushButton("get UI description for selected command", self.root())
        grid.addWidget(self.printDescbutton, 1, 0)

        self.cmddescr = Wt.WText("", Wt.PlainText, self.root())
        self.cmddescr.setWordWrap(True)
        grid.addWidget(self.cmddescr, 2, 0)

        Wt.WText("Chose a layer type, options: Raster / Vector; and a combobox will be populated with the relative layers available in the current Location/Mapset ", Wt.XHTMLText, self.root())

        container2 = Wt.WContainerWidget(self.root())
        grid2 = Wt.WGridLayout(container2)
        container2.setLayout(grid2)
        ltype = ['raster', 'vector']
        self.layertypeComboBox = WComboBox(self.root())
        grid2.addWidget(self.layertypeComboBox, 0, 0)

        layertype = WStandardItemModel(0, 1, self)
        for i in ltype:
            addEntry(layertype, i)
            self.layertypeComboBox.setModel(layertype)

        self.getLayerListbutton = Wt.WPushButton("get layer list", self.root())
        grid2.addWidget(self.getLayerListbutton, 0, 1)

        self.getLayerListbutton.clicked().connect(self.getLayerList)
        self.cmdescbutton.clicked().connect(self.cmdesc)
        self.printDescbutton.clicked().connect(self.printDesc)

        self.layerComboBox = WComboBox(self.root())
        grid2.addWidget(self.layerComboBox, 1, 0)

        self.getLayerInfobutton = Wt.WPushButton("get layer info", self.root())
        grid2.addWidget(self.getLayerInfobutton, 1, 1)
        self.getLayerInfobutton.clicked().connect(self.getLayerInfo)

        self.layerinfo = Wt.WText("", Wt.PlainText, self.root())
        self.layerinfo.setWordWrap(True)
        grid2.addWidget(self.layerinfo, 2, 0)

        self.quitbutton = Wt.WPushButton("Quit", self.root())
        self.quitbutton.clicked().connect(self.quit)
        self.gcommands = gcommands


    def cmdesc(self):
        grasscommands = WStandardItemModel(0, 1, self)
        for i in self.gcommands.keys():
            addEntry(grasscommands, i)
        self.cmdComboBox.setModel(grasscommands)

    def printDesc(self):
        try:
            self.cmddescr.setText(self.cmdComboBox.currentText() + " description : " + str(self.gcommands[str(self.cmdComboBox.currentText())]))
        except:
            self.cmddescr.setText("No module selected")


    def getLayerInfo(self):
        try:
            info = getLayerInfo(layer=str(self.layerComboBox.currentText()), ltype=str(self.layertypeComboBox.currentText()))
            self.layerinfo.setText(info)
        except:
            self.layerinfo.setText("No layer selected")


    def getLayerList(self):
        if str(self.layertypeComboBox.currentText()) == 'raster':
            layerlist = getRasterList()
            layer = WStandardItemModel(0, 1, self)
            for i in layerlist:
                addEntry(layer, i)
            self.layerComboBox.setModel(layer)
        if str(self.layertypeComboBox.currentText()) == 'vector':
            layerlist = getVectorList()
            layer = WStandardItemModel(0, 1, self)
            for i in layerlist:
                addEntry(layer, i)
            self.layerComboBox.setModel(layer)

    def connectSignals(self, w):
        w.changed().connect(self.update)
        if isinstance(w, WLineEdit):
            w.enterPressed().connect(self.update)


def createApplication(env):
    return MyApplication(env)


if __name__ == "__main__":
    import WtHttp
    WtHttp.WRun(sys.argv, createApplication)





