import ast

#Feedback for common mistakes
no_method = "No method called two_fer."
malformed_code = "The code is malformed and cannot be parsed for analysis."
simple_concat = "String concatenation with the + operator is a valid approach, but f-strings and str.format offer more " \
                "functionality and elegant solutions."
no_def_arg = "No default arguments are used in this solution. An ideal solution should make use of a default argument " \
             "and either f-strings or str.format."
conditionals = "Conditionals are unnecessarily used in this solution. An ideal solution should make use of a default " \
               "argument and either f-strings or str.format."

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
    #Whether to approve the user's solution based on analysis. Note that this only denotes if it's POSSIBLE for the
    #user's solution to be approved; just because the user didn't submit something that automatically makes it get
    #disapproved, like an empty file or missing method header, doesn't mean it's actually correct. Final assessment
    #of the user's solution must be done by a mentor.
    approve = True
    #Does the solution have a method called two_fer?
    has_method = False
    #Does the solution correctly use a default argument?
    uses_def_arg = False

    for node in ast.walk(tree):
        #Search for method called two_fer
        if isinstance(node, ast.FunctionDef):
            if node.name == 'two_fer': has_method = True

        #Search for use of string concatenation with + operator
        if isinstance(node, ast.Add) and simple_concat not in comments: comments += [simple_concat]

        #Search for use of default arguments
        if isinstance(node, ast.arguments):
            if node.defaults: uses_def_arg = True

        #Search for use of unnecessary conditionals
        if isinstance(node, ast.If) and conditionals not in comments: comments += [conditionals]

    if not has_method:
        comments += [no_method]
        approve = False

    if not uses_def_arg:
        comments += [no_def_arg]

    return (comments, approve)
