from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class InputInference:
    """
    Configuration class for setting parameters for text generation inference.

    Attributes:
        seed (int): Seed for the random number generator, ensuring reproducibility.
        n (int): Number of completions to generate and return.
        best_of (int): Number of completions generated internally, with the best one returned.
        max_tokens (int): Maximum number of tokens to generate in the completion.
        presence_penalty (float): Penalty for the presence of tokens already generated, discouraging repetition.
        frequency_penalty (float): Penalty based on the frequency of token appearance, reducing likelihood of repeated tokens.
        top_p (float): Nucleus sampling parameter, where only the tokens comprising the top_p probability mass are considered.
        temperature (float): Controls the randomness of the output; lower values make the output more deterministic.
        logprobs (int): If greater than 0, returns the log-probabilities of the top `logprobs` tokens.
        logit_bias (Dict[str, int]): A dictionary mapping tokens to bias values, adjusting their likelihood in the output.
    """

    seed: Optional[int] = 42

    n: Optional[int] = 1
    best_of: Optional[int] = 1
    max_tokens: Optional[int] = 4

    presence_penalty: Optional[float] = None
    frequency_penalty: Optional[float] = None

    top_p: Optional[float] = None
    temperature: Optional[float] = 0.3

    logprobs: Optional[int] = 0
    logit_bias: Dict[str, int] = field(default_factory=dict)
