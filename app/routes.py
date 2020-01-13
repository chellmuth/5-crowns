from flask import Flask
from flask import render_template

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

    dealer = Dealer(hand_size, wilds=False)
    hand = dealer.deal()

    current_configuration = scoring.find_best_configuration(hand, wilds)

    simulated = simulation.simulate(hand, wilds)

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

@app.route("/play")
def play():
    hand_size = 6

    dealer = Dealer(hand_size)
    hand = dealer.deal()

    game = {
        "hand": [
            card_to_fragment(card)
            for card in cards.sort(hand)
        ],
        "wilds": hand_size - len(hand),
    }

    return render_template("play.html", game=game)

if __name__ == '__main__':
    app.run()
