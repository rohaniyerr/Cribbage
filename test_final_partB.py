"""Tests for CS 1 final exam, Fall 2020, part B."""


import final_partA
from final_partA import InvalidDeck
from final_partB import *
import random
import pytest


ok_deckfiles = [
    'decks/test_deck_A',
    'decks/test_deck_B',
    'decks/test_deck_C',
    'decks/test_deck_D',
    'decks/test_deck_E',
    'decks/test_deck_F'
]


bad_deckfiles = [
    'decks/invalid_deck_A',
    'decks/invalid_deck_B',
    'decks/invalid_deck_C',
]


def test_load():
    for deckfile in ok_deckfiles:
        cs = CribbageSolitaire()
        cs.load(deckfile)
        assert cs.stack == []
        assert cs.count == 0
        assert cs.points == 0
        assert cs.history == []
        assert type(cs.cols) is list
        assert len(cs.cols) == 4
        for col in cs.cols:
            assert type(col) is list
            assert len(col) == 13
            for card in col:
                c1 = card in ['A', 'J', 'Q', 'K']
                try:
                    c2 = 2 <= int(card) <= 10
                except ValueError:
                    c2 = False
                assert c1 or c2

    for deckfile in bad_deckfiles:
        cs = CribbageSolitaire()
        with pytest.raises((final_partA.InvalidDeck, InvalidDeck)):
            cs.load(deckfile)


def test_legal_moves():
    cs = CribbageSolitaire()
    cs.load('decks/test_deck_A')
    assert cs.legal_moves() == [0, 1, 2, 3]
    assert cs.cols == \
        [['J', '6', 'J', '6', '7', '2', '5', '8', '2', '8', '8', '3', '10'],
         ['4', 'Q', '5', '5', '7', '6', '7', 'K', 'K', '9', '6', 'A', 'A'],
         ['2', '4', '4', '3', '10', '2', 'Q', 'A', 'K', '10', 'A', '9', 'Q'],
         ['Q', '4', 'J', '3', 'J', 'K', '7', '8', '9', '5', '9', '10', '3']]
    assert cs.make_move(0) == []
    assert cs.make_move(2) == []
    assert cs.make_move(2) == []
    assert cs.stack == ['10', 'Q', '9']
    assert cs.count == 29
    assert cs.legal_moves() == [1, 2]
    assert cs.cols == \
        [['J', '6', 'J', '6', '7', '2', '5', '8', '2', '8', '8', '3'],
         ['4', 'Q', '5', '5', '7', '6', '7', 'K', 'K', '9', '6', 'A', 'A'],
         ['2', '4', '4', '3', '10', '2', 'Q', 'A', 'K', '10', 'A'],
         ['Q', '4', 'J', '3', 'J', 'K', '7', '8', '9', '5', '9', '10', '3']]
    assert cs.make_move(2) == []
    assert cs.legal_moves() == [1]
    assert cs.count == 30
    codes = cs.make_move(1)
    codes.sort()
    assert codes == ['c31', 'k2']
    assert cs.stack == ['10', 'Q', '9', 'A', 'A']
    assert cs.count == 31
    assert cs.legal_moves() == []


def test_make_move():
    cs = CribbageSolitaire()
    cs.load('decks/test_deck_B')
    assert cs.count == 0
    assert cs.points == 0
    assert cs.stack == []

    with pytest.raises(InvalidMove):
        cs.make_move(100)

    assert cs.make_move(1) == ['j']
    assert cs.count == 10
    assert cs.points == 2
    assert cs.stack == ['J']
    assert cs.history == [('J', 1, [], 0, 0)]

    assert cs.make_move(3) == []
    assert cs.count == 20
    assert cs.points == 2
    assert cs.stack == ['J', 'Q']
    assert cs.history == [('J', 1, [], 0, 0), ('Q', 3, ['J'], 10, 2)]

    assert cs.make_move(2) == ['s3']
    assert cs.count == 30
    assert cs.points == 5
    assert cs.stack == ['J', 'Q', 'K']
    assert cs.history == [('J', 1, [], 0, 0), ('Q', 3, ['J'], 10, 2), ('K', 2, ['J', 'Q'], 20, 2)]

    # Move 1 would make the stack count too big.
    with pytest.raises(InvalidMove):
        cs.make_move(1)

    assert cs.points == 5
    cs.stack = []
    cs.count = 0

    assert cs.make_move(0) == []
    assert cs.make_move(3) == ['c15']
    assert cs.make_move(2) == ['s3']
    assert cs.history == \
        [('J', 1, [], 0, 0),
         ('Q', 3, ['J'], 10, 2),
         ('K', 2, ['J', 'Q'], 20, 2),
         ('8', 0, [], 0, 5),
         ('7', 3, ['8'], 8, 5),
         ('6', 2, ['8', '7'], 15, 7)]
    assert cs.count == 21
    assert cs.points == 10
    assert cs.stack == ['8', '7', '6']


def test_undo_move():
    cs = CribbageSolitaire()
    cs.load('decks/test_deck_C')
    assert cs.history == []
    cs.undo_move()
    assert cs.history == []

    assert cs.make_move(1) == []
    assert cs.history == [('10', 1, [], 0, 0)]

    assert cs.make_move(3) == []
    assert cs.history == [('10', 1, [], 0, 0), ('Q', 3, ['10'], 10, 0)]

    assert cs.make_move(2) == []
    assert cs.history == [('10', 1, [], 0, 0), ('Q', 3, ['10'], 10, 0), ('2', 2, ['10', 'Q'], 20, 0)]
    assert cs.stack == ['10', 'Q', '2']
    assert cs.count == 22

    cs.undo_move()
    assert cs.history == [('10', 1, [], 0, 0), ('Q', 3, ['10'], 10, 0)]
    assert cs.stack == ['10', 'Q']
    assert cs.count == 20

    cs.undo_move()
    assert cs.history == [('10', 1, [], 0, 0)]
    assert cs.stack == ['10']
    assert cs.count == 10

    assert cs.make_move(3) == []
    assert cs.make_move(3) == ['k2']
    assert cs.stack == ['10', 'Q', 'Q']
    assert cs.count == 30

    assert cs.make_move(0) == ['c31']
    assert cs.stack == ['10', 'Q', 'Q', 'A']
    assert cs.count == 31


def test_save_moves():
    cs = CribbageSolitaire()
    cs.load('decks/test_deck_D')
    assert cs.make_move(0) == []
    assert cs.make_move(0) == ['k2']
    assert cs.make_move(3) == ['c15']
    assert cs.make_move(2) == []
    assert cs.make_move(2) == []
    assert cs.make_move(2) == []
    assert cs.make_move(2) in [['c31', 's3'], ['s3', 'c31']]
    assert cs.count == 31
    cs.stack = []
    cs.count = 0
    assert cs.make_move(1) == []
    assert cs.make_move(1) == []
    assert cs.make_move(3) == ['k2']
    assert cs.make_move(3) == ['c31']
    cs.save_moves('moves.out')
    with open('moves.out') as moves_file:
        lines = moves_file.readlines()
        lines = list(map(lambda s: s.split(), lines))
        assert lines == \
            [['0', '0', '3', '2'],
             ['2', '2', '2', '1'],
             ['1', '3', '3']]


def test_best_moves():
    cs = CribbageSolitaire()
    cs.load('decks/test_deck_E')

    lm = cs.legal_moves()
    assert lm == [0, 1, 2, 3]
    assert cs.best_moves([0]) == [0]
    assert cs.best_moves(lm) == [0, 1, 2, 3]

    assert cs.make_move(3) == []
    lm = cs.legal_moves()
    assert lm == [0, 1, 2, 3]
    assert cs.best_moves(lm) == [3]

    assert cs.make_move(3) == ['k2']
    lm = cs.legal_moves()
    assert lm == [0, 1, 2, 3]
    assert cs.best_moves(lm) == [0, 1, 2, 3]

    assert cs.make_move(2) == []
    assert cs.count == 25
    lm = cs.legal_moves()
    assert lm == [0, 1]
    assert cs.best_moves([0, 1]) == [1]

    assert cs.make_move(1) == ['c31']
