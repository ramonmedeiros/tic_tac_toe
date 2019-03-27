import random

from unittest import TestCase
from tic_tac_toe.game import Game, GameException, GameFinished
from tic_tac_toe import log

log.set_verbosity(log.DEBUG)


class TestGame(TestCase):

    def setUp(self):
        self.game = Game()

    def test_board_size_three(self):
        expected = [None, None, None]
        assert (self.game.get_board().count(expected) == 3)

    def test_board_move(self):
        self.game.do_move(0, 0, 1)
        assert (self.game.get_board()[0][0] == 1)

    def test_random_board_move(self):
        line = random.randint(0, 2)
        column = random.randint(0, 2)
        self.game.do_move(line, column, 0)
        assert (self.game.get_board()[line][column] == 0)

    def test_finish_line(self):
        self.game.do_move(0, 0, 0)
        self.game.do_move(2, 2, 1)
        self.game.do_move(0, 1, 0)
        self.game.do_move(1, 1, 1)
        with self.assertRaises(GameFinished):
            self.game.do_move(0, 2, 0)

    def test_finish_column(self):
        self.game.do_move(0, 0, 0)
        self.game.do_move(2, 2, 1)
        self.game.do_move(1, 0, 0)
        self.game.do_move(1, 1, 1)
        with self.assertRaises(GameFinished):
            self.game.do_move(2, 0, 0)

    def test_finish_left_diagonal(self):
        self.game.do_move(0, 0, 0)
        self.game.do_move(0, 2, 1)
        self.game.do_move(1, 1, 0)
        self.game.do_move(2, 1, 1)
        with self.assertRaises(GameFinished):
            self.game.do_move(2, 2, 0)

    def test_finish_right_diagonal(self):
        self.game.do_move(0, 2, 0)
        self.game.do_move(2, 2, 1)
        self.game.do_move(1, 1, 0)
        self.game.do_move(2, 1, 1)
        with self.assertRaises(GameFinished):
            self.game.do_move(2, 0, 0)

    def test_use_invalid_player(self):
        with self.assertRaises(GameException):
            self.game.do_move(0, 0, 2)

    def test_move_after_finish_game(self):
        self.game.do_move(0, 0, 0)
        self.game.do_move(2, 2, 1)
        self.game.do_move(1, 0, 0)
        self.game.do_move(2, 1, 1)
        with self.assertRaises(GameFinished):
            self.game.do_move(2, 0, 0)

        with self.assertRaises(GameException):
            self.game.do_move(1, 1, 0)

    def test_try_do_two_moves_same_player(self):
        self.game.do_move(0,0,0)
        with self.assertRaises(GameException):
            self.game.do_move(1,0,0)
