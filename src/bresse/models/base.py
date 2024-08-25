import io
from abc import ABC, abstractmethod
from typing import List, Tuple, Union, final

import chess.pgn

from bresse.identifiers.base import ModelId
from bresse.output import Output
from bresse.process import preprocess_game
from bresse.result import CounterResult


class Model(ABC):
    """
    Base class for all LLM models.

    Attributes:
        list_models (List[ModelId]): List of models available for this class
    """

    list_models: List[ModelId] = []

    @abstractmethod
    def _inference(self, pgn_prompt: str) -> Tuple[Output, CounterResult]:
        """
        Inference of the model on any string

        Notes:
            This method should be implemented in the child class
            This method can be call by user but don't have preprocessing

        Args:
            pgn_prompt (str): PGN string to infer

        Returns:
            Tuple[Output, CounterResult]: Output object and CounterResult object
        """
        ...

    @final
    def inference(self, pgn: str) -> Tuple[Output, CounterResult]:
        """
        Inference the model on a given prompt

        Args:
            pgn (str): PGN string to infer

        Returns:
            Tuple[Output, CounterResult]: Output object and CounterResult object
        """
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
            raise ValueError(
                f"Model '{model_id}' does not exist. Available models: {available_models}"
            )

        return found_model


class ModelCloud(Model, ABC):
    """
    Base class for all LLM models using cloud services (OpenAI, Mistral, etc.).

    Attributes:
        model (ModelId): Model identifier chosen for inference
    """

    model: ModelId

    def __init__(self, model_id: Union[str, ModelId]):
        # Todo : Transform to Switch Pattern
        if not self.list_models:
            raise ValueError("No models defined for this class.")

        if isinstance(model_id, str):
            self.model = self._get_identifier_str(model_id)

        elif isinstance(model_id, ModelId):
            # Todo : Set this in method like get_identifier_id
            if model_id not in self.list_models:
                raise ValueError(
                    f"Model '{model_id.id}' is not available in '{self.__class__.__name__}'"
                )
            self.model = model_id

        else:
            raise TypeError("Model must be either a string or a ModelId instance.")
