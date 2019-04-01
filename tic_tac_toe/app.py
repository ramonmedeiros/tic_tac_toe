import json

from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from tic_tac_toe.game import Game, APIException, LINE, COLUMN, PLAYER
from tic_tac_toe import log
from uuid import uuid4

app = Flask("tic-tac-toe")
CORS(app)

games = {}

GET = "GET"
POST = "POST"
DELETE = "DELETE"
TITLE = "Tic Tac Toe by Ramon Medeiros"

logger = log.getLogger()
log.set_verbosity(log.DEBUG)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

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
        return game_uuid, 201

    elif request.method == GET:
        return jsonify(list(games.keys()))

    return f"{request.method} not implemented", 405


@app.route("/game/<uuid>", methods=[GET, POST, DELETE])
def deal_with_game(uuid: str):
    global games

    # check if uuid is valid
    this_game = games.get(uuid)

    if this_game is None:
        return "not found", 404

    if request.method == POST:

        if validate_request_json(request) is not True:
            return "invalid params", 404

        rjson = request.json

        if this_game.do_move(rjson[LINE], rjson[COLUMN],
                             rjson[PLAYER]) is True:
            return "moved", 200
        return "failed", 403

    if request.method == GET:
        return jsonify({"board": games.get(uuid).get_board(),
                        "winner": games.get(uuid).get_winner()})

    elif request.method == DELETE:
        return games.delete(request.form["uuid"])

    return f"{request.method} not implemented", 405


def validate_request_json(request):
    if request.is_json is False:
        return False

    rjson = request.json
    if list(rjson.keys()) != [COLUMN, LINE, PLAYER]:
        return False

    if isinstance(rjson[LINE], int) is False:
        raise GameException("Line must be int")

    if isinstance(rjson[COLUMN], int) is False:
        raise GameException("Column must be int")

    return True
