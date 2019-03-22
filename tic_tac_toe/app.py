import json

from flask import Flask, request
from tic_tac_toe.game import Game
from uuid import uuid4

app = Flask("tic-tac-toe")
games = {}

GET = "GET"
POST = "POST"
DELETE = "DELETE"

def pretty_print(data: dict) -> str:
    return json.dumps(data, sort_keys=True, 
                      indent=4, separators=(',', ': '))

@app.route("/")
def hello():
    return "Tic Tac Toe by Ramon Medeiros"


@app.route("/game", methods=[GET, POST])
def game() -> str:
    global games

    if request.method == POST:
        game = Game()
        game_uuid = uuid4().__str__()
        games[game_uuid] = game
        return game_uuid

    elif request.method == GET:
        return pretty_print(games.keys())


@app.route("/game/<uuid>", methods=[GET, DELETE])
def deal_with_game(uuid: str):
    global games
    if request.method == GET:
        return pretty_print(games.get(uuid).get_board())

    elif request.method == DELETE:
        return games.delete(request.form["uuid"])


