import unittest
from tests.test_helpers.test_case_with_helpers import TestCaseWithHelpers


class TestDeclarationAndAssignment(TestCaseWithHelpers):

    def test_enters_if(self):
        source = 'var a = 1;' \
                 'var b = 1;' \
                 'if (a == b) print "executed if";'
        self.assert_prints(source, 'executed if')

    def test_does_not_enter_if(self):
        source = 'var a = 1;' \
                 'var b = 2;' \
                 'if (a == b) print "executed if";' \
                 'print "end of program";'
        self.assert_prints(source, 'end of program')

    def test_if_else_enters_if(self):
        source = 'if (true) print "executed if";' \
                 'else print "executed else";'
        self.assert_prints(source, 'executed if')

    def test_if_else_enters_else(self):
        source = 'if (false) print "executed if";' \
                 'else print "executed else";'
        self.assert_prints(source, 'executed else')

    def test_if_else_with_blocks(self):
        source = 'if (true) {' \
                 '  print "executed if";' \
                 '}' \
                 'else {' \
                 '  print "executed else";' \
                 '}'
        self.assert_prints(source, 'executed if')


if __name__ == '__main__':
    unittest.main()
