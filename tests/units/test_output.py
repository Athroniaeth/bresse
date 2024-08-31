from collections import Counter

import pytest

from bresse.identifiers.base import ModelId
from bresse.output import OutputGeneration, OutputInference

model_id = ModelId(
    id="gpt-3.5-turbo-instruct",
    input_cost_million=10,
    output_cost_million=20,
)

output_gen = OutputInference(
    model_id=model_id,
    number_requests=10,
    inputs_tokens=3,
    outputs_tokens=6,
)


def test_output_inf_cost():
    """Test OutputInference cost property."""
    assert output_gen.cost == 0.00015


def test_output_number_requests_per_dollar():
    """Test OutputInference number_requests_per_dollar property"""
    result = round(output_gen.number_requests_per_dollar, 3)
    assert result == 6666.667


def test_output_avg_outputs_tokens():
    """Test OutputInference avg_outputs_tokens property"""
    assert output_gen.avg_outputs_tokens == 0.6


def test_output_gen_init_error():
    """Test OutputGeneration init with error."""
    output = OutputGeneration(
        counter=Counter(),
        list_result=[],
    )

    with pytest.raises(ValueError):
        output.most_common  # noqa
