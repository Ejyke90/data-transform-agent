# Installation and Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

### Option 1: Install from source (Recommended for Development)

```bash
# Clone the repository
git clone https://github.com/Ejyke90/data-transform-agent.git
cd data-transform-agent

# Create a virtual environment (recommended)
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

### Option 2: Install from PyPI (When published)

```bash
pip install iso20022-schema-agent
```

## Verify Installation

```bash
# Test the CLI
iso20022-agent --help

# Or run Python import test
python -c "from iso20022_agent import ISO20022SchemaAgent; print('✓ Installation successful')"
```

## Quick Start

### 1. Prepare Your Schema Files

Download ISO 20022 schemas from https://www.iso20022.org/

```bash
# Create schemas directory
mkdir -p schemas

# Place your XSD files in the schemas directory
# Example: schemas/pain.001.001.09.xsd
```

### 2. Analyze a Schema

#### Using Python:

```python
from iso20022_agent import ISO20022SchemaAgent

# Initialize agent
agent = ISO20022SchemaAgent()

# Analyze schema
agent.analyze_schema('schemas/pain.001.001.09.xsd')

# Print summary
agent.print_summary()

# Export to CSV
agent.export_csv('output/fields.csv')
```

#### Using CLI:

```bash
# Analyze and export to CSV
iso20022-agent analyze schemas/pain.001.001.09.xsd -o output/fields.csv

# Analyze and export to JSON
iso20022-agent analyze schemas/pain.001.001.09.xsd -o output/fields.json -f json

# Validate a message
iso20022-agent validate schemas/pain.001.001.09.xsd messages/payment.xml

# Compare two schema versions
iso20022-agent compare schemas/pain.001.001.09.xsd schemas/pain.001.001.11.xsd
```

### 3. Run Examples

```bash
# Basic usage example
python examples/basic_usage.py

# Validate a message
python examples/validate_message.py

# Compare versions
python examples/compare_versions.py
```

## Project Structure

```
data-transform-agent/
├── src/
│   └── iso20022_agent/
│       ├── __init__.py           # Package initialization
│       ├── schema_agent.py       # Main agent class
│       ├── field.py              # Field data model
│       ├── parser.py             # XSD parser
│       ├── exporters.py          # Export utilities
│       ├── validator.py          # Message validation
│       └── cli.py                # Command-line interface
├── examples/
│   ├── basic_usage.py            # Basic usage example
│   ├── validate_message.py       # Validation example
│   └── compare_versions.py       # Version comparison example
├── tests/
│   ├── test_field.py             # Field tests
│   └── test_agent.py             # Agent tests
├── schemas/                       # Place XSD files here
├── output/                        # Generated output files
├── requirements.txt               # Python dependencies
├── setup.py                       # Package setup
└── README.md                      # Project documentation
```

## Development Setup

### Install Development Dependencies

```bash
pip install -r requirements-dev.txt
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=iso20022_agent --cov-report=html

# Run specific test file
pytest tests/test_field.py
```

### Code Quality

```bash
# Format code with Black
black src/

# Lint with flake8
flake8 src/

# Type checking with mypy
mypy src/
```

## Configuration

Create a `config.yaml` file for custom configuration:

```yaml
iso20022_agent:
  schema_validation:
    strict_mode: true
    validate_code_lists: true
    check_deprecated_fields: true
  
  field_extraction:
    include_annotations: true
    extract_examples: true
    generate_patterns: true
  
  output_formats:
    default: csv
    available:
      - csv
      - json
      - markdown
```

## Troubleshooting

### Import Error: "No module named 'iso20022_agent'"

Make sure you've installed the package:
```bash
pip install -e .
```

Or add the src directory to your Python path:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### Schema Loading Error

Ensure your XSD file is valid and accessible:
```bash
# Check if file exists
ls -l schemas/pain.001.001.09.xsd

# Validate XML structure
xmllint --noout schemas/pain.001.001.09.xsd
```

### Missing Dependencies

Reinstall dependencies:
```bash
pip install --upgrade -r requirements.txt
```

## Getting ISO 20022 Schemas

1. Visit https://www.iso20022.org/iso-20022-message-definitions
2. Navigate to your desired message set (e.g., "Payments Initiation")
3. Download the complete message set
4. Extract XSD files to the `schemas/` directory

## Next Steps

- Read the [Quick Start Guide](.github/prompts/quick-start.md)
- Review [CSV Testing Guide](docs/csv-testing-guide.md)
- Check [ISO 20022 Reference](.github/skills/iso20022-reference.md)
- Browse [Agent Instructions](.github/prompts/agent-instructions.md)

## Support

- **Issues**: https://github.com/Ejyke90/data-transform-agent/issues
- **Discussions**: https://github.com/Ejyke90/data-transform-agent/discussions
- **Documentation**: See `docs/` directory

## License

This project is licensed under the MIT License - see the LICENSE file for details.
