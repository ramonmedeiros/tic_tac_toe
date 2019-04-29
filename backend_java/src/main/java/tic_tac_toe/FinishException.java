package tic_tac_toe;

import java.util.logging.Logger;

public class FinishException extends RuntimeException {
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private static final Logger LOGGER = Logger.getLogger(Game.class.getName());

	public FinishException(String errorMessage, String gameId) {
		super(String.format("Game %s: %s", gameId, errorMessage));
		LOGGER.fine(String.format("Game %s: %s", gameId, errorMessage));
	}
}
