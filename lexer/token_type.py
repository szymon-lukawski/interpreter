"""."""
from enum import Enum

class TokenType(Enum):
    """-"""
    COMMENT = 1
    IDENTIFIER = 2
    STR_LITERAL = 3
    FLOAT_LITERAL = 4
    INT_LITERAL = 5
    NULL = 6
    INT = 7
    FLOAT = 8
    STR = 9
    NULL_TYPE = 10
    MUT = 11
    IF = 12
    ELSE = 13
    WHILE = 14
    RETURN = 15
    BEGIN = 16
    END = 17
    STRUCT = 18
    VARIANT = 19
    VISIT = 20
    CASE = 21
    # PRINT = 22
    # READ = 23
    SEMICOLON = 24
    COLON = 25
    ASSIGNMENT = 26
    COMMA = 27
    DOT = 28
    LEFT_BRACKET = 29
    RIGHT_BRACKET = 30
    TIMES = 31
    DIVIDE = 32
    PLUS = 33
    MINUS = 34
    LESS = 35
    LESS_EQUAL = 36
    EQUAL = 37
    INEQUAL = 38
    GREATER_EQUAL = 39
    GREATER = 40
    AND = 41
    OR = 42
    EOT = 43
    
