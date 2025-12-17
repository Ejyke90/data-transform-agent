# Using CSV Output for Testing and Validation

## Overview

The CSV output format is specifically designed to make testing and validation easier. This document explains how to use the extracted field information for various testing scenarios.

## CSV Structure

Each row contains:
- **FieldName**: Business-friendly name (e.g., MessageIdentification)
- **Path**: XML path for locating the field in messages
- **Multiplicity**: Requirement indicator (1..1, 0..1, 1..n, 0..n)
- **Constraints**: Validation rules (length, pattern, type, codes)
- **Definition**: Business purpose of the field

## Use Case 1: Automated Validation Testing

### Load CSV into Test Framework

```python
import csv
import re
from typing import Dict, List

def load_field_definitions(csv_path: str) -> List[Dict]:
    """Load field definitions from CSV."""
    fields = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        # Skip comment lines
        reader = csv.DictReader(line for line in f if not line.startswith('#'))
        for row in reader:
            fields.append(row)
    return fields

# Load the field definitions
fields = load_field_definitions('pain001_fields_sample.csv')
print(f"Loaded {len(fields)} field definitions")
```

### Extract Mandatory Fields for Testing

```python
def get_mandatory_fields(fields: List[Dict]) -> List[Dict]:
    """Get all mandatory fields (1..1 or 1..n)."""
    return [
        field for field in fields
        if field['Multiplicity'].startswith('1..')
    ]

mandatory = get_mandatory_fields(fields)
print(f"Found {len(mandatory)} mandatory fields to test")

# Generate test cases for missing mandatory fields
for field in mandatory:
    print(f"TEST: Verify error when {field['FieldName']} is missing")
    print(f"  Path: {field['Path']}")
```

### Validate Field Constraints

```python
def parse_constraints(constraint_str: str) -> Dict:
    """Parse constraint string into validation rules."""
    constraints = {}
    
    # Parse MaxLength
    max_length = re.search(r'MaxLength: (\d+)', constraint_str)
    if max_length:
        constraints['max_length'] = int(max_length.group(1))
    
    # Parse Pattern
    pattern = re.search(r'Pattern: (.+?)(?:;|$)', constraint_str)
    if pattern:
        constraints['pattern'] = pattern.group(1).strip()
    
    # Parse TotalDigits
    total_digits = re.search(r'TotalDigits: (\d+)', constraint_str)
    if total_digits:
        constraints['total_digits'] = int(total_digits.group(1))
    
    # Parse FractionDigits
    fraction_digits = re.search(r'FractionDigits: (\d+)', constraint_str)
    if fraction_digits:
        constraints['fraction_digits'] = int(fraction_digits.group(1))
    
    # Parse Codes
    codes = re.search(r'Codes: (.+?)(?:;|\(|$)', constraint_str)
    if codes:
        constraints['codes'] = [c.strip() for c in codes.group(1).split(',')]
    
    return constraints

def validate_field_value(field: Dict, value: str) -> List[str]:
    """Validate a field value against its constraints."""
    errors = []
    constraints = parse_constraints(field['Constraints'])
    
    # Check max length
    if 'max_length' in constraints:
        if len(value) > constraints['max_length']:
            errors.append(
                f"{field['FieldName']}: Value exceeds max length "
                f"{constraints['max_length']} (got {len(value)})"
            )
    
    # Check pattern
    if 'pattern' in constraints:
        if not re.match(constraints['pattern'], value):
            errors.append(
                f"{field['FieldName']}: Value doesn't match pattern "
                f"{constraints['pattern']}"
            )
    
    # Check code list
    if 'codes' in constraints:
        if value not in constraints['codes']:
            errors.append(
                f"{field['FieldName']}: Invalid code '{value}'. "
                f"Must be one of: {', '.join(constraints['codes'])}"
            )
    
    return errors

# Example usage
msg_id_field = next(f for f in fields if f['FieldName'] == 'MessageIdentification')
test_value = "MSG-2025-12-16-001"

errors = validate_field_value(msg_id_field, test_value)
if errors:
    print("Validation errors:")
    for error in errors:
        print(f"  - {error}")
else:
    print("✓ Validation passed")
```

## Use Case 2: Test Data Generation

### Generate Valid Test Messages

```python
def generate_test_value(field: Dict) -> str:
    """Generate a valid test value based on field constraints."""
    constraints = parse_constraints(field['Constraints'])
    
    # Handle codes
    if 'codes' in constraints:
        return constraints['codes'][0]  # Use first valid code
    
    # Handle dates
    if 'Format: ISODate' in field['Constraints']:
        return '2025-12-16'
    if 'Format: ISODateTime' in field['Constraints']:
        return '2025-12-16T10:30:00Z'
    
    # Handle text with max length
    if 'max_length' in constraints:
        base_value = f"TEST_{field['FieldName'][:10]}"
        return base_value[:constraints['max_length']]
    
    # Handle numbers
    if 'TotalDigits' in field['Constraints']:
        return '100.00'
    
    # Default
    return f"TEST_{field['FieldName']}"

# Generate test data for mandatory fields
test_data = {}
for field in get_mandatory_fields(fields):
    test_data[field['Path']] = generate_test_value(field)

print("Generated test data:")
for path, value in list(test_data.items())[:5]:
    print(f"  {path}: {value}")
```

## Use Case 3: Excel-Based Test Case Management

### Import into Excel

1. Open the CSV in Excel or Google Sheets
2. Add columns for test cases:
   - `TestCase1_Value`
   - `TestCase1_Expected`
   - `TestCase2_Value`
   - `TestCase2_Expected`
3. Add test scenarios per field

**Example in Excel:**

| FieldName | Path | Multiplicity | TestCase1_Value | TestCase1_Result |
|-----------|------|--------------|-----------------|------------------|
| MessageIdentification | Document/.../MsgId | 1..1 | MSG-001 | PASS |
| MessageIdentification | Document/.../MsgId | 1..1 | (empty) | FAIL - Missing mandatory |
| MessageIdentification | Document/.../MsgId | 1..1 | Very long string exceeding 35 chars | FAIL - Length exceeded |

### Export Test Cases

```python
def load_test_cases_from_excel(excel_path: str) -> List[Dict]:
    """Load test cases from Excel file."""
    import pandas as pd
    
    df = pd.read_csv(excel_path)
    test_cases = []
    
    for _, row in df.iterrows():
        if pd.notna(row.get('TestCase1_Value')):
            test_cases.append({
                'field_name': row['FieldName'],
                'path': row['Path'],
                'test_value': row['TestCase1_Value'],
                'expected': row['TestCase1_Expected']
            })
    
    return test_cases
```

## Use Case 4: Database-Driven Validation

### Import into SQLite

```python
import sqlite3
import csv

def import_to_database(csv_path: str, db_path: str):
    """Import field definitions into SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS field_definitions (
            field_name TEXT,
            path TEXT PRIMARY KEY,
            multiplicity TEXT,
            constraints TEXT,
            definition TEXT,
            is_mandatory BOOLEAN
        )
    ''')
    
    # Load CSV and insert
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(line for line in f if not line.startswith('#'))
        for row in reader:
            is_mandatory = row['Multiplicity'].startswith('1..')
            cursor.execute('''
                INSERT OR REPLACE INTO field_definitions 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                row['FieldName'],
                row['Path'],
                row['Multiplicity'],
                row['Constraints'],
                row['Definition'],
                is_mandatory
            ))
    
    conn.commit()
    conn.close()

# Import the CSV
import_to_database('pain001_fields_sample.csv', 'iso20022.db')

# Query mandatory fields
conn = sqlite3.connect('iso20022.db')
cursor = conn.cursor()
cursor.execute('SELECT field_name, path FROM field_definitions WHERE is_mandatory = 1')
mandatory_fields = cursor.fetchall()
print(f"Found {len(mandatory_fields)} mandatory fields in database")
```

### Query for Validation

```python
def get_field_definition(db_path: str, path: str) -> Dict:
    """Get field definition from database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT field_name, path, multiplicity, constraints, definition
        FROM field_definitions 
        WHERE path = ?
    ''', (path,))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            'field_name': row[0],
            'path': row[1],
            'multiplicity': row[2],
            'constraints': row[3],
            'definition': row[4]
        }
    return None

# Use in validation
field_def = get_field_definition('iso20022.db', 'Document/CstmrCdtTrfInitn/GrpHdr/MsgId')
if field_def:
    print(f"Validating {field_def['field_name']}")
    print(f"Constraints: {field_def['constraints']}")
```

## Use Case 5: Continuous Integration Testing

### GitHub Actions / CI Pipeline

```yaml
# .github/workflows/validate-messages.yml
name: Validate ISO 20022 Messages

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install pandas lxml
      
      - name: Load field definitions
        run: |
          python scripts/load_field_defs.py examples/pain001_fields_sample.csv
      
      - name: Validate test messages
        run: |
          python scripts/validate_messages.py tests/messages/*.xml
      
      - name: Generate validation report
        run: |
          python scripts/generate_report.py
```

### Validation Script

```python
# scripts/validate_messages.py
import sys
import csv
from lxml import etree

def load_field_definitions(csv_path):
    """Load field definitions from CSV."""
    fields = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(line for line in f if not line.startswith('#'))
        for row in reader:
            fields[row['Path']] = row
    return fields

def validate_message_file(xml_path, field_definitions):
    """Validate an XML message against field definitions."""
    tree = etree.parse(xml_path)
    root = tree.getroot()
    errors = []
    
    # Check mandatory fields
    for path, field in field_definitions.items():
        if field['Multiplicity'].startswith('1..'):
            # Convert path to XPath and check existence
            xpath = path.replace('Document/', './/')
            elements = root.xpath(xpath)
            if not elements:
                errors.append(f"Missing mandatory field: {field['FieldName']} at {path}")
    
    return errors

if __name__ == '__main__':
    fields = load_field_definitions('examples/pain001_fields_sample.csv')
    
    for xml_file in sys.argv[1:]:
        print(f"\nValidating {xml_file}...")
        errors = validate_message_file(xml_file, fields)
        
        if errors:
            print(f"❌ Found {len(errors)} errors:")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)
        else:
            print("✓ Validation passed")
```

## Use Case 6: Documentation Generation

### Generate Field Documentation from CSV

```python
def generate_field_documentation(csv_path: str, output_path: str):
    """Generate Markdown documentation from CSV."""
    fields = load_field_definitions(csv_path)
    
    # Separate mandatory and optional
    mandatory = [f for f in fields if f['Multiplicity'].startswith('1..')]
    optional = [f for f in fields if f['Multiplicity'].startswith('0..')]
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# ISO 20022 Field Documentation\n\n")
        
        f.write("## Mandatory Fields\n\n")
        f.write("| Field Name | Path | Constraints | Definition |\n")
        f.write("|------------|------|-------------|------------|\n")
        for field in mandatory:
            f.write(f"| {field['FieldName']} | `{field['Path']}` | {field['Constraints']} | {field['Definition']} |\n")
        
        f.write("\n## Optional Fields\n\n")
        f.write("| Field Name | Path | Constraints | Definition |\n")
        f.write("|------------|------|-------------|------------|\n")
        for field in optional:
            f.write(f"| {field['FieldName']} | `{field['Path']}` | {field['Constraints']} | {field['Definition']} |\n")

generate_field_documentation('pain001_fields_sample.csv', 'docs/fields.md')
```

## Benefits of CSV Format

### ✅ Testing Benefits
- **Easy to import** into test frameworks (pytest, unittest, Jest)
- **Quick validation** of field presence and constraints
- **Test data generation** from field definitions
- **Version control friendly** - easy to diff changes

### ✅ Integration Benefits
- **Excel/Sheets compatible** - business users can add test cases
- **Database import** - SQLite, MySQL, PostgreSQL
- **API generation** - use as schema for API validation
- **CI/CD integration** - automated validation in pipelines

### ✅ Collaboration Benefits
- **Non-technical accessibility** - anyone can open and understand
- **Easy to review** - clear, tabular format
- **Comments preserved** - metadata in header comments
- **Tool agnostic** - works with any CSV-compatible tool

## Next Steps

1. **Generate CSV** from your schema using the agent
2. **Import into your testing framework** or database
3. **Create test cases** based on field constraints
4. **Automate validation** in your CI/CD pipeline
5. **Share with team** in Excel or Google Sheets

## Example Queries

### Find all mandatory IBAN fields
```python
mandatory_ibans = [
    f for f in fields 
    if f['Multiplicity'].startswith('1..') 
    and 'IBAN' in f['Path']
]
```

### Find all fields with code lists
```python
coded_fields = [
    f for f in fields 
    if 'Codes:' in f['Constraints']
]
```

### Find all date/time fields
```python
datetime_fields = [
    f for f in fields 
    if 'Format: ISO' in f['Constraints']
]
```

## Resources

- **Sample CSV**: `examples/pain001_fields_sample.csv`
- **Validation Scripts**: `scripts/` directory
- **Test Examples**: `tests/` directory
