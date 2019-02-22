source = '''
class Foo(object):
    def setUp(self):
        self.var1 = "some value"
        self.var2 = 1
    def bar(self):
        var3 = 2
    def baz(self, var):
        var4 = var
'''

import ast

def hack(source):
    root = ast.parse(source)

    for node in ast.walk(root):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            yield node.id
        elif isinstance(node, ast.Attribute):
            yield node.attr
        elif isinstance(node, ast.FunctionDef):
            yield node.name

print(list(hack(source)))