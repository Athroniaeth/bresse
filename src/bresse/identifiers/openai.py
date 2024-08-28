
from bresse.identifiers.base import ModelId


class GPT35Turbo(ModelId):
    """OpenAI Model 'GPT-3.5 Turbo Model' information."""

    id: str = "gpt-3.5-turbo-instruct"
    input_cost_million: int = 3
    output_cost_million: int = 6

    def __init__(self):
        super().__init__(
            id=self.id,
            input_cost_million=self.input_cost_million,
            output_cost_million=self.output_cost_million,
        )
