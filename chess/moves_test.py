import re

# Use regular expressions and string methods (e.g. split) to create
# the moves dictionary.
# First find one or two integers followed by full stop and replace
# with a special character
# (eg. ^ --> '^ d4 Nf6 ^ Nc3 d5 ^ Bg5 Nd7 ^ Nf3 h6 ^ Bf4 e6 ^ Nb5 Bb4').


# Split the string into a list using the special character.
# Remove the first item in the list if it is empty.
# Remove the space at the start and end of each pair of moves (eg. ' d4 Nf6 ' to 'd4 Nf6')
# Iterate over the pairs of moves, split on the space to separate the players.
# For each player'smove determine type of piece if there is pawn by detecting
# if the first letter is not a capital otherwise lookup the type.
# Place everything into a dictionary.

# start with this set of moves. We will add the special ones later
# and increase the information in the dictionary.

game_moves_str = '1. d4 Nf6 2. Nc3 d5 3. Bg5 Nd7 4. Nf3 h6 5. Bf4 e6 6. Nb5 Bb4'
piece_types = ['pawn', 'rook', 'king', 'queen', 'bishop', 'knight']

def replace_with_char(string):
    replace_list = []
    for position, char in enumerate(string):
        test_str = ''
        test_pos = position
        while string[test_pos].isdigit():
            test_str = test_str + string[test_pos]
            test_pos += 1
            if test_pos >= len(string):
                break
        if not test_pos >= len(string)-1:
            if string[test_pos] == '.' and test_str.isdigit():
                test_str += '.'
                replace_list.append(test_str)

    for replacement in replace_list:
        string = string.replace(replacement, '^')

    return string

def getmove(string):
    if "N" in string:
        string = 'Knight'
        return string
    elif "B" in string:
            string = 'Bishop'
            return string
    elif "K" in string:
            string = 'King'
            return string
    elif "Q" in string:
            string = 'Queen'
            return string
    elif "R" in string:
        string = 'Rook'
        return string
    else:
        string = 'Pawn'
        return string



moves = '?????'

moves_target = {
    1: {
        'player_1': {'piece_type': 'pawn', 'move_des': 'd4', 'start_loc': 'd4',  'end_loc': 'd4'},
        'player_2': {'piece_type': 'knight', 'move_des': 'Nf6', 'end_loc': 'f6'}
    },
    2: {
        'player_1': {'piece_type': 'knight', 'move_des': 'Nc3', 'end_loc': 'c3'},
        'player_2': {'piece_type': 'pawn', 'move_des': 'd5', 'end_loc': 'd5'}
    },
    3: {
        'player_1': {'piece_type': 'bishop', 'move_des': 'Bg5', 'end_loc': 'g5'},
        'player_2': {'piece_type': 'knight', 'move_des': 'Nd7', 'end_loc': 'd7'}
    },
    4: {
        'player_1': {'piece_type': 'knight', 'move_des': 'Nf3', 'end_loc': 'f3'},
        'player_2': {'piece_type': 'pawn', 'move_des': 'h6', 'end_loc': 'h6'}
    },
    5: {
        'player_1': {'piece_type': 'bishop', 'move_des': 'Bf4', 'end_loc': 'f4'},
        'player_2': {'piece_type': 'pawn', 'move_des': 'e6', 'end_loc': 'e6'}
    },
    6: {
        'player_1': {'piece_type': 'knight', 'move_des': 'Nb5', 'end_loc': 'b5'},
        'player_2': {'piece_type': 'bishop', 'move_des': 'Bb4', 'end_loc': 'b4'}
    }
}

if __name__ == '__main__':
    a = replace_with_char('1. d4 Nf6 2. Nc3 d5 3. Bg5 Nd7 4. Nf3 h6 5. Bf4 e6 60. Nb5 Bb4')
    print(a)
    split_list = a.split(' ^ ')
    split_list[0] = split_list[0].replace('^ ', "")
    new_dict = {}
    for move_no, move in enumerate(split_list):
        split_moves = move.split(' ')
        test1 = getmove(split_moves[0])
        test2 = getmove(split_moves[1])
        print(split_moves)
        print(test1, test2)
        new_dict[move_no + 1] = {'White':{'Move': split_moves[0], 'Piece': test1}, 'Black':{'Move': split_moves[1], 'Piece': test2}}
    print(new_dict)


