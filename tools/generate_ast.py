import sys
from typing import List, TextIO
import os


def main():
    command_lines_args = sys.argv[1:]
    if len(command_lines_args) != 1:
        print("Usage: python generate_ast.py [output_directory]", file=sys.stderr)
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
    file_path = os.path.join(os.getcwd(), base_name + '.py')
    with open(file_path, "w") as file:
        # imports
        file.write('from lox_token import Token\n')
        file.write('from abc import ABC, abstractmethod\n\n\n')
        # base class
        file.write(f'class {base_name}(ABC):\n')
        file.write('    @abstractmethod\n')
        file.write('    def accept(self, visitor):\n')
        file.write('        pass\n\n\n')
        class_names = [type_string.split('::')[0].strip() for type_string in types]
        field_lists = [type_string.split('::')[1].strip() for type_string in types]
        # visitor abstract class
        define_visitor(file, base_name, class_names)
        # subclasses
        for i, (class_name, fields) in enumerate(zip(class_names, field_lists)):
            define_type(file, base_name, class_name, fields)
            is_last_type = i == len(types) - 1
            if not is_last_type:
                file.write('\n\n')


def define_visitor(file: TextIO, base_name: str, class_names: List[str]):
    file.write(f'class Visitor(ABC):\n')
    for i, class_name in enumerate(class_names):
        file.write('    @abstractmethod\n')
        file.write(f'    def visit_{class_name.lower()}_{base_name.lower()}(self, expr):\n')
        file.write('        pass\n')
        is_last_type = i == len(class_names) - 1
        file.write('\n\n' if is_last_type else '\n')


def define_type(file: TextIO, base_name: str, class_name: str, fields: str):
    # class definition
    file.write(f'class {class_name}({base_name}):\n')
    # constructor
    file.write(f'    def __init__(self, {fields}):\n')
    fields = fields.split(', ')
    # fields
    for field in fields:
        name = field.split(': ')[0]
        file.write(f'        self.{name} = {name}\n')
    file.write('\n')
    # accept method
    file.write('    def accept(self, visitor: Visitor):\n')
    file.write(f'        return visitor.visit_{class_name.lower()}_expr(self)\n')


if __name__ == '__main__':
    main()
