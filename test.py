from _ast import AST, AnnAssign, Assert, Assign, AsyncFor, AsyncFunctionDef, AsyncWith, AugAssign, ClassDef, Delete, For, FunctionDef, If, Import, Match, Name, Raise, Return, Try, While, With
import ast
from collections import defaultdict, deque
from typing import Any, Iterator


class Cell_Scope:
    INSIDE  = "inside"
    OUTSIDE = "outside"
    EITHER  = "either"

class Visit_AST(ast.NodeVisitor, Cell_Scope):
    def __init__(self):
        self.main_dict_store = list()
        self.main_dict_load = list()
        self.outside_reads = list()
        self.scope_stack = deque()
        self.reads_stack = deque()

        self.scope_stack.appendleft({})
    
    def visit_FunctionDef(self, node: FunctionDef) -> Any:
        ## Add function to current stack
        self.scope_stack[0][node.name] = (self.INSIDE, []) 
        ## Add a new scope for the function vars
        self.scope_stack.appendleft({}) 
        ## Visit the body
        super().generic_visit(node)

        self.scope_stack.popleft()  

    # ?? 
    def visit_Delete(self, node: Delete) -> Any:
        for target in node.targets:
            self.generic_visit(target)

    def visit_For(self, node: For) -> Any:
        ## If it enters a new scope, make a new scope with the current node
        scope = {node.target.id: self.INSIDE}
        self.scope_stack.appendleft(scope)
        super().generic_visit(node)
        self.scope_stack.popleft()

    def visit_AsyncFor(self,node: AsyncFor) -> Any:
        scope = {node.target.id: self.INSIDE}
        self.scope_stack.appendleft(scope)
        super().generic_visit(node)
        self.scope_stack.popleft()
    
    def visit_If(self, node: If) -> Any:                          
        scope = {node.test.lineno: self.INSIDE}
        self.scope_stack.appendleft(scope)
        self.generic_visit(node.test)
        self.scope_stack.popleft()

        for i in range(len(node.body)):
            scope = {node.body[i].lineno: self.INSIDE}
            self.scope_stack.appendleft(scope)
            self.generic_visit(node.body[i])
            self.scope_stack.popleft()
        

        if node.orelse:
            for i in range(len(node.orelse)):
                scope = {node.orelse[i].lineno: self.INSIDE}
                self.scope_stack.appendleft(scope)
                self.generic_visit(node.orelse[i])
                self.scope_stack.popleft()
         
    def visit_While(self, node: While) -> Any:
        scope = {node.test.lineno: self.INSIDE}
        self.scope_stack.appendleft(scope)
        self.generic_visit(node.test)
        self.scope_stack.popleft()

        for i in range(len(node.body)):
            scope = {node.body[i].lineno: self.INSIDE}
            self.scope_stack.appendleft(scope)
            self.generic_visit(node.body[i])
            self.scope_stack.popleft()
        

        if node.orelse:
            for i in range(len(node.orelse)):
                scope = {node.orelse[i].lineno: self.INSIDE}
                self.scope_stack.appendleft(scope)
                self.generic_visit(node.orelse[i])
                self.scope_stack.popleft()

    def visit_Assign(self, node: Assign) -> Any: ## NOT DONE
        ## Since append left puts it in the front, accessing the 0th element gets top of stack
        #self.scope_stack[0][node.targets[0].id] = self.OUTSIDE # Targets could be a list so we'd have to iterate over this

        # for n in self.scope_stack[0]:
            # n.id = self.OUTSIDE
        
      
        for target in node.targets:
            if isinstance(target, ast.Tuple):
                for elt in target.elts:
                    if isinstance(elt, ast.Name):
                        self.scope_stack[0][elt.id] = self.OUTSIDE
                    

        ## If we get something in a function that is declared outside the scope of the function add it to deps
        if isinstance(node.value, ast.Name) and (node.value.id not in self.scope_stack[0]) and (node.value.id in self.scope_stack[1]):
            for name in self.scope_stack[1]:
                if isinstance(self.scope_stack[1][name], tuple):
                    self.scope_stack[1][name][1].append(node.value.id)
        super().generic_visit(node)

    def visit_AugAssign(self, node: AugAssign) -> Any:
        self.scope_stack[0][node.target.id] = self.OUTSIDE
        super().generic_visit(node)

    def visit_AnnAssign(self, node: AnnAssign) -> Any:
        self.scope_stack[0][node.target.id] = self.OUTSIDE
        super().generic_visit(node)

    # Make this into a function of some sort ?? #
    def visit_Name(self, node: Name) -> Any:
        if isinstance(node.ctx, ast.Store) :
            ## Using this because what if we're curreingly in a scope and use a var defined in another scope
            self.main_dict_store.append(node.id) 
        if isinstance(node.ctx, ast.Load) and node.id not in self.main_dict_store:
            self.outside_reads.append(node.id)


def main():
    with open("example2.py", "r") as source:
        tree = ast.parse(source.read())

    print(ast.dump(tree, indent=4))
    vis = Visit_AST()
    vis.visit(tree)
    print("Scope: ", vis.scope_stack)
    print("store: ", vis.main_dict_store)
    print("Outside Reads:  ", vis.outside_reads)

            
        
if __name__ == '__main__':
    main()
