"""Tests for APIAgent."""

from unittest.mock import patch

import pytest
import responses

from agents.api_agent import APIAgent


class TestAPIAgent:
    """Test cases for APIAgent."""

    def test_api_agent_initialization(self) -> None:
        """Test APIAgent initializes correctly."""
        agent = APIAgent()
        assert agent.base_url == ""
        assert agent.timeout == 30
        assert agent.max_retries == 3

        config = {
            "base_url": "https://api.example.com",
            "timeout": 60,
            "max_retries": 5,
        }
        agent_with_config = APIAgent(config)
        assert agent_with_config.base_url == "https://api.example.com"
        assert agent_with_config.timeout == 60
        assert agent_with_config.max_retries == 5

    def test_api_agent_info(self) -> None:
        """Test APIAgent info method."""
        agent = APIAgent()
        info = agent.info()
        assert info["name"] == "APIAgent"
        assert "config" in info

    @responses.activate
    def test_api_agent_get_success(self) -> None:
        """Test APIAgent GET request success."""
        responses.add(
            responses.GET,
            "https://api.example.com/test",
            json={"message": "success"},
            status=200,
        )

        agent = APIAgent({"base_url": "https://api.example.com"})
        result = agent.get("/test")

        assert result["success"] is True
        assert result["status_code"] == 200
        assert result["data"]["message"] == "success"

    @responses.activate
    def test_api_agent_get_failure(self) -> None:
        """Test APIAgent GET request failure."""
        responses.add(responses.GET, "https://api.example.com/test", status=404)

        agent = APIAgent({"base_url": "https://api.example.com"})
        result = agent.get("/test")

        assert result["success"] is False
        assert "error" in result
        assert "error_type" in result

    @responses.activate
    def test_api_agent_post_success(self) -> None:
        """Test APIAgent POST request success."""
        responses.add(
            responses.POST,
            "https://api.example.com/test",
            json={"created": True},
            status=201,
        )

        agent = APIAgent({"base_url": "https://api.example.com"})
        result = agent.post("/test", {"data": "test"})

        assert result["success"] is True
        assert result["status_code"] == 201
        assert result["data"]["created"] is True

    def test_api_agent_run_get(self) -> None:
        """Test APIAgent run method with GET."""
        with patch.object(APIAgent, "get") as mock_get:
            mock_get.return_value = {"success": True, "method": "GET"}

            agent = APIAgent()
            result = agent.run(method="GET", endpoint="/test")

            assert "execution_time" in result
            assert result["method"] == "GET"
            assert result["endpoint"] == "/test"
            mock_get.assert_called_once_with("/test", None)

    def test_api_agent_run_post(self) -> None:
        """Test APIAgent run method with POST."""
        with patch.object(APIAgent, "post") as mock_post:
            mock_post.return_value = {"success": True, "method": "POST"}

            agent = APIAgent()
            result = agent.run(method="POST", endpoint="/test", data={"key": "value"})

            assert "execution_time" in result
            assert result["method"] == "POST"
            assert result["endpoint"] == "/test"
            mock_post.assert_called_once_with("/test", {"key": "value"})

    def test_api_agent_run_invalid_method(self) -> None:
        """Test APIAgent run with invalid HTTP method."""
        agent = APIAgent()

        with pytest.raises(ValueError, match="Unsupported HTTP method"):
            agent.run(method="INVALID", endpoint="/test")

    def test_api_agent_run_invalid_method_type(self) -> None:
        """Test APIAgent run with invalid method type."""
        agent = APIAgent()

        with pytest.raises(TypeError, match="method must be a string"):
            agent.run(method=123, endpoint="/test")  # type: ignore

    def test_api_agent_run_invalid_endpoint_type(self) -> None:
        """Test APIAgent run with invalid endpoint type."""
        agent = APIAgent()

        with pytest.raises(TypeError, match="endpoint must be a string"):
            agent.run(method="GET", endpoint=123)  # type: ignore

    def test_api_agent_close(self) -> None:
        """Test APIAgent close method."""
        agent = APIAgent()
        # Should not raise any exceptions
        agent.close()

        # Calling close multiple times should be safe
        agent.close()
