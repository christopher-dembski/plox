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

    def test_set_and_this_keyword(self):
        source = 'class Cake {' \
                 '  taste() {' \
                 '      var adjective = "delicious";' \
                 '      print "The " + this.flavor + " cake is " + adjective + "!";' \
                 '  }' \
                 '}' \
                 'var cake = Cake();' \
                 'cake.flavor = "German chocolate";' \
                 'cake.taste();'
        self.assert_prints(source, 'The German chocolate cake is delicious!')

    def test_invalid_this(self):
        self.assert_prints_to_std_err('print this.name;', "Can't use 'this' outside of a class.")

    def test_initializer(self):
        source = 'class Cake {' \
                 '  init(flavor) {' \
                 '      this.flavor = flavor;' \
                 '  }' \
                 '}' \
                 'var cake = Cake("Chocolate");' \
                 'print cake.flavor;'
        self.assert_prints(source, 'Chocolate')

    def test_valid_return_from_initializer(self):
        source = 'class Cake {' \
                 '  init(flavor) {' \
                 '      this.flavor = flavor;' \
                 '      return;' \
                 '      print "this is not printed";' \
                 '  }' \
                 '}' \
                 'var cake = Cake("Chocolate");' \
                 'print cake.flavor;'
        self.assert_prints(source, "Chocolate")

    def test_invalid_return_from_initializer(self):
        source = 'class Cake {' \
                 '  init(flavor) {' \
                 '      this.flavor = flavor;' \
                 '      return "piece of cake";' \
                 '  }' \
                 '}' \
                 'var cake = Cake("Chocolate");'
        self.assert_prints_to_std_err(source, "Can't return a value from an initializer.")

    def test_inheritance(self):
        source = 'class Doughnut {' \
                 '  cook() {' \
                 '      print "Fry until golden brown.";' \
                 '  }' \
                 '}' \
                 'class BostonCream < Doughnut {}' \
                 'BostonCream().cook();'
        self.assert_prints(source, "Fry until golden brown.")

    def test_invalid_inherit_form_self(self):
        self.assert_prints_to_std_err(
            "class Doughnut < Doughnut {}",
            "A class can't inherit from itself."
        )

    def test_invalid_inherit_form_not_a_class(self):
        source = 'var NotAClass = "not a class";' \
                 'class Doughnut < NotAClass {}'
        self.assert_prints_to_std_err(source, "Superclass must be a class.")

    def test_super(self):
        source = 'class Doughnut {' \
                 '  cook() {' \
                 '      print "Fry until golden brown.";' \
                 '  }' \
                 '}' \
                 'class BostonCream < Doughnut {' \
                 '  cook() {' \
                 '      super.cook();' \
                 '      print "Pipe full of custard and coat with chocolate.";' \
                 '  }' \
                 '}' \
                 'BostonCream().cook();'
        self.assert_prints(
            source,
            ["Fry until golden brown.", "Pipe full of custard and coat with chocolate."]
        )

    def test_invalid_super_with_no_superclass(self):
        source = 'class Eclair {' \
                 '  cook() {' \
                 '      super.cook();' \
                 '      print "Pipe full of creme patissiere.";' \
                 '  }' \
                 '}'
        self.assert_prints_to_std_err(
            source,
            "Can't use 'super' in a class with no superclass."
        )

    def test_invalid_super_outside_class(self):
        self.assert_prints_to_std_err(
            "super.notEvenInAClass();",
            "Can't use 'super' outside a class."
        )


if __name__ == '__main__':
    unittest.main()
