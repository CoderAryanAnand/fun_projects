import matplotlib
import matplotlib.pyplot as plt
import chess
import chess.svg
import chess.pgn
#from IPython.display import SVG

pgn = open("C:/Users/Aryan Anand/Documents/12323.pgn")

# n = 1
# print(n)


for i in range(1, 3):
    act_game = chess.pgn.read_game(pgn)

    print(act_game.headers["Event"] + " | " + act_game.headers["White"] +
          " - " + act_game.headers["Black"] + "  " + act_game.headers["Result"] +
          " | " + act_game.headers["Date"])

    # import chess.engine
    #
    # engine = chess.engine.SimpleEngine.popen_uci("C:/Users/iitda/Chess_analysis/stockfish_9_x64.exe")

    import chess.uci

    engine = chess.uci.popen_engine("C:/Users/Aryan Anand/Documents/stockfish_20011801_x64.exe")
    engine.uci()
    engine.name

    board = act_game.board()
    board.fen()

    import numpy as np


    def fentotensor(inputstr):
        pieces_str = "PNBRQK"
        pieces_str += pieces_str.lower()
        pieces = set(pieces_str)
        valid_spaces = set(range(1, 9))
        pieces_dict = {pieces_str[0]: 1, pieces_str[1]: 2, pieces_str[2]: 3, pieces_str[3]: 4,
                       pieces_str[4]: 5, pieces_str[5]: 6,
                       pieces_str[6]: -1, pieces_str[7]: -2, pieces_str[8]: -3, pieces_str[9]: -4,
                       pieces_str[10]: -5, pieces_str[11]: -6}

        boardtensor = np.zeros((8, 8, 6))

        inputliste = inputstr.split()
        rownr = 0
        colnr = 0
        for i, c in enumerate(inputliste[0]):
            if c in pieces:
                boardtensor[rownr, colnr, np.abs(pieces_dict[c]) - 1] = np.sign(pieces_dict[c])
                colnr = colnr + 1
            elif c == '/':  # new row
                rownr = rownr + 1
                colnr = 0
            elif int(c) in valid_spaces:
                colnr = colnr + int(c)
            else:
                raise ValueError("invalid fenstr at index: {} char: {}".format(i, c))

        return boardtensor


    def countpieces(fen):
        boardtensor = fentotensor(fen)
        count = np.sum(np.abs(boardtensor))
        return count


    countpieces(board.fen())


    def pawnending(fen):
        boardtensor = fentotensor(fen)
        counts = np.sum(np.abs(boardtensor), axis=(0, 1))
        if counts[1] == 0 and counts[2] == 0 and counts[3] == 0 and counts[4] == 0:
            return True
        else:
            return False


    def rookending(fen):
        boardtensor = fentotensor(fen)
        counts = np.sum(np.abs(boardtensor), axis=(0, 1))
        if counts[1] == 0 and counts[2] == 0 and counts[4] == 0 and counts[3] > 0:
            return True
        else:
            return False


    # Register a standard info handler.
    info_handler = chess.uci.InfoHandler()
    engine.info_handlers.append(info_handler)

    counts = {"movecount": [], "scores": [], "check": [], "bestdiff": [], "pawnending": [], "rookending": []}

    # Iterate through all moves and play them on a board.
    board = act_game.board()

    for move in act_game.mainline_moves():
        board.push(move)
        cnt = len([i for i in board.legal_moves])
        counts["movecount"].append(cnt)
        counts["check"].append(board.is_check())
        counts["pawnending"].append(pawnending(board.fen()))
        counts["rookending"].append(rookending(board.fen()))

        # Start a search.
        engine.position(board)
        engine.go(movetime=100)
        if board.turn == chess.WHITE:
            counts["scores"].append((info_handler.info["score"][1][0]) / 100)
        else:
            counts["scores"].append((-info_handler.info["score"][1][0]) / 100)
        nextmovescores = []

        for mov in board.legal_moves:
            board.push(mov)
            engine.position(board)
            engine.go(movetime=2)
            if board.turn == chess.WHITE:
                if info_handler.info["score"][1][0] != None:
                    nextmovescores.append(info_handler.info["score"][1][0])
            elif board.turn == chess.BLACK:
                if info_handler.info["score"][1][0] != None:
                    nextmovescores.append(-info_handler.info["score"][1][0])
            board.pop()

        if len(nextmovescores) > 1:
            nextmovescores.sort(reverse=True)
            counts["bestdiff"].append(nextmovescores[0] - nextmovescores[1])
        else:
            counts["bestdiff"].append(0)

    SVG(chess.svg.board(board=board, size=400))
    fig, ax = plt.subplots()
    ax.plot(counts["scores"])
    ax.grid()
    plt.show()

    import mplcursors

    mplcursors.cursor(hover=True)

