import unittest
from tests.test_helpers.test_case_with_helpers import TestCaseWithHelpers


class TestClasses(TestCaseWithHelpers):

    def test_enters_if(self):
        source = 'class DevonshireCream {' \
                 '  serveOn() {' \
                 '      return "Scones";' \
                 '  }' \
                 '}' \
                 'print DevonshireCream;'
        self.assert_prints(source, 'DevonshireCream')


if __name__ == '__main__':
    unittest.main()
