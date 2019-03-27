import random

from unittest import TestCase
from tic_tac_toe.game import Game, GameException, GameFinished
from tic_tac_toe import log

log.set_verbosity(log.DEBUG)


class TestGame(TestCase):
    def test_board_size_one(self):
        game = Game(board_size=1)
        assert (game.get_board() == [[None]])

    def test_board_size_three(self):
        game = Game()
        expected = [None, None, None]
        assert (game.get_board().count(expected) == 3)

    def test_board_move(self):
        game = Game()
        game.do_move(0, 0, 1)
        assert (game.get_board()[0][0] == 1)

    def test_random_board_move(self):
        line = random.randint(0, 2)
        column = random.randint(0, 2)
        game = Game()
        game.do_move(line, column, 0)
        assert (game.get_board()[line][column] == 0)

    def test_finish_line(self):
        game = Game()

        assert (game._winner is None)

        game.do_move(0, 0, 0)
        game.do_move(0, 1, 0)
        with self.assertRaises(GameFinished):
            game.do_move(0, 2, 0)

    def test_finish_column(self):
        game = Game()

        game.do_move(0, 0, 0)
        game.do_move(1, 0, 0)
        with self.assertRaises(GameFinished):
            game.do_move(2, 0, 0)

    def test_finish_left_diagonal(self):
        game = Game()

        game.do_move(0, 0, 0)
        game.do_move(1, 1, 0)
        with self.assertRaises(GameFinished):
            game.do_move(2, 2, 0)

    def test_finish_right_diagonal(self):
        game = Game()

        game.do_move(0, 2, 0)
        game.do_move(1, 1, 0)
        with self.assertRaises(GameFinished):
            game.do_move(2, 0, 0)

    def test_use_invalid_player(self):
        game = Game()

        with self.assertRaises(GameException):
            game.do_move(0, 0, 2)

    def test_move_after_finish_game(self):
        game = Game()

        game.do_move(0, 0, 0)
        game.do_move(1, 0, 0)
        with self.assertRaises(GameFinished):
            game.do_move(2, 0, 0)

        with self.assertRaises(GameException):
            game.do_move(1, 1, 0)
