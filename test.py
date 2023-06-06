from _ast import AST, AnnAssign, Assert, Assign, AsyncFor, AsyncFunctionDef, AsyncWith, AugAssign, ClassDef, Delete, For, FunctionDef, If, Import, Match, Name, Raise, Return, Try, While, With
import ast
from collections import defaultdict, deque
from typing import Any, Iterator

class Visit_AST(ast.NodeVisitor):
    def __init__(self):
        self.main_dict_store = list()
        self.main_dict_load = list()
        self.outside_reads = list()
        self.scope_stack = deque()
        self.reads_stack = deque()
    

    def visit_For(self, node) -> Any:
        scope = (node.target.id, "inside", [])
        self.scope_stack.appendleft(scope)
        super().generic_visit(node)
        self.scope_stack.pop()

    def visit_AsyncFor(self,node) -> Any:
        scope = (node.target.id, "inside", [])
        self.scope_stack.appendleft(scope)
        super().generic_visit(node)
        self.scope_stack.pop()
    
    def visit_AugAssign(self, node) -> Any:
        scope = (node.target.id, "outside", [])
        self.scope_stack.appendleft(scope)
        super().generic_visit(node)

    def visit_AnnAssign(self, node) -> Any:
        scope = (node.target.id, "outside", [])
        self.scope_stack.appendleft(scope)
        super().generic_visit(node)


def main():
    with open("example2.py", "r") as source:
        tree = ast.parse(source.read())

    print(ast.dump(tree, indent=4))
    vis = Visit_AST()
    vis.visit(tree)
    print(vis.scope_stack)

            
        
if __name__ == '__main__':
    main()
