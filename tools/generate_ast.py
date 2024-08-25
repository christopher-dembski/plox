import sys
from typing import List, TextIO
import os


def main():
    command_lines_args = sys.argv[1:]
    if command_lines_args:
        print("Usage: python generate_ast.py", file=sys.stderr)
        sys.exit(64)
    define_ast(
        "Expr",
        [
            "Binary   :: left: Expr, operator: Token, right: Expr",
            "Grouping :: expression: Expr",
            "Literal  :: value: object",
            "Unary    :: operator: Token, right: Expr",
        ]
    )


def define_ast(base_name: str, types: List[str]):
    file_path = os.path.join(os.getcwd(), base_name.lower() + '.py')
    with open(file_path, "w") as file:
        # imports
        file.write('from lox_token import Token\n')
        file.write('from abc import ABC, abstractmethod\n\n\n')
        # base class
        file.write(f'class {base_name}(ABC):\n')
        file.write('    @abstractmethod\n')
        file.write('    def accept(self, visitor):\n')
        file.write('        pass\n\n\n')
        expr_names = [type_string.split('::')[0].strip() for type_string in types]
        field_lists = [type_string.split('::')[1].strip() for type_string in types]
        # visitor abstract class
        define_visitor(file, base_name, expr_names)
        # subclasses
        for i, (expr_name, fields) in enumerate(zip(expr_names, field_lists)):
            define_type(file, base_name, expr_name, fields)
            is_last_type = i == len(types) - 1
            if not is_last_type:
                file.write('\n\n')


def define_visitor(file: TextIO, base_name: str, expr_names: List[str]):
    file.write(f'class ExprVisitor(ABC):\n')
    for i, expr_name in enumerate(expr_names):
        file.write('    @abstractmethod\n')
        file.write(f'    def visit_{expr_name.lower()}_{base_name.lower()}(self, expr):\n')
        file.write('        pass\n')
        is_last_type = i == len(expr_names) - 1
        file.write('\n\n' if is_last_type else '\n')


def define_type(file: TextIO, base_name: str, expr_name: str, fields: str):
    # class definition
    file.write(f'class {expr_name}{base_name}({base_name}):\n')
    # constructor
    file.write(f'    def __init__(self, {fields}):\n')
    fields = fields.split(', ')
    # fields
    field_names = tuple(field.split(': ')[0] for field in fields)
    for name in field_names:
        file.write(f'        self.{name} = {name}\n')
    file.write('\n')
    # accept method
    file.write('    def accept(self, visitor: ExprVisitor):\n')
    file.write(f'        return visitor.visit_{expr_name.lower()}_expr(self)\n\n')
    # __eq__ method
    file.write('    def __eq__(self, other):\n')
    file.write('        if type(self) != type(other):\n')
    file.write('            return False\n')
    # this is not very readable... but it is cool that you can have nested fstrings
    file.write(f'        return {" and ".join(f"self.{name} == other.{name}" for name in field_names)}')
    file.write('\n\n')
    # __repr__ method
    file.write('    def __repr__(self):\n')
    string_representation = f'{expr_name}{base_name}({", ".join(f"{name}={{self.{name}}}" for name in field_names)})'
    file.write(f"        return f'{string_representation}'")
    file.write('\n')


if __name__ == '__main__':
    main()
