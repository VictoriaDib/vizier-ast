# vizier-ast
AST



## Spec of python stmt ins and outs
- FunctionDef:
     ?
- AsyncFunctionDef:
     ?
- ClassDef:
     ?
- Return:
     `Return(value) -> in(value)`
- Delete:
     `Delete(targets) -> in(targets)`
- Assign:
     `Assign(target, value) -> in(value), out(targets introduced in scope)`
- AugAssign:
     `AugAssign(target, op, value) -> in(value) U in(target)`
- AnnAssign:
     ?
- For:
     `For(raget, itr, body, orelse, type_comment) -> in(itr) U (in(body) - {target}) U in(orelse), out()`
- AsyncFor:
     `For(raget, itr, body, orelse, type_comment) -> in(itr) U (in(body) - {target}) U in(orelse), out()`
- While:
     `while(test, body, orelse) -> in(test) U in(body) U in(orselse)`
- If:
     `if(test, body, orelse) -> in(test) U in(body) U in(oresle), out()`
- With:
     `with(items, body, type_comment) -> in(items) U in(body), out(items)`
- AsyncWith:
     `AsyncWith(items, body, type_comment) -> in(items) U in(body), out(items)`
- Match:
     `Match(subject, cases) -> in(subject) U in(cases), out()`
- Raise:
     `Raise(exc,cause) -> in(cause) U in(exc), out()`
- Try:
     `Try(body, handlers, finalbody) -> in(body) U in(handlers) U in(finalbody), out(body, finalbody)`
- Assert:
     `Assert(test, msg) -> in(message), out()`
- Import:
     `Import(names) -> in(names) -> out()`




