"""Module for testing the import command (if break, change minor version)."""

import importlib


def test_open_ai_model():
    """Test if user can import 'OpenAIModel' as usual."""
    try:
        importlib.util.find_spec("bresse.models OpenAIModel")
    except ImportError:
        assert (
            False
        ), "Can't import OpenAIModel with 'from bresse.models import OpenAIModel'"


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
