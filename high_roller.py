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