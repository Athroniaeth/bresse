import io
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Union, final

import chess.pgn

from bresse._chess import game_play_san
from bresse.identifiers.base import ModelId
from bresse.input import InputInference
from bresse.output import Output
from bresse.process import preprocess_game


class Model(ABC):
    """
    Base class for all LLM models.

    Attributes:
        list_models (List[ModelId]): List of models available for this class
    """

    list_models: List[ModelId] = []

    @abstractmethod
    def _inference(
        self, pgn_prompt: str, config: InputInference = InputInference()
    ) -> Output:
        """
        Inference of the model on any string

        Notes:
            This method should be implemented in the child class
            This method can be call by user but don't have preprocessing

        Args:
            pgn_prompt (str): PGN string to infer

        Returns:
            Output: Output object and CounterResult object
        """
        ...

    @final
    def inference(self, pgn: str, config: InputInference = InputInference()) -> Output:
        """
        Inference the model on a given prompt

        Args:
            pgn (str): PGN string to infer
            config (InputInference): Configuration for LLM inference

        Returns:
            Output: Output object and CounterResult object
        """
        io_pgn = io.StringIO(pgn)

        # Check if pgn is a valid chess game
        game = chess.pgn.read_game(io_pgn)

        # Reduce inputs tokens for generate san
        prompt_pgn = preprocess_game(game)

        return self._inference(prompt_pgn, config)

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

    def play(
        self,
        game: chess.pgn.Game,
        config: InputInference = InputInference(),
        number: int = 1,
    ):
        """
        Play a chess game with the model.

        Notes:
            game will be modified in place by adding variations
            play white or black depending on the number of moves played and the trait

        Args:
            game (chess.pgn.Game): Game to play
            config (InputInference): Configuration for LLM inference.
            number (int, optional): Number of moves to play. Defaults to 1.
        """
        for index in range(number):
            output = self.inference(pgn=f"{game}", config=config)
            san = output.most_common

            # Play the move in the game
            game_play_san(game=game, san=san)
            print(f"Model '{self}' (n={number}) predicts: '{san}'")


@dataclass
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
