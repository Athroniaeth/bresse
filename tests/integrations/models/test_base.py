from pathlib import Path

import pytest

from bresse.output import OutputInference, Output
from bresse.output import OutputGeneration
from tests.conftest import FakeModel, load_path_pgn


@pytest.mark.parametrize("path_pgn", load_path_pgn())
def test_models_inference(path_pgn: Path) -> None:
    pgn = path_pgn.read_text()
    model = FakeModel(model_id="gpt-3.5-turbo-instruct")

    output = model.inference(pgn)

    assert isinstance(output, Output)
    assert output.model_id == model.model

    assert output.number_requests == 1
    assert output.outputs_tokens == 3
    # assert output.inputs_tokens == ... # Depends on the PGN
    # OutputGeneration depends on Board (and therefore PGN, test only the type)
