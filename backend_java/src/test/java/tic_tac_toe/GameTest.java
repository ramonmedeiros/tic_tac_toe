package tic_tac_toe;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

import java.util.List;
import java.util.Random;
import java.util.Set;

import org.junit.Before;
import org.junit.Test;

import tic_tac_toe.Game;
import tic_tac_toe.FinishException;

public class GameTest {
	final String O_TOKEN = "O-token";
	final String X_TOKEN = "X-token";
	Game game;

	@Before
	public void setUp() throws Exception {
		this.game = new Game();
		assertEquals(0, this.game.getPlayers().size());

		this.game.players.replace(this.game.X, X_TOKEN);;
		assertTrue(this.game.getPlayers().containsAll(List.of(this.game.X)));

		this.game.players.replace(this.game.O, O_TOKEN);;
		assertTrue(this.game.getPlayers().containsAll(List.of(this.game.X, this.game.O)));
	}

	@Test
	public void testNewBoard() {
		assert this.game.getBoard().length == 3;
	}

	@Test
	public void testBoardMove() {	
		this.game.doMove("0", "0", X_TOKEN);; 
		assertEquals(this.game.getBoard()[0][0], this.game.X);
	}
	
	@Test
	public void testRandomBoardMove() {
		int line =  new Random().nextInt(2);
		int column = new Random().nextInt(2);
		this.game.doMove(Integer.toString(line), Integer.toString(column), O_TOKEN);;
		
		assertEquals(this.game.getBoard()[line][column], this.game.O);
	}
	
	@Test(expected = FinishException.class)
	public void testFinishLine() {
		this.game.doMove("0", "0", O_TOKEN);;
		this.game.doMove("2", "2", X_TOKEN);; 
		this.game.doMove("0", "1", O_TOKEN);;
		this.game.doMove("1", "1", X_TOKEN);;	 
		this.game.doMove("0", "2", O_TOKEN);;
	}

	@Test(expected = FinishException.class)
	public void testFinishColumn() {
		this.game.doMove("0", "0", O_TOKEN);;
		this.game.doMove("2", "2", X_TOKEN);; 
		this.game.doMove("1", "0", O_TOKEN);;
		this.game.doMove("1", "1", X_TOKEN);; 
		this.game.doMove("2", "0", O_TOKEN);;
	}

	@Test(expected = FinishException.class)
	public void testFinishLeftDiagonal() {
		this.game.doMove("0", "0", O_TOKEN);;	
		this.game.doMove("0", "2", X_TOKEN);;
		this.game.doMove("1", "1", O_TOKEN);;
		this.game.doMove("2", "1", X_TOKEN);;
		this.game.doMove("2", "2", O_TOKEN);;
	}
	
	@Test(expected = FinishException.class)
	public void testFinishRightDiagonal() {
		this.game.doMove("0", "2", O_TOKEN);
		this.game.doMove("2", "2", X_TOKEN);
		this.game.doMove("1", "1", O_TOKEN);
		this.game.doMove("2", "1", X_TOKEN);
		this.game.doMove("2", "0", O_TOKEN);
	}
	
	@Test(expected = GameErrorException.class)
	public void testUseInvalidPlayer() {
		 this.game.doMove("0", "0", "invalid-token");
	}

	@Test(expected = GameErrorException.class)
	public void testMoveAfterFinishGame() {
		this.game.doMove("0", "0", O_TOKEN);
		this.game.doMove("2", "2", X_TOKEN);
		this.game.doMove("1", "0", O_TOKEN);
		this.game.doMove("2", "1", X_TOKEN);
		try {
			this.game.doMove("2", "0", O_TOKEN);
		} catch (FinishException e) {
		
		}
		this.game.doMove("1", "1", O_TOKEN);
	}
	
	@Test(expected = GameErrorException.class)
	public void testTryDoTwoMovesSamePlayer() {
		this.game.doMove("0", "0", O_TOKEN);
		this.game.doMove("1", "0", O_TOKEN);
	}
}

