# Usage Examples

This guide provides practical examples of using the Data Transform Agent.

## Example 1: Transform Person Schema to JSON

```bash
python -m data_transform_agent.cli transform examples/person.xsd output.json --format json
```

**Input XSD** (`examples/person.xsd`):
- Person complex type with firstName, lastName, age, email, address
- Address complex type with street, city, state, zipCode, country
- Phone numbers as unbounded array

**Output JSON Schema** (`examples/person_schema.json`):
- JSON Schema Draft 2020-12 compliant
- Properties for Person element
- Type definitions for PersonType and AddressType
- Required fields properly marked
- Arrays for phone numbers

## Example 2: Transform Book Schema to Avro

```bash
python -m data_transform_agent.cli transform examples/book.xsd output.avsc --format avro --namespace com.example.library
```

**Input XSD** (`examples/book.xsd`):
- Book complex type with title, authors, ISBN, publish date, price, stock status
- Author complex type with name and nationality
- Multiple authors support

**Output Avro Schema** (`examples/book_schema.avsc`):
- Avro records for BookType and AuthorType
- Custom namespace: com.example.library
- Optional fields with null defaults
- Array type for multiple authors

## Example 3: Analyze XSD Structure

```bash
python -m data_transform_agent.cli analyze examples/person.xsd
```

**Output**:
```
=== XSD Schema Analysis ===

Target Namespace: http://example.com/person

Elements: 1
  - Person

Types: 2
  - PersonType (complex)
  - AddressType (complex)

Attributes: 0
```

## Example 4: Using the Python API

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

print("JSON Schema generated!")
```

### Transform to Avro with Custom Namespace

```python
from data_transform_agent.transformer import SchemaTransformer

transformer = SchemaTransformer(use_ai=False)

# Transform to Avro with custom namespace
avro_schema = transformer.transform_to_avro(
    xsd_path="examples/book.xsd",
    output_path="output.avsc",
    namespace="com.mycompany.books"
)

print(f"Avro schema: {avro_schema}")
```

### Parse and Inspect XSD

```python
from data_transform_agent.xsd_parser import XSDParser
import json

# Parse XSD file
parser = XSDParser("examples/person.xsd")
schema_info = parser.get_schema_info()

# Print schema information
print(json.dumps(schema_info, indent=2))
```

### Manual Conversion with Converters

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

print("Conversions complete!")
```

## Example 5: AI-Enhanced Transformation

To use AI enhancement, you need an OpenAI API key:

```bash
export OPENAI_API_KEY="your-api-key-here"

# Transform with AI enhancement
python -m data_transform_agent.cli transform examples/person.xsd output.json --format json --use-ai
```

**What AI Enhancement Does**:
- Reviews the XSD schema structure
- Provides suggestions for best practices
- Optimizes the converted schema
- Adds helpful descriptions where applicable

### Get AI Suggestions

```bash
python -m data_transform_agent.cli suggest examples/person.xsd --format json
```

## Type Mappings Reference

### XSD → JSON Schema

| XSD Type | JSON Schema Type |
|----------|------------------|
| xs:string | string |
| xs:int, xs:integer | integer |
| xs:decimal, xs:float, xs:double | number |
| xs:boolean | boolean |
| xs:date, xs:dateTime | string |

### XSD → Avro

| XSD Type | Avro Type |
|----------|-----------|
| xs:string | string |
| xs:int | int |
| xs:long | long |
| xs:float | float |
| xs:double | double |
| xs:boolean | boolean |

## Common Use Cases

### 1. API Schema Migration

Convert legacy XML schemas to modern JSON Schema for REST APIs:

```bash
python -m data_transform_agent.cli transform legacy_api.xsd api_schema.json --format json
```

### 2. Data Pipeline Schema Definition

Generate Avro schemas for Apache Kafka or Hadoop data pipelines:

```bash
python -m data_transform_agent.cli transform data_model.xsd kafka_schema.avsc --format avro --namespace com.company.data
```

### 3. Schema Documentation

Analyze and document existing XSD schemas:

```bash
python -m data_transform_agent.cli analyze complex_schema.xsd
```

### 4. Batch Processing

Process multiple schemas programmatically:

```python
from data_transform_agent.transformer import SchemaTransformer
from pathlib import Path

transformer = SchemaTransformer(use_ai=False)

# Process all XSD files in a directory
xsd_dir = Path("schemas")
output_dir = Path("output")

for xsd_file in xsd_dir.glob("*.xsd"):
    output_file = output_dir / f"{xsd_file.stem}.json"
    transformer.transform_to_json(str(xsd_file), str(output_file))
    print(f"Converted {xsd_file.name}")
```

## Tips and Best Practices

1. **Namespace Handling**: Always specify a meaningful namespace for Avro schemas
2. **Type Validation**: Review generated schemas to ensure type mappings are appropriate
3. **Complex Types**: For deeply nested structures, AI enhancement can provide valuable insights
4. **Testing**: Validate generated schemas with sample data before production use
5. **Version Control**: Keep both XSD and generated schemas in version control

## Troubleshooting

### Issue: XSD file not found
```
Error: XSD file not found: schema.xsd
```
**Solution**: Ensure the path to the XSD file is correct and the file exists.

### Issue: Invalid XSD schema
```
Error: Failed to parse XSD schema
```
**Solution**: Validate your XSD file against XML Schema standards.

### Issue: AI features not working
```
Warning: AI enhancement not available - API key not configured
```
**Solution**: Set the `OPENAI_API_KEY` environment variable or use `--api-key` option.

## More Information

- See [README.md](README.md) for installation and setup instructions
- Check the [tests/](tests/) directory for additional usage examples
- Review [examples/](examples/) for sample XSD files and outputs
