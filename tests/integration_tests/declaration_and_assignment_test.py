import unittest
from tests.test_helpers.test_case_with_helpers import TestCaseWithHelpers


class TestDeclarationAndAssignment(TestCaseWithHelpers):

    def test_declaration(self):
        source = 'var a = 1;' \
                 'var b = 2;' \
                 'print a + b;'
        self.assert_prints(source, '3')

    def test_assignment(self):
        source = 'var a;' \
                 'a = 2;' \
                 'print a;'
        self.assert_prints(source, '2')

    def test_reassignment(self):
        source = 'var a = 1;' \
                 'a = 2;' \
                 'a = 3;' \
                 'print a;'
        self.assert_prints(source, '3')

    def test_assignment_as_expression(self):
        source = 'var a;' \
                 'var b;' \
                 'a = b = 5;' \
                 'print a;' \
                 'print b;'
        self.assert_prints(source, ['5', '5'])

    def test_uninitialized_variable_error(self):
        self.assert_prints_to_std_err('print a;')

    def test_left_hand_side_not_identifier(self):
        self.assert_prints_to_std_err('2 = 2;')

    def test_block_scope(self):
        source = 'var a = "global a";' \
                 'var b = "global b";' \
                 'var c = "global c";' \
                 '{' \
                 '  var a = "outer a";' \
                 '  var b = "outer b";' \
                 '  {' \
                 '    var a = "inner a";' \
                 '    print a;' \
                 '    print b;' \
                 '    print c;' \
                 '  }' \
                 '  print a;' \
                 '  print b;' \
                 '  print c;' \
                 '}' \
                 'print a;' \
                 'print b;' \
                 'print c;'
        self.assert_prints(source, [
            'inner a',
            'outer b',
            'global c',
            'outer a',
            'outer b',
            'global c',
            'global a',
            'global b',
            'global c'
        ])


if __name__ == '__main__':
    unittest.main()
