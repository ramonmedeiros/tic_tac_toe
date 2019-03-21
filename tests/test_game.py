from unittest import TestCase
from tic_tac_toe.game import Game

class TestGame(TestCase):

    def test_board_size_one(self):
        size = 1
        game = Game(board_size=size)
        assert(game._board == [[None]])

    def test_board_size_three(self):
        game = Game()
        expected = [None, None, None]
        assert(game._board.count(expected) == 3)
