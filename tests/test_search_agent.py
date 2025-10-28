"""Tests for SearchAgent."""

import pytest

from agents.search_agent import SearchAgent


class TestSearchAgent:
    """Test cases for SearchAgent."""

    def test_search_agent_initialization(self) -> None:
        """Test SearchAgent initializes correctly."""
        agent = SearchAgent()
        assert agent.config == {}

        config = {"max_results": 5}
        agent_with_config = SearchAgent(config)
        assert agent_with_config.config == config

    def test_search_agent_info(self) -> None:
        """Test SearchAgent info method."""
        agent = SearchAgent()
        info = agent.info()
        assert info["name"] == "SearchAgent"
        assert "config" in info

    def test_search_agent_run_with_valid_query(self) -> None:
        """Test SearchAgent run with valid query."""
        agent = SearchAgent()
        result = agent.run(query="agents")

        assert isinstance(result, dict)
        assert "query" in result
        assert "result_count" in result
        assert "results" in result
        assert result["query"] == "agents"
        assert result["result_count"] >= 0
        assert isinstance(result["results"], list)

    def test_search_agent_run_with_matching_query(self) -> None:
        """Test SearchAgent returns expected results for matching query."""
        agent = SearchAgent()
        result = agent.run(query="SmallAgents")

        assert result["result_count"] > 0
        assert any("SmallAgents" in r for r in result["results"])

    def test_search_agent_run_with_empty_query(self) -> None:
        """Test SearchAgent with empty query."""
        agent = SearchAgent()
        result = agent.run(query="")

        assert result["query"] == ""
        assert result["result_count"] == 0
        assert result["results"] == []

    def test_search_agent_run_with_non_matching_query(self) -> None:
        """Test SearchAgent with query that doesn't match anything."""
        agent = SearchAgent()
        result = agent.run(query="nonexistent_term_xyz")

        assert result["result_count"] == 0
        assert result["results"] == []

    def test_search_agent_run_with_invalid_query_type(self) -> None:
        """Test SearchAgent raises TypeError for invalid query type."""
        agent = SearchAgent()

        with pytest.raises(TypeError, match="query must be a string"):
            agent.run(query=123)  # type: ignore

    def test_search_agent_run_with_multiple_tokens(self) -> None:
        """Test SearchAgent with multiple search tokens."""
        agent = SearchAgent()
        result = agent.run(query="agents Python")

        # Should find items that contain both "agents" and "Python"
        for item in result["results"]:
            assert "agents" in item.lower() or "python" in item.lower()

    def test_search_private_method(self) -> None:
        """Test SearchAgent private _search method."""
        agent = SearchAgent()

        # Test with valid query
        results = agent._search("SmallAgents")
        assert isinstance(results, list)
        assert len(results) > 0

        # Test with empty query
        empty_results = agent._search("")
        assert empty_results == []

        # Test with whitespace-only query
        whitespace_results = agent._search("   ")
        assert whitespace_results == []
