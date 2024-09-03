import sys

from lox_token import Token
from token_type import TokenType
from runtime_exception import RuntimeException
from parser import Parser
from scanner import Scanner
from interpreter import Interpreter


class Lox:

    def __init__(self):
        self.interpreter = Interpreter(self)
        self.had_parser_error = False
        self.had_runtime_exception = False

    def main(self) -> None:
        file_name, command_line_args = sys.argv[0], sys.argv[1::]
        if len(command_line_args) > 1:
            print('Usage: plox [script]')
            sys.exit(64)
        elif len(command_line_args) == 1:
            self.run_file(command_line_args[0])
        else:
            self.run_prompt()

    def run_file(self, file_path: str) -> None:
        with open(file_path, 'r') as file:
            source = file.read()
        self.run(source)
        if self.had_parser_error:
            sys.exit(65)
        elif self.had_runtime_exception:
            sys.exit(70)

    def run_prompt(self) -> None:
        print("> ", end='', flush=True)
        while line := sys.stdin.readline().rstrip():
            self.run(line)
            print("> ", end='', flush=True)
            self.had_parser_error = False

    def run(self, source: str) -> None:
        scanner = Scanner(source, self)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens, self)
        statements = parser.parse()
        if self.had_parser_error:
            return
        self.interpreter.interpret(statements)

    def report(self, line_number: int, where: str, message: str):
        print(f'[line {line_number}] Error {where}: {message}', file=sys.stderr)
        self.had_parser_error = True

    def error(self, line_number: int, where: str = '', message: str = '') -> None:
        self.report(line_number, where, message)

    def error_from_token(self, token: Token, message: str = ''):
        where = 'at end' if token.type == TokenType.EOF else f"at '{token.lexeme}'"
        self.report(token.line, where, message)

    def runtime_exception(self, exception: RuntimeException) -> None:
        print(f'{exception}\n[line {exception.token.line}]', file=sys.stderr)
        self.had_runtime_exception = True


if __name__ == '__main__':
    Lox().main()
