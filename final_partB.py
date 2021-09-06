"""
CS 1, Fall 2020.

Final exam, part B.
"""
#python final_partB.py autoplay
#python final_partB.py autoreplay decks/test_deck_A
import random
import sys


from final_partA import *


class InvalidMove(Exception):
    """Exception class raised when an invalid move is attempted."""

    pass


class CribbageSolitaire:
    """Cribbage Solitaire interactive player and autosolver."""

    def __init__(self):
        """Initialize this object."""
        deck = make_deck()
        save_deck(deck, 'deck.out')
        self.cols = [deck[:13], deck[13:26], deck[26:39], deck[39:]]
        self.stack = []
        self.count = 0
        self.points = 0
        self.history = []

    def __str__(self):
        """Convert the layout to a string for printing."""
        s = '\n   0  1  2  3\n'
        s += '+-------------+\n'
        for i in range(13):
            s += '| '
            for col in range(4):
                if len(self.cols[col]) > i:
                    contents = self.cols[col][i]
                else:
                    contents = '  '
                s += f'{contents:>2s} '
            s += '|\n'
        s += '+-------------+\n'
        return s

    def load(self, filename):
        """
        Load a deck from a file.

        Read the deck's card ranks from the file,
        validate the deck, use it to initialize the columns,
        and reset the other fields of the object.

        Arguments:
        - filename: the name of the deck file to load

        Return value: none
        """
        deck = load_deck(filename)
        validate_deck(deck)
        self.cols = [deck[:13], deck[13:26], deck[26:39], deck[39:]]
        self.stack = []
        self.count = 0
        self.points = 0
        self.history = []

    def legal_moves(self):
        """
        Return a list of column indices of all legal moves.

        The returned move list should be sorted in ascending order.
        """
        legal_moves = []
        for index, col in enumerate(self.cols):
            if col != []:
                if self.count + rank_count[col[-1]] <= 31:
                    legal_moves.append(index)
        return legal_moves

    def make_move(self, i):
        """
        Play the bottom card of column `i`.

        Add the points gained from playing the card.
        Save undo information.
        Raise `InvalidMove` if
        * the column index is invalid
        * the column is empty
        * the move can't be made without making the count go above 31.

        Arguments:
        - i: the column index

        Return value:
        - the list of category codes which represent
          the card configurations achieved by playing this card

        Assumption:
            This method assumes that `i` represents the index
            of a non-empty column whose last card can legally
            be played.
        """
        if i not in range(0, 4):
            raise InvalidMove(f'column index {i} is invalid')
        elif self.cols == []:
            raise InvalidMove(f'column index {i} is invalid')
        elif self.count + rank_count[self.cols[i][-1]] > 31:
            raise InvalidMove(f'column {i} card would make count go over 31')
        last_card = self.cols[i].pop()
        stack_copy = self.stack.copy()
        state = (last_card, i, stack_copy, self.count, self.points)
        self.history.append(state)
        self.stack.append(last_card)
        self.count += rank_count[last_card]
        points, combo = evaluate(self.stack)
        self.points += points
        return combo

    def undo_move(self):
        """Undo the last move, restoring the previous state."""
        if self.history:
            rank, index, stack, count, points = self.history.pop()
            self.cols[index].append(rank)
            self.count = count
            self.points = points
            self.stack = stack

    def save_moves(self, filename):
        """
        Save the moves of a game (column indices) to a file.

        Arguments:
        - filename: the name of the file to save the moves to.

        Return value: none
        """
        line = ''
        with open(filename, 'w') as f:
            for i in range(len(self.history)):
                line += str(self.history[i][1]) + ' '
                if (i + 1) % 4 == 0:
                    line = line[:-1]
                    line += '\n'
            f.write(line)

    def best_moves(self, moves):
        """
        Return the best of a list of moves.

        The "best" move is the one that, when played, improves the score the
        most.  There can be more than one such move.
        If no move improves the score, or if all moves improve the score
        by the same amount, return the entire list.

        This method assumes that the list of moves
        doesn't contain an illegal move.

        The game state is not changed by this method.

        Arguments:
        - moves: a list of moves (column indices)

        Return value: a list of the best moves
        """
        points = []
        if len(moves) in range(2):
            return moves
        for move in range(4):
            if move in moves:
                self.make_move(move)
                points.append(self.points)
                self.undo_move()
            else:
                points.append(0)
        best_moves = [i for i, x in enumerate(points) if x == max(points)]
        return best_moves

    def get_move(self, moves):
        """
        Interactively pick one of a set of legal moves.

        Argument:
        - moves: a list of ints representing all legal moves

        Return value: one of
        - one of the list of ints
        - the string 'q' (for "quit")
        - the string 'u' (for "undo")
        """
        print(f'Legal moves: {moves}')
        move = None
        while move not in moves:
            move = input('Enter move: ')
            # Handle one-character special "moves".
            if move in ['q', 'u']:
                return move
            try:
                move = int(move)
                if move not in moves:
                    print(f'Error: move {move} is not in ' +
                          f'list of moves {moves}')
                    move = None
            except ValueError:
                print('Error: invalid move entered.')
                move = None
        return move

    def game_over(self):
        """Return `True` if the game is over."""
        return self.cols == [[], [], [], []]

    def dump(self):
        """Print information about the current game."""
        print(self)
        print(f'STACK: {self.stack}')
        print(f'POINTS: {self.points}')
        print(f'COUNT: {self.count}')
        print()

    def win_or_lose(self):
        """Print a message telling whether the player won or lost."""
        if self.game_over():
            if self.points >= 61:
                print('You win!  Congratulations, well played!')
            else:
                print('Sorry, you lose.  Better luck next time.')
        else:
            print('The game is not over yet.  Keep playing!')

    def pause(self):
        """
        Pause so user can read the output.

        The user hits the return key to continue.
        If the user enters the 'q' key, the program exits.
        """
        while True:
            answer = input('Press <return> to continue... ')
            if answer == '':
                break
            elif answer == 'q':
                quit()

    def autoplay(self, verbose=True, pause=False):
        """Automatically play a game until finished.

        Argument:
        - verbose: if `True`, print extra information after a move
        - pause: if `True`, pause after printing move info.

        Return value: none
        """
        while not self.game_over():
            self.dump()
            moves = self.legal_moves()
            print(f'MOVES: {moves}')
            if not moves:
                print('No moves; starting a new stack...')
                # empty the stack, zero the count
                self.stack = []
                self.count = 0
                continue
            best = self.best_moves(moves)
            move = random.choice(best)
            print(f'MOVE: {move}')
            codes = self.make_move(move)
            if codes and verbose:
                print(f'Stack after move: {self.stack}')
                for code in codes:
                    print(f'+++ {category_codes[code]}')
            if pause:
                self.pause()
        self.dump()
        print(f'TOTAL POINTS: {self.points}')
        self.win_or_lose()
        self.save_moves('moves.out')

    def play(self):
        """Interactively play a game until finished."""
        while not self.game_over():
            self.dump()
            moves = self.legal_moves()
            if not moves:
                # empty the stack, zero the count
                print('No moves; starting a new stack...')
                self.stack = []
                self.count = 0
                self.pause()
                continue
            move = self.get_move(moves)
            if move == 'q':
                return
            elif move == 'u':
                if self.history == []:
                    print('no history to undo!')
                else:
                    print('undoing last move...')
                    self.undo_move()
            else:
                codes = self.make_move(move)
                if codes:
                    print(f'Stack after move: {self.stack}')
                    for code in codes:
                        print(f'+++ {category_codes[code]}')
        self.dump()
        print(f'TOTAL POINTS: {self.points}')
        self.win_or_lose()
        self.save_moves('moves.out')


if __name__ == '__main__':
    try:
        args = sys.argv[1:]
        cs = CribbageSolitaire()
        if len(args) == 0:
            cs.play()
        elif len(args) == 1 and args[0] == 'autoplay':
            cs.autoplay(verbose=True, pause=True)
        elif len(args) == 2 and args[0] == 'replay':
            cs.load(args[1])
            cs.play()
        elif len(args) == 2 and args[0] == 'autoreplay':
            cs.load(args[1])
            cs.autoplay()
    except InvalidDeck as e:
        print(f'Error (invalid deck): {e}')
        quit(1)
