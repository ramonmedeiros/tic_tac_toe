import json

from flask import Flask, request, make_response
from tic_tac_toe.game import Game
from tic_tac_toe import log
from uuid import uuid4

app = Flask("tic-tac-toe")
games = {}

GET = "GET"
POST = "POST"
DELETE = "DELETE"

TITLE = "Tic Tac Toe by Ramon Medeiros"

# do move params
LINE = "line"
COLUMN = "column"
PLAYER = "player"

logger = log.getLogger()


def pretty_print(data: dict) -> str:
    return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))


@app.route("/")
def hello():
    return TITLE


@app.route("/game", methods=[GET, POST])
def game():
    global games

    if request.method == POST:
        game = Game()
        game_uuid = uuid4().__str__()
        games[game_uuid] = game
        return make_response(game_uuid, 201)

    elif request.method == GET:
        return pretty_print(games.keys())

    return make_response(f"{request.method} not implemented", 405)


@app.route("/game/<uuid>", methods=[GET, POST, DELETE])
def deal_with_game(uuid: str):
    global games
    if request.method == GET:
        return pretty_print(games.get(uuid).get_board())

    elif request.method == DELETE:
        return games.delete(request.form["uuid"])


