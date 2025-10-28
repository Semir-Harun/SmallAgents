"""Small helper utilities for SmallAgents."""
from typing import Any


def ensure_str(x: Any, default: str = "") -> str:
    """Return a string or the default if None."""
    if x is None:
        return default
    return str(x)
