import uuid
from tic_tac_toe import log

logger = log.getLogger()

BOARD_SIZE = 3


class Game:
    # TODO: when auth will be added, the player id will be recorded
    _players = [None, None]
    game_id = None
    _winner = None

    def __init__(self, board_size: int = BOARD_SIZE):
        self._game_id = uuid.uuid4().hex
        self._players = [0, 1]
        self._size = board_size

        self._gen_board()

    def _gen_board(self):
        logger.debug(f"Board will be {self._size}X{self._size}")

        self._board = []
        for line in range(self._size):
            self._board.append([None for column in range(self._size)])

    def get_board(self):
        return self._board

    def get_winner(self):
        return self._winner

    def _validate_position(self, line: int, column: int) -> bool:

        if isinstance(column, int) is False or isinstance(
                line, int) is False:
            raise GameException(f"Position cordinates must be integer value")

        if line > self._size or line < 0:
            raise GameException("Line must be between 1 and {LINE_LEN}")

        if column > self._size or column < 0:
            raise GameException("Column must be between 1 and {COLUMN_LEN}")

        return True

    def do_move(self, line: int, column: int, player_id: int) -> bool:

        if self._winner is not None:
            raise GameException(f"Game finished. Winner is {self._winner}")

        if player_id not in self._players:
            raise GameException(f"Player {player_id} not found")

        # this will throw exception in case of failure
        self._validate_position(line, column)

        if self._board[line][column] is not None:
            raise GameException(
                f"This position is already full with {self._board[line][column]}"
            )

        logger.debug(f"{self._game_id} -> board[{line}][{column}] = {player_id}")
        self._board[line][column] = player_id

        # after doing some action, verify if it's done
        self.is_finished()

        return True

    def is_finished(self) -> bool:
        """
        In Tic tac, you can win by:
            * completing a line
            * completing a colum
            * completing a diagonal
        """
        # check for line
        for line in self._board:

            line_set = list(set(line))
            if len(line_set) == 1 and line_set[0] in self._players:
                self._winner = line_set[0]
                logger.debug(f"Line {line} completed by {self._winner}")
                return True

        # check for columns
        for column in range(self._size):
            colum_values = list(
                set([self._board[line][column] for line in range(self._size)]))

            if len(colum_values) == 1 and colum_values[0] in self._players:
                self._winner = colum_values[0]
                logger.debug(f"Column {column} completed by {self._winner}")
                return True

        # check for diagonals
        diagonal_left = list(
            set([self._board[index][index] for index in range(self._size)]))
        if len(diagonal_left) == 1 and diagonal_left[0] in self._players:
            self._winner = diagonal_left[0]
            logger.debug(f"Left diagonal completed by {self._winner}")
            return True

        diagonal_right = list(
            set([
                self._board[index][(self._size - 1) - index]
                for index in range(self._size)
            ]))
        if len(diagonal_right) == 1 and diagonal_right[0] in self._players:
            self._winner = diagonal_right[0]
            logger.debug(f"Right diagonal completed by {self._winner}")
            return True

        return False


class GameException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        logger.debug(args)
