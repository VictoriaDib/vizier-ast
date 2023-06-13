from _ast import AST, AnnAssign, Assert, Assign, AsyncFor, AsyncFunctionDef, AsyncWith, AugAssign, ClassDef, Delete, For, FunctionDef, If, Import, Match, Name, Raise, Return, Try, While, With
import ast
from collections import defaultdict, deque
from typing import Any, Iterator


class Cell_Scope:
    INSIDE = "inside"
    OUTSIDE= "outside"
    EITHER = "either"

class Visit_AST(ast.NodeVisitor, Cell_Scope):
    def __init__(self):
        self.main_dict_store = list()
        self.main_dict_load = list()
        self.outside_reads = list()
        self.scope_stack = deque()
        self.reads_stack = deque()

        self.scope_stack.appendleft({})
    
    def visit_FunctionDef(self, node: FunctionDef) -> Any:
        ## Need to deal with transitive d3eps here somehow
        return super().generic_visit(node)

    def visit_For(self, node: For) -> Any:
        ## If it enters a new scope, make a new scope with the current node
        scope = {node.target.id: (self.INSIDE, [])}
        self.scope_stack.appendleft(scope)
        super().generic_visit(node)
        self.scope_stack.popleft()

    def visit_AsyncFor(self,node: AsyncFor) -> Any:
        scope = {node.target.id: (self.INSIDE, [])}
        self.scope_stack.appendleft(scope)
        super().generic_visit(node)
        self.scope_stack.popleft()
    
    def visit_Assign(self, node: Assign) -> Any: ## NOT DONE
        ## Since append left puts it in the front, accessing the 0th element gets top o' stack
        self.scope_stack[0][node.targets[0].id] = (self.OUTSIDE, []) # Targets could be a list so we'd have to iterate over this
        super().generic_visit(node)

    def visit_AugAssign(self, node: AugAssign) -> Any:
        self.scope_stack[0][node.target.id] = (self.OUTSIDE, [])
        super().generic_visit(node)

    def visit_AnnAssign(self, node: AnnAssign) -> Any:
        self.scope_stack[0][node.target.id] = (self.OUTSIDE, [])
        super().generic_visit(node)

    def visit_Name(self, node: Name) -> Any:
        if isinstance(node.ctx, ast.Store) :
            ## Using this because what if we're curreingly in a scope and use a var defined in another scope
            self.main_dict_store.append(node.id) 
        if isinstance(node.ctx, ast.Load) and node.id not in self.main_dict_store:
            self.outside_reads.append(node.id)


def main():
    with open("example2.py", "r") as source:
        tree = ast.parse(source.read())

    # print(ast.dump(tree, indent=4))
    vis = Visit_AST()
    vis.visit(tree)
    # print("Scope: ", vis.scope_stack)
    # print("store: ", vis.main_dict_store)
    print("Outside Reads:  ", vis.outside_reads)

            
        
if __name__ == '__main__':
    main()
