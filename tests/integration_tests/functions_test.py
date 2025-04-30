from tests.test_helpers.test_case_with_helpers import TestCaseWithHelpers


class TestDeclarationAndAssignment(TestCaseWithHelpers):
    def test_print_function(self):
        source = 'fun add(a, b) {' \
                 '  print a + b;' \
                 '}' \
                 'print add;'
        self.assert_prints(source, '<fn add>')

    def test_print_foreign_function(self):
        self.assert_prints('print clock;', '<foreign fn: clock>')

    def test_function_call(self):
        source = 'fun say_hi(first, last) {' \
                 '  print "Hi, " + first + " " + last + "!" ;' \
                 '}' \
                 'say_hi("Dear", "Reader");'
        self.assert_prints(source, "Hi, Dear Reader!")
