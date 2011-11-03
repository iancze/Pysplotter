# Python Qt4 bindings for GUI objects
from PyQt4 import QtGui
# import the Qt4Agg FigureCanvas object, that binds Figure to
# Qt4Agg backend. It also inherits from QWidget
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
# Matplotlib Figure object
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
#from matplotlib.backend_bases import NavigationToolbar2
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):
    """Class to represent the FigureCanvas widget"""
    def __init__(self):
        # setup Matplotlib Figure and Axis
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        # initialization of the canvas
        FigureCanvas.__init__(self, self.fig)
        # we define the widget as expandable
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        # notify the system of updated policy
        FigureCanvas.updateGeometry(self)


class MplNavigationToolbar(NavigationToolbar):
    '''Class to represent the NavigationToolbar widget'''
    '''Temporarily unecessary until we sort things out'''
    def __init__(self,canvas,parent):
        #NavigationToolbar.__init__(self,parent,canevas)
        #self.layout = QVBoxLayout( self )
        self.canvas = canvas
        #QtGui.QWidget.__init__(self, parent)
        #self.layout.setMargin( 2 )
        #self.layout.setSpacing( 0 )
        NavigationToolbar.__init__(self, canvas, canvas)
        
    def set_message( self, s ):
        pass
                
class MplWidget(QtGui.QWidget):
    """Widget defined in Qt Designer"""
    def __init__(self, parent = None):
        # initialization of Qt MainWindow widget
        QtGui.QWidget.__init__(self, parent)
        # set the canvas to the Matplotlib widget
        self.canvas = MplCanvas()
        self.navbar = NavigationToolbar(self.canvas,self.canvas)
        # create a vertical box layout
        self.vbl = QtGui.QVBoxLayout()
        # add mpl widget to vertical box
        self.vbl.addWidget(self.canvas)
        self.vbl.addWidget(self.navbar)
        # set the layout to th vertical box
        self.setLayout(self.vbl)