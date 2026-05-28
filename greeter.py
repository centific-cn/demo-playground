"""Simple greeting module for demo purposes."""
from datetime import datetime
from typing import Optional


def greet(name: Optional[str] = None, formal: bool = False) -> str:
    """
    Generate a personalized greeting message.

    Args:
        name: Optional name to greet. If None, uses generic greeting.
        formal: If True, uses formal greeting style.

    Returns:
        Personalized greeting string.

    Examples:
        >>> greet("World")
        'Hello, World!'
        >>> greet("Alice", formal=True)
        'Good day, Alice.'
    """
    if formal:
        prefix = "Good day"
        suffix = "."
    else:
        prefix = "Hello"
        suffix = "!"

    hour = datetime.now().hour
    if 5 <= hour < 12:
        time_greeting = "Good morning"
    elif 12 <= hour < 18:
        time_greeting = "Good afternoon"
    elif 18 <= hour < 22:
        time_greeting = "Good evening"
    else:
        time_greeting = "Good night"

    if name:
        if formal:
            return f"{prefix}, {name}{suffix}"
        else:
            return f"{time_greeting}, {name}{suffix}"
    else:
        return f"{prefix}{suffix}"


def get_greeting_count() -> int:
    """Return the number of available greeting types."""
    return 4  # morning, afternoon, evening, night
