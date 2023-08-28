import sys as system
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QAction, QToolBar, QLineEdit, QVBoxLayout, QWidget, \
    QDialog, QDialogButtonBox

import matplotlib
from matplotlib import pyplot as plt

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Potential Fractals")
        self.resize(1000, 1000)

        #TODO Auslagern: CanvasBuilder
        widget = QWidget()
        layout = QVBoxLayout()

        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        toolbar = NavigationToolbar(self.sc, self)

        layout.addWidget(toolbar)
        layout.addWidget(self.sc)

        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self._createActions()
        self._createMenubar()
        self._createToolbars()
        self._connectActions()

        self.show()

    def run(self):
        size = int(self.canvasSizeTextLine.text())
        data = np.random.random((size, size, 1))
        self.sc.axes.set_xlim(0, size, auto=True)
        self.sc.axes.set_ylim(0, size, auto=True)
        self.sc.axes.cla()
        self.sc.axes.imshow(data, cmap='Greens', interpolation='nearest', origin='lower')
        self.sc.draw()

    def drawMass(self, mass, x, y):
        self.sc.axes.scatter(x, y)

    def save(self):
        plt.savefig("plot.png")

    def createMass(self):
        dlg = MassDialog(self)
        dlg.exec()

    def _connectActions(self):
        self.runAction.triggered.connect(self.run)
        self.exitAction.triggered.connect(self.close)
        self.saveAction.triggered.connect(self.save)
        self.createMassAction.triggered.connect(self.createMass)

    def _createActions(self):
        # Creating actions using the second constructor
        self.newAction = QAction("&New", self)
        self.openAction = QAction("&Open...", self)
        self.saveAction = QAction("&Save", self)
        self.exitAction = QAction("&Exit", self)
        self.copyAction = QAction("&Copy", self)
        self.pasteAction = QAction("&Paste", self)
        self.cutAction = QAction("&Cut", self)
        self.helpContentAction = QAction("&Help Content", self)
        self.aboutAction = QAction("&About", self)
        self.runAction = QAction("&Run", self)
        self.createMassAction = QAction("&Create Mass")
        self.potential1r = QAction("1/r potential", self)
        self.potential2r = QAction("1/r^2 potential", self)
        self.potentialx = QAction("1/x potential", self)
        self.potentialy = QAction("1/y potential", self)

    def _createMenubar(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&File")
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.exitAction)

        editMenu = menuBar.addMenu("&Edit")
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addAction(self.cutAction)

        helpMenu = menuBar.addMenu("&Help")
        helpMenu.addAction(self.helpContentAction)
        helpMenu.addAction(self.aboutAction)

    #TODO Unterteilen in Methode für horizontale und vertikale
    def _createToolbars(self):

        #TODO Naming
        runToolBar = QToolBar("Run", self)
        self.addToolBar(Qt.TopToolBarArea, runToolBar)

        runToolBar.addAction(self.runAction)
        runToolBar.addAction(self.saveAction)
        runToolBar.addAction(self.createMassAction)

        #TODO Extrahieren in Methode (Maybe in Layout zum Canvas verschieben)
        self.simEndTimeTextLabel = QLabel()
        self.simEndTimeTextLabel.setText("Time to simulate : ")
        self.simEndTimeTextLine = QLineEdit()
        self.simEndTimeTextLine.setFixedWidth(50)
        self.simEndTimeTextLine.setText("1000")

        self.simDeltaTimeTextLabel = QLabel()
        self.simDeltaTimeTextLabel.setText(" Time between simulation steps : ")
        self.simDeltaTimeTextLine = QLineEdit()
        self.simDeltaTimeTextLine.setFixedWidth(30)
        self.simDeltaTimeTextLine.setText("10")

        self.canvasSizeTextLabel = QLabel()
        self.canvasSizeTextLabel.setText(" Sidelength of Canvas : ")
        self.canvasSizeTextLine = QLineEdit()
        self.canvasSizeTextLine.setFixedWidth(30)
        self.canvasSizeTextLine.setText("10")

        self.canvasScaleTextLabel = QLabel()
        self.canvasScaleTextLabel.setText(" ratio of distance to pixelsize")
        self.canvasScaleTextLine = QLineEdit()
        self.canvasScaleTextLine.setFixedWidth(20)
        self.canvasScaleTextLine.setText("1")

        runToolBar.addWidget(self.simEndTimeTextLabel)
        runToolBar.addWidget(self.simEndTimeTextLine)
        runToolBar.addWidget(self.simDeltaTimeTextLabel)
        runToolBar.addWidget(self.simDeltaTimeTextLine)
        runToolBar.addWidget(self.canvasSizeTextLabel)
        runToolBar.addWidget(self.canvasSizeTextLine)
        runToolBar.addWidget(self.canvasScaleTextLabel)
        runToolBar.addWidget(self.canvasScaleTextLine)

        potentialToolBar = QToolBar("Potentials", self)
        potentialToolBar.addAction(self.potential1r)
        potentialToolBar.addAction(self.potential2r)
        potentialToolBar.addAction(self.potentialx)
        potentialToolBar.addAction(self.potentialy)
        self.addToolBar(Qt.LeftToolBarArea, potentialToolBar)


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot()
        super(MplCanvas, self).__init__(fig)


#TODO Auslagern in eigene Klasse/Methode
class MassDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("specify mass attributes")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.massLabel = QLabel("mass: ")
        self.xLabel = QLabel("x-coord: ")
        self.yLabel = QLabel("y-coord: ")
        self.massLine = QLineEdit()
        self.xLine = QLineEdit()
        self.yLine = QLineEdit()
        self.layout.addWidget(self.massLabel)
        self.layout.addWidget(self.massLine)
        self.layout.addWidget(self.xLabel)
        self.layout.addWidget(self.xLine)
        self.layout.addWidget(self.yLabel)
        self.layout.addWidget(self.yLine)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def accept(self):
        mass = self.massLine.text()
        x = self.xLine.text()
        y = self.yLine.text()
        # create body instance and draw


def createWindow() -> Window:
    app = QApplication(system.argv)
    window = Window()
    app.exec_()

    return window
