import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

from bresse.models.openai import OpenAIModel
from bresse.output import OutputInference
from bresse.result import OutputGeneration
from tests.conftest import load_path_pgn

# Load environment variables
load_dotenv()


@pytest.mark.costly
@pytest.mark.parametrize("path_pgn", load_path_pgn())
def test_models_inference(path_pgn: Path) -> None:
    pgn = path_pgn.read_text()

    model = OpenAIModel(
        model_id="gpt-3.5-turbo-instruct",
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    output, counter = model.inference(pgn)

    assert isinstance(output, OutputInference)
    assert output.model_id == model.model

    assert output.number_requests == 1
    # assert output.inputs_tokens == ... # Depends on the PGN

    assert isinstance(counter, OutputGeneration)
    print()
    # Result depends on Board (and therefore PGN, test only the type)
