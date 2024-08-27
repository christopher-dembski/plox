import sys

from lox_token import Token
from token_type import TokenType
from runtime_exception import RuntimeException


class Lox:
    HAD_PARSER_ERROR = False
    HAD_RUNTIME_EXCEPTION = False

    @staticmethod
    def main() -> None:
        file_name, command_line_args = sys.argv[0], sys.argv[1::]
        if len(command_line_args) > 1:
            print('Usage: plox [script]')
            sys.exit(64)
        elif len(command_line_args) == 1:
            Lox.run_file(command_line_args[0])
        else:
            Lox.run_prompt()

    @staticmethod
    def run_file(file_path: str) -> None:
        with open(file_path, 'r') as file:
            source = file.read()
        Lox.run(source)
        if Lox.HAD_PARSER_ERROR:
            sys.exit(65)
        elif Lox.HAD_RUNTIME_EXCEPTION:
            sys.exit(70)

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
        statements = parser.parse()
        if Lox.HAD_PARSER_ERROR:
            return
        Lox.INTERPRETER.interpret(statements)

    @staticmethod
    def report(line_number: int, where: str, message: str):
        print(f'[line {line_number}] Error {where}: {message}', file=sys.stderr)
        Lox.HAD_PARSER_ERROR = True

    @staticmethod
    def error(line_number: int, where: str = '', message: str = '') -> None:
        Lox.report(line_number, where, message)

    @staticmethod
    def error_from_token(token: Token, message: str = ''):
        where = 'at end' if token.type == TokenType.EOF else f"at '{token.lexeme}'"
        Lox.report(token.line, where, message)

    @staticmethod
    def runtime_exception(exception: RuntimeException) -> None:
        print(f'{exception}\n[line {exception.token.line}]', file=sys.stderr)
        Lox.HAD_RUNTIME_EXCEPTION = True


# avoid circular imports
from parser import Parser
from scanner import Scanner
from interpreter import Interpreter

# we need to instantiate interpreter here after the interpreter module is imported
Lox.INTERPRETER = Interpreter()

if __name__ == '__main__':
    Lox.main()
