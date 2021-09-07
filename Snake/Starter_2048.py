# End of first section
# ###########################################################################################################
# ################################# DO NOT CHANGE ANYTHING ABOVE THIS LINE ##################################    -
# Section 2 -
# ###########################################################################################################


try:
    import termcolor
except ImportError:
    termcolor = None
try:
    from tkinter import *

    # Assigned to None because import was successful but $DISPLAY may not be set
    gui, GUI_runnable, = None, None
except ImportError:
    gui, GUI_runnable, = False, False
# Importing standard libraries
import random
import os
import time
import sys
# import getch
import msvcrt


# ###########################################################################################################
# ################################# DO NOT CHANGE ANYTHING ABOVE THIS LINE ##################################    -
# Section 2 -
# ###########################################################################################################


def get_key_press():
    """Utility function that gets which key was pressed and translates it into its character ascii value - takes no
    arguments """
    # return ord(getch.getch())
    char = msvcrt.getch()
    return char


def clear():
    """Utility function that clears the terminal GUI's screen - takes no arguments"""
    try:
        try:
            # For Macs and Linux
            os.system('clear');
        except:
            # For Windows            REPORTED BUG: Sometimes does not work on 64 bit Windows
            os.system('cls');
    except:
        # If nothing else works, a hacky, non optimal solution
        for i in range(50): print("")


def pause(seconds):
    """
    Utility function that pauses for the given amount of time
    Arg seconds: a float or integer - number of seconds to pause for
    """
    time.sleep(seconds);


def made_move(board):
    for row in board:
        for piece in row:
            if piece != '*':
                return True;
    return False;


def num_pieces(board):
    num_pieces = 0
    for row in board:
        for piece in row:
            if piece != '*':
                num_pieces += 1;
    return num_pieces;


def make_board(N):
    """
    Utility function that returns a new N x N empty board (empty spaces represented by '*')
    Arg N: integer - board dimensions - must be greater than or equal to 1
    """
    assert N >= 1, "Invalid board dimension";
    assert type(N) == int, "N must be an integer";
    return [["*" for x in range(N)] for x in range(N)];


def print_board(board):
    """
    Utility function that prints out the state of the board
    Arg board: board - the board you want to print
    """

    colors = {
        '*': None,
        '2': 'red',
        '4': 'green',
        '8': 'yellow',
        '16': 'blue',
        '32': 'magenta',
        '64': 'cyan',
        '128': 'grey',
        '256': 'white',
        '512': 'green',
        '1024': 'red',
        '2048': 'blue',
        '4096': 'magenta'
    };
    header = "Use the arrows keys to play 2048! Press q to quit";
    print(header);
    N = len(board);
    vertical_edge = "";
    for i in range(N + 2):
        vertical_edge += "-\t";
    print(vertical_edge);
    for y in range(N):
        row = "";
        for x in board[y]:

            # Handling installation fail (no colors printed)
            if termcolor is not None:
                row += termcolor.colored(x, colors[x]);
            else:
                row += x

            row += "\t";
        print("|\t" + row + "|");
        if y is not N - 1: print("")
    print(vertical_edge);

    if GUI_runnable:
        gui.update_grid(board)
        gui.update()


def board_full(board):
    """
    Utility function that returns True if the given board is full and False otherwise
    Arg board: board - the board you want to check
    """

    for row in board:
        for piece in row:
            if piece == '*':  return False;

    return True;


def move_possible(x, y, board):
    """
    Utility function that, given a position, will return True if a move is possible at that (x,y) position and False otherwise
    Arg x: integer - x coordinate
    Arg y: integer - y coordinate
    Arg board: board - the board you wish to check if a move is possible on
    """

    piece_at_xy = starter.get_piece(x, y, board);
    if piece_at_xy == None:
        return False;
    elif piece_at_xy == '*':  # An empty space means a move is always possible
        return True;

    return (
            piece_at_xy == starter.get_piece(x + 1, y, board) or
            piece_at_xy == starter.get_piece(x - 1, y, board) or
            piece_at_xy == starter.get_piece(x, y + 1, board) or
            piece_at_xy == starter.get_piece(x, y - 1, board)
    );


def move(x, y, direction, board):
    """
    Utility function that moves the piece at the position (x,y) on the given board the given direction
    Returns whether an action was actually executed or not
    Arg x: integer - x coordinate
    Arg y: integer - y coordinate
    Arg direction: string - "left", "right", "up", "down"
    Arg board: board - the board you wish to make a move on
    """

    piece_at_xy = starter.get_piece(x, y, board);  # Getting necessary pieces

    assert piece_at_xy != '*', "Error in swipe logic";  # Logical debug case
    valid_direction = (direction == "left" or
                       direction == "right" or
                       direction == "up" or
                       direction == "down");
    assert valid_direction, "Invalid direction passed in";  # Logical debug case

    # The new x and y for the current piece (adjacent's current position) are stored alongside adjacent (fewer ifs + redundant code)
    if direction == "left":
        adjacent = (starter.get_piece(x - 1, y, board), x - 1, y);
    elif direction == "right":
        adjacent = (starter.get_piece(x + 1, y, board), x + 1, y);
    elif direction == "up":
        adjacent = (starter.get_piece(x, y - 1, board), x, y - 1);
    elif direction == "down":
        adjacent = (starter.get_piece(x, y + 1, board), x, y + 1);

    if adjacent[0] == None:  # Edge of the board case (no action taken)
        return False;

    elif piece_at_xy != adjacent[0] and adjacent[0] != '*':  # Can't combine two numbers case (no action taken)
        return False;

    elif adjacent[0] == '*':  # Empty spot adjacent case (recursive movement in direction)
        starter.place_piece('*', x, y, board);
        starter.place_piece(piece_at_xy, adjacent[1], adjacent[2], board);
        move(adjacent[1], adjacent[2], direction, board);
        return True;

    elif piece_at_xy == adjacent[0]:  # Adjacent same numbers case (combine them)
        starter.place_piece('*', x, y, board);
        starter.place_piece(str(int(adjacent[0]) * 2), adjacent[1], adjacent[2], board);
        move(adjacent[1], adjacent[2], direction, board);
        return True;

    else:
        # Logical debug case
        assert False, "No way you should be in here. Error in move logic";

    return False;


# End of utils
############################################################################################################
################################## DO NOT CHANGE ANYTHING BELOW THIS LINE ##################################
############################################################################################################


# You can minimize this class -- it handles the GUI and understanding it, examining it, or using it is not required to complete the project
class gui_2048(Frame):
    """
    The class gui_2048 is a tkinter GUI application that will run along with the main console
    2048 application. The class is initialized along in the main() function and is updated using
    update_grid in the while loop in the main() function.
    """

    def __init__(self, master=None):
        Frame.__init__(self, master)

        # Background and font colors for each number upto 8192.
        self.background_color = {'2': '#EBE1D7', '4': '#ECE0CA', '8': '#F4B176', '16': '#F7975C', '32': '#FA7961',
                                 '64': '#F2613C', '128': '#EBE899', '256': '#F0D069', '512': '#EBE544',
                                 '1024': '#EAC80D', '2048': '#F4FC08', '4096': '#A4FC0D', '8192': '#FC0D64'}
        self.foreground_color = {'2': '#857865', '4': '#857865', '8': '#FDF5E9', '16': '#FDF5E9', '32': '#FDF5E9',
                                 '64': '#FDF5E9', '128': '#FDF5E9', '256': '#FDF5E9', '512': '#FDF5E9',
                                 '1024': '#FDF5E9', '2048': '#FDF5E9', '4096': '#FDF5E9', '8192': '#FDF5E9'}

        # support window resizing
        self.grid(sticky=N + S + E + W)

        # Adding weights to each column in the row so they are resized correctly
        # 6/9/2016 top = self.winfo_toplevel()
        # 6/9/2016 top.rowconfigure(0,weight = 1)
        # 6/9/2016 top.columnconfigure(0,weight = 1)
        # 6/9/2016 self.rowconfigure(0,weight = 1)
        # 6/9/2016 self.columnconfigure(0,weight = 1)

        # Adding the size of the board to create. This may be changed anytime to get a different sized board
        self.board_size = 4

        # matrix_numbers is a list of frames (N x N frames) where N is board_size
        self.matrix_numbers = list()

        # initializing the GUI without any numbers (Starting point)
        self.create_grid(self.board_size)

    def create_grid(self, board_size):

        # creating one frame for the whole window
        f = Frame(self, width=500, height=500, bg='#BBADA0', borderwidth=5)

        # support window resizing each frame
        f.grid(sticky=N + S + E + W)

        # Adding weights to support resizing each frame
        # 6/9/2016 for m in range(int(board_size)):
        # 6/9/2016     f.rowconfigure(m,weight = 1)
        # 6/9/2016     f.columnconfigure(m,weight = 1)

        # Adding frames inside the main frame f for each grid point along with its background and font color
        for i in range(int(board_size)):
            label_row = []
            for j in range(int(board_size)):
                frames = Frame(f, bg='#EEE4DA', height=150, width=150, relief=SUNKEN)
                frames.grid(row=i, column=j, padx=5, pady=5, sticky=N + S + E + W)
                each_label = Label(f, text="", background="#EEE4DA", font=("Arial", 55), justify=CENTER)
                each_label.grid(row=i, column=j, padx=5, pady=5, sticky=N + S + E + W)
                label_row.append(each_label)
            self.matrix_numbers.append(label_row)

    # update function that updates the number matrix after every loop in the main function
    def update_grid(self, board):
        assert len(board) == self.board_size
        for x in range(len(board)):
            for y in range(len(board)):
                if board[x][y] == '*':
                    self.matrix_numbers[x][y].configure(text='', bg='#EEE4DA')
                else:
                    self.matrix_numbers[x][y].configure(text=str(board[x][y]), bg=self.background_color[board[x][y]
                    ], fg=self.foreground_color[board[x][y]])


# You can minimize these classes -- they handle getting user input for a key and understanding it, examining it,
# or using it is not required to complete this project
class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""

    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def getch(self):
        return self()

    def __call__(self):
        return self.impl()


# class _GetchUnix:
#     def __init__(self):
#         import tty, sys
#
#     def __call__(self):
#         import sys, tty, termios
#         fd = sys.stdin.fileno()
#         old_settings = termios.tcgetattr(fd)
#         try:
#             tty.setraw(sys.stdin.fileno())
#             ch = sys.stdin.read(1)
#         finally:
#             termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#         return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


# Check if the environment is GUI-runnable (no import error, GUI is able to initialize) OR if only CLI is supported
script_name = os.path.basename(sys.argv[0])

if GUI_runnable is None and script_name != 'ok':

    try:
        root = Tk()
        gui = gui_2048(root)
        GUI_runnable = True
    except:
        GUI_runnable = False

if getch is None:
    getch = msvcrt.getch()


# Start of Step 0 ###########################################################################################

def main():
    # Creating my new 4x4 board
    board = make_board(4)

    # Getting the game started with a single piece on the board
    place_random(board)
    print_board(board)

    # Runs the game loop until the user quits or the game is lost
    while True:

        # Gets the key pressed and stores it in the key variable
        key = get_key_press()

        # Quit case ('q')
        if key == 113:
            print("Game Finished!")
            quit()

        # Up arrow
        elif key == 65:
            swipe_up(board)

        # Down arrow
        elif key == 66:
            swipe_down(board)

        # Right arrow
        elif key == 67:
            swipe_right(board)

        # Left arrow
        elif key == 68:
            swipe_left(board)

        # Space bar
        elif key == 32:
            swap(board)

        # Check to see if I've lost at the end of the game or not
        if have_lost(board):

            print("You lost! Would you like to play again? (y/n)")
            if input() == 'y':
                main()
            else:
                quit()


# End of Step 0 #############################################################################################


# Start of Step 1 ###########################################################################################

def get_piece(x, y, board):
    """
Utility
function
that
gets
the
piece
at
a
given(x, y)
coordinate
on
the
given
board
Returns
the
piece if the
request
was
valid and None if the
request
was
not valid
Arg
x: integer - x
coordinate
Arg
y: integer - y
coordinate
Arg
board: board - the
board
you
wish
to
get
the
piece
from

"""

    # Ensure that x and y are both integers (use assert)
    assert type(x) == type(y) == int, "Coordinates must be integers"

    # What does this do?
    N = len(board)

    # Checking that the (x,y) coordinates given are valid for the N x N board
    if x >= N or y >= N or x < 0 or y < 0:
        return False
    # Getting the piece on the board
    return board[y][x]


def place_piece(piece, x, y, board):
    """
Utility function that places the piece at a
given(x, y)
coordinate
on
the
given
board if possible
Will
overwrite
the
current
value
at(x, y), no
matter
what
that
piece is
Returns
True if the
piece is placed
successfully and False
otherwise
Arg
piece: string - represents
a
piece
on
the
board('*' is an
empty
piece, '2' '8'
etc.represent
filled
spots)
Arg
x: integer - x
coordinate
Arg
y: integer - y
coordinate
Arg
board: board - the
board
you
wish
to
place
the
piece
on
"""
    # Ensure that x and y are both integers (use assert)
    assert type(x) == type(y) == int, "Coordinates must be integers"

    # What are the dimensions of the board?
    N = len(board)
    # Checking that the (x,y) coordinates given are valid for the board
    if x >= N or y >= N or x < 0 or y < 0:
        return False
    # Placing the piece on the board
    board[y][x] = piece
    return True


# End of Step 1 #############################################################################################


# Start of Step 2 ###########################################################################################

def place_random(board):
    """
Helper
function
which is necessary
for the game to continue playing
Returns
True if a
piece is placed and False if the
board is full
Places
a
2(60 %) or 4(37 %) or 8(3 %)
randomly
on
the
board in an
empty
space
Arg
board: board - the
board
you
wish
to
place
the
piece
on
"""
    # Check if the board is full and return False if it is
    if board_full(board):
        return False

    # random.random() generates a random decimal between [0, 1) ... Multiplying by 100 generates a number between [0,
    # 100)
    generated = random.random() * 100;

    # Assign to_place according to my generated random number

    if generated < 60:  # YOUR CODE HERE (replace -1) <<<<<
        to_place = "2"

    elif generated < 97 and generated >= 60:  # YOUR CODE HERE (replace -1) <<<<<
        to_place = "4"

    else:
        # What should to_place be if it's not a 2 or 4?
        to_place = "8"

    # Variable keeps track of whether a randomly generated empty spot has been found yet
    found = False
    N = len(board)

    while not found:
        # Generate a random (x,y) coordinate that we can try to put our new value in at
        # How did we "generate" a random number earlier? (hint: x and y should be between [0, N) )
        random_y = random.random() * N
        random_x = random.random() * N

        # Think about why this is necessary ( hint: changes 3.4 (float) -> 3 (int) )
        random_y = int(random_y)
        random_x = int(random_x)

        # If the randomly generated coordinates are empty, we have found a spot to place our random piece
        found = get_piece(random_x, random_y, board) == '*'

        # Place the piece at the randomly generated (x,y) coordinate
        place_piece(to_place, random_x, random_y, board)

    return True


# End of Step 2 #############################################################################################


# Start of Step 3 ###########################################################################################

def have_lost(board):
    """
Helper
function
which
checks
at
the
end
of
each
turn if the
game
has
been
lost
Returns
True if the
board is full and no
possible
turns
exist and False
otherwise
Arg
board: board - the
board
you
wish
to
check
for a losing state
"""
    N = len(board)

    # Check every (x,y) position on the board to see if a move is possible
    for y in range(N):
        for x in range(N):
            if move_possible(x, y, board):
                return False

    return True


# End of Step 3 #############################################################################################


# Start of Step 4 ###########################################################################################

def end_move(board):
    """
Prints
the
board
after
a
swipe, pauses
for .2 seconds, places a new random piece and prints the new state of the board
Arg
board: board - the
board
you
're finishing a move on
"""

    # Print the board
    clear()
    print_board(board)

    # Pause for .2 seconds
    pause(.2)

    # Place a random piece on the board at a random (x,y) position
    place_random(board)

    # Print the board again
    clear()
    print_board(board)


# End of Step 4 #############################################################################################


# Start of Step 5 ###########################################################################################

def swipe_left(board):
    """
YOUR
COMMENT
HERE(WHAT
DOES
THIS
FUNCTION
DO?)
Arg
board: board - (WHAT IS A BOARD ARGUMENT?)
"""

    # YOUR COMMENT HERE
    action_taken = False

    # YOUR COMMENT HERE
    N = len(board)

    # YOUR COMMENT HERE
    for y in range(N):
        for x in range(N):
            # YOUR COMMENT HERE
            piece_at_xy = get_piece(x, y, board)
            left_adjacent = get_piece(x - 1, y, board)

            # YOUR COMMENT HERE
            if piece_at_xy == '*':
                continue

            # YOUR COMMENT HERE
            if left_adjacent == None:
                continue

            # YOUR COMMENT HERE
            action_taken = move(x, y, "left", board) or action_taken

    # YOUR COMMENT HERE
    if action_taken:
        end_move(board)


def swipe_right(board):
    action_taken = False

    N = len(board)

    for y in range(N):
        for x in range(N):
            # Don't worry about why this is done (is not needed for up or left)
            x = N - 1 - x

            piece_at_xy = get_piece(x, y, board)
            right_adjacent = get_piece(x + 1, y, board)

            if piece_at_xy == '*':
                continue

            if right_adjacent is None:
                continue

            action_taken = move(x, y, "right", board) or action_taken

    if action_taken:
        end_move(board)


def swipe_up(board):
    action_taken = False

    N = len(board)

    for y in range(N):
        for x in range(N):
            piece_at_xy = get_piece(x, y, board)
            up_adjacent = get_piece(x, y - 1, board)

            if piece_at_xy == '*':
                continue

            if up_adjacent is None:
                continue

            action_taken = move(x, y, "up", board) or action_taken

    if action_taken:
        end_move(board)


def swipe_down(board):
    action_taken = False

    N = len(board)

    for y in range(N):
        # Don't worry about why this is done (is not needed for up or left)
        y = N - 1 - y

        for x in range(N):

            piece_at_xy = get_piece(x, y, board)
            down_adjacent = get_piece(x, y + 1, board)

            if piece_at_xy == '*':
                continue

            if down_adjacent is None:
                continue

            action_taken = move(x, y, "down", board) or action_taken

    if action_taken:
        end_move(board)


# End of Step 5 #############################################################################################


# End of second section
# ###########################################################################################################
# ####################### Optional Challenge -- ATTEMPT AFTER FINISHING PROJECT #############################    -
# Section 3 -
# ###########################################################################################################

def swap(board):
    """
Optional
Challenge: an
addition
to
our
game
that
adds
some
randomness and chance!
Randomly
swaps
2
different
numbers
on
the
board and returns
True if a
swap is performed and False
otherwise
Purpose: allows
you
to
evade
losing
for a little while longer ( if the swap is useful)

Note: have_lost
does
not take
into
account
possible
swaps
that
can
"save the day".This is expected
behavior.
"""

    print("Not implemented yet!")
    return False


def swap_possible(board):
    """
Optional
Challenge: helper
function
for swap
    Returns
    True if a
    swap is possible
    on
    the
    given
    board and False
    otherwise
"""

    print("Not implemented yet!")
    return False


# End of third section
# ###########################################################################################################
# ################################# DO NOT CHANGE ANYTHING BELOW THIS LINE ##################################   -
# Section 4 -
# ###########################################################################################################


# try:
#     from utils import *
# except ImportError:
#     from _2048.utils import *
#
# if __name__ == "__main__":
#     # Only want to see the game board at the top
#     clear();

# Starting the game
main()

# End of fourth section
# End of starter_2048.py
