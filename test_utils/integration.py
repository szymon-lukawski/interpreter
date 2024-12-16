from typing import Callable
from lexer.char_reader import TextIOReader
from io import StringIO
from lexer.lexer import Lexer
from parser.my_parser import Parser
from test_utils.printer import Printer
from interpreter.interpreter import Interpreter


def print_list_of_tokens(code : str, intentation : int = 0):
    reader = TextIOReader(StringIO(code))
    lexer = Lexer(reader)
    print(intentation*' ','tokens = [', sep="")
    while not lexer._is_end_of_file():
        print(intentation*' '*2,lexer.get_next_token(), ',', sep="")
    print(intentation*' ',']\n',sep="")

def print_ast(code : str, parse_func : Callable = Parser.parse_program, intendation : int = 0):
    printer = Printer()
    reader = TextIOReader(StringIO(code))
    lexer = Lexer(reader)
    parser = Parser(lexer)
    print(f"{intendation*" "}ast = {printer.print(parse_func(parser))}")



def main():
    code =     """A : struct begin x : int; end V : variant begin a : A; y:int; end v:V; v.x = '1.2'; print(v);"""
    indentation = 4
    # print('@pytest.mark.parametrize("rel_token_type,rel_str", rel_operators)')
    # print('@pytest.mark.parametrize("func", and_parse_funcs)')
    # print_list_of_tokens(code)
    print('def test_and_():')
    print(f'{indentation*' '}"""{code}"""')
    print_ast(code, Parser.parse_program, 4)
    print(f"{indentation*' '}i = Interpreter()")
    print(f"{indentation*' '}ast.accept(i)")
    # reader = TextIOReader(StringIO(code))
    # lexer = Lexer(reader)
    # parser = Parser(lexer)
    # ast = parser.parse_program()
    # interpreter = Interpreter()
    # ast.accept(interpreter)



if __name__ == "__main__":
    main()
