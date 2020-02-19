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
        self.LayerTree = None
        self.SelectedLayerNode = None

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
        
        self.m_editLayer = EditLayer()
        lay_grid.addWidget(self.m_editLayer, 1,0)
        def updateLayerEditor():
            self.SelectedLayerNode = self.m_editLayer.CurrentLayerNode
            self.showLayerTree()
        self.m_editLayer.updated.connect(updateLayerEditor)
        
        self.m_pbPrint = QPushButton("Print")
        self.m_pbPrint.clicked.connect(lambda: print("Print LayerTree:", self.SelectedLayerNode))
        lay_grid.addWidget(self.m_pbPrint, 2, 0)
        
        self.m_treeLayer.setHeaderLabels(["Слой", "Тип", "visible"])
        self.m_treeLayer.addTopLevelItems([QTreeWidgetItem(["root", "group", "true"])])
        self.m_treeLayer.currentItemChanged.connect(self.on_currentItemChanged)
        
    def read_psd(self):
        from psd_tools import PSDImage
        self.FileNamePSD = "./lines_2.psd"
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
                vis = "false" if "visible" in node and node["visible"]==False else "true"
                itm = QTreeWidgetItem([node["name"], "group" if "group" in node else "img", vis])
                tree_item.addChild(itm)
                if "group" in node: show_group(node["group"], itm)
        self.LayerTree.clear()
        show_group(self.LayerTree, self.m_treeLayer.topLevelItem(0))

    #def getIndexes_fromItem(itm):
    def getNames_fromItem(self, itm):
        names=[]
        while itm:
            names.insert(0,itm.text(0))
            itm = itm.parent()
        return names
    def getNode_fromNames(self, names):
        node = None
        currentGroup = self.LayerTree
        for name in names[1:]:
            for node in currentGroup:
                if node["name"] == name:
                    if "group" in node: 
                        currentGroup = node["group"]
                        break
                    else: return node
        return node
                
    def on_currentItemChanged(self, curent, prev):
        #print("on_currentItemChanged:", self.getNode_fromNames(self.getNames_fromItem(curent)))
        self.SelectedLayerNode = self.getNode_fromNames(self.getNames_fromItem(curent))
        self.m_editLayer.setLayerNode(self.SelectedLayerNode)
        
        
class EditLayer (QWidget):
    def __init__(self):
        super().__init__()
        self.createUI()
        self.CurrentLayerNode = None
       
    def createUI(self):
        lay_grid = QGridLayout()
        self.setLayout(lay_grid)
        
        lay_grid.addWidget(QLabel("Name"), 0,0)
        self.lbName = QLabel("TEXT");   lay_grid.addWidget(self.lbName, 0,1)
        lay_grid.setColumnStretch(0,20)
        lay_grid.setColumnStretch(1,40)
        
        lay_grid.addWidget(QLabel("X"), 1,0)
        self.lbX = QLabel("");   lay_grid.addWidget(self.lbX, 1,1)
        lay_grid.addWidget(QLabel("Y"), 2,0)
        self.lbY = QLabel("");   lay_grid.addWidget(self.lbY, 2,1)
        
        lay_grid.addWidget(QLabel("Width"), 1,2)
        self.lbW = QLabel("");   lay_grid.addWidget(self.lbW, 1,3)
        lay_grid.addWidget(QLabel("Height"), 2,2)
        self.lbH = QLabel("");   lay_grid.addWidget(self.lbH, 2,3)
        lay_grid.setColumnStretch(2,20)
        lay_grid.setColumnStretch(3,40)
        
        lay_grid.addWidget(QLabel("Options"), 0,4)
        self.cbVisible = QCheckBox("Visible"); lay_grid.addWidget(self.cbVisible, 1,4)
        self.cbVisible.toggled.connect(lambda vis: self.updateNode({"visible": vis}))
        
        lay_grid.setColumnStretch(4, 200)
        
    def setLayerNode(self, node):
        if node is None: return
        self.CurrentLayerNode=node
        self.lbName.setText(node["name"])
        self.lbX.setText(str(node["x"])); self.lbY.setText(str(node["y"]))
        self.lbW.setText(str(node["w"])); self.lbH.setText(str(node["h"]))
        vis = False if "visible" in node and node["visible"]==False else True
        self.cbVisible.setChecked(vis)
        
    updated = pyqtSignal()
    def updateNode(self, node_):
        if not self.CurrentLayerNode: return
        #print("Update Node:", node_)
        self.CurrentLayerNode.update(node_)
        #print("Update Node:", self.CurrentLayerNode)
        self.updated.emit()
