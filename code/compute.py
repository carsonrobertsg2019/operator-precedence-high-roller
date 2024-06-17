from stacknode import StackNode
from token_type import TokenType
import random

class Compute:
    def __init__(self):
        self.roll_num = 0
        self.cocked_rolls = []
    
    def roll_die(self, to_roll):
        num_rolls = int(to_roll[:to_roll.index('d')]) if to_roll[:to_roll.index('d')] != '' else 1
        num_sides = int(to_roll[to_roll.index('d')+1:])
        rolled_total = 0
        for i in range(num_rolls):
            self.roll_num += 1
            if random.random() < 0.025:
                self.cocked_rolls.append(random.randint(1, num_sides))
            rolled_total += random.randint(1, num_sides)
        return rolled_total

    def compute_expr(self, reduced_expr: StackNode):
        if reduced_expr.oper == TokenType.PLUS:
            left_expr = self.compute_expr(reduced_expr.left)
            right_expr = self.compute_expr(reduced_expr.right)
            return left_expr + right_expr
        elif reduced_expr.oper == TokenType.MINUS:
            left_expr = self.compute_expr(reduced_expr.left)
            right_expr = self.compute_expr(reduced_expr.right)
            return left_expr - right_expr
        elif reduced_expr.oper == TokenType.MULT:
            left_expr = self.compute_expr(reduced_expr.left)
            right_expr = self.compute_expr(reduced_expr.right)
            return left_expr * right_expr
        elif reduced_expr.oper == TokenType.DIV:
            left_expr = self.compute_expr(reduced_expr.left)
            right_expr = self.compute_expr(reduced_expr.right)
            return left_expr / right_expr
        elif 'd' in reduced_expr.token_info.lexeme:
            to_roll = reduced_expr.token_info.lexeme
            return self.roll_die(to_roll)
        else:
            num = reduced_expr.token_info.lexeme
            return num