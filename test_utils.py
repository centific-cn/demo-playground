"""Tests for utils module."""
from utils import greet


def test_greet():
    assert greet("World") == "Hello, World!"
    assert greet("Alice") == "Hello, Alice!"
    assert greet("Bob") == "Hello, Bob!"


def test_greet_empty():
    assert greet("") == "Hello, !"
