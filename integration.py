from char_reader import StringReader, StringIO
from lexer import Lexer
from my_parser import Parser
from pretty_printer import Printer

def main():
    code = StringIO("-(1 < 2 & 3 >= 4)|(5!=6 & (7 == 8 | 9 > 10)) & ((11 <= 12 | 13 > 14) & (-15 < 16) |(17 == 18 & -19 >= 20)) |((21 != 22) & (23 < 24 | 25 >= 26)) |(-(27 == 28) & (29 != 30 | 31 <= 32))")
    reader = StringReader(code)
    lexer = Lexer(reader)
    parser = Parser(lexer)
    printer = Printer()
    print(printer.print(parser._parse_expr()))

if __name__ == '__main__':
    main()
