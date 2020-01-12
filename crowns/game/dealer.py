import itertools
import random

from crowns.cards import Card, Rank, Suit

def init_deck():
    unshuffled = [
        Card(*card)
        for card
        in itertools.product(Suit, Rank)
    ]

    return unshuffled

def shuffle(deck):
    random.shuffle(deck)

def deal(count):
    deck = init_deck()
    shuffle(deck)

    return deck[:count]
