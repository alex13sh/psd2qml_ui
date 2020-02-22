from gui.MainWindw import MyWindow as MyMainWindw
from core import generator as gen
import os

class MyWindow(MyMainWindw):
    def __init__(self):
        super().__init__()
        self.resize(640, 480)
        self.setWindowTitle("My Main Window")
        
        def gen_file():
            txt_node = process_node(self.SelectedLayerNode, "./test/")
            with open("./test.qml", "w") as f:
                f.write(txt_node)
        self.m_pbPrint.clicked.connect(gen_file)
        

def process_node(node, path="./"):
    #gen.gen_qml_bynode(self.SelectedLayerNode, {})
    #txt = gen.gen_qml_type(node, tree=True)
    
    typ = "Item" if "group" in node else "Image"
    if typ=="Item":
        txt_childs=""
        for nod in node["group"]:
            nod_path = path
            in_sep_file = False
            if "opt" in nod:
                opt = nod["opt"]
                in_sep_file = opt.get("in_sep_file", False)
                in_sep_dir = opt.get("in_sep_dir", False)
                if in_sep_dir:
                    nod_path+=nod["name"]+"/"
                    os.mkdir(nod_path) # create dir
                
            txt_node = process_node(nod, nod_path)
            if not in_sep_file: txt_childs += txt_node
            else:
                with open(nod_path+nod["name"]+".qml", "w") as f:
                    f.write(txt_node)
            
        txt_childs = txt_childs.replace("\n", "\n"+" "*4)
        res = gen.gen_qml_item(node, txt_childs=txt_childs)
        if node.get("opt", {}).get("in_sep_dir", False):
            with open(nod_path+nod["name"]+"/"+nod["name"]+".qml", "w") as f:
                    f.write(res)
    else: 
        lay = node.get("lay", None)
        if lay:
            img = lay.topil()
            node["source"] = "./"+node["name"]+".png"
            img.save(path+node["source"])
        return gen.gen_qml_image(node)
