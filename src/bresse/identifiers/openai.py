from dataclasses import dataclass

from bresse.identifiers.base import ModelId


@dataclass
class GPT35Turbo(ModelId):
    """OpenAI Model 'GPT-3.5 Turbo Model' information."""

    id: str = "gpt-3.5-turbo-instruct"
    input_cost_million: int = 3
    output_cost_million: int = 6
