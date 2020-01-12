import random

import crowns.cards as cards
from crowns.cards import Card, Rank, Suit

def init_deck():
    unshuffled = cards.all()

    return unshuffled

def shuffle(deck):
    random.shuffle(deck)

def deal(count):
    deck = init_deck()
    shuffle(deck)

    return set(deck[:count])
