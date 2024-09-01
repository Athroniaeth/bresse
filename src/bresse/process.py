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

    """If trait is for White, need to add number of move
    Allow to add number without intervention of LLM"""
    if trait:
        count_move = length_moves // 2 + 1

        """Note: Don't add space after number, LLM have better result
        if he can set by himself the space (first black move give always '1...', idk why)
        set strip at end because chess library set space at end with black trait"""
        str_game += f"{count_move}."

    return str_game.strip()


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

    # Ex: ' O-O ' -> 'O-O'
    result = result.strip()

    return result
