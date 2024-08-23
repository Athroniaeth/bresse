from abc import abstractmethod, ABC
from typing import List, final, Union

from bresse.identifiers.base import ModelId


class Model(ABC):
    list_models: List[ModelId] = []

    @abstractmethod
    def _inference(self, prompt: str) -> str:
        """Inference of the model on any string"""
        ...

    @final
    def inference(self, prompt: str) -> str:
        """Inference the model on a given prompt"""
        return self._inference(prompt)

    def _get_identifier_str(self, model_id: str) -> ModelId:
        generator = filter(lambda x: x.id == model_id, self.list_models)
        found_model = next(generator, None)

        if found_model is None:
            available_models = ", ".join(m.id for m in self.list_models)
            raise ValueError(f"Model '{model_id}' does not exist. Available models: {available_models}")

        return found_model


class ModelCloud(Model):
    model: ModelId

    def __init__(self, model_id: Union[str, ModelId]):
        # Todo : Transform to Switch Pattern
        if not self.list_models:
            raise ValueError("No models defined for this class.")

        if isinstance(model_id, str):
            self.model = self._get_identifier_str(model_id)

        elif isinstance(model_id, ModelId):
            if model_id not in self.list_models:
                raise ValueError(f"Model '{model_id.id}' is not available in '{self.__class__.__name__}'")
            self.model = model_id

        else:
            raise TypeError("Model must be either a string or a ModelId instance.")

    @abstractmethod
    def _inference(self, prompt: str) -> str:
        ...
