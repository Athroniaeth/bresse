from abc import ABC, abstractmethod
from typing import List, Union, final, Tuple, Iterable, Optional, Callable

import chess.pgn

from bresse.chess_ import game_play_san, pgn_to_board
from bresse.identifiers.base import ModelId
from bresse.input import ConfigInference
from bresse.output import Output, OutputGeneration, OutputInference, Result
from bresse.process import preprocess_game, postprocess_result


class Model(ABC):
    """
    Base class for all LLM models.
    """

    model_id: ModelId

    def __init__(self, model_id: ModelId):
        """Create '__init__' method for type hinting."""
        if not isinstance(model_id, ModelId):
            raise TypeError("model_id must be a ModelId instance.")
        self.model_id = model_id

    @abstractmethod
    def _inference(
        self, pgn_prompt: str, config: ConfigInference = ConfigInference()
    ) -> Tuple[OutputInference, List[str]]:
        """
        Inference of the model on any string

        Notes:
            This method should be implemented in the child class
            This method can be call by user but don't have preprocessing

        Args:
            pgn_prompt (str): PGN string to infer (preprocess)

        Returns:
            Tuple[OutputInference, List[str]]: OutputInference object and list of generated SAN
        """
        ...

    @final
    def inference(
        self, game: chess.pgn.Game, input_: ConfigInference = ConfigInference()
    ) -> Output:
        """
        Inference the model on a given prompt

        Args:
            game (str): PGN string to infer
            input_ (ConfigInference): Configuration for LLM inference

        Returns:
            Output: Output object and CounterResult object
        """
        # Reduce inputs tokens for generate san
        prompt_pgn = preprocess_game(game)
        board = pgn_to_board(pgn=prompt_pgn)

        # Inference the model
        output_inf, list_san = self._inference(prompt_pgn, input_)

        # Postprocess the output (for 1 move)
        output_gen = OutputGeneration.from_inference(board=board, list_san=list_san)

        # Merge the two outputs
        output = Output.from_outputs(output_inf=output_inf, output_gen=output_gen)

        return output

    @final
    def play(
        self,
        game: chess.pgn.Game,
        config: ConfigInference = ConfigInference(),
    ) -> Output:
        """
        Play a chess game with the model.

        Notes:
            game will be modified in place by adding variations
            play white or black depending on the number of moves played and the trait

        Args:
            game (chess.pgn.Game): Game to play
            config (ConfigInference): Configuration for LLM inference.
        """
        output = self.inference(game=game, input_=config)
        san = output.most_common

        # Play the move in the game
        game_play_san(game=game, san=san)
        print(f"Model '{self}' predicts: '{san}'")
        return output

    def auto_play(
            self,
            game: chess.pgn.Game,
            config: ConfigInference = ConfigInference(),
            preprocess_func: Optional[Callable] = postprocess_result,
    ) -> OutputInference:
        """
        Auto-Play a full chess game with the model.

        Instead of making several requests with one data validation,
        the class will make one big inference until it finishes the game.

        Notes:
            game will be modified in place by adding variations
            play white or black depending on the number of moves played and the trait
            there are not output for generation (handle single san move)

        Args:
            game (chess.pgn.Game): Game to play
            config (ConfigInference): Configuration for LLM inference.
            preprocess_func (Callable, optional): Preprocess function for each san. Defaults to None.
        """
        # Give enough tokens for a full game (4 tokens/avg per move)
        config.n = 1
        config.max_tokens = 3800

        # Reduce inputs tokens for generate san
        prompt_pgn = preprocess_game(game)

        output_inf, list_san = self._inference(pgn_prompt=prompt_pgn, config=config)

        text = list_san[0]

        for san in text.split(' '):
            # Skip if not san move
            conditions = (
                not san in ["1-0", "0-1", "1/2-1/2", "*"],
                not san.startswith("#"),
                not san.startswith("\n"),
                not '.' in san,
                not san == ""
            )

            if all(conditions):
                san = preprocess_func(san)

                try:
                    game_play_san(game=game, san=san)
                except ValueError as e:
                    print(f"Error in move '{san}': {e}")
                    break

        return output_inf

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.model_id}')"

    def __eq__(self, other: "Model") -> bool:
        return self.model_id == other.model_id


class ModelOnline(Model, ABC):
    """
    Base class for all LLM available online (HuggingFace Hub, OpenAI, Mistral, etc.).
    """

    model_id: ModelId

    def __init__(self, model_id: Union[str, ModelId], api_key: str):
        if not api_key:
            raise ValueError("API key is required for cloud models.")

        # If identifier is a string, that model is free (hf_hub, etc.)
        if isinstance(model_id, str):
            model_id = ModelId(id=model_id, input_cost_million=0, output_cost_million=0)

        super().__init__(model_id=model_id)


class ModelCloud(ModelOnline, ABC):
    """
    Base class for all LLM models using cloud services (OpenAI, Mistral, etc.).

    Notes:
        The difference with ModelOnline is that ModelCloud
        have limited and deterministic list of models available.
    """

    list_models: List[ModelId] = []

    def __init__(self, model_id: Union[str, ModelId], api_key: str):
        # Todo : Transform to Switch Pattern
        if not self.list_models:
            raise ValueError("No models defined for this class.")

        if isinstance(model_id, str):
            model_id = self._get_identifier_str(model_id)

        elif isinstance(model_id, ModelId):
            # Todo : Set this in method like get_identifier_id
            model_id = self._get_identifier_model_id(model_id)

        else:
            raise TypeError("Model must be either a string or a ModelId instance.")

        super().__init__(model_id=model_id, api_key=api_key)

    def _get_identifier_str(self, model_id: str) -> ModelId:
        """Found the ModelId from id attributes and validate it."""
        generator = filter(lambda x: x.id == model_id, self.list_models)
        found_model = next(generator, None)

        if found_model is None:
            available_models = ", ".join(m.id for m in self.list_models)
            raise ValueError(
                f"Model '{model_id}' does not exist. Available models: {available_models}"
            )

        return found_model

    def _get_identifier_model_id(self, model_id: ModelId) -> ModelId:
        """Validate the ModelId instance is available."""
        if model_id not in self.list_models:
            raise ValueError(
                f"Model '{model_id.id}' is not available in '{self.__class__.__name__}'"
            )
        return model_id
