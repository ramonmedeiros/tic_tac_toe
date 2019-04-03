import random

from unittest import TestCase
from tic_tac_toe.game import Game, GameException, GameFinished, O, X
from tic_tac_toe import log

log.set_verbosity(log.DEBUG)

O_TOKEN = "O-token"
X_TOKEN = "X-token"

class TestGame(TestCase):
    def setUp(self):
        self.game = Game()
        assert(self.game.get_available_players() == ["X", "O"])

        self.game._players[X] = X_TOKEN
        assert(self.game.get_available_players() == ["O"])

        self.game._players[O] = O_TOKEN
        assert(self.game.get_available_players() == [])

    def test_board_size_three(self):
        expected = [None, None, None]
        assert (self.game.get_board().count(expected) == 3)

    def test_board_move(self):
        self.game.do_move(0, 0, X_TOKEN)
        assert (self.game.get_board()[0][0] == X)

    def test_random_board_move(self):
        line = random.randint(0, 2)
        column = random.randint(0, 2)
        self.game.do_move(line, column, O_TOKEN)
        assert (self.game.get_board()[line][column] == O)

    def test_finish_line(self):
        self.game.do_move(0, 0, O_TOKEN)
        self.game.do_move(2, 2, X_TOKEN)
        self.game.do_move(0, 1, O_TOKEN)
        self.game.do_move(1, 1, X_TOKEN)
        with self.assertRaises(GameFinished):
            self.game.do_move(0, 2, O_TOKEN)

    def test_finish_column(self):
        self.game.do_move(0, 0, O_TOKEN)
        self.game.do_move(2, 2, X_TOKEN)
        self.game.do_move(1, 0, O_TOKEN)
        self.game.do_move(1, 1, X_TOKEN)
        with self.assertRaises(GameFinished):
            self.game.do_move(2, 0, O_TOKEN)

    def test_finish_left_diagonal(self):
        self.game.do_move(0, 0, O_TOKEN)
        self.game.do_move(0, 2, X_TOKEN)
        self.game.do_move(1, 1, O_TOKEN)
        self.game.do_move(2, 1, X_TOKEN)
        with self.assertRaises(GameFinished):
            self.game.do_move(2, 2, O_TOKEN)

    def test_finish_right_diagonal(self):
        self.game.do_move(0, 2, O_TOKEN)
        self.game.do_move(2, 2, X_TOKEN)
        self.game.do_move(1, 1, O_TOKEN)
        self.game.do_move(2, 1, X_TOKEN)
        with self.assertRaises(GameFinished):
            self.game.do_move(2, 0, O_TOKEN)

    def test_use_invalid_player(self):
        with self.assertRaises(GameException):
            self.game.do_move(0, 0, 2)

    def test_move_after_finish_game(self):
        self.game.do_move(0, 0, O_TOKEN)
        self.game.do_move(2, 2, X_TOKEN)
        self.game.do_move(1, 0, O_TOKEN)
        self.game.do_move(2, 1, X_TOKEN)
        with self.assertRaises(GameFinished):
            self.game.do_move(2, 0, O_TOKEN)

        with self.assertRaises(GameException):
            self.game.do_move(1, 1, O_TOKEN)

    def test_try_do_two_moves_same_player(self):
        self.game.do_move(0, 0, O_TOKEN)
        with self.assertRaises(GameException):
            self.game.do_move(1, 0, O_TOKEN)


