from pathlib import Path

import chess.pgn
import pytest

from bresse import game_play_san, generate_pgn, get_child_node, pgn_to_board
from bresse._chess import generate_opening
from tests.conftest import load_path_pgn

POLYGLOT_PATH = Path(__file__).parents[1] / "data" / "gm2600.bin"


@pytest.mark.parametrize("path_pgn", load_path_pgn("error"))
def test_pgn_to_board_error(path_pgn):
    """Test pgn_to_board function detect error in PGN."""
    pgn = path_pgn.read_text()

    with pytest.raises(ValueError):
        pgn_to_board(pgn)


def test_get_child_node():
    """Test get_child_node function success to get last child node."""
    game = chess.pgn.Game()

    move = chess.Move.from_uci("e2e4")
    child_node = game.add_variation(move)

    move = chess.Move.from_uci("e7e5")
    last_child_node = child_node.add_variation(move)

    assert get_child_node(game) == last_child_node, "Last child node not found"


def test_game_play_san():
    """Test game_play_san function success to play a move in a chess game."""
    game = chess.pgn.Game()

    game_play_san(game, "e4")
    game_play_san(game, "e5")

    assert game.variations, "No variations found in game"
    assert game.variations[0].move == chess.Move.from_uci(
        "e2e4"
    ), "First move not found"
    assert game.variations[0].variations[0].move == chess.Move.from_uci(
        "e7e5"
    ), "Second move not found"


def test_generate_pgn():
    """Test generate_pgn function success to generate a PGN."""
    game = generate_pgn(
        round_=10,
        white="John Doe White",
        black="Jane Doe Black",
        white_elo=2000,
        black_elo=1900,
        time_control="5+5",
        termination="Normal",
        variant="Standard",
        result="1-0",
    )

    assert game.headers["Round"] == "10", "Round attribute is not correct"
    assert game.headers["White"] == "John Doe White", "White attribute is not correct"
    assert game.headers["Black"] == "Jane Doe Black", "Black attribute is not correct"
    assert game.headers["WhiteElo"] == "2000", "WhiteElo attribute is not correct"
    assert game.headers["BlackElo"] == "1900", "BlackElo attribute is not correct"
    assert game.headers["TimeControl"] == "5+5", "TimeControl attribute is not correct"
    assert (
        game.headers["Termination"] == "Normal"
    ), "Termination attribute is not correct"
    assert game.headers["Variant"] == "Standard", "Variant attribute is not correct"
    assert game.headers["Result"] == "1-0", "Result attribute is not correct"


def test_generate_pgn_base():
    """Test generate_pgn function success to generate a PGN with base PGN."""
    base_pgn = """[Round \"1\"]
    1. e4
    """

    game = generate_pgn(
        round_=10,
        base_pgn=base_pgn,
    )

    assert game.headers["Round"] == "10", "Round attribute is not correct"
    assert game.variations[0].move == chess.Move.from_uci(
        "e2e4"
    ), "First move not found"


def test_generate_opening():
    """Test generate_opening function success to generate an opening game."""
    game = generate_opening(POLYGLOT_PATH, seed=42)

    assert isinstance(game, chess.pgn.Game), "Opening game not generated"
