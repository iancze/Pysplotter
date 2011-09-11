import tkinter as tk
from tkinter import tix

class View(object):
    def __init__(self, root):
        self.root = root
        self.makeCheckList()

    def makeCheckList(self):
        self.cl = tix.CheckList(self.root, browsecmd=self.selectItem)
        self.button = tk.Button(self.root, text="Print Selected", command=self.printSelected)
        self.cl.pack()
        self.button.pack(fill=tk.BOTH)
        #The "text" command comes from tkDisplayStyle
        self.cl.hlist.add("CL1", text="checklist1")
        self.cl.hlist.add("CL1.Item1", text="subitem1")
        self.cl.hlist.add("CL2", text="checklist2")
        self.cl.hlist.add("CL2.Item1", text="subitem1")
        self.cl.hlist.add_child("CL2",text="Subitem2")
        self.cl.hlist.add("CL3", text="Another Item", underline=5)
        #Need to set the "on" or "off" so that they can be checked, otherwise "none" is chosen.
        self.cl.setstatus("CL2", "off")
        self.cl.setstatus("CL2.Item1", "off")
        self.cl.setstatus("CL1", "off")
        self.cl.setstatus("CL1.Item1", "off")
        #This mode comes from tixTree
        self.cl.autosetmode()

    def selectItem(self, item):
        print(item, self.cl.getstatus(item))

    def printSelected(self):
        print(self.cl.getselection())

def main():
    root = tix.Tk()
    view = View(root)
    root.update()
    root.mainloop()

if __name__ == '__main__':
    main()
