from typing import Callable
from char_reader import StringReader, StringIO
from lexer import Lexer
from my_parser import Parser
from printer import Printer


def print_list_of_tokens(code : str, intentation : int = 0):
    reader = StringReader(StringIO(code))
    lexer = Lexer(reader)
    print(intentation*' ','tokens = [', sep="")
    while not lexer._is_end_of_file():
        print(intentation*' '*2,lexer.get_next_token(), ',', sep="")
    print(intentation*' ',']\n',sep="")

def print_ast(code : str, parse_func : Callable = Parser.parse_program, intendation : int = 0):
    printer = Printer()
    reader = StringReader(StringIO(code))
    lexer = Lexer(reader)
    parser = Parser(lexer)
    print(f"{intendation*" "}expected = {printer.print(parse_func(parser))}")



def main():
    code = '1 & 2 & 0'
    indentation = 4
    # print('@pytest.mark.parametrize("rel_token_type,rel_str", rel_operators)')
    print('@pytest.mark.parametrize("func", and_parse_funcs)')
    print('def test_and_(func):')
    print(f'{indentation*' '}"""{code}"""')
    print_list_of_tokens(code, 4)
    print(f'{indentation*' '}lexer = TokenProvider(None, tokens)')
    print(f'{indentation*' '}parser = Parser(lexer)')
    print(f'{indentation*' '}result = func(parser)')
    print_ast(code, Parser._parse_expr, 4)
    print(f'{indentation*' '}assert result == expected')


if __name__ == "__main__":
    main()
