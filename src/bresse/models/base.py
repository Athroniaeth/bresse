import io
from abc import abstractmethod, ABC
from typing import List, final, Union, Iterable, Tuple

import chess.pgn

from bresse.identifiers.base import ModelId
from bresse.output import Output
from bresse.preprocess import preprocess_game
from bresse.result import CounterResult


class Model(ABC):
    list_models: List[ModelId] = []

    @abstractmethod
    def _inference(self, game: chess.pgn.Game) -> Tuple[Output, CounterResult]:
        """Inference of the model on any string"""
        ...

    @final
    def inference(self, pgn: str) -> Tuple[Output, CounterResult]:
        """Inference the model on a given prompt"""
        io_pgn = io.StringIO(pgn)
        # Check if pgn is a valid chess game
        game = chess.pgn.read_game(io_pgn)

        # Reduce inputs tokens for generate san
        prompt_pgn = preprocess_game(game)

        return self._inference(prompt_pgn)

    def _get_identifier_str(self, model_id: str) -> ModelId:
        """Found the ModelId from id attributes."""
        generator = filter(lambda x: x.id == model_id, self.list_models)
        found_model = next(generator, None)

        if found_model is None:
            available_models = ", ".join(m.id for m in self.list_models)
            raise ValueError(f"Model '{model_id}' does not exist. Available models: {available_models}")

        return found_model


class ModelCloud(Model, ABC):
    model: ModelId

    def __init__(self, model_id: Union[str, ModelId]):
        # Todo : Transform to Switch Pattern
        if not self.list_models:
            raise ValueError("No models defined for this class.")

        if isinstance(model_id, str):
            self.model = self._get_identifier_str(model_id)

        elif isinstance(model_id, ModelId):
            if model_id not in self.list_models:
                raise ValueError(f"Model '{model_id.id}' is not available in '{self.__class__.__name__}'")
            self.model = model_id

        else:
            raise TypeError("Model must be either a string or a ModelId instance.")
