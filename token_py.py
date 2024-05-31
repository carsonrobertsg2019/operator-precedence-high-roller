from token_type import TokenType

class Token:
    def __init__(self):
        self.lexeme = ""
        self.TokenType = TokenType.ERROR
        self.reserved_strings = [
            "END_OF_FILE",
            "PLUS",
            "MINUS",
            "DIV",
            "MULT",
            "LPAREN",
            "RPAREN",
            "NUM",
            "ROLL",
            "ERROR"
        ]
        #line_num = 0 (probably unnecessary)

    def Print(self):
        print("{" + self.lexeme + " , " + self.reserved_strings[self.TokenType.value] + "}")
