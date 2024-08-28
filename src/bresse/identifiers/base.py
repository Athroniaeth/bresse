from dataclasses import dataclass


@dataclass
class ModelId:
    """
    Model identifier purpose by company

    Attributes:
        id (str): Model identifier (ex: 'gpt-3.5-turbo')
        input_cost_million (int): Cost in million for input (in $)
        output_cost_million (int): Cost in million for output (in $)
    """

    id: str
    input_cost_million: int
    output_cost_million: int

    def __repr__(self):
        return f"{self.id}"
