from command_token import Token
from token_type import TokenType
from input_buffer import InputBuffer

class LexicalAnalyzer:
    def __init__(self, input_string):
        self.input_string = input_string
        self.token_list = []
        self.index = 0
        self.tmp = Token()
        self.tmp.lexeme = ""
        self.tmp.TokenType = TokenType.ERROR
        self.input = InputBuffer(input_string)
        token = self.get_token_main()
        while token.TokenType != TokenType.END_OF_FILE:
            self.token_list.append(token)
            token = self.get_token_main()

    def isspace(self, c):
        return (
            c == ' ' or
            c == '\t' or
            c == '\v' or
            c == '\n' or
            c == '\r' or
            c == '\f'
        )
    
    def isdigit(self, c):
        return (
            c == '0' or
            c == '1' or
            c == '2' or
            c == '3' or
            c == '4' or
            c == '5' or
            c == '6' or
            c == '7' or
            c == '8' or
            c == '9'
        )

    def skip_space(self):
        c = self.input.get_char()
        while not self.input.end_of_input() and self.isspace(c):
            c = self.input.get_char()
        if not self.input.end_of_input():
            self.input.unget_char(c)

    def scan_number_or_roll(self):
        tmp = Token()
        tmp.lexeme = ""
        c = self.input.get_char()
        if self.isdigit(c):
            while not self.input.end_of_input() and self.isdigit(c):
                tmp.lexeme += c
                c = self.input.get_char()
            if c in ['d', 'e']:
                tmp.lexeme += c
                c = self.input.get_char()
                if self.isdigit(c):
                    while not self.input.end_of_input() and self.isdigit(c):
                        tmp.lexeme += c
                        c = self.input.get_char()
                    if not self.input.end_of_input():
                        self.input.unget_char(c)
                    tmp.TokenType = TokenType.ROLL
                    return tmp
                else:
                    if not self.input.end_of_input():
                        self.input.unget_char(c)
                    tmp.lexeme = ""
                    tmp.TokenType = TokenType.ERROR
                    return tmp
            if not self.input.end_of_input():
                self.input.unget_char(c)
            tmp.TokenType = TokenType.ROLL
            return tmp
        else:
            if not self.input.end_of_input():
                self.input.unget_char(c)
            tmp.TokenType = TokenType.ERROR
            return tmp
        
    def scan_roll(self):
        tmp = Token()
        tmp.lexeme = self.input.get_char()
        c = self.input.get_char()
        if self.isdigit(c):
            while not self.input.end_of_input() and self.isdigit(c):
                tmp.lexeme += c
                c = self.input.get_char()
            if not self.input.end_of_input():
                self.input.unget_char(c)
            tmp.TokenType = TokenType.ROLL
            return tmp
        else:
            if not self.input.end_of_input():
                self.input.unget_char(c)
            tmp.lexeme = ""
            tmp.TokenType = TokenType.ERROR
            return tmp
    
    def get_token(self):
        token = Token()
        if self.index == len(self.token_list):
            token.lexeme = ""
            token.TokenType = TokenType.END_OF_FILE
        else:
            token = self.token_list[self.index]
            self.index += 1
        return token
    
    def peek(self, how_far) -> Token:
        if how_far <= 0:
            print("cannot peek a non-positive amount")
            return
        peekIndex = self.index + how_far - 1
        if peekIndex > len(self.token_list) - 1:
            token = Token()
            token.lexeme = ""
            token.TokenType = TokenType.END_OF_FILE
            return token
        else:
            return self.token_list[peekIndex]

    def get_token_main(self):
        c = None
        self.skip_space()
        tmp = Token()
        tmp.lexeme = ""
        tmp.TokenType = TokenType.END_OF_FILE
        if not self.input.end_of_input():
            c = self.input.get_char()
        else:
            return tmp
        match c:
            case '!': tmp.TokenType = TokenType.COMMAND_START
            case '+': tmp.TokenType = TokenType.PLUS
            case '-': tmp.TokenType = TokenType.MINUS
            case '*': tmp.TokenType = TokenType.MULT
            case '/': tmp.TokenType = TokenType.DIV
            case '(': tmp.TokenType = TokenType.LPAREN
            case ')': tmp.TokenType = TokenType.RPAREN
            case _:
                if self.isdigit(c):
                    self.input.unget_char(c)
                    tmp = self.scan_number_or_roll()
                elif c in ['d', 'e']:
                    self.input.unget_char(c)
                    tmp = self.scan_roll()
                else:
                    tmp.TokenType = TokenType.ERROR
        return tmp