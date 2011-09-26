#!/usr/bin/env python
# This class is used to define a nice base structure for any reasonable, medium featured, GUI app
# Adapted from Programming Python by Mark Lutz, 4th ed. (O'Reilly). Copyright 2011 Mark Lutz, 978-0-596-15810-1

from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter.ttk import *
import collections

class GuiMixin:
    def infobox(self, title, text, *args):
        return showinfo(title, text)

    def errorbox(self, text):
        showerror("Error!", text)

    def question(self, title, text, *args):
        return askyesno(title, text)
    
    def notdone(self):
        showerror("Not Implemented", "Option not available")

    def quit(self):
        ans = self.question("Verify quit", "Are you sure you want to quit?")
        if ans:
            Frame.quit(self)

    def help(self):
        self.infobox("RTFM","Yes")

    def selectOpenFile(self, file="", dir="."):
        return askopenfilename(initialdir=dir, initialfile=file)

    def selectSaveFile(self, file="", dir="."):
        return asksaveasfilename(initialfile=file, initialdir=dir)

    def clone(self, args=()):
        new = Toplevel()
        myclass = self.__class__
        myclass(new, *args)

    def spawn(self, pycmdline, wait=False):
        pass

    def browser(self, filename):
        new = Toplevel()
        view = ScrolledText(new, file=filename)
        view.text.config(height=30, width=85)
        view.text.config(font=('courier', 10, 'normal'))
        new.title("Text Viewer")
        new.iconname("browser")

        """
        def browser(self, filename):
            new = Toplevel()
            text = ScrolledText(new, height=30, width=85)
            text.config(font=('courier', 10, 'normal'))
            text.pack(expand=YES, fill=BOTH)
            new.title("Text Viewer")
            new.iconname("browser")
            text.insert("0.0", open(filename, "r").read() )
        """

    def oneWordPopup(self,label,temp_answer):
        popup = OneWordPopup(label,temp_answer)
        return popup.answer



class Window_base(Frame):
    def __init__(self,parent=None):
        Frame.__init__(self,parent)
    pass


class ScrolledList(Frame):
    def __init__(self, options, parent=None, **listkwargs):
        Frame.__init__(self,parent)
        self.pack(expand=YES,fill=BOTH)
        self.makeWidgets(options,**listkwargs)

    def handleList(self,event):
        index = self.listbox.curselection()
        label = self.listbox.get(index)
        self.runCommand(label)

    def makeWidgets(self, options,**listkwargs):
        sbar = Scrollbar(self)
        self.listbox = Listbox(self, relief=SUNKEN, **listkwargs)
        sbar.config(command=self.listbox.yview)
        self.listbox.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        self.listbox.pack(side=LEFT, expand=YES, fill=BOTH)
        self.loadList(options)
        self.listbox.bind('<Double-1>', self.handleList)
        self.listbox.bind('<Return>', self.handleList)

    def runCommand(self, selection):
        print('You selected:', selection)

    def deleteList(self):
        self.listbox.delete(0,END)

    def loadList(self,key_list):
        key_list.sort()
        for label in key_list:
            self.listbox.insert(END, label)


entrysize = 40
class Form(Frame):
    '''Mixin form class. If using tkinter variables, then set them in a collections.OrderedDict instance that uses {"Label":variable,} '''
    def __init__(self,labels,parent=None,button=False):
        Frame.__init__(self,parent)
        #Automatically set the correct width given the labelsizes
        self.labelsize = max(len(x) for x in labels) + 2
        self.pack(expand=YES, fill=X)
        self.rows = Frame(self, relief=GROOVE)
        self.rows.pack(side=TOP, expand=YES, fill=X)
        #This variable tracks the field boxes, so that the information can be retrieved later.
        self.entries = {}
        
        if type(labels) == list:
            print("List type form")
            for label in labels:
                row = Frame(self.rows)
                row.pack(fill=X)
                Label(row, text=label, width=self.labelsize).pack(side=LEFT)
                entry = Entry(row, width=entrysize)
                entry.pack(side=RIGHT, expand=YES, fill=X)
                entry.bind('<Return>', (lambda event: self.onSubmit()))
                self.entries[label] = entry
        elif type(labels) == collections.OrderedDict:
            for label in labels.keys():
                row = Frame(self.rows)
                row.pack(fill=X)
                Label(row, text=label, width=self.labelsize).pack(side=LEFT)
                entry = Entry(row, width=entrysize,textvariable=labels[label])
                entry.pack(side=RIGHT, expand=YES, fill=X)
                self.entries[label] = entry
        else:            
            print("Unable to create labels, check input of label list or collections.OrderedDict")


        if button:
            Button(self, text='Cancel', command=self.onCancel).pack(side=RIGHT)
            Button(self, text='Submit', command=self.onSubmit).pack(side=RIGHT)

    def setValues(self,values):
        pass

    def clearForm(self):
        pass

    def onSubmit(self):
        '''override this class'''
        for key in self.entries:
            print(key, '\t=>', self.entries[key].get())

    def onCancel(self):
        Tk().quit()




class OneWordPopup(object):
    #Modal dialog created from Lutz pg 439
    def __init__(self,label,temp_answer=""):
        self.win = Toplevel()
        self.label = Label(self.win, text=label)
        self.label.pack(side=LEFT)
        self.entry = Entry(self.win)
        self.entry.pack(side=LEFT)
        self.entry.bind('<Return>', (lambda event: self.onSubmit()))
        self.entry.insert(0,temp_answer)
        self.submit_button = Button(self.win,text="Submit",command=self.onSubmit)
        self.submit_button.pack(side=LEFT)
        self.win.grab_set()
        self.win.focus_set()
        self.win.wait_window()

    def onSubmit(self):
        self.answer = self.entry.get()
        self.win.destroy()
        





if __name__=="__main__":
    
    class TestMixin(GuiMixin, Frame):
        def __init__(self, parent=None):
            Frame.__init__(self, parent)
            self.pack()
            Button(self, text='quit', command=self.quit).pack(fill=X)
            Button(self, text='help', command=self.help).pack(fill=X)
            Button(self, text='clone', command=self.clone).pack(fill=X)
            Button(self, text='OWP', command=self.pop).pack(fill=X)    

        def pop(self):
            print(self.oneWordPopup("Name","Ian"))

    
    TestMixin().mainloop()

