import sys

from ast_printer import AstPrinter
from lox_token import Token
from token_type import TokenType


class Lox:
    HAD_ERROR = False

    @staticmethod
    def main() -> None:
        file_name, command_line_args = sys.argv[0], sys.argv[1::]
        if len(command_line_args) > 1:
            print('Usage: plox [script]')
            sys.exit(64)
        elif len(command_line_args) == 1:
            Lox.run_file(sys.argv[0])
        else:
            Lox.run_prompt()

    @staticmethod
    def run_file(file_path: str) -> None:
        with open(file_path, 'r') as file:
            source = file.read()
        Lox.run(source)
        if Lox.HAD_ERROR:
            sys.exit(65)

    @staticmethod
    def run_prompt() -> None:
        print("> ", end='', flush=True)
        while line := sys.stdin.readline().rstrip():
            Lox.run(line)
            print("> ", end='', flush=True)

    @staticmethod
    def run(source: str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        if Lox.HAD_ERROR:
            return
        print(AstPrinter().build_ast_string(expression))

    @staticmethod
    def report(line_number: int, where: str, message: str):
        print(f'[line {line_number}] Error {where}: {message}', file=sys.stderr)
        Lox.HAD_ERROR = True

    @staticmethod
    def error(line_number: int, where: str = '', message: str = '') -> None:
        Lox.report(line_number, where, message)

    @staticmethod
    def error_from_token(token: Token, message: str = ''):
        where = 'at end' if token.type == TokenType.EOF else f"at '{token.lexeme}'"
        Lox.report(token.line, where, message)


# avoid circular imports
from parser import Parser
from scanner import Scanner

if __name__ == '__main__':
    Lox.main()
