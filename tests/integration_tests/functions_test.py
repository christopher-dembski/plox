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

    def test_return(self):
        source = 'fun fib(n) {' \
                 '  if (n <= 1) return n;' \
                 '  return fib(n - 2) + fib(n - 1);' \
                 '}' \
                 'for (var i = 0; i < 7; i = i + 1) {' \
                 '  print fib(i);' \
                 '}'
        fibonacci_sequence = (0, 1, 1, 2, 3, 5, 8)
        self.assert_prints(source, '\n'.join(map(str, fibonacci_sequence)))

    def test_return_no_value(self):
        source = 'fun print_a() {' \
                 '  print "a";' \
                 '  return;' \
                 '  print "b";' \
                 '}' \
                 'print_a();'
        self.assert_prints(source, "a")
