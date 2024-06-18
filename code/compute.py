from stacknode import StackNode
from token_type import TokenType
import random

class Compute:
    def __init__(self):
        self.i = 0
        self.cocked_rolls = []
        self.all_lists_of_rolls = []
        self.error = False
    
    def roll_die(self, to_roll):
        num_rolls = int(to_roll[:to_roll.index('d')]) if to_roll[:to_roll.index('d')] != '' else 1
        num_sides = int(to_roll[to_roll.index('d')+1:])
        if num_rolls > 1000 or num_rolls > 10000:
            self.error = True
            return 0
        rolled_total = 0
        list_of_rolls = []
        for i in range(num_rolls):
            self.i += 1
            if random.random() < 0.025:
                self.cocked_rolls.append((random.randint(1, num_sides), self.i))
            roll = random.randint(1, num_sides)
            list_of_rolls.append(roll)
            rolled_total += roll
        self.all_lists_of_rolls.append(list_of_rolls)
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
            if right_expr == 0:
                self.error = True
                return 0
            return int(left_expr / right_expr)
        elif reduced_expr.token_info.TokenType == TokenType.ERROR:
            self.error = True
            return 0
        elif 'd' in reduced_expr.token_info.lexeme:
            to_roll = reduced_expr.token_info.lexeme
            return self.roll_die(to_roll)
        else:
            num = int(reduced_expr.token_info.lexeme)
            return num