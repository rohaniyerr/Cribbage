# Rohan Iyer
# riiyer@caltech.edu
"""
CS 1, Fall 2020.

Final exam, part A.
"""

import random


# Card ranks.
valid_ranks = \
    ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']


# Category codes for cribbage point types.
category_codes = {
    'j': 'initial jack (2 points)',
    'c15': '15 count (2 points)',
    'c31': '31 count (2 points)',
    's3': '3 card straight (3 points)',
    's4': '4 card straight (4 points)',
    's5': '5 card straight (5 points)',
    's6': '6 card straight (6 points)',
    's7': '7 card straight (7 points)',
    'k2': '2 of a kind (2 points)',
    'k3': '3 of a kind (6 points)',
    'k4': '4 of a kind (12 points)'
}


# Order of each rank.
rank_order = {
   'A': 1, '2': 2, '3': 3, '4': 4,
   '5': 5, '6': 6, '7': 7, '8': 8,
   '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13
}


# Point value of each rank.
rank_count = {
   'A': 1, '2': 2, '3': 3, '4': 4,
   '5': 5, '6': 6, '7': 7, '8': 8,
   '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10
}


# One-character representation of each rank.
rank_rep = {
   'A': 'A', '2': '2', '3': '3', '4': '4',
   '5': '5', '6': '6', '7': '7', '8': '8',
   '9': '9', '10': '0', 'J': 'J', 'Q': 'Q', 'K': 'K'
}


class InvalidDeck(Exception):
    """Exception class for invalid card decks (ranks only)."""

    pass


def same_ranks(ranks):
    """Return True if the cards in a list of ranks are all of the same rank."""
    if ranks == []:
        return True
    rank = ranks[0]
    for elt in ranks:
        if elt != rank:
            return False
    return True


def is_straight(ranks):
    """Return `True` if the card ranks form a linear sequence.

    A linear sequence means a sequence of consecutive card ranks
    with no gaps.  The rank sequence is: A, 2, 3, ... 10, J, Q, K.
    The order of the cards is unimportant.
    """
    sorted_ranks = []
    if ranks == []:
        return True
    for card in ranks:
        if card in rank_order:
            sorted_ranks.append(rank_order[card])
    sorted_ranks.sort()
    first_card = sorted_ranks[0]
    for elt in sorted_ranks[1::]:
        if elt != first_card + 1:
            return False
        else:
            first_card = elt
    return True


def evaluate(stack):
    """Return the number of points gained from the last card in the stack.

    Arguments:
    - stack: a list of card ranks

    Return value: a 2-tuple of
    - the points gained from the last card in the stack
    - a list of tags of the cribbage point types from the last card
      in the stack.
    """
    points = 0
    combo = []
    # Check if 'j' is the first element
    if stack[0] == 'J' and len(stack) == 1:
        combo.append('j')
        points += 2
    # Check if count gets to 15 or 31
    sorted_ranks = []
    for card in stack:
        if card in rank_count:
            sorted_ranks.append(rank_count[card])
    if sum(sorted_ranks) == 15:
        combo.append('c15')
        points += 2
    elif sum(sorted_ranks) == 31:
        combo.append('c31')
        points += 2
    # Check if the stack has a straight
    if len(stack) in range(3, 8):
        for num in range(7, 2, -1):
            if is_straight(stack[-num:]) and len(stack) >= num:
                combo.append('s{n}'.format(n=num))
                points += num
                break
    # Check if the stack has a pair
    if same_ranks(stack[-4:]) and len(stack) > 3:
        combo.append('k4')
        points += 12
    elif same_ranks(stack[-3:]) and len(stack) > 2:
        combo.append('k3')
        points += 6
    elif same_ranks(stack[-2:]) and len(stack) > 1:
        combo.append('k2')
        points += 2
    return (points, combo)


def make_deck():
    """Return a shuffled "deck" of 52 cards (ranks only)."""
    deck = 4 * valid_ranks
    random.shuffle(deck)
    return deck


def validate_deck(cards):
    """
    Validate a deck of cards (ranks only).

    If the deck is not valid, raise an InvalidDeck exception
    with a meaningful error message.
    """
    if type(cards) is not list:
        raise InvalidDeck(f'expected a list; got {cards}')
    elif len(cards) != 52:
        raise InvalidDeck(f'expected exactly 52 cards in list; ' +
                          f'got {len(cards)}')
    for card in cards:
        if type(card) is not str or card not in valid_ranks:
            raise InvalidDeck(f'expected a valid rank; got {card}')
        elif cards.count(card) != 4:
            raise InvalidDeck(f'expected 4 cards of rank {card}; ' +
                              f'got {cards.count(card)}')


def save_deck(deck, filename):
    """Save a full deck to a file with the name `filename`."""
    validate_deck(deck)
    with open(filename, 'w') as f:
        content = " ".join(deck)
        f.write(content)


def load_deck(filename):
    """Load the deck."""
    with open(filename) as f:
        lst_lines = []
        for line in f:
            lst_lines.append(line.rstrip('\n').upper().split())
        deck = [item for line in lst_lines for item in line]
    return deck
