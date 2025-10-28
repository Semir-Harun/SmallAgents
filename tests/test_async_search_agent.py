"""Tests for AsyncSearchAgent."""

import asyncio

import pytest

from agents.async_search_agent import AsyncSearchAgent


class TestAsyncSearchAgent:
    """Test cases for AsyncSearchAgent."""

    def test_async_search_agent_initialization(self) -> None:
        """Test AsyncSearchAgent initializes correctly."""
        agent = AsyncSearchAgent()
        assert agent.config == {}
        assert agent.concurrent_searches == 3

        config = {"concurrent_searches": 5}
        agent_with_config = AsyncSearchAgent(config)
        assert agent_with_config.concurrent_searches == 5

    def test_async_search_agent_info(self) -> None:
        """Test AsyncSearchAgent info method."""
        agent = AsyncSearchAgent()
        info = agent.info()
        assert info["name"] == "AsyncSearchAgent"
        assert info["async"] is True
        assert "config" in info

    @pytest.mark.asyncio
    async def test_async_search_agent_run_with_valid_query(self) -> None:
        """Test AsyncSearchAgent run with valid query."""
        agent = AsyncSearchAgent()
        result = await agent.run(query="agents")

        assert isinstance(result, dict)
        assert "query" in result
        assert "result_count" in result
        assert "results" in result
        assert "execution_time" in result
        assert "concurrent_searches" in result
        assert result["query"] == "agents"
        assert result["result_count"] >= 0
        assert isinstance(result["results"], list)

    @pytest.mark.asyncio
    async def test_async_search_agent_run_with_matching_query(self) -> None:
        """Test AsyncSearchAgent returns expected results for matching query."""
        agent = AsyncSearchAgent()
        result = await agent.run(query="SmallAgents")

        assert result["result_count"] > 0
        assert any("SmallAgents" in r for r in result["results"])

    @pytest.mark.asyncio
    async def test_async_search_agent_run_with_empty_query(self) -> None:
        """Test AsyncSearchAgent with empty query."""
        agent = AsyncSearchAgent()
        result = await agent.run(query="")

        assert result["query"] == ""
        assert result["result_count"] == 0
        assert result["results"] == []

    @pytest.mark.asyncio
    async def test_async_search_agent_run_with_non_matching_query(self) -> None:
        """Test AsyncSearchAgent with query that doesn't match anything."""
        agent = AsyncSearchAgent()
        result = await agent.run(query="nonexistent_term_xyz")

        assert result["result_count"] == 0
        assert result["results"] == []

    @pytest.mark.asyncio
    async def test_async_search_agent_run_with_invalid_query_type(self) -> None:
        """Test AsyncSearchAgent raises TypeError for invalid query type."""
        agent = AsyncSearchAgent()

        with pytest.raises(TypeError, match="query must be a string"):
            await agent.run(query=123)  # type: ignore

    @pytest.mark.asyncio
    async def test_async_search_agent_concurrent_execution(self) -> None:
        """Test AsyncSearchAgent executes concurrently."""
        agent = AsyncSearchAgent({"concurrent_searches": 2})

        # Run multiple searches concurrently
        tasks = [
            agent.run(query="agents"),
            agent.run(query="Python"),
            agent.run(query="async"),
        ]

        results = await asyncio.gather(*tasks)

        assert len(results) == 3
        for result in results:
            assert "execution_time" in result
            assert "concurrent_searches" in result
            assert result["concurrent_searches"] == 2

    @pytest.mark.asyncio
    async def test_async_search_private_method(self) -> None:
        """Test AsyncSearchAgent private _search method."""
        agent = AsyncSearchAgent()

        # Test with valid query
        results = await agent._search("async")
        assert isinstance(results, list)

        # Test with empty query
        empty_results = await agent._search("")
        assert empty_results == []

    @pytest.mark.asyncio
    async def test_async_search_item_method(self) -> None:
        """Test AsyncSearchAgent private _async_search_item method."""
        agent = AsyncSearchAgent()

        # Test matching item
        result = await agent._async_search_item("test agents here", ["agents"])
        assert result == "test agents here"

        # Test non-matching item
        result = await agent._async_search_item("no match", ["agents"])
        assert result is None
