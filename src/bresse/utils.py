from typing import Type

from bresse.identifiers.base import ModelId
from bresse.models.base import ModelCloud


def _find_model_id(model_id: str) -> Type[ModelId]:
    """Browse all existing ModelId to find the class."""
    generator = (model for model in ModelId.__subclasses__() if model.id == model_id)
    result = next(generator, None)

    if result is not None:
        return result

    raise ValueError(f"ModelId with ID '{model_id}' not found.")


def find_model(model_id: str) -> Type[ModelCloud]:
    """Find a model by its ID."""
    model_id = _find_model_id(model_id)
    models = (model for model in ModelCloud.__subclasses__())

    for model in models:
        generator = (
            model
            for model_id_found in model.list_models
            if isinstance(model_id_found, model_id)
        )
        result = next(generator, None)

        if result is not None:
            return result

    raise ValueError(f"Model with ModelId '{model_id}' not found.")
