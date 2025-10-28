"""Async SearchAgent implementation."""

import asyncio
from typing import Any, Dict, List, Optional

from .async_agent import AsyncBaseAgent


class AsyncSearchAgent(AsyncBaseAgent):
    """Async version of SearchAgent with concurrent processing capabilities."""

    CORPUS = [
        "SmallAgents: lightweight Python agents",
        "How to build agents with LangChain",
        "Agent orchestration patterns",
        "Writing tests for autonomous components",
        "Async programming in Python",
        "Concurrent agent execution",
        "Scalable agent architectures",
        "Event-driven agent systems",
    ]

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Initialize the AsyncSearchAgent."""
        super().__init__(config)
        self.concurrent_searches = self.config.get("concurrent_searches", 3)

    async def _async_search_item(self, item: str, tokens: List[str]) -> Optional[str]:
        """Async helper to search a single item."""
        # Simulate some async work (e.g., database lookup, API call)
        await asyncio.sleep(0.01)  # Small delay to simulate async operation

        if all(tok in item.lower() for tok in tokens):
            return item
        return None

    async def _search(self, query: str) -> List[str]:
        """Perform async search over corpus with concurrent processing."""
        tokens = [t.lower() for t in query.split() if t.strip()]
        if not tokens:
            return []

        # Process corpus items concurrently
        semaphore = asyncio.Semaphore(self.concurrent_searches)

        async def search_with_semaphore(item: str) -> Optional[str]:
            async with semaphore:
                return await self._async_search_item(item, tokens)

        # Create tasks for all corpus items
        tasks = [search_with_semaphore(item) for item in self.CORPUS]
        results = await asyncio.gather(*tasks)

        # Filter out None results
        return [result for result in results if result is not None]

    async def run(self, query: str = "") -> Dict[str, Any]:
        """Run the async search agent with the given query."""
        if not isinstance(query, str):
            raise TypeError("query must be a string")

        start_time = asyncio.get_event_loop().time()
        results = await self._search(query)
        execution_time = asyncio.get_event_loop().time() - start_time

        return {
            "query": query,
            "result_count": len(results),
            "results": results,
            "execution_time": execution_time,
            "concurrent_searches": self.concurrent_searches,
        }
