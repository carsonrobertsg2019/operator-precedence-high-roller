from lexical_analyzer import LexicalAnalyzer
from token_type import TokenType
from command_token import Token
from stacknode import StackNode

class CommandParser:
    def __init__(self, input_string):
        self.input_string = input_string
        self.stack = self.initialize_stack()
        self.rhs: list[StackNode] = []
        self.syntax_error = False
        self.lexer = LexicalAnalyzer(input_string)

    def initialize_stack(self):
        temp = [StackNode()]
        temp[0].token_info = Token()
        temp[0].token_info.TokenType = TokenType.END_OF_FILE
        return temp

    def define_operator_precedence_table(self):
        return [
            ['?', '+', '-', '*', '/', '(', ')', 'R', 'N', '$', 'X'],
            ['+', '>', '>', '<', '<', '<', '>', '<', '<', '>', 'X'],
            ['-', '>', '>', '<', '<', '<', '>', '<', '<', '>', 'X'],
            ['*', '>', '>', '>', '>', '<', '>', '<', '<', '>', 'X'],
            ['/', '>', '>', '>', '>', '<', '>', '<', '<', '>', 'X'],
            ['(', '<', '<', '<', '<', '<', '=', '<', '<', 'X', 'X'],
            [')', '>', '>', '>', '>', 'X', '>', 'X', 'X', '>', 'X'],
            ['R', '>', '>', '>', '>', 'X', '>', 'X', 'X', '>', 'X'],
            ['N', '>', '>', '>', '>', 'X', '>', 'X', 'X', '>', 'X'],
            ['$', '<', '<', '<', '<', '<', 'X', '<', '<', 'A', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
        ]

    def expect(self, expected_type):
        token = self.lexer.get_token()
        if token.TokenType != expected_type:
            print('syntax error')
            self.syntax_error = True
            return None
        return token

    def parse_init(self):
        self.expect(TokenType.COMMAND_START)
        self.parse_expr()

    def terminal_peek(self):
        if self.stack[-1].is_terminal: return self.stack[-1]
        elif self.stack[-2].is_terminal: return self.stack[-2]
        else: return None

    def null_token(self):
        token = Token()
        token.TokenType = TokenType.ERROR
        return token

    def is_roll_or_num(self):
        return (
            self.rhs[0].token_info.TokenType == TokenType.ROLL or
            self.rhs[0].token_info.TokenType == TokenType.NUM
        )
    
    def is_operation(self):
        return (
            self.rhs[1].token_info.TokenType == TokenType.PLUS or
            self.rhs[1].token_info.TokenType == TokenType.MINUS or
            self.rhs[1].token_info.TokenType == TokenType.MULT or
            self.rhs[1].token_info.TokenType == TokenType.DIV
        )

    def is_arithm_expr(self):
        return (
            not self.rhs[2].is_terminal and
            self.is_operation() and
            not self.rhs[0].is_terminal
        )
    
    def is_closed_par(self):
        return (
            self.rhs[2].token_info.TokenType == TokenType.LPAREN and
            not self.rhs[1].is_terminal and
            self.rhs[0].token_info.TokenType == TokenType.RPAREN
        )
    
    def is_valid_expr(self):
        if len(self.rhs) == 1:
            return self.is_roll_or_num()
        elif len(self.rhs) == 3:
            return self.is_arithm_expr() or self.is_closed_par()
        else:
            print('syntax error')
            self.syntax_error = True
            return None

    def reduce_roll_or_num(self):
        new_node = StackNode()
        new_node.is_terminal = False
        new_node.token_info = self.rhs[0].token_info
        return new_node
    
    def determine_operation(self):
        if self.rhs[1].token_info.TokenType == TokenType.PLUS:
            return TokenType.PLUS
        if self.rhs[1].token_info.TokenType == TokenType.MINUS:
            return TokenType.MINUS
        if self.rhs[1].token_info.TokenType == TokenType.MULT:
            return TokenType.MULT
        if self.rhs[1].token_info.TokenType == TokenType.DIV:
            return TokenType.DIV

    def reduce_arithm_expr(self):
        new_node = StackNode()
        new_node.is_terminal = False
        new_node.token_info = self.null_token()
        new_node.oper = self.determine_operation()
        new_node.left = self.rhs[2]
        new_node.right = self.rhs[0]
        return new_node
    
    def reduce_closed_par(self):
        return self.rhs[1]

    def reduce_expr(self):
        if len(self.rhs) == 1:
            return self.reduce_roll_or_num()
        elif self.is_arithm_expr(): 
            return self.reduce_arithm_expr()
        else: 
            return self.reduce_closed_par()

    def shift(self):
        new_node = StackNode()
        new_node.token_info = self.lexer.get_token()
        self.stack.append(new_node)
        
    def reduce(self, table):
        self.rhs = []
        last_popped_terminal = self.null_token()
        while True:
            s = self.stack.pop()
            if s.is_terminal:
                last_popped_terminal = s.token_info
            self.rhs.append(s)
            a = self.terminal_peek().token_info.TokenType.value
            b = last_popped_terminal.TokenType.value
            if self.stack[-1].is_terminal and table[a][b] == '<':
                break
        if self.is_valid_expr():
            new_node = self.reduce_expr()
            self.stack.append(new_node)
        else:
            print('syntax error')
            self.syntax_error = True
            return None

    def more_expr_parsing(self):
        return (
            not self.terminal_peek().token_info.TokenType == TokenType.END_OF_FILE or
            not self.lexer.peek(1).TokenType == TokenType.END_OF_FILE
        )

    def parse_expr(self):
        table = self.define_operator_precedence_table()
        while self.more_expr_parsing():
            t = self.lexer.peek(1)
            a = self.terminal_peek().token_info.TokenType.value
            b = t.TokenType.value
            if table[a][b] in ['<', '=']:
                self.shift()
            elif table[a][b] == '>':
                self.reduce(table)
            else:
                print('syntax error')
                self.syntax_error = True
                return None