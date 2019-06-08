from PyQt5.QtCore import *
#from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
 
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(640, 480)
        self.setWindowTitle("Main Window")
        self.createUI()

    def createUI(self):
        self.setCentralWidget(QWidget())
        lay = QVBoxLayout()
        self.centralWidget().setLayout(lay)
        
        lay_path = QHBoxLayout()
        lay.addLayout(lay_path)
        self.m_txtPath = QLineEdit()
        lay_path.addWidget(self.m_txtPath)
        self.m_pbOpen = QPushButton("Open")
        lay_path.addWidget(self.m_pbOpen)
        
        lay_grid = QGridLayout()
        lay.addLayout(lay_grid)
        self.m_treeLayer = QTreeWidget()
        lay_grid.addWidget(self.m_treeLayer, 0,0)
        lay_grid.setColumnStretch(0,20)
        #lay_grid.setColumnStretch(1,80)
        
        #lay.addStretch()
        
        self.m_treeLayer.setColumnCount(2);
        self.m_treeLayer.setHeaderLabels(["Слой", "Тип"])
        self.m_treeLayer.addTopLevelItems([QTreeWidgetItem([txt, "group"]) for txt in ["LOL", "KEK", "LAL"]])
        #self.m_treeLayer.addTopLevelItems([QTreeWidgetItem(["LOL", "KEK", "LAL"])])
