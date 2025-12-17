# Coding Standards

## Python Style Guide

- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Keep functions focused and single-purpose
- Maximum line length: 88 characters (Black formatter standard)

## Code Organization

```
project/
├── agents/          # Agent implementations
├── transformers/    # Data transformation logic
├── validators/      # Data validation modules
├── utils/          # Utility functions
└── tests/          # Test suite
```

## Documentation

- Add docstrings to all classes and functions
- Use Google-style or NumPy-style docstrings
- Include type information and examples in docstrings
clear- Maintain up-to-date README with usage examples

## Testing

- Write unit tests for all transformation logic
- Use pytest as the testing framework
- Aim for >80% code coverage
- Include edge cases and error scenarios in tests

## Error Handling

- Use specific exception types
- Provide meaningful error messages
- Log errors with appropriate context
- Implement retry logic for transient failures

## Version Control

- Write clear, descriptive commit messages
- Use conventional commits format (feat:, fix:, docs:, etc.)
- Keep commits atomic and focused
- Update documentation with code changes
