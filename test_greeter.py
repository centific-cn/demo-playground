"""Tests for greeter module."""
import pytest
from greeter import greet, get_greeting_count


class TestGreet:
    """Test suite for greet function."""

    def test_greet_basic(self):
        """Test basic greeting with name."""
        assert "World" in greet("World")
        assert greet("World").endswith("!")

    def test_greet_formal(self):
        """Test formal greeting style."""
        result = greet("Alice", formal=True)
        assert result.startswith("Good day")
        assert result.endswith(".")
        assert "Alice" in result

    def test_greet_none_name(self):
        """Test greeting with no name."""
        result = greet()
        assert "Hello" in result
        assert "!" in result or "." in result

    def test_greet_time_aware(self):
        """Test greeting includes time awareness."""
        result = greet("Bob")
        # Should contain time-based greeting
        time_phrases = ["Good morning", "Good afternoon", "Good evening", "Good night"]
        assert any(phrase in result for phrase in time_phrases)

    def test_greet_preserves_name(self):
        """Test that name is preserved in greeting."""
        name = "TestUser"
        assert name in greet(name)

    def test_greet_edge_cases(self):
        """Test edge cases."""
        # Empty string name - treated as no name
        assert greet("", formal=True) == "Good day."
        # Unicode name
        unicode_name = "世界"
        assert unicode_name in greet(unicode_name)


class TestGetGreetingCount:
    """Test suite for get_greeting_count function."""

    def test_count_positive(self):
        """Test count is positive integer."""
        count = get_greeting_count()
        assert isinstance(count, int)
        assert count > 0

    def test_count_expected_value(self):
        """Test count matches expected value."""
        assert get_greeting_count() == 4
