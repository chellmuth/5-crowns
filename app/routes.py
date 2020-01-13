from flask import Flask, render_template, request

import crowns.cards as cards
import crowns.decision as decision
import crowns.scoring as scoring
import crowns.simulation as simulation
from crowns.cards import Rank, Suit
from crowns.game.dealer import Dealer

from app import app

def card_to_fragment(card):
    if card == "*": return "*"

    ranks = {
        Rank.Three: "3",
        Rank.Four: "4",
        Rank.Five: "5",
        Rank.Six: "6",
        Rank.Seven: "7",
        Rank.Eight: "8",
        Rank.Nine: "9",
        Rank.Ten: "T",
        Rank.Jack: "J",
        Rank.Queen: "Q",
        Rank.King: "K",
    }

    suits = {
        Suit.Spades: '<span class="spades">&spades;</span>',
        Suit.Hearts: '<span class="hearts">&hearts;</span>',
        Suit.Clubs: '<span class="clubs">&clubs;</span>',
        Suit.Diamonds: '<span class="diamonds">&diams;</span>',
        Suit.Stars: '<span class="stars">&#9733;</span>',
    }

    return f"{ranks[card.rank]}{suits[card.suit]}"

def configuration_view(configuration):
    return {
        "score": configuration.score,
        "matches": [
            [
                card_to_fragment(card)
                for card in cards.sort(match.cards)
            ] + [ "*" for _ in range(match.wilds) ]
            for match in configuration.matches
        ],
        "remaining": [ card_to_fragment(card) for card in configuration.remaining ]
    }

def build_histogram(scores):
    import matplotlib.pyplot as plt

    fig = plt.figure()

    ax = fig.add_subplot(111, facecolor="white")
    ax.hist(
        scores,
        density=True,
        histtype='stepfilled',
        fc='lightblue',
        edgecolor="darkblue",
        alpha=1.
    )

    ax.grid(True, color="#cccccc", linestyle="dashed")
    ax.set_axisbelow(True)

    from io import BytesIO
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)  # rewind to beginning of file

    import base64
    figdata_png = base64.b64encode(figfile.getvalue())
    return figdata_png

@app.route('/')
def hello_world():
    hand_size = 6
    wilds = 1

    dealer = Dealer(hand_size, include_wilds=False)
    hand = dealer.deal()

    current_configuration = scoring.find_best_configuration(set(hand), wilds)

    simulated = simulation.simulate(set(hand), wilds)

    game = {
        "hand": [
            card_to_fragment(card)
            for card in cards.sort(hand)
        ],
        "wilds": wilds,
        "scenarios": [
            (
                card_to_fragment(draw),
                configuration_view(configuration),
                configuration.score
            )
            for draw, configuration
            in simulated["scenarios"]
        ],
        "wild_configuration": configuration_view(simulated["wild_configuration"]),
        "expected_score": simulated["expected_score"],
        "current_configuration": configuration_view(current_configuration),
        "scores": simulated["scores"],
        "chart_embed": build_histogram(simulated["scores"]).decode('utf8')
    }

    return render_template('index.html', game=game)


class Game:
    def __init__(self, hand_size):
        self.hand_size = hand_size
        self.dealer = Dealer(hand_size)
        self.hand = cards.sort(self.dealer.deal())
        self.wilds = self.hand_size - len(self.hand)
        self.out = self._check_out()

    def draw(self):
        self.dealer.draw(self.hand)
        self.hand = cards.sort(self.hand)
        self.wilds = (self.hand_size + 1) - len(self.hand)

    def discard(self, index):
        self.hand.pop(index)
        self.out = self._check_out()
        self.dealer.fake_discard()

    def _check_out(self):
        configuration = scoring.find_best_configuration(
            set(self.hand),
            self.wilds
        )
        return configuration.score == 0

    @property
    def discard_top(self):
        return self.dealer.discard

current_game = Game(3)

def render_game(game):
    game_view = {
        "hand": [
            card_to_fragment(card)
            for card in cards.sort(game.hand)
        ],
        "wilds": game.wilds,
        "out": game.out,
        "discard_top": card_to_fragment(game.discard_top)
    }

    return render_template("play.html", game=game_view)

@app.route("/play", methods=["GET"])
def play():
    global current_game
    return render_game(current_game)

@app.route("/play", methods=["POST"])
def make_move():
    global current_game

    move = request.form["move"]
    if move == "draw":
        current_game.draw()
    elif move.startswith("discard-"):
        verb, index_str = move.split("-")
        index = int(index_str)
        current_game.discard(index)

    return render_game(current_game)

if __name__ == '__main__':
    app.run()
