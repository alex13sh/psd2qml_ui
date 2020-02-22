
import json    
def gen_qml_bynode(node, opt):
    res = ""
    typ = "Item" if "group" in node else "Image"
    
    txt_childs = ""
    if typ=="Item":
        for nod in node["group"]:
            txt_childs += gen_qml_bynode(nod, opt)
        txt_childs = txt_childs.replace("\n", "\n"+" "*4)
            
    txt = """
{type}{{
    id: {id}
    x: {x}; y: {y}
    width: {w}; height: {h}
{txt_childs}
}}"""
    newnode = node.copy()
    if not "type" in newnode: 
        newnode.update({"type": typ, "id": "id_"+newnode["name"], "txt_childs": txt_childs})
    res = txt.format(**newnode)
    print("\nRes:\n", res)
    return res

def gen_qml_image(node):
    res = ""
    txt = """
Image{{
    id: img_{name}
    x: {x}; y: {y}
    width: {w}; height: {h}
    source: "{source}"
}}"""
    newnode = node.copy()
    if not "type" in newnode: 
        newnode.update({"id": "id_"+newnode["name"]})
    res = txt.format(**newnode)
    return res

def gen_qml_item(node, tree=False, txt_childs=""):
    res = ""
    
    if tree:
        for nod in node.get("group",[]):
            txt_childs += gen_qml_type(nod, tree)
        txt_childs = txt_childs.replace("\n", "\n"+" "*4)
        
    txt = """
Item{{
    id: {id}
    x: {x}; y: {y}
    width: {w}; height: {h}
{txt_childs}
}}"""
    newnode = node.copy()
    if not "type" in newnode: 
        newnode.update({"id": "id_"+newnode["name"], "txt_childs": txt_childs})
    res = txt.format(**newnode)
    return res
