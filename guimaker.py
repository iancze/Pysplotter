#!/usr/bin/env python
# Class to quickly create a menu bar for an application
# Adapted from Programming Python by Mark Lutz, 4th ed. (O'Reilly). Copyright 2011 Mark Lutz, 978-0-596-15810-1

from tkinter import *

class GuiMaker(Frame):
    menuBar = []
    toolBar = []
    helpButton = True

    def __init__(self,parent=None):
        Frame.__init__(self,parent)
        self.pack(expand=YES,fill=BOTH)
        self.start()
        self.makeMenuBar()
        self.makeToolBar()
        self.makeWidgets()

    def makeMenuBar(self):
        '''make menu bar at the top (for Tk 8.0 menus see below)
        expand=no, fill=X so same width on resize'''
        menubar = Frame(self,relief=RAISED, bd=2)
        menubar.pack(side=TOP,fill=X)

        for (name, key, items) in self.menuBar:
            mbutton = Menubutton(menubar, text=name, underline=key)
            mbutton.pack(side=LEFT)
            pulldown = Menu(mbutton)
            self.addMenuItems(pulldown, items)
            mbutton.config(menu=pulldown)

        if self.helpButton:
            Button(menubar, text = "Help", cursor = "gumby", relief = FLAT, command = \
                    self.help).pack(side=RIGHT)

    def addMenuItems(self, menu, items):
        for item in items:
            if item == "separator":
                menu.add_separator({})
            elif type(item) == list:
                for num in item:
                    menu.entryconfig(num, state=DISABLED)
            elif type(item[2]) != list:
                    menu.add_command(label=item[0], #command
                                     underline=item[1], #add command
                                     command=item[2]) #cmd=callable
            else:
                pullover = Menu(menu)
                self.addMenuItems(pullover, item[2])
                menu.add_cascade(label=item[0],
                                 underline=item[1],
                                 menu=pullover)

    def makeToolBar(self):
        '''make button bar at bottom, if any
        expand=no, fill=x so same width on resize
        this could support images too'''
        if self.toolBar:
            self.toolbar = Frame(self, cursor="hand2", relief=SUNKEN, bd=2)
            self.toolbar.pack(side=BOTTOM, fill=X)
            self.tool_buttons = {}
            for (name, action, where) in self.toolBar:
                self.tool_buttons[name] = Button(self.toolbar, text=name, command=action)
                self.tool_buttons[name].pack(where)

    def makeWidgets(self):
        '''make the 'middle' part last, so menu/toolbar 
        is always on top/bottom and clipped last;
        override this default, pack middle any side;
        for grid: grid middle part in a packed frame'''
        name = Label(self,
                width=40,height=10,relief=SUNKEN,bg='white',
                text = self.__class__.__name__,
                cursor='crosshair')
        name.pack(expand=YES,fill=BOTH,side=TOP)

    def help(self):
        "override me in subclass"
        showinfo('Help','Sorry, no help for ' + self.__class__.__name__)

    def start(self):
        "override me in subclass"
        pass

#To use the regular frame menu
GuiMakerFrameMenu = GuiMaker

class GuiMakerWindowMenu(GuiMaker):
    def makeMenuBar(self):
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        for (name,key,items) in self.menuBar:
            pulldown = Menu(menubar)
            self.addMenuItems(pulldown,items)
            menubar.add_cascade(label=name,underline=key,menu=pulldown)

        if self.helpButton:
            if sys.platform[:3] == "win":
                menubar.add_command(label="Help", command=self.help)
            else:
                pulldown = Menu(menubar) #Linux needs real pull down (??)
                pulldown.add_command(label="About", command=self.help)
                menubar.add_cascade(label="Help", menu=pulldown)

#        self.file = Menu(top_menu)
#        self.file.add_command(label="Open", command=parent.selectOpenFile)
#        self.file.add_command
#        self.file.add_command(label="Quit", command=parent.quit)
#        top_menu.add_cascade(label="File", menu=self.file, underline=0)
        #self.edit(Menu(self))
        
    def empty(self):
        pass

if __name__=="__main__":
    from guimixin import GuiMixin


#    class TestAppFrameMenu(GuiMixin, GuiMakerFrameMenu):
#        def start(self):
#            self.menuBar = menuBar
#            self.toolBar = toolBar
#
#    class TestAppWindowMenu(GuiMixin, GuiMakerWindowMenu):
#        def start(self):
#            self.menuBar = menuBar
#            self.toolBar = toolBar

    class TestAppWindowMenuBasic(GuiMixin,GuiMakerWindowMenu):
        def start(self):    
            self.menuBar = [
            ('File', 0, 
                [('Open', 0, self.selectOpenFile),
                    ('Quit', 0, self.quit)]),
            ('Edit', 0,
                [('Cut', 0, lambda: 0),
                 ('Paste', 0, lambda: 0)]) ]

            self.toolBar = [('Quit', self.quit, {'side':LEFT})]

    root = Tk()
#    TestAppFrameMenu(Toplevel())
#    TestAppWindowMenu(Toplevel())
    TestAppWindowMenuBasic(root)
    root.mainloop()