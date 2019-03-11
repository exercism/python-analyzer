import ast
import unittest
import analyzer

#This is only here because the indentation within the class and function definitions makes ast.parse fail
#for multi-line function definitions in string form
conditional = '''
def two_fer(name=None):
    if not name: return "One for you, one for me."
    else: return "One for %s, one for me." %name
'''

class TwoFerTest(unittest.TestCase):
    def test_malformed_input(self):
        malformed_input = ")^*()&*$@Jfjlkajsdf;"
        feedback = analyzer.analyze(malformed_input)
        self.assertTrue(analyzer.malformed_code in feedback[0])
        self.assertFalse(feedback[1])

    def test_missing_method(self):
        wrong_method_name = '''def one_fer(name="you"): return "One for %s, one for me." % name'''
        feedback = analyzer.analyze(wrong_method_name)
        self.assertTrue(analyzer.no_method in feedback[0])
        self.assertFalse(feedback[1])

    def test_has_method(self):
        correct_method_name = '''def two_fer(name="you"): return "One for %s, one for me." % name'''
        feedback = analyzer.analyze(correct_method_name)
        self.assertFalse(analyzer.no_method in feedback[0])

    def test_simple_concat(self):
        simple_concat = '''def two_fer(name="you"): return "One for " + name + ", one for me."'''
        feedback = analyzer.analyze(simple_concat)
        self.assertTrue(analyzer.simple_concat in feedback[0])

    def test_no_simple_concat(self):
        correct_style = '''def two_fer(name="you"): return "One for %s, one for me." % name'''
        feedback = analyzer.analyze(correct_style)
        self.assertFalse(analyzer.simple_concat in feedback[0])

    def test_approves_correct_solution(self):
        correct_style = '''def two_fer(name="you"): return "One for %s, one for me." % name'''
        feedback = analyzer.analyze(correct_style)
        self.assertTrue(feedback[1])
        self.assertFalse(feedback[0])

    def test_no_def_arg(self):
        no_def_arg = '''def two_fer(name): return "One for %s, one for me." % name'''
        feedback = analyzer.analyze(no_def_arg)
        self.assertTrue(analyzer.no_def_arg in feedback[0])

    def test_uses_def_args(self):
        def_arg = '''def two_fer(name="you"): return "One for %s, one for me." % name'''
        feedback = analyzer.analyze(def_arg)
        self.assertFalse(analyzer.no_def_arg in feedback[0])

    def test_uses_conditionals(self):
        feedback = analyzer.analyze(conditional)
        self.assertTrue(analyzer.conditionals in feedback[0])

    def test_no_conditionals(self):
        correct_style = '''def two_fer(name="you"): return "One for %s, one for me." % name'''
        feedback = analyzer.analyze(correct_style)
        self.assertFalse(analyzer.conditionals in feedback[0])

    def test_no_return(self):
        no_return = '''def two_fer(name="you"): print ("One for %s, one for me." % name)'''
        feedback = analyzer.analyze(no_return)
        self.assertTrue(analyzer.no_return in feedback[0])
        self.assertFalse(feedback[1])

    def test_has_return(self):
        has_return = '''def two_fer(name="you"): return "One for %s, one for me." % name'''
        feedback = analyzer.analyze(has_return)
        self.assertFalse(analyzer.no_return in feedback[0])
        self.assertTrue(feedback[1])

    def test_pylint(self):
        has_pylint = '''def two_fer(name="you"): return "One for %s, one for me." % name'''
        feedback = analyzer.analyze(has_pylint)
        self.assertFalse(not feedback[2])

    def test_wrong_def_arg(self):
        wrong_def_arg = '''def two_fer(name="them"): return "One for %s, one for me." % name'''
        feedback = analyzer.analyze(wrong_def_arg)
        self.assertTrue(analyzer.wrong_def_arg in feedback[0])

    def test_correct_def_arg(self):
        correct_def_arg = '''def two_fer(name="you"): return "One for %s, one for me." % name'''
        feedback = analyzer.analyze(correct_def_arg)
        self.assertFalse(analyzer.wrong_def_arg in feedback[0])

if __name__ == '__main__':
    unittest.main()
