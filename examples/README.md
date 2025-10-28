# SmallAgents Examples

This directory contains practical examples and tutorials for using SmallAgents.

## Available Examples

### 1. Basic Agent Usage (`basic_usage.py`)
- Creating and running simple agents
- Configuration management
- Error handling

### 2. Async Agents (`async_examples.py`)
- Using async agents for concurrent processing
- Performance comparisons
- Best practices for async code

### 3. API Integration (`api_examples.py`)
- Making HTTP requests with retry logic
- Handling different response types
- Authentication patterns

### 4. Custom Agents (`custom_agent_example.py`)
- Building your own agent from scratch
- Advanced configuration options
- Testing strategies

## Running Examples

Each example can be run independently:

```bash
cd examples
python basic_usage.py
python async_examples.py
python api_examples.py
python custom_agent_example.py
```

## Interactive Examples

For a more interactive experience, try the Jupyter notebooks (coming soon):

```bash
pip install jupyter
jupyter notebook
```

## Docker Examples

Run examples in containers:

```bash
# Run all examples
docker-compose run smallagents python examples/basic_usage.py

# Interactive shell
docker-compose run smallagents-interactive
```