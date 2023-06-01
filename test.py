from _ast import AST, AnnAssign, Assert, Assign, AsyncFor, AsyncFunctionDef, AsyncWith, AugAssign, ClassDef, Delete, For, FunctionDef, If, Import, Match, Raise, Return, Try, While, With
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
            ##
            if isinstance(node, ast.Name):
                # Store variables defined in cell
                if isinstance(node.ctx, ast.Store) and node.id not in self.main_dict_store:
                    self.main_dict_store.append(node.id)
                # Variable is not defined in cell, therefore reading from out of cell
                elif isinstance(node.ctx, ast.Load) and node.id not in self.main_dict_store:
                    self.outside_reads.append(node.id)

def main():
    with open("example.py", "r") as source:
        tree = ast.parse(source.read())


    print(ast.dump(tree, indent=4))
    vis = Visit_AST()
    # vis.visit(tree)
    vis.parse_ast(tree)
            
        
if __name__ == '__main__':
    main()
