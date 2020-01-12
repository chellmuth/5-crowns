from flask import Flask

import crowns.game.dealer as dealer

app = Flask(__name__)

@app.route('/')
def hello_world():
    hand = dealer.deal(6)
    return str(hand)

if __name__ == '__main__':
    app.run()
