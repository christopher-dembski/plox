import sys
from scanner import Scanner


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
        for token in tokens:
            print(token)

    @staticmethod
    def error(line_number: int, where: str, message: str) -> None:
        print(f'[line {line_number}] Error {where}: {message}', file=sys.stderr)
        Lox.HAD_ERROR = True


if __name__ == '__main__':
    Lox.main()
