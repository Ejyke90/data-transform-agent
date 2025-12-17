# Data Transform Agent

An AI-powered tool to transform data schemas from XSD (XML Schema Definition) format to JSON Schema and Avro schema formats.

## Features

- **XSD Parser**: Parse and analyze XSD schema files
- **JSON Schema Converter**: Transform XSD to JSON Schema (Draft 2020-12)
- **Avro Schema Converter**: Transform XSD to Apache Avro schema format
- **AI Enhancement**: Optional AI-powered schema optimization using OpenAI GPT-4
- **CLI Interface**: Easy-to-use command-line interface
- **Type Mapping**: Comprehensive type mappings between XSD, JSON Schema, and Avro
- **Complex Types**: Support for complex types, nested structures, and attributes

## Installation

### Using pip

```bash
pip install -r requirements.txt
```

### For development

```bash
pip install -e ".[dev]"
```

## Quick Start

### Basic Usage

Transform an XSD schema to JSON Schema:

```bash
python -m data_transform_agent.cli transform examples/person.xsd output.json --format json
```

Transform an XSD schema to Avro format:

```bash
python -m data_transform_agent.cli transform examples/person.xsd output.avsc --format avro
```

### With AI Enhancement

To use AI-powered enhancement, set your OpenAI API key:

```bash
export OPENAI_API_KEY="your-api-key-here"
python -m data_transform_agent.cli transform examples/person.xsd output.json --format json --use-ai
```

### Analyze XSD Schema

Analyze and display the structure of an XSD schema:

```bash
python -m data_transform_agent.cli analyze examples/person.xsd
```

### Get AI Suggestions

Get AI-powered suggestions for schema transformation:

```bash
python -m data_transform_agent.cli suggest examples/person.xsd --format json
```

## Python API

### Basic Transformation

```python
from data_transform_agent.transformer import SchemaTransformer

# Initialize transformer
transformer = SchemaTransformer(use_ai=False)

# Transform to JSON Schema
json_schema = transformer.transform_to_json(
    xsd_path="examples/person.xsd",
    output_path="output.json"
)

# Transform to Avro Schema
avro_schema = transformer.transform_to_avro(
    xsd_path="examples/person.xsd",
    output_path="output.avsc",
    namespace="com.myorg"
)
```

### With AI Enhancement

```python
from data_transform_agent.transformer import SchemaTransformer

# Initialize transformer with AI
transformer = SchemaTransformer(
    use_ai=True,
    api_key="your-openai-api-key"
)

# Transform with AI enhancement
json_schema = transformer.transform(
    xsd_path="examples/person.xsd",
    output_format="json",
    output_path="output.json"
)
```

### Parse XSD Only

```python
from data_transform_agent.xsd_parser import XSDParser

# Parse XSD file
parser = XSDParser("examples/person.xsd")
schema_info = parser.get_schema_info()

# Access schema components
print(f"Elements: {schema_info['elements']}")
print(f"Types: {schema_info['types']}")
print(f"Attributes: {schema_info['attributes']}")
```

### Manual Conversion

```python
from data_transform_agent.xsd_parser import XSDParser
from data_transform_agent.json_converter import JSONSchemaConverter
from data_transform_agent.avro_converter import AvroSchemaConverter

# Parse XSD
parser = XSDParser("examples/person.xsd")
xsd_info = parser.get_schema_info()

# Convert to JSON Schema
json_converter = JSONSchemaConverter(xsd_info)
json_schema = json_converter.convert()

# Convert to Avro Schema
avro_converter = AvroSchemaConverter(xsd_info, namespace="com.example")
avro_schema = avro_converter.convert()
```

## CLI Commands

### transform

Transform an XSD schema to JSON or Avro format.

```bash
data-transform transform <xsd_file> <output_file> --format <json|avro> [options]
```

**Options:**
- `--format, -f`: Output format (json or avro) [required]
- `--namespace, -n`: Namespace for Avro schemas (default: com.example)
- `--use-ai`: Enable AI-powered enhancement
- `--api-key`: OpenAI API key (or set OPENAI_API_KEY env var)

**Examples:**

```bash
# Convert to JSON Schema
data-transform transform schema.xsd output.json --format json

# Convert to Avro with custom namespace
data-transform transform schema.xsd output.avsc --format avro --namespace com.myorg

# Use AI enhancement
data-transform transform schema.xsd output.json --format json --use-ai
```

### analyze

Analyze an XSD schema and display its structure.

```bash
data-transform analyze <xsd_file>
```

**Example:**

```bash
data-transform analyze examples/person.xsd
```

### suggest

Get AI suggestions for schema transformation.

```bash
data-transform suggest <xsd_file> --format <json|avro>
```

**Example:**

```bash
export OPENAI_API_KEY="your-api-key"
data-transform suggest examples/person.xsd --format json
```

## Type Mappings

### XSD to JSON Schema

| XSD Type | JSON Schema Type |
|----------|------------------|
| string, normalizedString, token | string |
| int, integer, long, short, byte | integer |
| decimal, float, double | number |
| boolean | boolean |
| date, time, dateTime | string (with format) |
| base64Binary, hexBinary | string |

### XSD to Avro

| XSD Type | Avro Type |
|----------|-----------|
| string | string |
| int, short, byte | int |
| long, integer | long |
| float | float |
| double, decimal | double |
| boolean | boolean |
| base64Binary, hexBinary | bytes |

## Examples

The `examples/` directory contains sample XSD schemas:

- `person.xsd`: A person schema with contact information
- `book.xsd`: A book catalog schema with authors

## Testing

Run tests with pytest:

```bash
pytest tests/
```

Run tests with coverage:

```bash
pytest --cov=data_transform_agent tests/
```

## Architecture

The tool is structured into modular components:

1. **XSD Parser** (`xsd_parser.py`): Parses XSD files and extracts schema information
2. **JSON Converter** (`json_converter.py`): Converts XSD schema info to JSON Schema
3. **Avro Converter** (`avro_converter.py`): Converts XSD schema info to Avro schema
4. **AI Agent** (`ai_agent.py`): Provides AI-powered enhancement and suggestions
5. **Transformer** (`transformer.py`): Orchestrates the transformation process
6. **CLI** (`cli.py`): Command-line interface

## Requirements

- Python 3.8+
- lxml >= 4.9.0
- xmlschema >= 2.5.0
- jsonschema >= 4.19.0
- avro >= 1.11.0
- click >= 8.1.0
- openai >= 1.0.0 (optional, for AI features)
- python-dotenv >= 1.0.0

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key for AI enhancement features

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Future Enhancements

- Support for additional schema formats (Protobuf, Thrift)
- Data validation and transformation
- Schema evolution and migration tools
- GUI interface
- Batch processing
- Schema comparison and diff tools