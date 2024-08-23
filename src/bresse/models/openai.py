from typing import List, Literal, final

from bresse.identifiers.base import ModelId
from bresse.identifiers.openai import GPT35Turbo
from bresse.models.base import ModelCloud


class OpenAIModel(ModelCloud):
    list_models: List[ModelId] = [GPT35Turbo()]

    def __init__(self, model_id: Literal['gpt-3.5-turbo']):
        super().__init__(model_id)

    @final
    def _inference(self, prompt: str) -> str:
        # Implementation specific to OpenAI model inference
        return f"Inferencing using {self.model.id} with prompt: {prompt}"
