import uuid
import log

logger = log.getLogger()

LINE_LEN = 3
COLUMN_LEN = 3

class Game:
    _board = []
    # TODO: when auth will be added, the player id will be recorded
    _players = [None, None]
    game_id = None
    _winner = None

    def __init__(self):
        self._game_id = uuid.uuid4().hex
        self._players = [0, 1] 

    def _gen_board(self):
        for line in len(LINE_LEN):
            self._board.append([None for column in COLUMN_LEN])

    def _validate_position(self, position: list) -> bool:
        # validate params
        if isinstance(position, list) is False or len(position) == 2:
            raise GameException(f"Position {position} must be a list of two cordinates")

        if isinstance(position[0]) not int or isinstance(position[1]) not int:
            raise GameException(f"Position cordinates must be integer value")

        if position[0] > LINE_LEN or position[0] < 1:
            raise GameException("Line must be between 1 and {LINE_LEN}")

        if position[1] > COLUMN_LEN or position[1] < 1:
            raise GameException("Column must be between 1 and {COLUMN_LEN}")
        
        return True


    def do_move(self, position: list, player_id: int) -> bool:

        if player_id not in self._players:
            raise GameException(f"Player {player_id} not found")

        # this will throw exception in case of failure
        self._validate_position(position)

        line, column = position
        if self._board[line][column] is not None:
            raise GameException(f"This position is already full with {self._board[line][column]}")

        self._board[line][column] = player_id


    def is_finished(self) -> bool:
        """
        In Tic tac, you can win by:
            * completing a line
            * completing a colum
            * completing a diagonal
        """
        # check for line
        for line in self._board:

            line_set = set(line)
            if len(line_set) == 1:
                self._winner = line_set

       # check for columns
        for column in len(self._board[0]):
            
            column_set = set(self
             

class GameException(Exception):
    pass
