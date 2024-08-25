import chess.pgn


def game_to_board(game: chess.pgn.Game):
    """Get Board from pgn party"""
    board = chess.Board()
    moves = game.mainline_moves()

    generator = (move.uci for move in moves)
    map(lambda san: board.push_uci(san), generator)

    return board
