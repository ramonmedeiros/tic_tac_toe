package tic_tac_toe;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
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
		String[][] t = { { "", "", "" }, { "", "", "" }, { "", "", "" } };
		return t;
	}

	public String[][] getBoard() {
		String[][] board = genBoard();

		for (Map<String, String> move : this.moves) {
			Integer line = Integer.parseInt(move.get(this.LINE));
			Integer colum = Integer.parseInt(move.get(this.COLUMN));
			String player = move.get(this.PLAYER);
			board[line][colum] = player;
		}
		//LOGGER.info(Arrays.deepToString(board));
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
			LOGGER.info("Line must be between 1 and {LINE_LEN}");
		}

		if ((column > BOARD_SIZE) || (column < 0)) {
			LOGGER.info("Column must be between 1 and {COLUMN_LEN}");
		}
		return;
	}

	public boolean registerMove(String l, String c, String player_id) throws GameErrorException {
		int line = Integer.parseInt(l);
		int column = Integer.parseInt(c);

		validatePosition(line, column);

		String[][] board = getBoard();

		// check if place is empty
		if (board[line][column] != "") {
			throw new GameErrorException(String.format("This position is already full with %s", board[line][column]),
					this.game_id);
		}

		// check if its players turn
		int last = this.moves.size() - 1;
		if ((this.moves.size() > 0) && (this.moves.get(last).get(PLAYER) == player_id)) {
			throw new GameErrorException("You did the last move, wait for other player", this.game_id);
		}

		LOGGER.info(String.format("%s -> board[%s][%s] = %s", this.game_id, l, c, player_id));
		return this.moves.add(Map.of(PLAYER, player_id, COLUMN, c, LINE, l));
	}

	public boolean doMove(String line, String column, String token) {

		String player_id = getPlayerByToken(token);

		if (this.getWinner() != null) {
			throw new GameErrorException("Game is already finished, can't move", this.game_id);
		}

		if (this.players.containsKey(player_id) == false) {
			throw new GameErrorException(String.format("Player %s not found", player_id), this.game_id);
		}

		// force player to uppercase
		player_id = player_id.toUpperCase();

		// this will throw exception in case of failure
		registerMove(line, column, player_id);

		// after doing some action, verify if it's done
		isFinished();

		return true;
	}

	private void isFinished() throws FinishException{
		/*
		 * In Tic tac, you can win by: 
		 *     completing a line
		 *     completing a column
		 *     completing a diagonal
		 */
		String[][] board = getBoard();

		checkLines(board);
		checkColumns(board);
		checkDiagonals(board);
		checkDraw(board);
	}

	private void checkDiagonals(String[][] board) throws FinishException {
		// check for diagonals
		Set<String> left_diagonal = new HashSet<String>();
		left_diagonal.addAll(Arrays.asList(new String[] { board[0][0], board[1][1], board[2][2] }));
		Set<String> right_diagonal = new HashSet<String>();
		right_diagonal.addAll(Arrays.asList(new String[] { board[0][2], board[1][1], board[0][2] }));

		checkSet(left_diagonal, "Left diagonal filled by player");
		checkSet(right_diagonal, "Right filled by player");
		return;
	}

	private void checkLines(String[][] board) throws FinishException {

		for (int line = 0; line < BOARD_SIZE; line++) {
			Set<String> line_set = new HashSet<String>();
			line_set.addAll(Arrays.asList(board[line]));
			checkSet(line_set, String.format("Line %d filled by player", line));
		}
		return;
	}

	private void checkColumns(String[][] board) throws FinishException {

		for (int column = 0; column < BOARD_SIZE; column++) {
			Set<String> column_set = new HashSet<String>();
			column_set.addAll(Arrays.asList(new String[] { board[0][column], board[1][column], board[2][column] }));
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
				if (item == "") {
					return;
				}
			}
		}
		throw new FinishException("Draw game", this.game_id);
	}
}
