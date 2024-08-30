from typing import List, Literal, final, override

from openai import OpenAI

from bresse._chess import pgn_to_board
from bresse.identifiers.base import ModelId
from bresse.identifiers.openai import GPT35Turbo
from bresse.input import InputInference
from bresse.models.base import ModelCloud
from bresse.output import Output, OutputGeneration, OutputInference

AVAILABLE_MODELS = Literal["gpt-3.5-turbo-instruct",]


class OpenAIModel(ModelCloud):
    """OpenAI Cloud Model class for inference."""

    list_models: List[ModelId] = [GPT35Turbo()]

    def __init__(self, model_id: AVAILABLE_MODELS, api_key: str):
        # Check if model_id is available
        super().__init__(model_id)

        # Initialize OpenAI client
        self.client = OpenAI(api_key=api_key)

    @final
    @override
    def _inference(
        self, pgn_prompt: str, config: InputInference = InputInference()
    ) -> Output:
        completion = self.client.completions.create(
            model=self.model.id,
            prompt=pgn_prompt,
            stop=["\n", "#", "1-0", "0-1"],  # '1/2-1/2' is not a valid stop token
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
            model_id=self.model,
            number_requests=1,
            inputs_tokens=input_tokens,
            outputs_tokens=output_tokens,
        )

        board = pgn_to_board(pgn=pgn_prompt)
        list_san = [choice.text for choice in completion.choices]
        output_gen = OutputGeneration.from_inference(board=board, list_san=list_san)

        output = Output.from_outputs(output_inf=output_inf, output_gen=output_gen)

        return output
