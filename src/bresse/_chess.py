from io import StringIO
from typing import Literal, Optional

import chess.pgn


def pgn_to_board(pgn: str) -> chess.Board:
    """Get chess.Board from PGN string."""
    io_pgn = StringIO(pgn)
    game = chess.pgn.read_game(io_pgn)
    moves = game.mainline_moves()

    if game.errors:
        list_error = (f"{error}" for error in game.errors)
        list_error = ", ".join(list_error)
        raise ValueError(f"Error in PGN, list of errors: {list_error}")

    board = chess.Board()
    generator = (move.uci() for move in moves)

    for move in generator:
        board.push_uci(move)

    return board


def get_child_node(node: chess.pgn.GameNode) -> chess.pgn.GameNode:
    """Get the last variation of game node."""
    if node.variations:
        last_node = node.variations[-1]
        return get_child_node(last_node)

    return node


def game_play_san(game: chess.pgn.Game, san: str) -> None:
    """
    Play a move in a chess game.

    Notes:
        game will be modified in place by adding variations

    Args:
        game (chess.pgn.Game): Game to play
        san (str): SAN move to play
    """
    # Create board from PGN
    board = pgn_to_board(pgn=f"{game}")

    # Get move from SAN
    move = board.parse_san(san)

    # Add move to last variation (else create new)
    child_node = get_child_node(game)
    child_node.add_variation(move)


def generate_pgn(
    round_: int = 1,
    white: str = "Carlsen, M.",
    black: str = "Caruana, F.",
    white_elo: int = 2882,
    black_elo: int = 2818,
    time_control: str = "-",
    termination: Literal["Normal"] = "Normal",
    variant: Literal["Standard"] = "Standard",
    result: Literal["*", "1-0", "0-1", "1/2-1/2"] = "*",
    base_pgn: Optional[str] = None,
) -> chess.pgn.Game:
    """
    Generate a PGN game.

    Args:
        round_ (int): Round number of tournament.
        white (str): White player name.
        black (str): Black player name.
        result (Literal["*", "1-0", "0-1", "1/2-1/2"]): Game result (* is ongoing).
        white_elo (int): White player Elo.
        black_elo (int): Black player Elo.
        variant (Literal["Standard"]): Chess variant.
        time_control (str): Time control of the game.
        termination (Literal["Normal"]): Termination of the game.
        base_pgn (Optional[str]): Base PGN string to start the game (only moves).

    Returns:
        chess.pgn.Game: PGN game object.
    """

    if base_pgn is not None:
        io_pgn = StringIO(base_pgn)
        game = chess.pgn.read_game(io_pgn)
    else:
        game = chess.pgn.Game()

    game.headers = chess.pgn.Headers(
        {
            "Round": f"{round_}",
            "White": white,
            "Black": black,
            "Result": result,
            "WhiteElo": f"{white_elo}",
            "BlackElo": f"{black_elo}",
            "Variant": variant,
            "TimeControl": time_control,
            "Termination": termination,
        }
    )

    return game
