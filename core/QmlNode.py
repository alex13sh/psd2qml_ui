
class QmlNode:
    path = "./"
    
    def __init__(self, name="", node=None ):
        self._name = name
        if node: self.getfromNode(node)
    
    def getfromNode(node):
        self._name = node["name"]
        self._node = node
        self._id = "id_"+self._name;
        self._x = node["x"]; self._y = node["y"]
        self._w = node["w"]; self._h = node["h"]
        self._source = node.get("source", None)
        self._lay = node.get("lay", None)
        self._type = "Item" if "group" in node else "Image"
        self._childs = []
        for nod in node.get("group", []):
            self._childs.append(QmlNode(node=nod))
            
    @staticmethod
    def fromNode(node):
        nod = QmlNode()
        nod.getfromNode(node)
        return nod
    
    def setPath(path_app="./", path_qml="./"):
        self._path_app = path_app # Путь относительно app.py или абсолютный для создания файлов
        self._path_qml = path_qml # Путь относительно созданного qml файла или абсолютный для ссалки на изображения.
