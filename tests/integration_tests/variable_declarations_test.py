import unittest
from tests.test_helpers.test_case_with_helpers import TestCaseWithHelpers


class TestInterpretValidSingleStatement(TestCaseWithHelpers):
    def test_variable_declaration(self):
        source = 'var a = 1;' \
                 'var b = 2;' \
                 'print a + b;'
        self.assert_prints(source, '3')


if __name__ == '__main__':
    unittest.main()
