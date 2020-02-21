def func():
    print("func()")

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
