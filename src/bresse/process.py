from io import StringIO

import chess.pgn


def preprocess_game(game: chess.pgn.Game):
    """
    Preprocess a game to be used as prompt for LLM

    Args:
        game (chess.pgn.Game): Game (pgn) to preprocess pgn text (str)

    Returns:
        str: Preprocessed game
    """
    str_game = str(game)
    list_moves = list(game.mainline())
    length_moves = len(list_moves)
    trait = length_moves % 2 == 0

    # Delete at end the '1-0' if exist (for LLM predict next move)
    length_result = len(game.headers["Result"])
    str_game = str_game[:-length_result]

    # If trait is for White, need to add number of move
    # Allow to add number without intervention of LLM
    if trait:
        count_move = length_moves // 2 + 1
        str_game += f"{count_move}. "

    return str_game


def postprocess_result(result: str):
    """
    Clean result, san move prediction, for try to no have errors

    Args:
        result (str): San move prediction

    Returns:
        str: San move prediction cleaned
    """
    # Ex: ' O-O Bc' -> 'O-O Bc'
    result = result.strip()

    # Ex: 'O-O Bc' -> 'O-O'
    result = result.split(" ")[0]

    # Castling can have '–' instead of '-'
    result = result.replace("–", "-")

    # Ex: '0-0' -> 'O-O' (can have '1-0' also replace all '0-0' by 'O-O')
    result = result.replace("0-0", "O-O")
    result = result.replace("o-o", "O-O")

    return result


def pgn_to_board(pgn: str):
    """Get Board from PGN string."""
    io_pgn = StringIO(pgn)
    game = chess.pgn.read_game(io_pgn)
    moves = game.mainline_moves()

    if not moves:
        last_line = pgn.strip().split("\n")[-1]
        raise ValueError(f"chess-python can't parse this PGN '{last_line[:15]}'...")

    board = chess.Board()
    generator = (move.uci for move in moves)
    map(lambda san: board.push_uci(san), generator)

    return board
