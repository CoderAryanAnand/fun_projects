board = {
    '1': ' ', '2': ' ', '3': ' ',
    '4': ' ', '5': ' ', '6': ' ',
    '7': ' ', '8': ' ', '9': ' '
}

player = 1          # to initialise first player
total_moves = 0     # to count the moves
end_check = 2


def game_over(board):
    # checking the moves of player one
    # for horizontal(start)
    if board['1'] == 'X' and board['2'] == 'X' and board['3'] == 'X':
        print('Player one won !')
        return 1
    if board['4'] == 'X' and board['5'] == 'X' and board['6'] == 'X':
        print('Player One Won!!')
        return 1
    if board['7'] == 'X' and board['8'] == 'X' and board['9'] == 'X':
        print('Player One Won!!')
        return 1
    # for horizontal(end)
    # for diagonal(start)
    if board['1'] == 'X' and board['5'] == 'X' and board['9'] == 'X':
        print('Player One Won!!')
        return 1
    if board['3'] == 'X' and board['5'] == 'X' and board['7'] == 'X':
        print('Player One Won!!')
        return 1
    # for diagonal(end)
    # for vertical(start)
    if board['1'] == 'X' and board['4'] == 'X' and board['7'] == 'X':
        print('Player One Won!!')
        return 1
    if board['2'] == 'X' and board['5'] == 'X' and board['8'] == 'X':
        print('Player One Won!!')
        return 1
    if board['3'] == 'X' and board['6'] == 'X' and board['9'] == 'X':
        print('Player One Won!!')
        return 1
    # for vertical(end)

    # checking the moves of player two
    if board['1'] == 'O' and board['2'] == 'O' and board['3'] == 'O':
        print('Player Two Won!!')
        return -1  # used to end the game
    if board['4'] == 'O' and board['5'] == 'O' and board['6'] == 'O':
        print('Player Two Won!!')
        return -1
    if board['7'] == 'O' and board['8'] == 'O' and board['9'] == 'O':
        print('Player Two Won!!')
        return -1
    if board['1'] == 'O' and board['4'] == 'O' and board['7'] == 'O':
        print('Player Two Won!!')
        return -1
    if board['2'] == 'O' and board['5'] == 'O' and board['8'] == 'O':
        print('Player Two Won!!')
        return -1
    if board['3'] == 'O' and board['6'] == 'O' and board['9'] == 'O':
        print('Player Two Won!!')
        return -1
    if board['1'] == 'O' and board['5'] == 'O' and board['9'] == 'O':
        print('Player Two Won!!')
        return -1
    if board['3'] == 'O' and board['5'] == 'O' and board['7'] == 'O':
        print('Player Two Won!!')
        return -1

    # for tie
    total = 0
    for space in board:
        if board[space] != ' ':
            total += 1

    if total == 9:
        print('Tie!')
        return 0

    return 2


def minimax(position, maximizing_player):
    if game_over(position) != 2:
        return game_over(position), ' '

    posi = position

    mvs_possible = [space for space in posi if posi[space] == ' ']
    print(mvs_possible)
    print(posi['1'] + '|' + posi['2'] + '|' + posi['3'])
    print('-+-+-')
    print(posi['4'] + '|' + posi['5'] + '|' + posi['6'])
    print('-+-+-')
    print(posi['7'] + '|' + posi['8'] + '|' + posi['9'])
    # for space in board:
    #     if board[space] == ' ':
    #         mvs_possible.append(space)

    if maximizing_player:
        max_eval = -2
        for move in mvs_possible:
            posi[move] = 'O'
            eval, n = minimax(posi, False)
            posi[move] = ' '
            print(eval)
            bestmove = move
            if eval > max_eval:
                max_eval = eval
        print(max_eval, bestmove)
        return max_eval, bestmove
    else:
        min_eval = 3
        for move in mvs_possible:
            posi[move] = 'X'
            eval, n = minimax(posi, True)
            posi[move] = ' '
            bestmove = move
            if eval < min_eval:
                min_eval = eval
        print(min_eval, bestmove)
        return min_eval, bestmove


while True:
    print(board['1']+'|'+board['2']+'|'+board['3'])
    print('-+-+-')
    print(board['4'] + '|' + board['5'] + '|' + board['6'])
    print('-+-+-')
    print(board['7'] + '|' + board['8'] + '|' + board['9'])
    end_check = game_over(board)
    if end_check != 2:
        break
    if player == 1:  # choose player
        p1_input = input('player one')
        if p1_input.upper() in board and board[p1_input.upper()] == ' ':
            board[p1_input.upper()] = 'X'
            player = 2
            total_moves += 1
        # on wrong input
        else:
            print('Invalid input, please try again')
            continue
    else:
        n, bm = minimax(board, True)
        board[bm] = 'O'
        total_moves += 1
        player = 1
