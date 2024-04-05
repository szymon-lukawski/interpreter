"""."""
from enum import Enum

class TokenType(Enum):
    """-"""

    IDENTIFIER = 1
    STR_LITERAL = 2
    FLOAT_LITERAL = 3
    INT_LITERAL = 4
    NULL = 5
    COMMENT = 6
    MUT = 7
    INT = 8
    FLOAT = 9
    STR = 10
    NULL_TYPE = 11
    IF = 12
    ELSE = 13
    WHILE = 14
    RETURN = 15
    PRINT = 16
    READ = 17
    LEFT_BRACKET = 18
    RIGHT_BRACKET = 19
    SEMICOLON = 20
    COLON = 21
    PLUS = 22
    MINUS = 23
    TIMES = 24
    DIVIDE = 25
    DOT = 26
    ASSIGNMENT = 27
    LESS = 28
    GREATER = 29
    OR = 30
    AND = 31
    LESS_EQUAL = 32
    EQUAL = 33
    INEQUAL = 34
    GREATER_EQUAL = 35
    BEGIN = 36
    END = 37
    STRUCT = 38
    VARIANT = 39
    VISIT = 40
    CASE = 41
