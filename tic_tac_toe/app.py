import json

from flask import Flask, request, make_response, jsonify
from tic_tac_toe.game import Game, GameException
from tic_tac_toe import log
from uuid import uuid4
from wtforms import Form, FieldList, IntegerField, StringField, FormField, validators

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


@app.route("/")
def hello():
    return TITLE

@app.errorhandler(GameException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route("/game", methods=[GET, POST])
def game():
    global games

    if request.method == POST:
        game = Game()
        game_uuid = uuid4().__str__()
        games[game_uuid] = game
        return make_response(game_uuid, 201)

    elif request.method == GET:
        return jsonify(games.keys())

    return make_response(f"{request.method} not implemented", 405)


@app.route("/game/<uuid>", methods=[GET, POST, DELETE])
def deal_with_game(uuid: str):
    global games

    # check if uuid is valid
    this_game = games.get(uuid)

    if this_game is None:
        return make_response("not found", 404)

    params = DoMoveParameters(request.form)
    if request.method == POST: 
        if params.validate():
            logger.debug(params.errors)
            return params.errors, 400

        if this_game.do_move(params.column.data,
                                 params.line.data,
                                 params.player.data) is True:
            return "moved", 200
        return "failed", 403

    if request.method == GET:
        return jsonify(games.get(uuid).get_board())

    elif request.method == DELETE:
        return games.delete(request.form["uuid"])

    return make_response(f"{request.method} not implemented", 405)


class DoMoveParameters(Form):
    column = IntegerField(COLUMN, [validators.DataRequired()])
    line =  IntegerField(LINE, [validators.DataRequired()])
    player = IntegerField(PLAYER, [validators.DataRequired()])
