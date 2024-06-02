from lexical_analyzer import LexicalAnalyzer
from token_type import TokenType

class CommandParser:
    def __init__(self):
        self.syntax_error = False
        self.lexer = LexicalAnalyzer()

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