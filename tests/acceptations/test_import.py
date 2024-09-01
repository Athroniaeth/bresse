"""Module for testing the import command (if break, change minor version)."""

import importlib.util

import pytest


@pytest.mark.parametrize(
    "class_name",
    ["OpenAIModel", "HuggingFaceModel"],
)
def test_models_import(class_name):
    """Test if user can import models as usual."""
    try:
        importlib.util.find_spec(f"bresse.models {class_name}")
    except ImportError:
        assert (
            False
        ), f"Can't import {class_name} with 'from bresse.models import {class_name}'"


def test_generate_pgn():
    """Test if user can import 'generate_pgn' as usual."""
    try:
        importlib.util.find_spec("bresse generate_pgn")
    except ImportError:
        assert False, "Can't import generate_pgn with 'from bresse import generate_pgn'"


def test_game_play_san():
    """Test if user can import 'game_play_san' as usual."""
    try:
        importlib.util.find_spec("bresse game_play_san")
    except ImportError:
        assert (
            False
        ), "Can't import game_play_san with 'from bresse import game_play_san'"


def test_pgn_to_board():
    """Test if user can import 'pgn_to_board' as usual."""
    try:
        importlib.util.find_spec("bresse._chess pgn_to_board")
    except ImportError:
        assert (
            False
        ), "Can't import pgn_to_board with 'from bresse._chess import pgn_to_board'"


def test_get_child_node():
    """Test if user can import 'get_child_node' as usual."""
    try:
        importlib.util.find_spec("bresse._chess get_child_node")
    except ImportError:
        assert (
            False
        ), "Can't import get_child_node with 'from bresse._chess import get_child_node'"


def test_find_model():
    """Test if user can import 'get_child_node' as usual."""
    try:
        importlib.util.find_spec("bresse find_model")
    except ImportError:
        assert (
            False
        ), "Can't import get_child_node with 'from bresse._chess import get_child_node'"
