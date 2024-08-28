from io import StringIO
from typing import Union

import chess.pgn


def pgn_to_board(pgn: str):
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


def get_child_node(
    node: Union[chess.pgn.Game, chess.pgn.ChildNode],
) -> chess.pgn.ChildNode:
    """Get the last variation of game node."""
    if node.variations:
        last_node = node.variations[-1]
        return get_child_node(last_node)

    return node


def game_play_san(game: chess.pgn.Game, san: str):
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
