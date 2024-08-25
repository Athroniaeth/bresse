from dataclasses import dataclass

from bresse.identifiers.base import ModelId


@dataclass
class Output:
    """
    Output of LLM Inference.

    Attributes:
        model_id (ModelId): Model identifier
        number_requests (int): Number of requests
        inputs_tokens (int): Number of tokens for input
        outputs_tokens (int): Number of tokens for output

    Properties:
        cost (float): Cost of the inference in $ (input + output)
        number_requests_per_dollar (float): Number of requests available for 1$
        avg_outputs_tokens (float): Average number of tokens for output
    """

    model_id: ModelId
    number_requests: int
    inputs_tokens: int
    outputs_tokens: int

    @property
    def cost(self):
        """Return the cost of the inference in $"""
        cost_input = self.inputs_tokens * self.model_id.input_cost_million
        cost_output = self.outputs_tokens * self.model_id.output_cost_million
        calcul = (cost_input + cost_output) / 1_000_000
        return calcul

    @property
    def number_requests_per_dollar(self):
        """Return the number of requests available for 1$"""
        return 1 / self.cost

    @property
    def avg_outputs_tokens(self):
        """Return the average number of tokens for output"""
        return self.outputs_tokens / self.number_requests
