from gui.MainWindw import MyWindow as MyMainWindw
from core.QmlNode import QmlNode
import os

class MyWindow(MyMainWindw):
    def __init__(self):
        super().__init__()
        self.resize(640, 480)
        self.setWindowTitle("My Main Window")
        
        def gen_file():
            qmlnode = QmlNode(node=self.SelectedLayerNode)
            qmlnode.setPath("./", "./test/")
            qmlnode.process_node()
            qmlnode.createFile()
        self.m_pbPrint.clicked.connect(gen_file)
        
        self.m_txtPath.setText("./lines_2.psd")
