import unittest
from tests.test_helpers.test_case_with_helpers import TestCaseWithHelpers


class TestClasses(TestCaseWithHelpers):

    def test_print_class(self):
        source = 'class DevonshireCream {' \
                 '  serveOn() {' \
                 '      return "Scones";' \
                 '  }' \
                 '}' \
                 'print DevonshireCream;'
        self.assert_prints(source, 'DevonshireCream')

    def test_print_instance(self):
        source = 'class Bagel {}' \
                 'var bagel = Bagel();' \
                 'print bagel;'
        self.assert_prints(source, 'Bagel instance')

    def test_call_method(self):
        source = 'class Bacon {' \
                 '  eat() {' \
                 '      print "Crunch, crunch, crunch!";' \
                 '  }' \
                 '}' \
                 'Bacon().eat();'
        self.assert_prints(source, 'Crunch, crunch, crunch!')


if __name__ == '__main__':
    unittest.main()
