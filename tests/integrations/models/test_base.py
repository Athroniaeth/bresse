from pathlib import Path

import chess.pgn
import pytest

from bresse.output import Output
from tests.conftest import FakeModel, load_path_pgn


@pytest.mark.parametrize("path_pgn", load_path_pgn())
def test_models_inference(path_pgn: Path) -> None:
    """Test the inference method of the model."""
    with path_pgn.open() as pgn_file:
        game = chess.pgn.read_game(pgn_file)

    model = FakeModel(model_id="gpt-3.5-turbo-instruct")

    output = model.inference(game)

    assert isinstance(output, Output)
    assert output.model_id == model.model_id

    assert output.number_requests == 1
    assert output.outputs_tokens == 3
    # assert output.inputs_tokens == ... # Depends on the PGN
    # OutputGeneration depends on Board (and therefore PGN, test only the type)
