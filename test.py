from _ast import AST, AnnAssign, Assert, Assign, AsyncFor, AsyncFunctionDef, AsyncWith, AugAssign, ClassDef, Delete, For, FunctionDef, If, Import, Match, Raise, Return, Try, While, With
import ast
from collections import defaultdict, deque
from typing import Any, Iterator

class Visit_AST(ast.NodeVisitor):
    def __init__(self):
        self.main_dict_store = defaultdict(list)
        self.main_dict_load  = defaultdict(list)
        self.scope_stack = deque()
        self.reads_stack = deque()
    

    def visit_FunctionDef(self, node: FunctionDef) -> Any:
        print("Function def")

    def visit_AsyncFunctionDef(self, node: AsyncFunctionDef) -> Any:
        print("AsynchFucntionDef")

    def visit_ClassDef(self, node: ClassDef) -> Any:
        print("ClassDef")

    def visit_Return(self, node: Return) -> Any:
        # Return(value) -> in(value)
        print("Return")

    def visit_Delete(self, node: Delete) -> Any:
        # Delete(targets) -> in(targets)
        print("Delete")

    def visit_Assign(self, node: Assign) -> Any:
        # assign(target, value) -> in(value)
        print("Assign")

    def visit_AugAssign(self, node: AugAssign) -> Any:
        # AugAssign(target, op, value) -> in(value) U in(target)
        print("AugAssign")

    def visit_AnnAssign(self, node: AnnAssign) -> Any:
        print("AnnAssign")

    def visit_For(self, node: For) -> Any:
        # for(target, itr, body, orelse) -> in(itr) U (in(body) - {taraget}) U in(orselse)
        print("For")

    def visit_AsyncFor(self, node: AsyncFor) -> Any:
        print("AsynchFor")

    def visit_While(self, node: While) -> Any: # While can have an or else statement in python
        # while( test, body, orelse) -> in(test) U in(body) U in(orelse)
        print("While")

    def visit_If(self, node: If) -> Any:
        print("If")

    def visit_With(self, node: With) -> Any:
        print("With")

    def visit_AsyncWith(self, node: AsyncWith) -> Any:
        print("AsyncWith")

    def visit_Match(self, node: Match) -> Any:
        print("Match")

    def visit_Raise(self, node: Raise) -> Any:
        print("Raise")

    def visit_Try(self, node: Try) -> Any:
        print("Try")

    def visit_Assert(self, node: Assert) -> Any:
        print("Assert")

    def visit_Import(self, node: Import) -> Any:
        print("Ipmort")

def main():
    with open("example.py", "r") as source:
        tree = ast.parse(source.read())

    vis = Visit_AST()
    vis.visit(tree)
            
        
if __name__ == '__main__':
    main()