"""Base agent interface for SmallAgents.

This file contains a minimal BaseAgent class to be extended by concrete agents.
"""
from typing import Any, Dict

class BaseAgent:
    """Minimal agent interface.

    Contract:
    - input: a dict-like `config` and arbitrary kwargs
    - output: a dict with at least a "result" key on success
    - error modes: raise exceptions on invalid input
    """

    def __init__(self, config: Dict[str, Any] | None = None) -> None:
        self.config = config or {}

    def run(self, *args, **kwargs) -> Dict[str, Any]:
        """Run the agent. Must be implemented by subclasses."""
        raise NotImplementedError("Agents must implement run()")

    def info(self) -> Dict[str, Any]:
        """Return metadata about the agent."""
        return {"name": self.__class__.__name__, "config": self.config}
