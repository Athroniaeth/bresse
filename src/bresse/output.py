from collections import Counter
from dataclasses import dataclass
from typing import Callable, Iterable, List, Optional, Self

import chess
from chess import InvalidMoveError

from bresse.identifiers.base import ModelId
from bresse.process import postprocess_result


@dataclass
class Result:
    """Result of LLM generation."""

    san: str
    postprocess_san: str
    exception: Optional[InvalidMoveError]


@dataclass
class OutputInference:
    """
    Output of LLM Inference.

    Attributes:
        model_id (ModelId): Model identifier
        number_requests (int): Number of requests
        inputs_tokens (int): Number of tokens for input
        outputs_tokens (int): Number of tokens for output

    Properties:
        cost (float): Cost of the inference in $ (input + output)
        number_requests_per_dollar (float): Number of requests available for 1$
        avg_outputs_tokens (float): Average number of tokens for output
    """

    model_id: ModelId
    number_requests: int
    inputs_tokens: int
    outputs_tokens: int

    @property
    def cost(self):
        """Return the cost of the inference in $"""
        cost_input = self.inputs_tokens * self.model_id.input_cost_million
        cost_output = self.outputs_tokens * self.model_id.output_cost_million
        calcul = (cost_input + cost_output) / 1_000_000
        return calcul

    @property
    def number_requests_per_dollar(self):
        """Return the number of requests available for 1$"""
        return 1 / self.cost

    @property
    def avg_outputs_tokens(self):
        """Return the average number of tokens for output"""
        return self.outputs_tokens / self.number_requests


@dataclass
class OutputGeneration:
    """
    Stock and count a list of result (LLM generation).

    Attributes:
        counter (Dict[int]): Counter of each san
        list_result (List[Result]): List of result
    """

    counter: Counter
    list_result: List[Result]

    @property
    def most_common(self) -> str:
        """Return the most common SAN move."""
        list_san_count = self.counter.most_common(1)

        if not list_san_count:
            list_valid_san = [", ".join(result.san for result in self.list_result)]
            raise ValueError(f"No valid SAN move found, all results: {list_valid_san}")

        return list_san_count[0][0]

    @classmethod
    def from_inference(
        cls,
        board: chess.Board,
        list_san: Iterable[str],
        preprocess_func: Optional[Callable] = None,
    ) -> Self:
        """
        Create CounterResult from inference outputs of method Model class.

        Args:
            board (chess.Board): Board to test each san
            list_san (Iterable[str]): List of san to test
            preprocess_func (Callable, optional): Preprocess function for each san. Defaults to None.

        Returns:
            OutputGeneration: instance with all results
        """
        list_results = []
        counter = Counter()

        # If no preprocess function, don't change san
        if preprocess_func is None:
            preprocess_func = postprocess_result

        for san in list_san:
            exception = None
            postprocess_san = preprocess_func(san)

            try:
                # Test if the san is valid move
                board.push_san(postprocess_san)
            except Exception as _exception:
                # Get error for stock in Result
                exception = _exception
            else:
                # Board don't push on error
                board.pop()

                # Add to Counter only if don't have error
                counter.update([postprocess_san])
            finally:
                # Any case, stock result of validation move
                result = Result(
                    san=san,
                    postprocess_san=postprocess_san,
                    exception=exception,
                )

                list_results.append(result)

        return cls(
            counter=counter,
            list_result=list_results,
        )


class Output(OutputGeneration, OutputInference):
    """Output of LLM Inference and generation."""

    def __init__(
        self,
        model_id: ModelId,
        number_requests: int,
        inputs_tokens: int,
        outputs_tokens: int,
        counter: Counter,
        list_result: List[Result],
    ):
        OutputGeneration.__init__(
            self,
            counter=counter,
            list_result=list_result,
        )

        OutputInference.__init__(
            self,
            model_id=model_id,
            number_requests=number_requests,
            inputs_tokens=inputs_tokens,
            outputs_tokens=outputs_tokens,
        )

    @classmethod
    def from_outputs(
        cls,
        output_gen: OutputGeneration,
        output_inf: OutputInference,
    ) -> "Output":
        """Allow to create Output from OutputGeneration and OutputInference."""
        return cls(
            counter=output_gen.counter,
            list_result=output_gen.list_result,
            model_id=output_inf.model_id,
            number_requests=output_inf.number_requests,
            inputs_tokens=output_inf.inputs_tokens,
            outputs_tokens=output_inf.outputs_tokens,
        )
