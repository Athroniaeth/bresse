from typing import List, Literal, final, override

from openai import OpenAI

from bresse.identifiers.base import ModelId
from bresse.identifiers.openai import GPT35Turbo
from bresse.input import ConfigInference
from bresse.models.base import ModelCloud
from bresse.output import OutputInference

AVAILABLE_MODELS = Literal["gpt-3.5-turbo-instruct",]


class OpenAIModel(ModelCloud):
    """OpenAI Cloud Model class for inference."""

    list_models: List[ModelId] = [GPT35Turbo()]

    def __init__(self, model_id: AVAILABLE_MODELS, api_key: str):
        # Check if model_id is available, api_key is valid
        super().__init__(model_id, api_key)

        # Initialize OpenAI client
        self.client = OpenAI(api_key=api_key)

    @final
    @override
    def _inference(self, pgn_prompt: str, config: ConfigInference = ConfigInference()):
        completion = self.client.completions.create(
            model=self.model_id.id,
            prompt=pgn_prompt,
            # stop=["\n", "#", "1-0", "0-1"],  # '1/2-1/2' is not a valid stop token
            seed=config.seed,
            n=config.n,
            best_of=config.best_of,
            max_tokens=config.max_tokens,
            presence_penalty=config.presence_penalty,
            frequency_penalty=config.frequency_penalty,
            top_p=config.top_p,
            temperature=config.temperature,
            logprobs=config.logprobs,
            logit_bias=config.logit_bias,
        )

        input_tokens = completion.usage.prompt_tokens
        output_tokens = completion.usage.completion_tokens

        output_inf = OutputInference(
            model_id=self.model_id,
            number_requests=1,
            inputs_tokens=input_tokens,
            outputs_tokens=output_tokens,
        )

        list_generation = [choice.text for choice in completion.choices]

        return output_inf, list_generation
