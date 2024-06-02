from enum import Enum

class TokenType(Enum):
    COMMAND_START = 0
    END_OF_FILE = 1
    PLUS = 2
    MINUS = 3
    DIV = 4
    MULT = 5
    LPAREN = 6
    RPAREN = 7
    NUM = 8
    ROLL = 9
    ERROR = 10