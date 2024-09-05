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

    def test_while(self):
        source = 'var i = 0;' \
                 'while (i < 5) {' \
                 '  print i;' \
                 '  i = i + 1;' \
                 '}'
        self.assert_prints(source, ['0', '1', '2', '3', '4'])

    def test_while_single_non_block_statement(self):
        source = 'var i = 0;' \
                 'while (i < 5)' \
                 '  i = i + 1;' \
                 'print i;'
        self.assert_prints(source, '5')

    def test_while_no_left_paren_before_condition(self):
        source = 'var i = 0;' \
                 'while i < 3)' \
                 'i = i + 1;'
        self.assert_prints_to_std_err(source)

    def test_while_no_right_paren_after_condition(self):
        source = 'var i = 0;' \
                 'while (i < 3' \
                 'i = i + 1;'
        self.assert_prints_to_std_err(source)

    def test_for(self):
        source = 'var a = 0;' \
                 'var temp;' \
                 'for (var b = 1; a < 10; b = temp + b) {' \
                 '  print a;' \
                 '  temp = a;' \
                 '  a = b;' \
                 '}'
        self.assert_prints(source, ['0', '1', '1', '2', '3', '5', '8'])

    def test_for_no_intitializer(self):
        source = 'var i = 0;' \
                 'for (; i < 3; i = i +1)' \
                 '  print i;'
        self.assert_prints(source, ['0', '1', '2'])

    def test_for_no_condition(self):
        source = 'var i = 0;' \
                 'for (; i < 5;)' \
                 '  i = i + 1;' \
                 'print i;'
        self.assert_prints(source, '5')

    def test_for_expression_statament_as_initializer(self):
        source = 'var i;' \
                 'for (i = 0; i < 3; i = i + 1)' \
                 '  print i;'
        self.assert_prints(source, ['0', '1', '2'])

    def test_for_no_left_paren_after_for_keyword(self):
        source = 'for var i = 0; i < 3; i = i + 1)' \
                 'print i;'
        self.assert_prints_to_std_err(source)

    def test_for_no_semicolon_after_condition(self):
        source = 'for (var i = 0; i < 3 i = i + 1)' \
                 'print i;'
        self.assert_prints_to_std_err(source)

    def test_for_no_right_paren_after_increment(self):
        source = 'for (var i = 0; i < 3; i = i + 1' \
                 'print i;'
        self.assert_prints_to_std_err(source)


if __name__ == '__main__':
    unittest.main()
