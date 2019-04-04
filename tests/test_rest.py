from unittest import TestCase
from tic_tac_toe import app, log
from tic_tac_toe.game import X, O, PLAYER, TOKEN
from tic_tac_toe.app import USERNAME

logger = log.getLogger()
log.set_verbosity(log.DEBUG)

X_USERNAME = "X-name"
O_USERNAME = "O-name"

class TestRest(TestCase):

    @classmethod
    def setUpClass(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def setUp(self):
        
        # login players
        self.x_token = self.app.post(f'/login', json={USERNAME: X_USERNAME}).get_json()["token"]
        self.o_token = self.app.post(f'/login', json={USERNAME: O_USERNAME}).get_json()["token"]

        # create game
        rv = self.app.post('/game', json={TOKEN: self.x_token})
        assert (rv.status_code == 201)
        self.uuid = rv.data.decode()

        # validate token
        assert(self.app.post('/validate_token', json={TOKEN: self.x_token}).status_code == 200)

        assert(self.app.get(f'/game/{self.uuid}/player', json={TOKEN: self.x_token}).status_code == 404)

        # register
        assert(self.app.post(f'/game/{self.uuid}/player', json={PLAYER: X, TOKEN: self.x_token}).status_code == 200)
        assert(self.app.post(f'/game/{self.uuid}/player', json={PLAYER: O, TOKEN: self.o_token}).status_code == 200)
     
    def tearDown(self):
        assert(self.app.post("/logout", json={TOKEN: self.x_token, USERNAME: X_USERNAME}).status_code == 200)
        assert(self.app.post("/logout", json={TOKEN: self.o_token, USERNAME: O_USERNAME}).status_code == 200)
        assert(app.users == {})

    def test_hello(self):
        rv = self.app.get('/')
        assert (rv.data.decode() == app.TITLE)

    def test_get_player_by_token(self):
        assert(self.app.get(f'/game/{self.uuid}/player?token={self.x_token}').get_json()[PLAYER] == X)

    def test_get_new_game(self):
        rv = self.app.get('/game/' + self.uuid)
        assert (rv.status_code == 200)

    def test_reach_non_existing_game(self):
        assert (self.app.get('/game/not-exists').status_code == 404)

    def test_available_players(self):
        assert (self.app.get(f'/game/{self.uuid}').get_json()["players"] == [X, O])

    def test_do_move(self):
        move = self.app.post(f'/game/{self.uuid}',
            json={
                "column": 0,
                "line": 0,
                "token": self.o_token
            })
        assert (move.status_code == 200)

        board = self.app.get(f'/game/{self.uuid}')
        assert (board.get_json()["board"][0][0] == O)

    def test_do_move_previous_filled(self):
        move = self.app.post(
            f'/game/{self.uuid}',
            json={
                "column": 0,
                "line": 0,
                "token": self.o_token
            })
        move = self.app.post(f'/game/{self.uuid}',
            json={
                "column": 0,
                "line": 0,
                "token": self.x_token
            })
        assert (move.status_code == 400)

    def test_finishing_game(self):
        move = self.app.post(
            f'/game/{self.uuid}',
            json={
                "column": 0,
                "line": 0,
                "token": self.o_token
            })
        move = self.app.post(
            f'/game/{self.uuid}',
            json={
                "column": 1,
                "line": 1,
                "token": self.x_token
            })
        move = self.app.post(
            f'/game/{self.uuid}',
            json={
                "column": 1,
                "line": 0,
                "token": self.o_token
            })
        move = self.app.post(
            f'/game/{self.uuid}',
            json={
                "column": 2,
                "line": 1,
                "token": self.x_token
            })
        move = self.app.post(
            f'/game/{self.uuid}',
            json={
                "column": 2,
                "line": 0,
                "token": self.o_token
            })
        assert (move.status_code == 218)

    def test_do_move_column(self):
        move = self.app.post(
            f'/game/{self.uuid}',
            json={
                "column": 1,
                "line": 0,
                "token": self.o_token
            })
        assert (move.status_code == 200)

        board = self.app.get(f'/game/{self.uuid}')
        assert (board.get_json()["board"][0][1] == O)

