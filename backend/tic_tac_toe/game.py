import uuid
from tic_tac_toe import log

logger = log.getLogger()

BOARD_SIZE = 3

LINE = "line"
COLUMN = "column"
PLAYER = "player"
TOKEN = "token"
O = 'O'
X = 'X'


class Game:
    def __init__(self):
        self._game_id = uuid.uuid4().hex
        self._players = {X: None, O: None}
        self._winner = None
        self._moves = []

    def _gen_board(self):
        board = []
        for line in range(BOARD_SIZE):
            board.append([None for column in range(BOARD_SIZE)])

        return board

    def __str__(self):
        return self._game_id

    def get_board(self):
        board = self._gen_board()

        for move in self._moves:
            line = move[LINE]
            colum = move[COLUMN]
            player = move[PLAYER]
            board[line][colum] = player

        return board

    def get_winner(self):
        return self._winner

    def get_players(self):
        return [player for player,token in self._players.items() if token is not None]

    def _get_player_by_token(self, token):
        for player,tk in self._players.items():
            if token == tk:
                return player
        raise GameException("Player not found")

    def _validate_position(self, line: int, column: int):

        if isinstance(column, int) is False or isinstance(line, int) is False:
            raise GameException(f"Position cordinates must be integer value")

        if line > BOARD_SIZE or line < 0:
            raise GameException("Line must be between 1 and {LINE_LEN}")

        if column > BOARD_SIZE or column < 0:
            raise GameException("Column must be between 1 and {COLUMN_LEN}")

    def _register_move(self, line: int, column: int, player_id: str) -> bool:
        self._validate_position(line, column)

        board = self.get_board()

        # check if place is empty
        if board[line][column] is not None:
            raise GameException(
                f"This position is already full with {board[line][column]}")

        # check if its players turn
        if len(self._moves) > 0 and self._moves[-1][PLAYER] == player_id:
            raise GameException("You did the last move, wait for other player")

        logger.debug(
            f"{self._game_id} -> board[{line}][{column}] = {player_id}")
        self._moves.append({PLAYER: player_id, COLUMN: column, LINE: line})

    def do_move(self, line: int, column: int, token: str) -> bool:
        player_id = self._get_player_by_token(token)

        if self._winner is not None:
            raise GameException("Game is already finished, can't move")

        if player_id not in self._players.keys():
            raise GameException(f"Player {player_id} not found")

        # force player to uppercase
        player_id = player_id.upper()

        # this will throw exception in case of failure
        self._register_move(line, column, player_id)

        # after doing some action, verify if it's done
        self.is_finished()

        return True

    def is_finished(self):
        """
        In Tic tac, you can win by:
            * completing a line
            * completing a colum
            * completing a diagonal
        """
        board = self.get_board()

        # check for line
        for line in board:

            line_set = list(set(line))
            if len(line_set) == 1 and line_set[0] in self._players.keys():
                self._winner = line_set[0]
                raise GameFinished(f"Line {line} completed by {self._winner}")

        # check for columns
        for column in range(BOARD_SIZE):
            colum_values = list(
                set([board[line][column] for line in range(BOARD_SIZE)]))

            if len(colum_values) == 1 and colum_values[0] in self._players.keys():
                self._winner = colum_values[0]
                raise GameFinished(
                    f"Column {column} completed by {self._winner}")

        # check for diagonals
        diagonal_left = list(
            set([board[index][index] for index in range(BOARD_SIZE)]))
        if len(diagonal_left) == 1 and diagonal_left[0] in self._players.keys():
            self._winner = diagonal_left[0]
            raise GameFinished(f"Left diagonal completed by {self._winner}")

        diagonal_right = list(
            set([
                board[index][(BOARD_SIZE - 1) - index]
                for index in range(BOARD_SIZE)
            ]))
        if len(diagonal_right) == 1 and diagonal_right[0] in self._players.keys():
            self._winner = diagonal_right[0]
            raise GameFinished(f"Right diagonal completed by {self._winner}")


class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
        logger.debug(message)

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class GameException(APIException):
    status_code = 400


class GameFinished(APIException):
    status_code = 218
