# SmallAgents

[![CI](https://github.com/Semir-Harun/SmallAgents/workflows/CI/badge.svg)](https://github.com/Semir-Harun/SmallAgents/actions)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

## Purpose

SmallAgents is a minimal Python framework for building small, standalone "agents"—lightweight components that perform autonomous tasks (searching, web requests, simple workflows) and can be composed into larger systems.

## Stack

- **Python 3.8+** - Modern Python with type hints
- **PyYAML** - Configuration parsing
- **requests** - HTTP client for API calls
- **aiohttp** - Async HTTP support
- **pytest** - Testing framework
- **ruff** - Fast Python linter and formatter
- **mypy** - Static type checking

Designed to be framework-agnostic (easy to integrate with LangChain, AgentScript, or other agent frameworks)

## Features

- 🚀 **Lightweight & Fast** - Minimal dependencies, maximum performance
- 🔄 **Sync & Async** - Support for both synchronous and asynchronous agents
- 🛡️ **Error Handling** - Built-in retry logic and robust error handling
- 🧪 **Well Tested** - Comprehensive test suite with high coverage
- 📦 **Easy Integration** - Simple API that works with existing Python projects
- 🐳 **Docker Ready** - Containerized deployment support
- 🔧 **Type Safe** - Full type hint coverage with mypy validation

## Usage

This repository contains a CLI entrypoint (`main.py`) that demonstrates running agents. Agents live under `agents/` and implement a simple `BaseAgent` interface.

### Available Agents

- **SearchAgent** - Performs text search over a predefined corpus
- **APIAgent** - Makes HTTP requests with retry logic and error handling
- **AsyncSearchAgent** - Async version with concurrent processing

## Project Structure

```
SmallAgents/
├── agents/
│   ├── __init__.py            # Package initialization
│   ├── base_agent.py          # Base Agent class and interface
│   ├── search_agent.py        # Example search agent
│   ├── api_agent.py           # HTTP API agent with retries
│   ├── async_agent.py         # Async base agent
│   └── async_search_agent.py  # Async search agent
├── utils/
│   ├── __init__.py            # Utility package
│   └── helpers.py             # Helper functions
├── tests/
│   ├── test_base_agent.py     # Base agent tests
│   ├── test_search_agent.py   # Search agent tests
│   ├── test_api_agent.py      # API agent tests
│   └── test_async_search_agent.py # Async agent tests
├── examples/                   # Usage examples (coming soon)
├── .github/workflows/          # CI/CD configuration
├── config.yaml                # Example configuration
├── main.py                    # CLI entrypoint
├── pyproject.toml             # Project configuration
├── requirements.txt           # Production dependencies
├── requirements-dev.txt       # Development dependencies
├── Dockerfile                 # Container configuration
├── docker-compose.yml         # Multi-container setup
├── README.md                  # This file
├── CONTRIBUTING.md            # Contribution guidelines
├── LICENSE                    # MIT License
└── .gitignore                 # Git ignore rules
```

## Quickstart

### Option 1: Local Installation

1. **Clone and setup**
   ```bash
   git clone https://github.com/Semir-Harun/SmallAgents.git
   cd SmallAgents
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run examples**
   ```bash
   # Search agent
   python main.py --agent search --query "agents"
   
   # With custom config
   python main.py --agent search --query "Python" --config config.yaml
   ```

### Option 2: Docker

```bash
# Run with Docker Compose
docker-compose run smallagents

# Run tests in container
docker-compose run smallagents-dev

# Interactive development
docker-compose run smallagents-interactive
```

## Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest -v

# Run tests with coverage
pytest --cov=agents --cov=utils

# Check code quality
ruff check .
ruff format --check .
mypy .
```

### Creating New Agents

```python
from agents.base_agent import BaseAgent
from typing import Any, Dict

class MyAgent(BaseAgent):
    def run(self, **kwargs: Any) -> Dict[str, Any]:
        # Your agent logic here
        return {"result": "success", "data": kwargs}

# Usage
agent = MyAgent({"setting": "value"})
result = agent.run(param="test")
```

### Async Agents

```python
import asyncio
from agents.async_agent import AsyncBaseAgent

class MyAsyncAgent(AsyncBaseAgent):
    async def run(self, **kwargs: Any) -> Dict[str, Any]:
        # Async agent logic here
        await asyncio.sleep(0.1)  # Simulate async work
        return {"result": "async_success"}

# Usage
async def main():
    agent = MyAsyncAgent()
    result = await agent.run(param="test")
    
asyncio.run(main())
```

## Examples

### Basic Search
```python
from agents.search_agent import SearchAgent

agent = SearchAgent()
result = agent.run(query="Python agents")
print(f"Found {result['result_count']} results")
```

### API Requests
```python
from agents.api_agent import APIAgent

agent = APIAgent({
    "base_url": "https://jsonplaceholder.typicode.com",
    "timeout": 30
})
result = agent.run(method="GET", endpoint="/posts/1")
print(result["data"])
```

### Async Processing
```python
import asyncio
from agents.async_search_agent import AsyncSearchAgent

async def main():
    agent = AsyncSearchAgent({"concurrent_searches": 5})
    result = await agent.run(query="async")
    print(f"Execution time: {result['execution_time']:.3f}s")

asyncio.run(main())
```

## Configuration

Create a `config.yaml` file to customize agent behavior:

```yaml
agents:
  search:
    max_results: 10
  api:
    base_url: "https://api.example.com"
    timeout: 30
    max_retries: 3
    backoff_factor: 0.3
  async_search:
    concurrent_searches: 5
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Roadmap

- [ ] Add more agent examples (file processing, database operations)
- [ ] Integration with popular agent frameworks (LangChain, CrewAI)
- [ ] Web UI for agent management
- [ ] Plugin system for custom agents
- [ ] Performance benchmarking tools
- [ ] Agent composition and chaining utilities