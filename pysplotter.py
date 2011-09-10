#!/usr/bin/env python
# pysplotter.py, a Python3 GUI implementation of IRAF-like splot capabilities. Name credit thanks to officemate Nathan Sanders.

import matplotlib
matplotlib.use("tkagg")
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
import sys, os
import collections

sys.path.insert(0, os.path.abspath('/home/ian/Grad/Programming/Python'))
from guimixin import GuiMixin,ScrolledList,Form
from guimaker import GuiMakerWindowMenu

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import spectrum


class Pysplotter(GuiMixin, GuiMakerWindowMenu):
    def __init__(self,parent=None):


        self.spec_list = []
        self.gridOn = False
        GuiMakerWindowMenu.__init__(self,parent)
        

    def start(self):    
        self.menuBar = [
        ('File', 0, 
            [('Load Spectrum', 0, self.loadSpec),
                ('Quit', 0, self.quit)]),
        ('Edit', 0,
            [('Cut', 0, lambda: 0),
             ('Paste', 0, lambda: 0)]),
        ('View', 0,
            [('Toggle Grid', 0, self.toggleGrid),
             ('Toggle linear/log', 0, lambda: 0),
             ('Velocity Space', 0, lambda: 0)])]
        self.toolBar = [('Quit', self.quit, {'side':tk.LEFT}),('Update', self.update, {'side':tk.LEFT})]#,('New', self.askNewWord, {'side':tk.LEFT}),('Apply', self.updateDB, {'side':tk.LEFT}),('Delete', self.deleteWord, {'side':tk.LEFT}),('Search',self.searchClicked, {'side':tk.LEFT})]

    def quit(self):
        ans = self.question("Now Leaving", "Save changes?")
        if ans:
            print("Saving Files not implemented")
            GuiMakerWindowMenu.quit(self)
        else:
            GuiMakerWindowMenu.quit(self)

    def makeWidgets(self):

        self.f = Figure() #figsize=(5,4), dpi=100)
        self.ax = self.f.add_subplot(111)

        # tk.DrawingArea
        self.canvas = FigureCanvasTkAgg(self.f, master=self)
        self.canvas.show()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        #self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
          
        self.pack(side=tk.LEFT,expand=tk.YES,fill=tk.BOTH)

    def update(self):
        print("Updated")
        self.plot = self.f.add_subplot(111)
        x = np.linspace(0,10.)
        y = x**2
        self.plot.plot(x,y)
        self.canvas.show()

    def loadSpec(self):
        spec_file_name = self.selectOpenFile()
        recent = spectrum.Spectrum(spec_file_name)
        self.spec_list.append(recent)
        self.ax.plot(recent.wls[0],recent.fls[0])
        self.canvas.show()

    def toggleGrid(self):
        if self.gridOn:
            self.ax.grid()
        else:
            self.ax.grid(which="both")
            self.canvas.show()


if __name__ == "__main__":
    '''If file run as top-level, begin constructing the GUI'''
    root = tk.Tk()
    Pysplotter(parent=root)
    root.title("Pysplotter by Ian Czekala")
    root.mainloop()
