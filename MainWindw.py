from gui.MainWindw import MyWindow as MyMainWindw
from core import generator as gen
 
class MyWindow(MyMainWindw):
    def __init__(self):
        super().__init__()
        self.resize(640, 480)
        self.setWindowTitle("My Main Window")
        
        self.m_pbPrint.clicked.connect(lambda: gen.gen_qml_bynode(self.SelectedLayerNode, {}))
