'''
My solutin to two-fer
'''

# def two_fer(name='you'):
#
#     result = f"One for {name}, one for me."
#
#     return result
#
#
# def two_fer(name=None):
#     if name != None:
#         Result = f"One for {name}, one for me."
#     else:
#         Result = "One for you, one for me."
#
#     return Result
#

def two_fer(name=None):
    '''My solution to twofer on exercism.org.

    Uses a default argument of 'you'
    '''

    if name == None:
        return "One for you, one for me."
    else:
        return f"One for {name}, one for me."
#
# def placeholder_0(placeholder_1=None):
#     if placeholder_1 is not None:
#         placeholder_2 = "One for" + placeholder_1 + ", one for me."
#         #placeholder_2 = f"One for {placeholder_1}, one for me."
#     else:
#         placeholder_2 = "One for you, one for me."
#     return placeholder_2
# def two_fer(name='you'):
#     return "One for {}, one for me.".format(name)
