# SmallAgents

Purpose

SmallAgents is a minimal Python framework for building small standalone "agents"—lightweight components that perform autonomous tasks (searching, web requests, simple workflows) and can be composed into larger systems.

Stack

- Python 3.8+
- Optional: PyYAML for config parsing
- Minimal deps: requests (network), pytest (tests)
- Designed to be framework-agnostic (easy to integrate with LangChain, AgentScript, or other agent frameworks)

Usage

This repository contains a small CLI entrypoint (`main.py`) that demonstrates running an agent. Agents live under `agents/` and implement a simple `BaseAgent` interface.

By default the example `SearchAgent` performs a mock search (stub) — replace the implementation with real logic or integrate an external library.

Project layout

SmallAgents/
├── agents/
│   ├── base_agent.py      # Base Agent class and interface
│   └── search_agent.py    # Example agent (search)
├── utils/
│   └── helpers.py         # Small helper functions
├── config.yaml            # Example configuration
├── main.py                # CLI entrypoint
├── README.md              # This file
├── requirements.txt       # Minimal dependencies
├── tests/
│   └── test_base_agent.py # Simple pytest tests
└── .gitignore

Quickstart

1. (Optional) Create a virtualenv and activate

2. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

3. Run the example CLI (runs the example SearchAgent):

```powershell
python main.py --agent search --query "example"
```

Contributing

- Keep agents small, single-responsibility.
- Add tests for new behavior.
- Document config options in `config.yaml`.

License

Add a license file if you plan to open-source this repository.