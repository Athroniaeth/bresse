from typing import final, override

from huggingface_hub import InferenceClient

from bresse.chess_ import pgn_to_board
from bresse.input import ConfigInference
from bresse.models.base import ModelOnline
from bresse.output import Output, OutputGeneration, OutputInference


class HuggingFaceModel(ModelOnline):
    """OpenAI Cloud Model class for inference."""

    def __init__(self, model_id: str, api_key: str):
        # Check if model_id is available, api_key is valid
        super().__init__(model_id, api_key)

        # Initialize HuggingFace client
        self.client = InferenceClient(api_key=api_key)  # api_key == token

    @final
    @override
    def _inference(
        self, pgn_prompt: str, config: ConfigInference = ConfigInference()
    ) -> Output:
        list_san = []
        input_tokens = 0
        output_tokens = 0

        # HuggingFace throws an error if temperature is no positive
        if config.temperature == 0.0:
            config.temperature = 1e-3

        for _ in range(config.n):
            completion = self.client.text_generation(
                pgn_prompt,
                details=True,
                decoder_input_details=True,
                return_full_text=False,
                seed=config.seed,
                best_of=config.best_of,
                max_new_tokens=config.max_tokens,
                # presence_penalty=config.presence_penalty,
                frequency_penalty=config.frequency_penalty,
                top_p=config.top_p,
                temperature=config.temperature,
                # logprobs=config.logprobs,
                # logit_bias=config.logit_bias,
            )

            input_tokens += len(completion.details.prefill)
            output_tokens += completion.details.generated_tokens
            list_san.append(completion.generated_text)

        output_inf = OutputInference(
            model_id=self.model_id,
            number_requests=1,
            inputs_tokens=input_tokens,
            outputs_tokens=output_tokens,
        )

        board = pgn_to_board(pgn=pgn_prompt)
        output_gen = OutputGeneration.from_inference(board=board, list_san=list_san)

        output = Output.from_outputs(output_inf=output_inf, output_gen=output_gen)

        return output
