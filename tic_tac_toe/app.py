from flask import Flask
app = Flask("tic-tac-toe")

@app.route("/")
def hello():
    return "Tic Tac Toe by Ramon Medeiros"
