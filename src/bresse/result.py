from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, Iterable, List, Optional, Self

import chess
from chess import InvalidMoveError


@dataclass
class Result:
    """Result of LLM generation."""

    san: str
    postprocess_san: str
    exception: Optional[InvalidMoveError]


@dataclass
class CounterResult:
    """
    Stock and count a list of result (LLM generation).

    Attributes:
        counter (Dict[int]): Counter of each san
        list_result (List[Result]): List of result
    """

    counter: defaultdict
    list_result: List[Result]

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
            CounterResult: instance with all results
        """
        list_results = []
        counter = defaultdict(int)

        # If no preprocess function, don't change san
        if preprocess_func is None:
            preprocess_func = lambda x: x  # noqa: E731

        for san in list_san:
            exception = None
            postprocess_san = preprocess_func(san)
            counter[postprocess_san] += 1

            try:
                # Test if the san is valid move
                board.push_san(postprocess_san)
            except Exception as _exception:
                # Get error for stock in Result
                _exception = exception
            else:
                # Board don't push on error
                board.pop()
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
