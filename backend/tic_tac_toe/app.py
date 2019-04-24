import json

from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from tic_tac_toe.game import Game, APIException, LINE, COLUMN, PLAYER, TOKEN
from tic_tac_toe import log
from uuid import uuid4

app = Flask("tic-tac-toe")
CORS(app)

games = {}
users = {}

GET = "GET"
POST = "POST"
DELETE = "DELETE"
TITLE = "Tic Tac Toe by Ramon Medeiros"
USERNAME = "username"

logger = log.getLogger()
log.set_verbosity(log.DEBUG)


@app.before_request
def only_json():
    if request.method == POST and not request.is_json: 
        return "not json", 400


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/")
def hello():
    return TITLE

@app.route("/login", methods=[POST])
def login():
    global users
    rjson = request.json
    if validate_params(rjson, [USERNAME]) is False or len(rjson.get(USERNAME)) == 0:
        return "invalid or inexistent username", 404
    user = rjson[USERNAME]
    
    token = uuid4().__str__()
    users[token] = user
    return jsonify({TOKEN:token})

@app.route("/logout", methods=[POST])
def logout():
    rjson = request.json
    if validate_params(rjson, [TOKEN, USERNAME]) is False or len(rjson.get(USERNAME)) == 0:
        return "invalid or inexistent username", 404

    user = rjson[USERNAME]
    token = rjson[TOKEN]
    
    if validate_user(user, token) is True:
        users.pop(token)
        return "accepted", 200

    return "not found", 404
 

@app.route("/game", methods=[GET, POST])
def game():
    global games

    if request.method == POST:
        if TOKEN not in request.json:
            return "expected token", 404

        token = request.json[TOKEN]
        if users.get(token) == None:
            return "invalid token", 404

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

        rjson = request.json
        if validate_request_json(rjson) is not True:
            return "invalid params", 406

        if this_game.do_move(rjson[LINE], rjson[COLUMN],
                             rjson[TOKEN]) is True:
            return "moved", 200
        return "failed", 403

    if request.method == GET:
        return jsonify({
            "board": this_game.get_board(),
            "winner": this_game.get_winner(),
            "players": this_game.get_players()
        })

    elif request.method == DELETE:
        return games.delete(request.form["uuid"])

    return f"{request.method} not implemented", 405

@app.route("/game/<uuid>/player", methods=[POST, GET])
def register_player(uuid: str):
    global users

    # check if uuid is valid
    this_game = games.get(uuid)

    if this_game is None:
        return "not found", 404

    rjson = request.json

    if request.method == POST:

        if validate_params(rjson, [PLAYER, TOKEN]) is False:
            return "expected player and token", 404

        player = rjson[PLAYER]
        token = rjson[TOKEN]

        if users.get(token) is None:
            return "not valid token", 401

        if player in games[uuid].get_players():
            return f"Player {player} its already being used", 400

        games[uuid]._players[player] = token
        return "done", 200

    elif request.method == GET:
        params = request.args.to_dict()
        if TOKEN not in params:
            return "expected token", 404

        token = params[TOKEN]

        if users.get(token) is None:
            return "not valid token", 401

        for player,tk in this_game._players.items():
            if tk == token:
                return jsonify({"player": player})
        return "not found", 404


    return f"{request.method} not implemented", 405


def validate_user(user, token):
    global users
    if users.get(token) != user:
        return False

    return True

def validate_params(json, expected_headers: list):
    json_keys = list(json.keys())
    json_keys.sort()
    expected_headers.sort()

    if json_keys == expected_headers:
        return True
    return False


def validate_request_json(rjson):
    global users
    if validate_params(rjson, [COLUMN, LINE, TOKEN]) is False:
        return False

    if users.get(rjson[TOKEN]) == None:
        raise GameException("Token must be valid")

    if isinstance(rjson[LINE], int) is False:
        raise GameException("Line must be int")

    if isinstance(rjson[COLUMN], int) is False:
        raise GameException("Column must be int")

    return True
