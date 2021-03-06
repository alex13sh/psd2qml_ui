class GenerateOpt:
    in_sep_file = False # else in_cur_file
    in_sep_dir = False # else in_cur_dir
    
    # if in_sep_file and in_sep_dir
    file_in_sep_dir = True # else in_cur_dir
    file_hold_prop_pos = False # True - свойства позиции храняться в отдельном файле, иначе они указываются в файле использования.
    
    def __init__(self, node=None):
        if node:
            self.in_sep_dir = node.get("in_sep_dir", False)
            self.in_sep_file = node.get("in_sep_file", False)
  
import os
from os.path import join

class QmlNode:
    path = "./"
    opt_sep = GenerateOpt()
    def __init__(self, name="", node=None, parent=None ):
        self._name = name
        if node: self.getfromNode(node)
        #if type(parent) == QmlNode:
        self._parent = parent
        self._imports_path = []
    
    def getfromNode(self, node):
        self._name = node["name"]
        self._node = node
        self._id = "id_"+self._name;
        self._x = node["x"]; self._y = node["y"]
        self._w = node["w"]; self._h = node["h"]
        self._source = node.get("source", None)
        self._lay = node.get("lay", None)
        self.opt_sep = GenerateOpt(node.get("opt", None))
        self._visible = MyBool(node.get("visible", True))
        self._type = "Item" if "group" in node else "Image"
        self._childs = []
        for nod in node.get("group", []):
            self._childs.append(QmlNode(node=nod, parent=self))
            
    @staticmethod
    def fromNode(node):
        nod = QmlNode()
        nod.getfromNode(node)
        return nod
    
    def setPath(self, path_file="./", path_app=None):
        self._path_file = path_file # Путь относительно app.py или абсолютный для создания файлов
        self._path_app = path_app if path_app else path_file
        import os
        self._path_qml = os.path.relpath(path_app, path_file)+"/" # Путь относительно созданного qml файла или абсолютный для ссалки на изображения.
        
        try: os.mkdir(self._path_app)
        except: print("Error path:", self._path_app)
        
    def updatePath(self, opt=None):
        if opt: self.opt_sep=opt
        else: opt = self.opt_sep
        if not self._parent or not opt: return
        
        
        if opt.in_sep_dir:
            self._path_app = join(self._parent._path_app, self._name)
        else: self._path_app = self._parent._path_app
        
        if opt.in_sep_file and opt.file_in_sep_dir:
            self._path_file = self._path_app # opt.in_sep_dir
        else: self._path_file = self._parent._path_file
        
        self._path_qml = os.path.relpath(self._path_app, self._path_file)+"/"
            
        try: os.mkdir(self._path_app)
        except: pass
            
    def gen_item(self, tree=False):
        return txt_item.format(**self.__dict__)
    def gen_image(self):
        return txt_image.format(**self.__dict__)
    def gen_loader(self, source=None):
        if not source: source=join(self._path_file, self._name+".qml")
        return txt_loader_full.format(source=source, **self.__dict__)
    
    def process_node(self):
        if self._type=="Item":
            self._txt_childs=""
            self._imports_path = []
            for nod in self._childs:
                nod.updatePath()
                nod.process_node()
                if not nod.opt_sep.in_sep_file: 
                    self._txt_childs += nod._txt_node
                else:
                    nod.createFile()
                    if nod.opt_sep.in_sep_dir and nod.opt_sep.file_in_sep_dir:
                        #self._imports_path.append(nod._path_file)
                        self._txt_childs += nod.gen_loader(join(os.path.relpath(nod._path_file, self._path_file), nod._name+".qml"))
                        
            self._txt_childs = self._txt_childs.replace("\n", "\n"+" "*4)
            self._txt_node = self.gen_item()
        else: 
            self.createImageFile()
            self._txt_node = self.gen_image()
            
    def createFile(self):
        with open(join(self._path_file,self._name+".qml"), "w") as f:
            f.write("import QtQuick 2.0\n")
            for path in self._imports_path:
                f.write(f"import \"{path}\"\n")
            f.write(self._txt_node)
    def createImageFile(self):
        if self._lay:
            img = self._lay.topil()
            self._source = join(self._path_qml, self._name+".png")
            img.save(join(self._path_app, self._name+".png"))
    
txt_item = """
Item{{
    id: {_id}
    visible: {_visible}
    x: {_x}; y: {_y}
    width: {_w}; height: {_h}
{_txt_childs}
}}"""

txt_image = """
Image{{
    id: img_{_name}
    visible: {_visible}
    x: {_x}; y: {_y}
    width: {_w}; height: {_h}
    source: "{_source}"
}}"""

txt_loader_small = """
Loader{{
    source: {source}
}}
"""
txt_loader_full = """
Loader{{
    id: loader_{_name}
    visible: {_visible}
    x: {_x}; y: {_y}
    width: {_w}; height: {_h}
    source: "{source}"
}}
"""

class MyBool:
    def __init__(self, b):
        self.bool = b
    def __str__(self):
        return "true" if self.bool else "false"
    def __repr__(self):
        return f"MyBool({self.bool})"
    def __bool__(self): return self.bool
    
