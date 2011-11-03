#!/usr/bin/env python
# pysplotter.py, a Python3 GUI implementation of IRAF-like splot capabilities. Name credit thanks to officemate Nathan Sanders.

import matplotlib
#matplotlib.use("tkagg")
#import matplotlib.pyplot as plt
import numpy as np
import sys, os
import collections

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_pysplotter

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

import spectrum
import common_lines

class Pysplotter(QMainWindow, ui_pysplotter.Ui_PysplotterDlg):
    def __init__(self,parent=None):
        super(Pysplotter, self).__init__(parent)
        self.setupUi(self)

        self.connect(self.actionOpen, SIGNAL("triggered()"), self.fileOpen)
        self.connect(self.action_Load_Spectrum, SIGNAL("triggered()"), self.fileOpen)
        self.connect(self.actionQuit, SIGNAL("triggered()"), self.close)
        self.connect(self.actionToggle_Grid, SIGNAL("triggered()"), self.toggleGrid)
        self.connect(self.actionToggle_linear_log, SIGNAL("triggered()"), self.toggleLog)

        self.canvas = self.mplwidget.canvas
        self.ax = self.canvas.ax
        x = np.linspace(0,10)
        y = x*x
        self.ax.plot(x,y)
        
        self.spec_dic = {}
        self.single_lines = common_lines.single_lines
        self.multiplets = common_lines.multiplets
        self.gridOn = False
        self.logOn = False

        self.statusbar.showMessage("Loaded")

        item = QListWidgetItem("Hello")
        item.setCheckState(2)
        self.listWidget.addItem(item)
        

    def fileOpen(self):
        print("Open File")
        



    #def loadSpec(self):
        #spec_file_name = self.selectOpenFile()
        #recent = spectrum.Spectrum(spec_file_name)
        ##Insert code here to change name of spectrum
        #recent.name = self.oneWordPopup("Name of Spectrum",recent.name)
        #self.spec_dic[recent.name] = recent
        #self.ax.plot(recent.wls[0],recent.fls[0],ls="steps-mid")
        #self.canvas.show()
        #self.spec_browser.add_spec(recent)

    def toggleGrid(self):
        if self.gridOn:
            self.ax.grid()
            self.gridOn = False
            self.statusbar.showMessage("Grid Off")
        else:
            self.ax.grid(which="both")
            self.gridOn = True
            self.statusbar.showMessage("Grid On")
        self.canvas.draw()
    
    def toggleLog(self):
        if self.logOn:
            self.ax.set_yscale('linear')
            self.logOn = False
            self.statusbar.showMessage("Linear y")
        else:
            self.ax.set_yscale('log')
            self.logOn = True
            self.statusbar.showMessage("Log y")
        self.canvas.draw()

    #def showAvailSpec(self):
        #'''Pop-up the spectrum selector'''
        #print(self.spec_browser.returnSelected())

    #def selectLine(self):
        #line_selector = LineSelector(self.single_lines)
        #line = line_selector.line
        #return line
        
    #def viewLineBrowser(self):
        #pass


#class SpecBrowser(object):
    #def __init__(self):
        #self.window = tix.Toplevel()
        #self.cl = tix.CheckList(self.window, browsecmd=self.selectItem)
        #self.cl.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
        ##Somehow just map the quit button to hide this dialog, and then get view=>showAvail to redisplay this.

    #def selectItem(self,item):
        #print(item, self.cl.getstatus(item))
        
    #def add_spec(self,spectrum):
        #'''Takes in a spectrum object and adds it to the list box'''
        #self.cl.hlist.add(spectrum.name, text=spectrum.name)
        #self.cl.setstatus(spectrum.name, "on")
        ##If the list is a multispec, then add all of the other items as subitems
        #if len(spectrum.wls) > 1:
            #for i in range(spectrum.num_spec):
                #sub_tag = spectrum.name + ".%s" % i
                #self.cl.hlist.add(sub_tag, text="%s" % i)
                #if i==0:
                    #self.cl.setstatus(sub_tag, "on")
                #else:
                    #self.cl.setstatus(sub_tag, "off")

    #def returnSelected(self):
        #return self.cl.getselection()


#class LineSelector(ScrolledList):
    #'''This is called to interface anytime the wavelength of a certain line is needed'''
    ##Modal dialog created from Lutz pg 439
    #def __init__(self,single_lines):
        #self.single_lines = single_lines
        #ScrolledList.__init__(self,[],parent=False)
        ##Create list of keys with wl
        #wl_list = []
        #for i in self.single_lines.keys():
            #wl_list.append("%s: %.0f" % (i, self.single_lines[i]))
        #self.loadList(wl_list)
        #self.window.bind('<Return>', (lambda event: self.onSubmit()))
        #self.window.grab_set()
        #self.window.focus_set()
        #self.window.wait_window()

    #def onSubmit(self):
        #self.line = self.handleList(None)
        #self.window.destroy()
        
        
#class LineLabeller(object):
    #def __init__(self,single_lines):
        ## Pass single_lines by reference since it is mutable
        #self.single_lines = single_lines
        #self.window = tix.Toplevel()
        #self.cl = tix.CheckList(self.window, browsecmd=self.selectItem)
        #self.cl.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
        #self.load_lines()
        ##Somehow just map the quit button to hide this dialog, and then get view=>showAvail to redisplay this.
        
    #def selectItem(self,item):
        #print(item, self.cl.getstatus(item))

    #def load_lines(self):
        #for i in self.single_lines:
            #self.cl.hlist.add(i, text=i)
            #self.cl.setstatus(i, "off")
        
    #def add_user_spec(self,line):
        #'''Pop up a form box for label and wavelength'''
        #pass


    #def returnSelected(self):
        #return self.cl.getselection()	


class MultipletBrowser(object):
    pass




if __name__ == "__main__":
    '''If file run as top-level, begin constructing the GUI'''
    app = QApplication(sys.argv)
    form = Pysplotter()
    form.show()
    app.exec_()
