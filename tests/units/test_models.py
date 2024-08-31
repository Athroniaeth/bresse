import chess.pgn
import pytest

from bresse.input import Input
from tests.conftest import FakeModel, FakeModelId


def test_model_list_models_empty():
    model_id = "gpt-3.5-turbo-instruct"

    class FakeModelEmpty(FakeModel):
        list_models = []

    with pytest.raises(ValueError):
        FakeModelEmpty(model_id=model_id)  # type: ignore


def test_model_id():
    model_id = FakeModelId("gpt-3.5-turbo-instruct")

    model = FakeModel(model_id=model_id)  # type: ignore

    assert model.model == model_id


def test_model_id_not_exist_str():
    model_id = "dont_exist"

    with pytest.raises(ValueError):
        FakeModel(model_id=model_id)  # type: ignore


def test_model_id_not_exist_class():
    model_id = FakeModelId(id="dont_exist")

    with pytest.raises(ValueError):
        FakeModel(model_id=model_id)  # type: ignore


def test_model_id_bad_type():
    model_id = 42

    with pytest.raises(TypeError):
        FakeModel(model_id=model_id)  # type: ignore


def test_model_play():
    game = chess.pgn.Game()

    input_ = Input(n=1)
    model = FakeModel(
        model_id="gpt-3.5-turbo-instruct",
        list_san=["a4"],
    )

    model.play(game, input_)
    assert game.variations[0].move == chess.Move.from_uci(
        "a2a4"
    ), "Move could not be played"
