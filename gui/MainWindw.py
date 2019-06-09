from PyQt5.QtCore import *
#from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
 
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(640, 480)
        self.setWindowTitle("Main Window")
        self.createUI()
        
        self.FileNamePSD = None

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
        def on_pbPath():
            self.FileNamePSD=self.m_txtPath.text(); self.read_psd(); self.showLayerTree()
        self.m_pbOpen.clicked.connect(on_pbPath)
        
        lay_grid = QGridLayout()
        lay.addLayout(lay_grid)
        self.m_treeLayer = QTreeWidget()
        lay_grid.addWidget(self.m_treeLayer, 0,0)
        lay_grid.setColumnStretch(0,20)
        #lay_grid.setColumnStretch(1,80)
        
        #lay.addStretch()
        
        self.m_treeLayer.setColumnCount(2);
        self.m_treeLayer.setHeaderLabels(["Слой", "Тип"])
        self.m_treeLayer.addTopLevelItems([QTreeWidgetItem(["root", "group"])])
        #self.m_treeLayer.addTopLevelItems([QTreeWidgetItem(["LOL", "KEK", "LAL"])])
        
    def read_psd(self):
        from psd_tools import PSDImage
        self.FileNamePSD = "/home/alex97sh/Документы/Projects/Python/Download/toQML/lines_2.psd"
        psd = PSDImage.open(self.FileNamePSD)
        
        import re
        reg = re.compile('[^a-zA-Z0-9_.]')
        
        lay_tree = []
        def get_group(group, tree):
            for layer in group:
                node = {
                    "name": reg.sub('', layer.name),
                    "x": layer.left, "y": layer.top,
                    "w": layer.width, "h": layer.height,
                    #"lay": layer
                }
                if layer.is_group():node["group"]=[]; get_group(layer, node["group"])
                else:
                    pass
                tree.append(node)
        get_group(psd, lay_tree)
        print("lay_tree:", lay_tree)
        self.LayerTree = lay_tree
        
    def showLayerTree(self):
        
        def show_group(lay_group, tree_item):
            if tree_item is None: return
            for node in lay_group:
                itm = QTreeWidgetItem([node["name"], "group" if "group" in node else "img"])
                tree_item.addChild(itm)
                if "group" in node: show_group(node["group"], itm)
            
        show_group(self.LayerTree, self.m_treeLayer.topLevelItem(0))
                
