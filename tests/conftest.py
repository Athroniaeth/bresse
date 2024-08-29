from dataclasses import dataclass
from pathlib import Path
from typing import List, Literal, Optional, Tuple, final, override

from bresse._chess import pgn_to_board
from bresse.identifiers.base import ModelId
from bresse.models.base import ModelCloud
from bresse.output import Output
from bresse.result import CounterResult

# Path to the "data" directory
CURRENT_FOLDER = Path(__file__).parents[0]
DATA_FOLDER = CURRENT_FOLDER / "data"


@dataclass
class FakeModelId(ModelId):
    """Fake ModelId class for inference."""

    id: str = "gpt-3.5-turbo-instruct"
    input_cost_million: int = 3
    output_cost_million: int = 6


class FakeModel(ModelCloud):
    """Fake Model class for inference."""

    list_models: List[ModelId] = [FakeModelId()]

    def __init__(
        self,
        model_id: Literal["gpt-3.5-turbo-instruct"],
        list_san: Optional[List[str]] = None,
    ):
        # Check if model_id is available
        super().__init__(model_id)

        if list_san is None:
            list_san = ["e4", "e5", "Nf3", "Nc6", "Bc4", "Bc5", "Ka1"]

        self.list_san = list_san

    @final
    @override
    def _inference(self, pgn_prompt: str) -> Tuple[Output, CounterResult]:
        input_tokens = len(pgn_prompt)
        output_tokens = 3

        output = Output(
            model_id=self.model,
            number_requests=1,
            inputs_tokens=input_tokens,
            outputs_tokens=output_tokens,
        )

        board = pgn_to_board(pgn=pgn_prompt)
        parser = CounterResult.from_inference(board=board, list_san=self.list_san)

        return output, parser


def load_path_pgn() -> List[Path]:
    """Parametrize func, return all PGN files in the "data" directory."""
    generator = DATA_FOLDER.glob("**/*.pgn")
    generator = (path.absolute() for path in generator)

    list_path_pgn = list(generator)

    # Validate PGN file
    for path_pgn in list_path_pgn:
        pgn = path_pgn.read_text()
        pgn_to_board(pgn=pgn)

    assert list_path_pgn, "No PGN files found in the 'data' directory."
    return list_path_pgn
