#!/usr/bin/env python3
"""Basic usage examples for SmallAgents."""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.api_agent import APIAgent
from agents.search_agent import SearchAgent


def basic_search_example():
    """Demonstrate basic search agent usage."""
    print("=== Basic Search Agent Example ===")

    # Create agent with default configuration
    agent = SearchAgent()

    # Run some searches
    queries = ["agents", "Python", "LangChain", "nonexistent"]

    for query in queries:
        result = agent.run(query=query)
        print(f"Query: '{query}' -> Found {result['result_count']} results")
        for item in result["results"]:
            print(f"  - {item}")
        print()


def configured_search_example():
    """Demonstrate search agent with custom configuration."""
    print("=== Configured Search Agent Example ===")

    # Create agent with custom configuration
    config = {"max_results": 5, "case_sensitive": False}
    agent = SearchAgent(config)

    # Show agent info
    info = agent.info()
    print(f"Agent: {info['name']}")
    print(f"Config: {info['config']}")
    print()

    # Run search
    result = agent.run(query="agents")
    print(f"Results: {result}")
    print()


def api_agent_example():
    """Demonstrate API agent usage with a test API."""
    print("=== API Agent Example ===")

    # Create API agent for JSONPlaceholder (a test API)
    config = {
        "base_url": "https://jsonplaceholder.typicode.com",
        "timeout": 10,
        "max_retries": 2,
    }
    agent = APIAgent(config)

    try:
        # GET request example
        print("Making GET request to /posts/1...")
        result = agent.get("/posts/1")

        if result["success"]:
            print(f"Success! Status: {result['status_code']}")
            print(f"Title: {result['data']['title']}")
        else:
            print(f"Failed: {result['error']}")
        print()

        # POST request example
        print("Making POST request to /posts...")
        post_data = {
            "title": "SmallAgents Test",
            "body": "This is a test post from SmallAgents",
            "userId": 1,
        }
        result = agent.post("/posts", post_data)

        if result["success"]:
            print(f"Success! Status: {result['status_code']}")
            print(f"Created post ID: {result['data']['id']}")
        else:
            print(f"Failed: {result['error']}")
        print()

    finally:
        # Always close the session
        agent.close()


def error_handling_example():
    """Demonstrate error handling in agents."""
    print("=== Error Handling Example ===")

    agent = SearchAgent()

    # Test invalid input
    try:
        agent.run(query=123)  # This should raise TypeError
    except TypeError as e:
        print(f"Caught expected error: {e}")

    # Test API agent with bad URL
    bad_agent = APIAgent({"base_url": "https://nonexistent-api.example.com"})
    result = bad_agent.run(method="GET", endpoint="/test")

    if not result["success"]:
        print(f"API error handled gracefully: {result['error_type']}")

    bad_agent.close()
    print()


def main():
    """Run all basic usage examples."""
    print("SmallAgents - Basic Usage Examples")
    print("=" * 40)
    print()

    try:
        basic_search_example()
        configured_search_example()
        api_agent_example()
        error_handling_example()

        print("All examples completed successfully!")

    except Exception as e:
        print(f"Example failed: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
