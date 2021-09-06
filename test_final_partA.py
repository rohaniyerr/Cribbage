"""Tests for CS 1 final exam, Fall 2020, part A."""


from final_partA import *
import pytest
import random


def test_same_ranks():
    assert same_ranks([]) == True
    assert same_ranks(['9']) == True
    assert same_ranks(['9', 'A']) == False
    assert same_ranks(['2', '2', '2']) == True
    assert same_ranks(['3', '2', '2']) == False
    assert same_ranks(['J', 'J', 'J', 'J']) == True
    assert same_ranks(['J', 'J', 'J', 'Q']) == False
    assert same_ranks(['A', 'A', 'A', 'A', 'A', 'A']) == True
    assert same_ranks(['A', 'A', '2', 'A', 'A', 'A']) == False


def test_is_straight():
    assert is_straight([]) == True
    assert is_straight(['7']) == True
    assert is_straight(['A', '2']) == True
    assert is_straight(['2', 'A']) == True
    assert is_straight(['A', '2', '3']) == True
    assert is_straight(['Q', 'K', 'A']) == False
    assert is_straight(['K', 'A', '2']) == False
    assert is_straight(['2', 'A', '3']) == True
    assert is_straight(['2', 'A', '3', '3']) == False
    assert is_straight(['5', '9', '7', '8', '6']) == True
    assert is_straight(['5', '5', '9', '7', '8', '6']) == False


def test_evaluate():
    def evaluate_equivalent(got, expected):
        assert type(got) is tuple
        assert len(got) == 2
        # Sanity checks:
        assert type(expected) is tuple
        assert len(expected) == 2

        (gcount, gcodes) = got
        (ecount, ecodes) = expected
        assert gcount == ecount
        gcodes.sort()
        ecodes.sort()
        assert gcodes == ecodes

    evaluate_equivalent(evaluate(['5']), (0, []))
    evaluate_equivalent(evaluate(['10', 'J']), (0, []))
    evaluate_equivalent(evaluate(['J']), (2, ['j']))
    evaluate_equivalent(evaluate(['5', '10']), (2, ['c15']))
    evaluate_equivalent(evaluate(['J', '5']), (2, ['c15']))
    evaluate_equivalent(evaluate(['5', 'J']), (2, ['c15']))
    evaluate_equivalent(evaluate(['5', 'J', '10']), (0, []))
    evaluate_equivalent(evaluate(['5', 'J', '10', '6']), (2, ['c31']))
    evaluate_equivalent(evaluate(['6', '6']), (2, ['k2']))
    evaluate_equivalent(evaluate(['3', '6', '6']), (4, ['c15', 'k2']))
    evaluate_equivalent(evaluate(['6', '6', '6']), (6, ['k3']))
    evaluate_equivalent(evaluate(['9', '6', '6', '6']), (6, ['k3']))
    evaluate_equivalent(evaluate(['6', '6', '6', '6']), (12, ['k4']))
    evaluate_equivalent(evaluate(['A', 'A', '6', '6', '6', '6']),
            (12, ['k4']))
    evaluate_equivalent(evaluate(['2', '3']), (0, []))
    evaluate_equivalent(evaluate(['2', '3', '4']), (3, ['s3']))
    evaluate_equivalent(evaluate(['10', '2', '3', '4']), (3, ['s3']))
    evaluate_equivalent(evaluate(['2', '3', '4', '5']), (4, ['s4']))
    evaluate_equivalent(evaluate(['4', '3', '2', '5']), (4, ['s4']))
    evaluate_equivalent(evaluate(['K', '4', '3', '2', '5']), (4, ['s4']))
    evaluate_equivalent(evaluate(['4', '3', '2', '5', 'A']),
            (7, ['c15', 's5']))
    evaluate_equivalent(evaluate(['4', '3', '2', '5', 'A', '6']), (6, ['s6']))
    evaluate_equivalent(evaluate(['4', '3', '2', '5', 'A', '7', '6']), 
            (7, ['s7']))
    evaluate_equivalent(evaluate(['5', '5', '5']), (8, ['c15', 'k3']))
    evaluate_equivalent(evaluate(['10', 'A', '2', '2']), (4, ['c15', 'k2']))
    evaluate_equivalent(evaluate(['10', '9', '3', '3', '3', '3']),
            (14, ['c31', 'k4']))
    evaluate_equivalent(evaluate(['5', '3', 'A', '2', '4']),
            (7, ['c15', 's5']))

    # Make sure `evaluate` doesn't change the input deck.
    # Use a lot of examples to get many kinds of evaluations.
    for _ in range(1000):
        deck = make_deck()
        deck_copy = deck[:]
        evaluate(deck)  # ignore return value
        assert deck == deck_copy


def test_make_deck():
    # NOTE: We can't test this very well without using `validate_deck`,
    # and we don't want to give that code here,
    # so take this test with a grain of salt.
    for _ in range(20):
        deck = make_deck()
        assert type(deck) is list
        assert len(deck) == 52


def test_validate_deck():
    with pytest.raises(InvalidDeck):
        validate_deck('A')

    with pytest.raises(InvalidDeck):
        validate_deck(['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'])

    with pytest.raises(InvalidDeck):
        validate_deck(['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'F'])

    with pytest.raises(InvalidDeck):
        validate_deck(['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'Q'])

    d = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    # Make sure `validate_deck` doesn't change the input deck.
    d_copy = d[:]
    validate_deck(d)
    assert d == d_copy


def test_save_deck():
    for _ in range(10):
        deck = make_deck()
        save_deck(deck, 'my_deck')
        deck2 = load_deck('my_deck')
        assert deck == deck2

    # Make sure `save_deck` doesn't change `deck`.
    for _ in range(10):
        deck = make_deck()
        deck_copy = deck[:]
        save_deck(deck, 'my_deck')
        assert deck == deck_copy

    # Make sure you can't save bogus decks.
    with pytest.raises(InvalidDeck):
        save_deck('A', 'my_deck')
    deck = make_deck()
    deck.pop()
    with pytest.raises(InvalidDeck):
        save_deck(deck, 'my_deck')
    deck = make_deck()
    deck[0] = 'F'
    with pytest.raises(InvalidDeck):
        save_deck(deck, 'my_deck')
    deck = make_deck()
    for i in range(52):
        deck[i] = 'A'
    with pytest.raises(InvalidDeck):
        save_deck(deck, 'my_deck')


def test_load_deck():
    deck = load_deck('decks/test_deck_A')
    assert deck == ['J', '6', 'J', '6', '7', '2', '5', '8', '2', '8', '8', '3', '10', '4', 'Q', '5', '5', '7', '6', '7', 'K', 'K', '9', '6', 'A', 'A', '2', '4', '4', '3', '10', '2', 'Q', 'A', 'K', '10', 'A', '9', 'Q', 'Q', '4', 'J', '3', 'J', 'K', '7', '8', '9', '5', '9', '10', '3']
    deck = load_deck('decks/test_deck_B')
    assert deck == ['10', '2', 'A', 'A', '7', '5', '3', 'K', '8', '9', 'Q', '7', '8', '4', '4', 'K', '5', 'J', '3', '5', '9', '10', '10', 'Q', '4', 'J', '6', '3', '8', '7', '6', '5', '6', 'J', '4', 'Q', 'A', '6', 'K', '2', '2', '10', '9', 'A', '3', '2', 'K', '9', '8', 'J', '7', 'Q']
    deck = load_deck('decks/test_deck_C')
    assert deck == ['J', 'K', '9', '6', '4', '4', '4', '9', '5', '6', '9', '3', 'A', 'A', 'Q', '8', '2', 'K', '7', '8', 'K', '8', '5', 'K', '6', '10', '2', '7', 'Q', '7', '7', '3', 'A', '5', '10', 'J', '6', 'J', '2', 'A', '10', '4', '5', '10', '2', 'J', '9', '3', '3', '8', 'Q', 'Q']
    deck = load_deck('decks/test_deck_D')
    assert deck == ['J', 'K', 'Q', 'K', '6', '6', '9', '2', 'K', 'J', '5', '4', '4', 'A', '9', '10', '3', 'Q', '10', '7', '4', '8', '8', 'K', '9', '3', '6', 'A', '7', 'J', '8', 'Q', '10', '3', '2', '4', '5', '6', 'A', '8', '2', '7', '5', 'Q', '5', 'J', 'A', '3', '2', '10', '9', '7']
