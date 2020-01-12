import random

import crowns.cards as cards
from crowns.cards import Card, Rank, Suit

def init_deck(hand_size):
    unshuffled = cards.all(hand_size)

    return unshuffled

def shuffle(deck):
    random.shuffle(deck)

def deal(hand_size, count):
    deck = init_deck(hand_size)
    shuffle(deck)

    return set(deck[:count])
