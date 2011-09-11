import tkinter
from tkinter import tix

class View(object):
    def __init__(self, root):
        self.root = root
        self.makeCheckList()

    def makeCheckList(self):
        self.cl = tix.CheckList(self.root, browsecmd=self.selectItem)
        self.cl.pack()
        self.cl.hlist.add("CL1", text="checklist1")
        self.cl.hlist.add("CL1.Item1", text="subitem1")
        self.cl.hlist.add("CL2", text="checklist2")
        self.cl.hlist.add("CL2.Item1", text="subitem1")
        self.cl.setstatus("CL2", "on")
        self.cl.setstatus("CL2.Item1", "on")
        self.cl.setstatus("CL1", "off")
        self.cl.setstatus("CL1.Item1", "off")
        self.cl.autosetmode()

    def selectItem(self, item):
        print(item, self.cl.getstatus(item))

def main():
    root = tix.Tk()
    view = View(root)
    root.update()
    root.mainloop()

if __name__ == '__main__':
    main()
