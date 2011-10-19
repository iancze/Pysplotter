#!/usr/bin/env python

import tkinter
from tkinter import tix

class HListApp(object):
    def __init__(self,parent=None):
        self.frame = tix.Frame(parent)
        self.frame.pack(side=tix.TOP, fill=tix.BOTH, expand=1)
        self.shl = tix.ScrolledHList(self.frame, options='hlist.columns 3 hlist.header 1')
        self.shl.pack(side=tix.TOP, fill=tix.BOTH)
        self.hlist = self.shl.hlist

        
        style = {}
        style['header'] = tix.DisplayStyle(tix.TEXT, fg='black', refwindow=self.frame,anchor=tix.CENTER, padx=8, pady=2)
        #style['mgr_name'] = tix.DisplayStyle(tix.TEXT, refwindow=self.frame, fg='#202060', selectforeground= '#202060')

        self.hlist.config(separator='.', width=25, drawbranch=0, indent=10)
        self.hlist.column_width(0, chars=20)
        
        #self.hlist.header_create(0, itemtype=tix.TEXT, text='Name',style=style['header'])
        #self.hlist.header_create(1, itemtype=tix.TEXT, text='Position',style=style['header'])
        
        self.hlist.add('.', itemtype=tix.TEXT, data="Hello")#, style = style["mgr_name"])
        self.hlist.item_create('.', 1, itemtype=tix.TEXT, text="Ian")#, style=style["mgr_name"])
        self.hlist.add('.1', itemtype=tix.TEXT, text="Bye")#, style = style["mgr_name"])
        self.hlist.item_create('.1', 1, itemtype=tix.TEXT, text="Bob")#,

        self.button = tix.Button(self.frame, text="OK", command=self.get_item)
        self.button.pack(side=tix.BOTTOM)

    def get_item(self):
        #hlist.selection_get() is the wrong "selection"
        #Use this isntead
        selection = self.hlist.info_selection()
        print(selection)
        print(selection[0])
        print(self.hlist.info_data(selection[0]))
        print(self.hlist.info_children(selection[0]))
        print(self.hlist.entryconfigure(selection[0]))
        print(self.hlist.entrycget(selection[0],None))
        #print(self.hlist.item_cget(selection[0],col=1,option=tix.TEXT))


if __name__=="__main__":
    root = tix.Tk()
    my_app = HListApp(root)
    root.mainloop()
    