import io
import os
from collections import defaultdict
from typing import List, Literal, final

import chess.pgn
from chess import InvalidMoveError
from openai import OpenAI

from bresse.identifiers.base import ModelId
from bresse.identifiers.openai import GPT35Turbo
from bresse.models.base import ModelCloud
from bresse.preprocess import preprocess_game, postprocess_result


class OpenAIModel(ModelCloud):
    list_models: List[ModelId] = [GPT35Turbo()]

    def __init__(self, model_id: Literal['gpt-3.5-turbo'], api_key: str):
        super().__init__(model_id)
        self.client = OpenAI(api_key=api_key)

    @final
    def _inference(self, pgn: str) -> str:
        io_pgn = io.StringIO(pgn)
        base_game = chess.pgn.read_game(io_pgn)

        memory_game = chess.pgn.Game()
        memory_game.headers = base_game.headers

        child_node = None
        mainline_moves = list(base_game.mainline_moves())
        for move in mainline_moves:
            if child_node:
                child_node = child_node.add_variation(move)
            else:
                child_node = memory_game.add_variation(move)

        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        completion = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=preprocess_game(base_game),
            temperature=0.0,
            stop=["\n"],
            # seed=42,
            max_tokens=3,
            n=1,
        )

        board = chess.Board()
        for move in mainline_moves:
            san = move.uci()
            board.push_uci(san)

        counter = defaultdict(int)

        for choice in completion.choices:
            text = choice.text
            preprocess_text = postprocess_result(text)

            print(f"Result: '{text}'")
            print(f"Result (pre): '{preprocess_text}'")

            counter[preprocess_text] += 1

            # Test if preprocess_text is a valid move
            try:
                board.push_san(preprocess_text)
            except InvalidMoveError:
                print(f"Invalid move: {text=}, {preprocess_text=}")
            else:
                board.pop()

        return preprocess_game(memory_game)
