"""Example SearchAgent implementation.

This is a simple, synchronous example. Replace the `_search` stub with real logic
(e.g. web requests, API calls, or integration with a search/indexing library).
"""

from typing import Any, Dict, List, Optional

from .base_agent import BaseAgent


class SearchAgent(BaseAgent):
    """Performs a simple mock search over a predefined corpus."""

    CORPUS = [
        "SmallAgents: lightweight Python agents",
        "How to build agents with LangChain",
        "Agent orchestration patterns",
        "Writing tests for autonomous components",
    ]

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Initialize the SearchAgent."""
        super().__init__(config)

    def _search(self, query: str) -> List[str]:
        """Perform naive search over corpus."""
        # Very naive search: return corpus lines that contain all query tokens
        tokens = [t.lower() for t in query.split() if t.strip()]
        if not tokens:
            return []
        results = [s for s in self.CORPUS if all(tok in s.lower() for tok in tokens)]
        return results

    def run(self, query: str = "") -> Dict[str, Any]:
        """Run the search agent with the given query."""
        if not isinstance(query, str):
            raise TypeError("query must be a string")
        results = self._search(query)
        return {"query": query, "result_count": len(results), "results": results}
