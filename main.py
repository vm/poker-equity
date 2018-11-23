from itertools import product, combinations

from funcy import rcompose, partial, rpartial

from models import Suit, Rank, Card, Hand


BOARD_SIZE = 5
CARDS = set(map(lambda x: Card(*x), product(list(Rank), list(Suit))))


def generate_boards(pocket, current_board):
    remaining_cards = CARDS - set(current_board) - set(pocket)
    return rcompose(
        rpartial(combinations, BOARD_SIZE - len(current_board)),
        partial(
            map,
            lambda remaining_board: current_board + list(remaining_board)),
        partial(sorted, reverse=True))(remaining_cards)


def generate_hands(pocket, board):
    return lmap(
        lambda hand: Hand(sorted(hand, reverse=True)),
        combinations(pocket + board, 5))
