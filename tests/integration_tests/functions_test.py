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

    def test_function_call_2(self):
        source = 'fun f(name) {' \
                 '  print name;' \
                 '}' \
                 'f("Hi");'
        self.assert_prints(source, "Hi")

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
        self.assert_prints(source, [str(n) for n in fibonacci_sequence])

    def test_return_no_value(self):
        source = 'fun print_a() {' \
                 '  print "a";' \
                 '  return;' \
                 '  print "b";' \
                 '}' \
                 'print_a();'
        self.assert_prints(source, "a")

    def test_closure(self):
        source = 'fun make_counter() {' \
                 '  var i = 0;' \
                 '  fun count() {' \
                 '    i = i + 1;' \
                 '    print i;' \
                 '  }' \
                 '  return count;' \
                 '}' \
                 'var counter = make_counter();' \
                 'counter();' \
                 'counter();'
        self.assert_prints(source, ['1', '2'])

    def test_invalid_return_from_top_level(self):
        self.assert_prints_to_std_err('return;', "Can't return from top-level code.")

    def test_read_variable_in_own_initializer(self):
        source = 'var a = outer;' \
                 '{' \
                 '  var a = a;' \
                 '}'
        self.assert_prints_to_std_err(source, "Can't read local variable in its own initializer.")
