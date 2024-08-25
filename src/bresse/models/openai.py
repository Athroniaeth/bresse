import io
import os
from collections import defaultdict
from typing import List, Literal, final, Tuple, Any

import chess.pgn
from chess import InvalidMoveError
from openai import OpenAI

from bresse.identifiers.base import ModelId
from bresse.identifiers.openai import GPT35Turbo
from bresse.models.base import ModelCloud
from bresse.output import Output
from bresse.preprocess import preprocess_game, postprocess_result, pgn_to_board
from bresse.result import Result, CounterResult

_AVAILABLE_MODELS = Literal[
    'gpt-3.5-turbo-instruct',
]


class OpenAIModel(ModelCloud):
    list_models: List[ModelId] = [GPT35Turbo()]

    def __init__(
            self,
            model_id: _AVAILABLE_MODELS,
            api_key: str
    ):
        super().__init__(model_id)
        self.client = OpenAI(api_key=api_key)

    @final
    def _inference(self, pgn_prompt: str) -> Tuple[Output, CounterResult]:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        completion = client.completions.create(
            model=self.model.id,
            prompt=pgn_prompt,
            temperature=0.0,
            stop=["\n"],
            # seed=42,
            max_tokens=2,
            n=1,
        )

        input_tokens = completion.usage.prompt_tokens
        output_tokens = completion.usage.completion_tokens

        output = Output(
            model_id=self.model,
            number_requests=1,
            inputs_tokens=input_tokens,
            outputs_tokens=output_tokens,
        )

        board = pgn_to_board(pgn=pgn_prompt)
        list_san = [choice.text for choice in completion.choices]
        parser = CounterResult.from_inference(board=board, list_san=list_san)

        return output, parser


