import pytest

from bresse.models import OpenAIModel
from bresse.utils import find_model


def test_find_model():
    """Test find_model function result."""
    model_type = find_model("gpt-3.5-turbo-instruct", api_key="random_key")
    assert model_type == OpenAIModel("gpt-3.5-turbo-instruct", api_key="random_key")


def test_find_model_error():
    """Test find_model function with error."""
    with pytest.raises(ValueError):
        find_model("not_found")
