def func():
    print("func()")

import json    
def gen_qml_bynode(node, opt):
    #print("Gen node:", json.dumps(node,indent=3))
    childs = []
    newnode={}
    for nod, newnod in for_node_tree_create(node,newnode, reverse=True):
        name = nod["name"]
        newnod["id"] = "id_"+name
        print("node name:", name, ", newnod:", newnod)
        
    
def for_node_tree(node, reverse=False, lvl=0):
    #print("for_node")
    if not reverse: yield node, lvl
    for nod in node.get("group", []):
        yield from for_node_tree(nod,reverse, lvl+1)     
    if reverse: yield node, lvl
    
def for_node_tree_create(node, newnode, reverse=False):
    #print("for_node")
    if not reverse: yield node, newnode
    childs = []
    for nod in node.get("group", []):
        newchild = {}; childs.append(newchild)
        yield from for_node_tree_create(nod, newchild, reverse)
    if len(childs)>0: newnode.update({"cilds:":childs})
    if reverse: yield node, newnode
