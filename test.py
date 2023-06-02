from _ast import AST, AnnAssign, Assert, Assign, AsyncFor, AsyncFunctionDef, AsyncWith, AugAssign, ClassDef, Delete, For, FunctionDef, If, Import, Match, Raise, Return, Try, While, With
import pprint
import ast_scope
import ast
from collections import defaultdict, deque
from typing import Any, Iterator
from matplotlib import pyplot as plt
import networkx as nx

class Visit_AST(ast.NodeVisitor):
    def __init__(self):
        self.main_dict_store = list()
        self.main_dict_load = list()
        self.outside_reads = list()
        self.scope_stack = deque()
        self.reads_stack = deque()
    
    def parse_ast(self, tree: Any):
        for node in ast.walk(tree):
            ##
            # Go through and if node is x stmnt keep track of certain things according to spec
            # ast proiveds ast.iter_child_nodes(node) which could be useful I'm not sure how the
            # recursion would work because walk calls all the nodes eventually I feel like
            # at that point we might as well use visit i'm not sure how to set up recursively going through
            # everything unless we manually walk (which we might have to do actually) 
            ##
            ##
            # Or we could just ignore it walking over the nodes that aren't stmnts and then
            # rec
            if isinstance(node, ast.Name):
                # Store variables defined in cell
                if isinstance(node.ctx, ast.Store) and node.id not in self.main_dict_store:
                    self.main_dict_store.append(node.id)
                # Variable is not defined in cell, therefore reading from out of cell
                elif isinstance(node.ctx, ast.Load) and node.id not in self.main_dict_store:
                    self.outside_reads.append(node.id)


main_dict_store = list()
main_dict_load = list()
outside_reads = list()

## An example to help recursively go through things
def collect_variables(node) -> list:
    if type(node) is ast.Module:
        return [v for s in node.body for v in collect_variables(s)]
    elif type(node) is ast.FunctionDef:
        vs = [v for s in node.body for v in collect_variables(s)]
        return [node.name] + vs
    elif type(node) is ast.Assign:
            vs = [v for s in node.targets for v in collect_variables(s)]
            return vs + collect_variables(node.value)
        
    elif type(node) is ast.Return:
        return collect_variables(node.value)
    elif type(node) is ast.Name:
           # if isinstance(node.ctx, ast.Load) and node.id not in main_dict_store:
            if isinstance(node.ctx, ast.Load) :
                main_dict_load.append(node.id)
            if isinstance(node.ctx, ast.Store) :
                main_dict_store.append(node.id)
                
            return [node.id]
    elif type(node) is ast.BinOp:
            return\
                collect_variables(node.left) + collect_variables(node.right)

    else:
        print(type(node)) # Display trees not captured by cases above.
        return []  



def main():
    with open("example2.py", "r") as source:
        tree = ast.parse(source.read())


    # print(ast.dump(tree, indent=4))
    vis = Visit_AST()
    # vis.visit(tree)
    # vis.parse_ast(tree)
    print(collect_variables(tree))
    print(main_dict_load)
    print(main_dict_store)
            
        
if __name__ == '__main__':
    main()
