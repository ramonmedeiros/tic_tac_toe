from unittest import TestCase
from tic_tac_toe import app, log
from tic_tac_toe.game import X, O

logger = log.getLogger()
log.set_verbosity(log.DEBUG)


class TestRest(TestCase):
    @classmethod
    def setUpClass(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def test_hello(self):
        rv = self.app.get('/')
        assert (rv.data.decode() == app.TITLE)

    def test_start_new_game(self):
        rv = self.app.post('/game')
        uid = rv.data.decode()
        assert (rv.status_code == 201)

        rv = self.app.get('/game/' + uid)
        assert (rv.status_code == 200)

    def test_reach_non_existing_game(self):
        assert (self.app.get('/game/not-exists').status_code == 404)

    def test_do_move(self):
        new_game = self.app.post('/game')
        move = self.app.post(
            '/game/' + new_game.data.decode(),
            json={
                "column": 0,
                "line": 0,
                "player": O
            })
        assert (move.status_code == 200)

        board = self.app.get('/game/' + new_game.data.decode())
        assert (board.get_json()["board"][0][0] == O)

    def test_do_move_previous_filled(self):
        new_game = self.app.post('/game')
        move = self.app.post(
            '/game/' + new_game.data.decode(),
            json={
                "column": 0,
                "line": 0,
                "player": O
            })
        move = self.app.post(
            '/game/' + new_game.data.decode(),
            json={
                "column": 0,
                "line": 0,
                "player": X
            })
        assert (move.status_code == 400)

    def test_finishing_game(self):
        new_game = self.app.post('/game')
        move = self.app.post(
            '/game/' + new_game.data.decode(),
            json={
                "column": 0,
                "line": 0,
                "player": O
            })
        move = self.app.post(
            '/game/' + new_game.data.decode(),
            json={
                "column": 1,
                "line": 1,
                "player": X
            })
        move = self.app.post(
            '/game/' + new_game.data.decode(),
            json={
                "column": 1,
                "line": 0,
                "player": O
            })
        move = self.app.post(
            '/game/' + new_game.data.decode(),
            json={
                "column": 2,
                "line": 1,
                "player": X
            })
        move = self.app.post(
            '/game/' + new_game.data.decode(),
            json={
                "column": 2,
                "line": 0,
                "player": O
            })
        assert (move.status_code == 218)

    def test_do_move_column(self):
        new_game = self.app.post('/game')
        move = self.app.post(
            '/game/' + new_game.data.decode(),
            json={
                "column": 1,
                "line": 0,
                "player": O
            })
        assert (move.status_code == 200)

        board = self.app.get('/game/' + new_game.data.decode())
        assert (board.get_json()["board"][0][1] == O)


