package tic_tac_toe;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import java.util.logging.Logger;
import tic_tac_toe.FinishException;

public class Game {

	// general constants
	final int BOARD_SIZE = 3;
	final String LINE = "line";
	final String COLUMN = "column";
	final String PLAYER = "player";
	final String TOKEN = "token";
	String O = "O";
	String X = "X";
	private static final Logger LOGGER = Logger.getLogger(Game.class.getName());

	// global variables
	public String game_id;
	public Map<String, String> players;
	private String winner;
	private ArrayList<Map> moves;

	public Game() {
		this.game_id = UUID.randomUUID().toString();
		this.players = new HashMap<String, String>();
		this.players.put(X, "");
		this.players.put(O, "");
		this.winner = null;
		this.moves = new ArrayList<Map>();
	}

	private String[][] genBoard() {
		String[][] t = { { null, null, null }, { null, null, null }, { null, null, null } };
		return t;
	}

	public String[][] getBoard() {
		String[][] board = genBoard();

		for (Map<String, String> move : this.moves) {
			int line = Integer.parseInt(move.get(LINE));
			int colum = Integer.parseInt(move.get(COLUMN));
			String player = move.get(PLAYER);
			board[line][colum] = player;
		}
		return board;
	}

	public String getWinner() {
		return this.winner;
	}

	public ArrayList<String> getPlayers() {
		ArrayList<String> ret = new ArrayList<String>();
		for (Map.Entry<String, String> entry : this.players.entrySet()) {
			if (entry.getValue().length() != 0) {
				ret.add(entry.getKey());
			}
		}
		return ret;
	}

	public String getPlayerByToken(String token) {
		for (Map.Entry<String, String> entry : this.players.entrySet()) {
			if (entry.getValue() == token) {
				return entry.getKey();
			}
		}
		return null;
	}

	private void validatePosition(int line, int column) {

		if ((line > BOARD_SIZE) || (line < 0)) {
			LOGGER.fine("Line must be between 1 and {LINE_LEN}");
		}

		if ((column > BOARD_SIZE) || (column < 0)) {
			LOGGER.fine("Column must be between 1 and {COLUMN_LEN}");
		}
		return;
	}

	public boolean registerMove(int line, int column, String player_id) {
		validatePosition(line, column);

		String[][] board = getBoard();

		// check if place is empty
		if (board[line][column] != null) {
			LOGGER.fine("This position is already full with {board[line][column]}");
		}
		// check if its players turn
		int last = this.moves.size() - 1;
		if ((this.moves.size() > 0) && (this.moves.get(last).get(PLAYER) == player_id)) {
			LOGGER.fine("You did the last move, wait for other player");
			LOGGER.fine("{self._game_id} -> board[{line}][{column}] = {player_id}");
		}
		return this.moves.add(Map.of(PLAYER, player_id, COLUMN, column, LINE, line));
	}

	public boolean doMove(int line, int column, String token) {
		String player_id = getPlayerByToken(token);

		if (this.getWinner() != null) {
			LOGGER.fine("Game is already finished, can't move");
		}

		if (this.players.containsKey(player_id) == true) {
			LOGGER.fine("Player {player_id} not found");
		}

		// force player to uppercase
		player_id = player_id.toUpperCase();

		// this will throw exception in case of failure
		registerMove(line, column, player_id);

		// after doing some action, verify if it's done
		isFinished();

		return true;
	}

	private void isFinished() {
		/*
		 * In Tic tac, you can win by: completing a line completing a colum completing a
		 * diagonal
		 */
		String[][] board = getBoard();

		try {
			checkLines(board);
			checkColumns(board);
			checkDiagonals(board);
			checkDraw(board);
		} catch (FinishException e) {
			//System.out.println(e.getMessage());
		}
	}

	private void checkDiagonals(String[][] board) throws FinishException {
		// check for diagonals
		Set<String> left_diagonal = Set.of(board[0][0], board[1][1], board[2][2]);
		Set<String> right_diagonal = Set.of(board[0][2], board[1][1], board[0][2]);

		checkSet(left_diagonal, "Left diagonal filled by player");
		checkSet(right_diagonal, "Right filled by player");
		return;
	}

	private void checkLines(String[][] board) throws FinishException {

		for (int line = 0; line < BOARD_SIZE; line++) {
			Set<String> line_set = Set.of(board[line]);
			checkSet(line_set, String.format("Line %d filled by player", line));
		}
		return;
	}

	private void checkColumns(String[][] board) throws FinishException {

		for (int column = 0; column < BOARD_SIZE; column++) {
			Set<String> column_set = Set.of(board[0][column], board[1][column], board[2][column]);
			checkSet(column_set, String.format("Column %d filled by player", column));
		}
		return;
	}

	private void checkSet(Set<String> thisSet, String message) throws FinishException {
		if ((thisSet.size() == 1) && (players.containsKey(thisSet.toArray()[0]))) {
			this.winner = (String) thisSet.toArray()[0];
			throw new FinishException(String.format("%s %s", message, this.winner), this.game_id);
		}
		return;
	}

	private void checkDraw(String[][] board) throws FinishException {
		for (String[] line : board) {
			for (String item : line) {
				if (item == null) {
					throw new FinishException("Draw game", this.game_id);
				}
			}
		}
		return;
	}
}
