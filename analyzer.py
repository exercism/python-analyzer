import ast

#Feedback for common mistakes
var_convention = "It is Python convention to name variables using underscores and all lowercase letters " \
                 "instead of camel case. This will make your code easier to read and understand for our Python " \
                 "mentors."
no_method = "No method called two_fer."
malformed_code = "The code is malformed and cannot be parsed for analysis."

def analyze(user_solution):
    """
    Analyze the user's Two Fer solution to give feedback and disapprove malformed solutions.

    :return: A tuple containing a list of feedback comments as its first entry and a bool indicating whether a
        solution should be approved as its second entry.
    """

    try:
        tree = ast.parse(user_solution)
    except:
        #If ast.parse fails, the code is malformed
        return ([malformed_code], False)

    #List of comments to return at end, each comment is a string
    comments = []
    #Whether to approve the user's solution based on analysis
    approve = True
    #Does the solution have a method called two_fer?
    has_method = False

    for node in ast.walk(tree):
        #Find all variable names in the user's code to check for naming conventions
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            for char in node.id:
                if char.isupper(): comments += [var_convention]

        #Find all attribute names in the user's code to check for naming convetions again
        if isinstance(node, ast.Attribute):
            for char in node.attr:
                if char.isupper() and var_convention not in comments: comments += [var_convention]

        #Search for method called two_fer
        if isinstance(node, ast.FunctionDef):
            if node.name == 'two_fer': has_method = True

    if not has_method:
        comments += [no_method]
        approve = False

    return (comments, approve)
