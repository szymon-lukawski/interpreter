import warnings
import argparse
import os
from lexer.char_reader import TextIOReader
from io import StringIO
from lexer.lexer import Lexer
from parser.my_parser import Parser
from interpreter.interpreter import Interpreter

warnings.filterwarnings("ignore")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=str,
        help="Specify the source file to be interpreted",
    )

    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Enable passing expressions to be printed. If --source specified then source will be interpreted first.",
    )
    args = parser.parse_args()
    interpreter = Interpreter()
    if args.source:
        if not os.path.exists(args.source):
            print(f"Error: The specified source path does not exist: {args.source}")
            return
        with open(args.source, "r", encoding="ascii") as sf:
            try:
                reader = TextIOReader(sf)
                lexer = Lexer(reader)
                parser = Parser(lexer)
                ast = parser.parse_program()
                ast.accept(interpreter)
            except Exception as e:
                print(e)
                return
    else:
        print("No source specified.")

    if args.interactive:
        print("Interactive mode enabled. Type q to quit")
        statement_code = input("Type statement : ")
        while statement_code != "q":
            try:
                reader = TextIOReader(StringIO(statement_code))
                lexer = Lexer(reader)
                parser = Parser(lexer)
                ast = parser._parse_statement()
                ast.accept(interpreter)
            except Exception as e:
                print(e)
            statement_code = input("Type statement : ")
    else:
        print("Interactive mode disabled.")


if __name__ == "__main__":
    main()
