from dataclasses import dataclass

from bresse.identifiers.base import ModelId


@dataclass
class Output:
    model_id: ModelId
    number_requests: int
    inputs_tokens: int
    outputs_tokens: int

    @property
    def cost(self):
        cost_input = self.inputs_tokens * self.model_id.input_cost_million
        cost_output = self.outputs_tokens * self.model_id.output_cost_million
        calcul = (cost_input + cost_output) / 1_000_000
        return calcul

    @property
    def number_requests_per_dollar(self):
        """Return the number request available for 1$"""
        return 1 / self.cost

    @property
    def avg_outputs_tokens(self):
        return self.outputs_tokens / self.number_requests
