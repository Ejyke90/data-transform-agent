# ISO 20022 Payment Schema Transformation Skills

## Core Transformation Patterns

### 1. Schema Ingestion & Parsing
- Parse ISO 20022 XSD schemas
- Extract ComplexType and SimpleType definitions
- Build hierarchical element structures
- Extract annotations and documentation
- Handle namespace declarations
- Process schema imports and includes

### 2. Field Extraction & Classification
- Identify mandatory fields (minOccurs >= 1)
- Identify optional fields (minOccurs == 0)
- Detect conditional requirements
- Extract multiplicity constraints (1..1, 0..1, 1..n, 0..n)
- Map field paths (XPath expressions)
- Extract data type information

### 3. ISO 20022 Metadata Extraction
- Extract message identification (e.g., pain.001.001.09)
- Identify business area and domain
- Extract message version information
- Parse field definitions and business meanings
- Extract code lists and enumerations
- Identify pattern constraints (regex)
- Extract length constraints

### 4. Data Validation & Compliance
- Validate against ISO 20022 XSD schemas
- Check mandatory field presence
- Validate data types and formats
- Verify code list values
- Validate business rules
- Check cross-field constraints
- Verify IBAN, BIC format compliance

### 5. Data Enrichment for Payments
- Add calculated fields (checksums, validation codes)
- Lookup BIC codes from IBAN
- Resolve currency codes to names
- Apply payment routing logic
- Generate transaction references
- Add timestamp metadata
- Enrich with country/bank information

## ISO 20022 Payment Schema Agent

```python
from typing import Any, Dict, List, Optional
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from enum import Enum

class FieldRequirement(Enum):
    """Field requirement classification."""
    MANDATORY = "mandatory"
    OPTIONAL = "optional"
    CONDITIONAL = "conditional"

@dataclass
class ISO20022Field:
    """Represents a field in an ISO 20022 message."""
    path: str
    name: str
    data_type: str
    multiplicity: str
    requirement: FieldRequirement
    definition: str
    constraints: Dict[str, Any]
    code_list: Optional[List[str]] = None
    parent_path: Optional[str] = None
    
class ISO20022SchemaAgent:
    """Agent for processing ISO 20022 payment schemas."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.namespaces = {}
        self.fields = []
        self.message_type = None
        
    def load_schema(self, schema_path: str) -> None:
        """Load and parse ISO 20022 XSD schema."""
        tree = ET.parse(schema_path)
        self.root = tree.getroot()
        self._extract_namespaces()
        self._identify_message_type()
        
    def _extract_namespaces(self) -> None:
        """Extract namespace declarations from schema."""
        self.namespaces = dict([
            node for _, node in ET.iterparse(
                self.schema_path, events=['start-ns']
            )
        ])
        
    def _identify_message_type(self) -> None:
        """Identify the message type from namespace or schema."""
        # Extract from namespace URI
        # e.g., urn:iso:std:iso:20022:tech:xsd:pain.001.001.09
        ns_uri = self.namespaces.get('', '')
        if ':xsd:' in ns_uri:
            self.message_type = ns_uri.split(':xsd:')[1]
            
    def extract_fields(self) -> List[ISO20022Field]:
        """Extract all fields from the schema."""
        self.fields = []
        self._parse_elements(self.root, path="Document")
        return self.fields
        
    def _parse_elements(self, element: ET.Element, path: str = "") -> None:
        """Recursively parse XML schema elements."""
        for child in element:
            if self._is_element(child):
                field = self._extract_field_metadata(child, path)
                if field:
                    self.fields.append(field)
                    # Recurse into complex types
                    new_path = f"{path}/{field.name}"
                    self._parse_elements(child, new_path)
                    
    def _extract_field_metadata(
        self, element: ET.Element, parent_path: str
    ) -> Optional[ISO20022Field]:
        """Extract metadata for a single field."""
        name = element.get('name')
        if not name:
            return None
            
        # Extract multiplicity
        min_occurs = int(element.get('minOccurs', '1'))
        max_occurs = element.get('maxOccurs', '1')
        multiplicity = f"{min_occurs}..{max_occurs}"
        
        # Determine requirement level
        if min_occurs >= 1:
            requirement = FieldRequirement.MANDATORY
        else:
            requirement = FieldRequirement.OPTIONAL
            
        # Extract type
        data_type = element.get('type', 'Unknown')
        
        # Extract definition from annotation
        definition = self._extract_definition(element)
        
        # Extract constraints
        constraints = self._extract_constraints(element)
        
        # Extract code list if applicable
        code_list = self._extract_code_list(element)
        
        return ISO20022Field(
            path=f"{parent_path}/{name}",
            name=name,
            data_type=data_type,
            multiplicity=multiplicity,
            requirement=requirement,
            definition=definition,
            constraints=constraints,
            code_list=code_list,
            parent_path=parent_path
        )
        
    def _extract_definition(self, element: ET.Element) -> str:
        """Extract field definition from annotation."""
        annotation = element.find('.//xs:annotation/xs:documentation', 
                                  self.namespaces)
        return annotation.text if annotation is not None else ""
        
    def _extract_constraints(self, element: ET.Element) -> Dict[str, Any]:
        """Extract validation constraints."""
        constraints = {}
        
        # Length constraints
        restriction = element.find('.//xs:restriction', self.namespaces)
        if restriction is not None:
            max_length = restriction.find('xs:maxLength', self.namespaces)
            if max_length is not None:
                constraints['maxLength'] = int(max_length.get('value'))
                
            min_length = restriction.find('xs:minLength', self.namespaces)
            if min_length is not None:
                constraints['minLength'] = int(min_length.get('value'))
                
            # Pattern constraints
            pattern = restriction.find('xs:pattern', self.namespaces)
            if pattern is not None:
                constraints['pattern'] = pattern.get('value')
                
        return constraints
        
    def _extract_code_list(self, element: ET.Element) -> Optional[List[str]]:
        """Extract enumeration values if present."""
        enumerations = element.findall('.//xs:enumeration', self.namespaces)
        if enumerations:
            return [enum.get('value') for enum in enumerations]
        return None
        
    def get_mandatory_fields(self) -> List[ISO20022Field]:
        """Return all mandatory fields."""
        return [
            field for field in self.fields 
            if field.requirement == FieldRequirement.MANDATORY
        ]
        
    def get_optional_fields(self) -> List[ISO20022Field]:
        """Return all optional fields."""
        return [
            field for field in self.fields 
            if field.requirement == FieldRequirement.OPTIONAL
        ]
        
    def get_conditional_fields(self) -> List[ISO20022Field]:
        """Return all conditional fields."""
        return [
            field for field in self.fields 
            if field.requirement == FieldRequirement.CONDITIONAL
        ]
        
    def validate_message(self, message_xml: str) -> Dict[str, Any]:
        """Validate an ISO 20022 message instance."""
        validation_results = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Parse message
        try:
            message = ET.fromstring(message_xml)
        except ET.ParseError as e:
            validation_results['valid'] = False
            validation_results['errors'].append(f"XML parsing error: {e}")
            return validation_results
            
        # Check mandatory fields
        mandatory_fields = self.get_mandatory_fields()
        for field in mandatory_fields:
            if not self._field_exists(message, field.path):
                validation_results['valid'] = False
                validation_results['errors'].append(
                    f"Missing mandatory field: {field.path}"
                )
                
        # Validate field constraints
        for field in self.fields:
            field_value = self._get_field_value(message, field.path)
            if field_value:
                constraint_errors = self._validate_constraints(
                    field, field_value
                )
                validation_results['errors'].extend(constraint_errors)
                
        return validation_results
        
    def _field_exists(self, message: ET.Element, path: str) -> bool:
        """Check if a field exists in the message."""
        # Convert path to XPath and search
        xpath = path.replace('/', '/')
        return message.find(xpath, self.namespaces) is not None
        
    def _get_field_value(self, message: ET.Element, path: str) -> Optional[str]:
        """Get field value from message."""
        element = message.find(path, self.namespaces)
        return element.text if element is not None else None
        
    def _validate_constraints(
        self, field: ISO20022Field, value: str
    ) -> List[str]:
        """Validate field value against constraints."""
        errors = []
        
        # Check length constraints
        if 'maxLength' in field.constraints:
            if len(value) > field.constraints['maxLength']:
                errors.append(
                    f"{field.path}: Value exceeds maximum length "
                    f"{field.constraints['maxLength']}"
                )
                
        if 'minLength' in field.constraints:
            if len(value) < field.constraints['minLength']:
                errors.append(
                    f"{field.path}: Value below minimum length "
                    f"{field.constraints['minLength']}"
                )
                
        # Check pattern constraints
        if 'pattern' in field.constraints:
            import re
            pattern = field.constraints['pattern']
            if not re.match(pattern, value):
                errors.append(
                    f"{field.path}: Value does not match required pattern"
                )
                
        # Check code list constraints
        if field.code_list and value not in field.code_list:
            errors.append(
                f"{field.path}: Invalid value '{value}'. "
                f"Must be one of: {', '.join(field.code_list)}"
            )
            
        return errors
        
    def export_field_catalog(
        self, output_path: str, format: str = 'csv'
    ) -> None:
        """Export field catalog to file. Default format is CSV."""
        import json
        from datetime import datetime
        
        catalog = {
            'messageType': self.message_type,
            'extractionDate': datetime.utcnow().isoformat() + 'Z',
            'totalFields': len(self.fields),
            'mandatoryCount': len(self.get_mandatory_fields()),
            'optionalCount': len(self.get_optional_fields()),
            'fields': self.fields
        }
        
        if format == 'csv':
            self._export_csv(catalog, output_path)
        elif format == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self._catalog_to_dict(catalog), f, indent=2)
        elif format == 'markdown':
            self._export_markdown(catalog, output_path)
    
    def _catalog_to_dict(self, catalog: Dict) -> Dict:
        """Convert catalog to JSON-serializable dict."""
        return {
            'messageType': catalog['messageType'],
            'extractionDate': catalog['extractionDate'],
            'totalFields': catalog['totalFields'],
            'mandatoryCount': catalog['mandatoryCount'],
            'optionalCount': catalog['optionalCount'],
            'fields': [
                {
                    'fieldName': field.name,
                    'path': field.path,
                    'multiplicity': field.multiplicity,
                    'constraints': self._format_constraints(field),
                    'definition': field.definition
                }
                for field in catalog['fields']
            ]
        }
            
    def _get_current_timestamp(self) -> str:
        """Get current ISO 8601 timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat() + 'Z'
        
    def _export_markdown(self, catalog: Dict, output_path: str) -> None:
        """Export catalog as Markdown."""
        with open(output_path, 'w') as f:
            f.write(f"# {catalog['messageType']} Field Catalog\n\n")
            f.write(f"**Total Fields:** {catalog['totalFields']}\n")
            f.write(f"**Mandatory:** {catalog['mandatoryCount']}\n")
            f.write(f"**Optional:** {catalog['optionalCount']}\n\n")
            
            f.write("## Mandatory Fields\n\n")
            f.write("| Path | Name | Type | Definition |\n")
            f.write("|------|------|------|------------|\n")
            for field in catalog['fields']:
                if field['requirement'] == 'mandatory':
                    f.write(
                        f"| {field['path']} | {field['name']} | "
                        f"{field['type']} | {field['definition']} |\n"
                    )
                    
            f.write("\n## Optional Fields\n\n")
            f.write("| Path | Name | Type | Definition |\n")
            f.write("|------|------|------|------------|\n")
            for field in catalog['fields']:
                if field['requirement'] == 'optional':
                    f.write(
                        f"| {field['path']} | {field['name']} | "
                        f"{field['type']} | {field['definition']} |\n"
                    )
                    
    def _export_csv(self, catalog: Dict, output_path: str) -> None:
        """Export catalog as CSV with simplified structure."""
        import csv
        from datetime import datetime
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            # Write header comments
            f.write(f"# Message Type: {catalog['messageType']}\n")
            f.write(f"# Total Fields: {catalog['totalFields']}\n")
            f.write(f"# Mandatory Fields: {catalog['mandatoryCount']}\n")
            f.write(f"# Optional Fields: {catalog['optionalCount']}\n")
            f.write(f"# Extraction Date: {catalog['extractionDate']}\n")
            f.write("#\n")
            
            # Write CSV data
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['FieldName', 'Path', 'Multiplicity', 'Constraints', 'Definition'])
            
            for field in catalog['fields']:
                writer.writerow([
                    field.name,
                    field.path,
                    field.multiplicity,
                    self._format_constraints(field),
                    field.definition
                ])
    
    def _format_constraints(self, field: ISO20022Field) -> str:
        """Format constraints as a single string."""
        constraint_parts = []
        
        # Add data type for complex types
        if not field.data_type.startswith('Max') and not field.data_type in ['ISODate', 'ISODateTime', 'DecimalNumber']:
            constraint_parts.append(f"Type: {field.data_type}")
        
        # Add length constraints
        if 'maxLength' in field.constraints:
            constraint_parts.append(f"MaxLength: {field.constraints['maxLength']}")
        if 'minLength' in field.constraints:
            constraint_parts.append(f"MinLength: {field.constraints['minLength']}")
        
        # Add pattern
        if 'pattern' in field.constraints:
            constraint_parts.append(f"Pattern: {field.constraints['pattern']}")
        
        # Add decimal constraints
        if 'totalDigits' in field.constraints:
            constraint_parts.append(f"TotalDigits: {field.constraints['totalDigits']}")
        if 'fractionDigits' in field.constraints:
            constraint_parts.append(f"FractionDigits: {field.constraints['fractionDigits']}")
        
        # Add code list
        if field.code_list:
            codes = ', '.join(field.code_list[:5])  # Limit to first 5
            if len(field.code_list) > 5:
                codes += f" (+ {len(field.code_list) - 5} more)"
            constraint_parts.append(f"Codes: {codes}")
        
        # Add format hints for date/time
        if field.data_type == 'ISODate':
            constraint_parts.append("Format: ISODate (YYYY-MM-DD)")
        elif field.data_type == 'ISODateTime':
            constraint_parts.append("Format: ISODateTime")
        
        return '; '.join(constraint_parts) if constraint_parts else 'None'
```

## Common Use Cases

### 1. Payment Schema Analysis
**Objective**: Extract and document all fields from an ISO 20022 payment schema

```python
# Initialize agent
agent = ISO20022SchemaAgent(config={
    'strict_validation': True,
    'extract_annotations': True
})

# Load schema
agent.load_schema('schemas/pain.001.001.09.xsd')

# Extract all fields
fields = agent.extract_fields()

# Get mandatory fields only
mandatory = agent.get_mandatory_fields()
print(f"Found {len(mandatory)} mandatory fields")

# Export documentation
agent.export_field_catalog(
    'docs/pain001_fields.md',
    format='markdown'
)
```

### 2. Payment Message Validation
**Objective**: Validate a payment message against its schema

```python
# Load the schema
agent.load_schema('schemas/pacs.008.001.08.xsd')
agent.extract_fields()

# Load payment message
with open('messages/payment.xml', 'r') as f:
    message_xml = f.read()

# Validate
results = agent.validate_message(message_xml)

if not results['valid']:
    print("Validation errors:")
    for error in results['errors']:
        print(f"  - {error}")
```

### 3. Field Requirement Analysis
**Objective**: Identify which fields are required for a specific payment scenario

```python
# Extract fields
agent.load_schema('schemas/pain.001.001.09.xsd')
fields = agent.extract_fields()

# Filter for SEPA credit transfer requirements
sepa_mandatory = [
    f for f in fields 
    if f.requirement == FieldRequirement.MANDATORY
    or 'IBAN' in f.path
    or 'BIC' in f.path
]

# Generate requirements doc
print("SEPA Credit Transfer Required Fields:")
for field in sepa_mandatory:
    print(f"  {field.path}: {field.definition}")
```

### 4. Schema Version Comparison
**Objective**: Compare two versions of a schema to identify changes

```python
# Load both versions
agent_v09 = ISO20022SchemaAgent(config={})
agent_v09.load_schema('schemas/pain.001.001.09.xsd')
fields_v09 = agent_v09.extract_fields()

agent_v11 = ISO20022SchemaAgent(config={})
agent_v11.load_schema('schemas/pain.001.001.11.xsd')
fields_v11 = agent_v11.extract_fields()

# Compare
paths_v09 = {f.path for f in fields_v09}
paths_v11 = {f.path for f in fields_v11}

added = paths_v11 - paths_v09
removed = paths_v09 - paths_v11

print(f"Added fields: {len(added)}")
print(f"Removed fields: {len(removed)}")
```

### 5. Message Generation Template
**Objective**: Generate a template message with all mandatory fields

```python
agent.load_schema('schemas/camt.053.001.08.xsd')
mandatory_fields = agent.get_mandatory_fields()

# Generate XML template
template = generate_xml_template(mandatory_fields)
with open('templates/camt053_template.xml', 'w') as f:
    f.write(template)
```

## ISO 20022 Specific Skills

### Payment Message Type Detection
```python
def detect_message_type(xml_content: str) -> str:
    """Detect ISO 20022 message type from XML."""
    root = ET.fromstring(xml_content)
    namespace = root.tag.split('}')[0].strip('{')
    
    # Extract message type from namespace
    # e.g., urn:iso:std:iso:20022:tech:xsd:pain.001.001.09
    if ':xsd:' in namespace:
        return namespace.split(':xsd:')[1]
    
    return "Unknown"
```

### BIC/IBAN Validation
```python
def validate_iban(iban: str) -> bool:
    """Validate IBAN checksum."""
    # Remove spaces and convert to uppercase
    iban = iban.replace(' ', '').upper()
    
    # Move first 4 chars to end
    rearranged = iban[4:] + iban[:4]
    
    # Replace letters with numbers (A=10, B=11, ...)
    numeric = ''.join(
        str(int(c, 36)) for c in rearranged
    )
    
    # Check modulo 97
    return int(numeric) % 97 == 1

def validate_bic(bic: str) -> bool:
    """Validate BIC format."""
    import re
    # BIC format: 4 letters (bank) + 2 letters (country) + 
    # 2 alphanumeric (location) + optional 3 alphanumeric (branch)
    pattern = r'^[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?$'
    return bool(re.match(pattern, bic.upper()))
```

### Field Path Navigation
```python
def get_nested_field(message: ET.Element, path: str, 
                     namespaces: Dict) -> Optional[str]:
    """Navigate to nested field using path notation."""
    parts = path.split('/')
    current = message
    
    for part in parts:
        if not part:
            continue
        current = current.find(f".//{part}", namespaces)
        if current is None:
            return None
            
    return current.text if current is not None else None
```

### Business Rule Validation
```python
def validate_payment_amount(
    amount: str, 
    currency: str,
    max_amount: Dict[str, float]
) -> List[str]:
    """Validate payment amount against business rules."""
    errors = []
    
    try:
        amount_value = float(amount)
    except ValueError:
        return [f"Invalid amount format: {amount}"]
    
    # Check positive
    if amount_value <= 0:
        errors.append("Amount must be positive")
    
    # Check currency limit
    if currency in max_amount:
        if amount_value > max_amount[currency]:
            errors.append(
                f"Amount exceeds limit for {currency}: "
                f"{max_amount[currency]}"
            )
    
    return errors
```

## Advanced Transformation Patterns

### 1. Message Format Conversion
Convert between XML and JSON representations:

```python
def xml_to_json(xml_message: str) -> Dict:
    """Convert ISO 20022 XML to JSON."""
    import xmltodict
    return xmltodict.parse(xml_message)

def json_to_xml(json_data: Dict, message_type: str) -> str:
    """Convert JSON back to ISO 20022 XML."""
    import xmltodict
    return xmltodict.unparse(json_data, pretty=True)
```

### 2. Message Enrichment
Add derived and lookup data:

```python
def enrich_payment_message(message: Dict) -> Dict:
    """Enrich payment with additional data."""
    # Add BIC from IBAN lookup
    debtor_iban = message['payment']['debtor_account']
    message['payment']['debtor_bic'] = lookup_bic(debtor_iban)
    
    # Add bank name
    message['payment']['debtor_bank_name'] = lookup_bank_name(
        message['payment']['debtor_bic']
    )
    
    # Add currency name
    currency_code = message['payment']['amount_currency']
    message['payment']['currency_name'] = get_currency_name(
        currency_code
    )
    
    return message
```

### 3. Multi-Schema Validation
Validate across multiple related schemas:

```python
def validate_payment_workflow(messages: List[str]) -> Dict:
    """Validate a sequence of related payment messages."""
    results = {'valid': True, 'errors': []}
    
    # pain.001 -> pacs.008 -> camt.054
    expected_sequence = [
        'pain.001',  # Initiation
        'pacs.008',  # FI transfer
        'camt.054'   # Notification
    ]
    
    for i, (msg, expected) in enumerate(zip(messages, expected_sequence)):
        msg_type = detect_message_type(msg)
        if not msg_type.startswith(expected):
            results['valid'] = False
            results['errors'].append(
                f"Step {i+1}: Expected {expected}, got {msg_type}"
            )
    
    return results
```

## Performance Optimization

### Caching Schema Metadata
```python
import functools
import hashlib

@functools.lru_cache(maxsize=128)
def get_schema_metadata(schema_path: str) -> Dict:
    """Cache schema metadata extraction."""
    agent = ISO20022SchemaAgent({})
    agent.load_schema(schema_path)
    return {
        'message_type': agent.message_type,
        'field_count': len(agent.extract_fields()),
        'mandatory_count': len(agent.get_mandatory_fields())
    }
```

### Batch Message Processing
```python
def process_message_batch(
    messages: List[str], 
    schema_path: str
) -> List[Dict]:
    """Process multiple messages efficiently."""
    # Load schema once
    agent = ISO20022SchemaAgent({})
    agent.load_schema(schema_path)
    agent.extract_fields()
    
    # Validate all messages
    results = []
    for msg in messages:
        result = agent.validate_message(msg)
        results.append(result)
    
    return results
```

## Testing & Quality Assurance

### Unit Testing Schema Extraction
```python
def test_mandatory_field_extraction():
    """Test mandatory field identification."""
    agent = ISO20022SchemaAgent({})
    agent.load_schema('test_schemas/pain.001.001.09.xsd')
    
    mandatory = agent.get_mandatory_fields()
    
    # Verify known mandatory fields
    mandatory_paths = {f.path for f in mandatory}
    assert 'Document/CstmrCdtTrfInitn/GrpHdr/MsgId' in mandatory_paths
    assert 'Document/CstmrCdtTrfInitn/GrpHdr/CreDtTm' in mandatory_paths
```

### Integration Testing
```python
def test_end_to_end_validation():
    """Test complete validation workflow."""
    agent = ISO20022SchemaAgent({})
    agent.load_schema('schemas/pain.001.001.09.xsd')
    agent.extract_fields()
    
    # Load valid test message
    with open('test_data/valid_pain001.xml') as f:
        valid_msg = f.read()
    
    result = agent.validate_message(valid_msg)
    assert result['valid'] == True
    assert len(result['errors']) == 0
```
