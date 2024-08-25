from dataclasses import dataclass

from bresse.identifiers.base import ModelId


@dataclass
class GPT35Turbo(ModelId):
    id: str = "gpt-3.5-turbo-instruct"
    input_cost_million: int = 3
    output_cost_million: int = 6
