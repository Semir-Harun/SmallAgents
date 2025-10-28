# Contributing to SmallAgents

We welcome contributions to SmallAgents! This document provides guidelines for contributing to the project.

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Semir-Harun/SmallAgents.git
   cd SmallAgents
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

## Code Quality

We maintain high code quality standards using automated tools:

### Linting and Formatting
```bash
# Check code formatting
ruff format --check .

# Format code
ruff format .

# Check for linting issues
ruff check .

# Fix auto-fixable linting issues
ruff check --fix .
```

### Type Checking
```bash
# Run type checking
mypy .
```

### Testing
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=agents --cov=utils

# Run specific test file
pytest tests/test_search_agent.py

# Run tests matching a pattern
pytest -k "test_search"
```

## Contribution Guidelines

### 1. Code Style
- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Write descriptive docstrings for all classes and functions
- Keep functions small and focused on a single responsibility

### 2. Testing
- Write tests for all new functionality
- Maintain or improve test coverage
- Include both unit tests and integration tests where appropriate
- Use descriptive test names that explain what is being tested

### 3. Documentation
- Update README.md if adding new features
- Add docstrings to new classes and methods
- Include usage examples for new agents

### 4. Git Workflow

#### Branch Naming
- `feature/description` - for new features
- `bugfix/description` - for bug fixes
- `docs/description` - for documentation updates

#### Commit Messages
Use conventional commit format:
```
type(scope): description

Examples:
feat(agents): add new APIAgent with retry logic
fix(search): handle empty query edge case
docs(readme): update installation instructions
test(api): add integration tests for APIAgent
```

#### Pull Request Process
1. Create a feature branch from `main`
2. Make your changes with appropriate tests
3. Ensure all tests pass and code quality checks pass
4. Update documentation as needed
5. Submit a pull request with a clear description

## Adding New Agents

When creating a new agent:

1. **Inherit from BaseAgent or AsyncBaseAgent**
   ```python
   from agents.base_agent import BaseAgent
   
   class MyAgent(BaseAgent):
       def run(self, **kwargs) -> Dict[str, Any]:
           # Implementation here
           return {"result": "success"}
   ```

2. **Add comprehensive type hints**
3. **Write thorough tests**
4. **Add configuration options to config.yaml**
5. **Update the CLI in main.py if needed**
6. **Document usage in README.md**

## Testing Your Changes

Before submitting a pull request:

```bash
# Run the full test suite
pytest -v

# Check code quality
ruff check .
ruff format --check .
mypy .

# Test the CLI
python main.py --agent search --query "test"

# Test with Docker
docker-compose run smallagents-dev
```

## Questions?

If you have questions about contributing, please:
1. Check existing issues and discussions
2. Create a new issue with the "question" label
3. Join our discussions in the repository

Thank you for contributing to SmallAgents!