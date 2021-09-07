

class ChessPiece:

    def __init__(self, colour, type):
        self.colour = colour
        self._type = type
        self.move_no = 0

    def move(self, move_type):
        print(f'I have moved {self.move_no}!')
        print(f'You have made a {move_type}')
        self.move_no += 1


if __name__ == '__main__':
    piece_1 = ChessPiece('black', 'knight')
    piece_2 = ChessPiece('white', 'pawn')