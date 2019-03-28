from flask import Flask, render_template, make_response, jsonify

app = Flask("frotend", template_folder="frontend/templates", static_folder="frontend/static")

GET = "GET"

@app.route("/", methods=[GET])
def index():
    return render_template("games.html")

@app.route("/game/<uuid>", methods=[GET])
def play_game(uuid):
    return render_template("game.html", uuid=uuid)

def get_backend_uri():
    return "http://localhost:5000"
