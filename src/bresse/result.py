from collections import defaultdict
from dataclasses import dataclass
from typing import Optional, Callable, Iterable, List

import chess
from chess import InvalidMoveError


@dataclass
class Result:
    san: str
    postprocess_san: str
    exception: Optional[InvalidMoveError]


@dataclass
class CounterResult:
    counter: defaultdict
    list_result: List[Result]

    @classmethod
    def from_inference(
            cls,
            board: chess.Board,
            list_san: Iterable[str],
            preprocess_func: Optional[Callable] = None
    ):
        # Get the Board of end PGN
        if preprocess_func is None:
            preprocess_func = lambda x: x

        counter = defaultdict(int)
        list_results = []

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
