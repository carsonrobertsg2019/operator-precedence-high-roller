from lexical_analyzer import LexicalAnalyzer
from token_type import TokenType

class CommandParser:
    def __init__(self):
        self.syntax_error = False
        self.lexer = LexicalAnalyzer()

    def map_to_index(map_char):
        if map_char == '+':         return 1
        elif map_char == '-':       return 2
        elif map_char == '*':       return 3
        elif map_char == '/':       return 4
        elif map_char == '(':       return 5
        elif map_char == ')':       return 6
        elif map_char == 'R':       return 7 #ROLL
        elif map_char == 'N':       return 8 #NUM
        elif map_char == '$':       return 9
        else:                       return -1 #force an index out of bounds

    def determine_operator_precedence(a, b):
        operator_precedence_table = [
            ['?', '+', '-', '*', '/', '(', ')', 'R', 'N', '$'], 
            ['+', '>', '>', '<', '<', '<', '>', '<', '<', '>'],
            ['-', '>', '>', '<', '<', '<', '>', '<', '<', '>'],
            ['*', '>', '>', '>', '>', '<', '>', '<', '<', '>'],
            ['/', '>', '>', '>', '>', '<', '>', '<', '<', '>'],
            ['(', '<', '<', '<', '<', '<', '=', '<', '<', 'X'],
            [')', '>', '>', '>', '>', 'X', '>', 'X', 'X', '>'],
            ['R', '>', '>', '>', '>', 'X', '>', 'X', 'X', '>'],
            ['N', '>', '>', '>', '>', 'X', '>', 'X', 'X', '>'],
            ['$', '<', '<', '<', '<', '<', 'X', '<', '<', 'A']
        ]
        return operator_precedence_table[a][b]

    def expect(self, expected_type):
        token = self.lexer.get_token()
        if token.TokenType != expected_type:
            print('syntax error')
            self.syntax_error = True
            return None
        return token
    
    """
    init => COMMAND_START expr
    expr => expr oper expr || ( expr ) || ROLL || NUM
    oper => PLUS || MINUS || MULT || DIV
    """

    def parse_init(self):
        self.expect(TokenType.COMMAND_START)
        self.parse_expr()

    def parse_expr(self):
        print('parsing expression')