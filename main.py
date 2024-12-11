import argparse
import os
from char_reader import TextIOReader
from io import StringIO
from lexer import Lexer
from my_parser import Parser
from interpreter import Interpreter


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
            reader = TextIOReader(sf)
            lexer = Lexer(reader)
            parser = Parser(lexer)
            ast = parser.parse_program()
            ast.accept(interpreter)
    else:
        print("No source specified.")

    if args.interactive:
        print("Interactive mode enabled. Type q to quit")
        interactive_expr_code = input("Type expr : ")
        while interactive_expr_code != 'q':
            reader = TextIOReader(StringIO(interactive_expr_code))
            lexer = Lexer(reader)
            parser = Parser(lexer)
            ast = parser._parse_expr()
            ast.accept(interpreter) # add printing expr
            interactive_expr_code = input("Type expr : ")
    else:
        print("Interactive mode disabled.")




if __name__ == "__main__":
    main()
