import ast
import unittest
import os
# Import two-fer analyzer
import sys
sys.path.append('../lib/two-fer')
import analyzer

#NOTE: Comment out JSON writing and pylint generating code in analyzer before running tests

#This is only here because the indentation within the class and function definitions makes ast.parse fail
#for multi-line function definitions in string form
conditional = '''
def two_fer(name=None):
    if not name: return "One for you, one for me."
    else: return "One for %s, one for me." %name
'''

test_file = 'test.py'

def create_test_file(user_solution):
    file = open(test_file,  'w')
    file.write(user_solution)
    file.close()

class TwoFerTest(unittest.TestCase):
    def test_no_module(self):
        feedback = analyzer.analyze('non_exist_test_file.py')
        self.assertTrue(analyzer.no_module in feedback[0])
        self.assertFalse(feedback[1])

    def test_malformed_input(self):
        malformed_input = ")^*()&*$@Jfjlkajsdf;"
        create_test_file(malformed_input)
        feedback = analyzer.analyze(test_file)
        self.assertTrue(analyzer.malformed_code in feedback[0])
        self.assertFalse(feedback[1])

    def test_missing_method(self):
        wrong_method_name = '''def one_fer(name="you"): return "One for %s, one for me." % name'''
        create_test_file(wrong_method_name)
        feedback = analyzer.analyze(test_file)
        self.assertTrue(analyzer.no_method in feedback[0])
        self.assertFalse(feedback[1])

    def test_has_method(self):
        correct_method_name = '''def two_fer(name="you"): return "One for %s, one for me." % name'''
        create_test_file(correct_method_name)
        feedback = analyzer.analyze(test_file)
        self.assertFalse(analyzer.no_method in feedback[0])

    def test_simple_concat(self):
        simple_concat = '''def two_fer(name="you"): return "One for " + name + ", one for me."'''
        create_test_file(simple_concat)
        feedback = analyzer.analyze(test_file)
        self.assertTrue(analyzer.simple_concat in feedback[0])

    def test_no_simple_concat(self):
        correct_style = '''def two_fer(name="you"): return "One for %s, one for me." % name'''
        create_test_file(correct_style)
        feedback = analyzer.analyze(test_file)
        self.assertFalse(analyzer.simple_concat in feedback[0])

    def test_approves_correct_solution(self):
        correct_style = '''def two_fer(name='you'): return 'One for {}, one for me.'.format(name)'''
        create_test_file(correct_style)
        feedback = analyzer.analyze(test_file)
        self.assertTrue(feedback[1])
        self.assertFalse(feedback[0])

    def test_no_def_arg(self):
        no_def_arg = '''def two_fer(name): return "One for %s, one for me." % name'''
        create_test_file(no_def_arg)
        feedback = analyzer.analyze(test_file)
        self.assertTrue(analyzer.no_def_arg in feedback[0])

    def test_uses_def_args(self):
        def_arg = '''def two_fer(name="you"): return "One for %s, one for me." % name'''
        create_test_file(def_arg)
        feedback = analyzer.analyze(test_file)
        self.assertFalse(analyzer.no_def_arg in feedback[0])

    def test_uses_conditionals(self):
        create_test_file(conditional)
        feedback = analyzer.analyze(test_file)
        self.assertTrue(analyzer.conditionals in feedback[0])

    def test_no_conditionals(self):
        correct_style = '''def two_fer(name="you"): return "One for %s, one for me." % name'''
        create_test_file(correct_style)
        feedback = analyzer.analyze(test_file)
        self.assertFalse(analyzer.conditionals in feedback[0])

    def test_no_return(self):
        no_return = '''def two_fer(name="you"): print ("One for %s, one for me." % name)'''
        create_test_file(no_return)
        feedback = analyzer.analyze(test_file)
        self.assertTrue(analyzer.no_return in feedback[0])
        self.assertFalse(feedback[1])

    def test_has_return(self):
        has_return = '''def two_fer(name="you"): return "One for %s, one for me." % name'''
        create_test_file(has_return)
        feedback = analyzer.analyze(test_file)
        self.assertFalse(analyzer.no_return in feedback[0])
        self.assertTrue(feedback[1])

    # def test_pylint(self):
    #     has_pylint = '''def two_fer(name="you"): return "One for %s, one for me." % name'''
    #     feedback = analyzer.analyze(has_pylint)
    #     self.assertFalse(not feedback[2])

    def test_wrong_def_arg(self):
        wrong_def_arg = '''def two_fer(name="them"): return "One for %s, one for me." % name'''
        create_test_file(wrong_def_arg)
        feedback = analyzer.analyze(test_file)
        self.assertTrue(analyzer.wrong_def_arg in feedback[0])

    def test_correct_def_arg(self):
        correct_def_arg = '''def two_fer(name="you"): return "One for %s, one for me." % name'''
        create_test_file(correct_def_arg)
        feedback = analyzer.analyze(test_file)
        self.assertFalse(analyzer.wrong_def_arg in feedback[0])

    def test_uses_percent(self):
        uses_percent = '''def two_fer(name="you"): return "One for %s, one for me." % name'''
        create_test_file(uses_percent)
        feedback = analyzer.analyze(test_file)
        self.assertTrue(analyzer.percent_formatting in feedback [0])

    def test_no_percent(self):
        no_percent = '''def two_fer(name='you'): return 'One for {}, one for me.'.format(name)'''
        create_test_file(no_percent)
        feedback = analyzer.analyze(test_file)
        self.assertFalse(analyzer.percent_formatting in feedback[0])

if __name__ == '__main__':
    unittest.main()
    os.remove(test_file)
    print("remove")
