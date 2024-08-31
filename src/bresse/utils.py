from typing import Optional, Type

from bresse.identifiers.base import ModelId
from bresse.models.base import Model, ModelCloud


def _find_model_id(model_id: str) -> Type[ModelId]:
    """Browse all existing ModelId to find the class."""
    generator = (model for model in ModelId.__subclasses__() if model.id == model_id)
    result = next(generator, None)

    if result is not None:
        return result

    raise ValueError(f"ModelId with ID '{model_id}' not found.")


def find_model(model_id: str, api_key: Optional[str] = None) -> Model:
    """
    Find a model by its ModelId string.

    Notes:
        The purpose of this function is for CLI applications
        so that you don't have to manage all the possibilities yourself

    Args:
        model_id (str): Model ID to find
        api_key (Optional[str]): API key for cloud models

    Returns:
        Model: Model found by its ModelId string
    """
    identifier = _find_model_id(model_id)
    models = (model for model in ModelCloud.__subclasses__())

    for model in models:
        generator = (
            model
            for identifier_found in model.list_models
            if isinstance(identifier_found, identifier)
        )
        result = next(generator, None)

        if result is not None:
            if issubclass(result, ModelCloud):
                return result(model_id=model_id, api_key=api_key)

            if issubclass(result, Model):
                return result(model_id=model_id)

    raise ValueError(f"Model with ModelId '{identifier}' not found.")
