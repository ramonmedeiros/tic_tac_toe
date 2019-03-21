import random

from unittest import TestCase
from tic_tac_toe.game import Game
from tic_tac_toe import log


log.set_verbosity(log.DEBUG)

class TestGame(TestCase):


    def test_board_size_one(self):
        game = Game(board_size=1)
        assert(game._board == [[None]])

    def test_board_size_three(self):
        game = Game()
        expected = [None, None, None]
        assert(game._board.count(expected) == 3)

    def test_board_move(self):
        game = Game()
        game.do_move([0, 0], 1)
        assert(game._board[0][0] == 1)

    def test_random_board_move(self):
        line = random.randint(0, 2)
        column = random.randint(0, 2)
        game = Game()
        game.do_move([line, column], 0)
        assert(game._board[line][column] == 0)

    def test_finish_line(self):
        game = Game()

        assert(game.is_finished() is False)

        game.do_move([0,0], 0)
        game.do_move([0,1], 0)
        game.do_move([0,2], 0)
        assert(game.is_finished() is True)

    def test_finish_column(self):
        game = Game()

        assert(game.is_finished() is False)

        game.do_move([0,0], 0)
        game.do_move([1,0], 0)
        game.do_move([2,0], 0)
        assert(game.is_finished() is True)

    def test_finish_left_diagonal(self):
        game = Game()

        assert(game.is_finished() is False)

        game.do_move([0,0], 0)
        game.do_move([1,1], 0)
        game.do_move([2,2], 0)
        assert(game.is_finished() is True)

    def test_finish_right_diagonal(self):
        game = Game()

        assert(game.is_finished() is False)

        game.do_move([0,2], 0)
        game.do_move([1,1], 0)
        game.do_move([2,0], 0)
        assert(game.is_finished() is True)


