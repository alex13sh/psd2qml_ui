def func():
    print("func()")

import json    
def gen_qml_bynode(node, opt):
    print("Gen node:", json.dumps(node,indent=3))
    for nod in for_node_tree(node, reverse=True):
        print("Node name:", nod["name"])
    
def for_node_tree(node, reverse=False):
    #print("for_node")
    if not reverse: yield node
    for nod in node.get("group", []):
        yield from for_node_tree(nod,reverse)     
    if reverse: yield node
