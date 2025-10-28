"""Async base agent interface for SmallAgents."""

from typing import Any, Dict, Optional


class AsyncBaseAgent:
    """Async version of the minimal agent interface.

    Contract:
    - input: a dict-like `config` and arbitrary kwargs
    - output: a dict with at least a "result" key on success
    - error modes: raise exceptions on invalid input
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Initialize the agent with optional configuration."""
        self.config = config or {}

    async def run(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """Run the agent asynchronously. Must be implemented by subclasses."""
        raise NotImplementedError("Async agents must implement run()")

    def info(self) -> Dict[str, Any]:
        """Return metadata about the agent."""
        return {"name": self.__class__.__name__, "config": self.config, "async": True}
