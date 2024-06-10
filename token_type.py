from enum import Enum

class TokenType(Enum):
    COMMAND_START = 1
    END_OF_FILE = 2
    PLUS = 3
    MINUS = 4
    DIV = 5
    MULT = 6
    LPAREN = 7
    RPAREN = 8
    NUM = 9
    ROLL = 10
    ERROR = 11