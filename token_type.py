from enum import Enum

class TokenType(Enum):
    COMMAND_START = 0
    PLUS = 1
    MINUS = 2
    MULT = 3
    DIV = 4
    LPAREN = 5
    RPAREN = 6
    ROLL = 7
    NUM = 8
    END_OF_FILE = 9
    ERROR = 10