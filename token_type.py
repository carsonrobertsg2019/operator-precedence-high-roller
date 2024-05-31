from enum import Enum

class TokenType(Enum):
    END_OF_FILE = 0
    PLUS = 1
    MINUS = 2
    DIV = 3
    MULT = 4
    LPAREN = 5
    RPAREN = 6
    NUM = 7
    ROLL = 8
    ERROR = 9