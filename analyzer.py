import ast

def analyze(user_solution):
    tree = ast.parse(user_solution)

    var_convention = "It is Python convention to name variables using underscores and all lowercase letters " \
                     "instead of camel case. This will make your code easier to read and understand for our Python " \
                     "mentors."

    #List of comments to return at end, each comment is a string
    comments = []
    for node in ast.walk(tree):
        #Find all variable names in the user's code to check for naming conventions
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            for char in node.id:
                if char.isupper(): comments += [var_convention]

        #Find all attribute names in the user's code to check for naming convetions again
        if  isinstance(node, ast.Attribute):
            for char in node.attr:
                if char.isupper() and var_convention not in comments: comments += [var_convention]

    return comments
