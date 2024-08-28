from collections import Counter
from dataclasses import dataclass
from typing import Callable, Iterable, List, Optional, Self

import chess
from chess import InvalidMoveError

from bresse.process import postprocess_result


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
            CounterResult: instance with all results
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
