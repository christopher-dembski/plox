import unittest
from tests.test_helpers.test_case_with_helpers import TestCaseWithHelpers


class TestInterpretInvalidSingleStatement(TestCaseWithHelpers):

    # parser errors

    def test_invalid_operator(self):
        self.assert_expression_prints_to_std_err('1 << 5')

    def test_unmatched_left_parenthesis(self):
        self.assert_expression_prints_to_std_err('1 * ( 3 + 1')

    # runtime errors

    def test_invalid_type_unary_expression_negation(self):
        self.assert_expression_prints_to_std_err('-true')

    def test_invalid_type_binary_expression(self):
        self.assert_expression_prints_to_std_err('5 + "hello"')


if __name__ == '__main__':
    unittest.main()
