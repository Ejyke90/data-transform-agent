"""
Convert pain.001.001.12 XSD schema to AVRO format for testing.
This creates an AVRO schema with the same 1,673 fields.
"""

import json
from iso20022_agent import ISO20022SchemaAgent

def xsd_to_avro_type(xsd_type: str, multiplicity: str) -> dict:
    """Convert XSD type and multiplicity to AVRO type."""
    # Determine if optional based on multiplicity
    is_optional = multiplicity.startswith('0')
    is_array = 'unbounded' in multiplicity or multiplicity.endswith('..n')
    
    # Map XSD types to AVRO types
    type_mapping = {
        'string': 'string',
        'boolean': 'boolean',
        'int': 'int',
        'long': 'long',
        'float': 'float',
        'double': 'double',
        'decimal': 'string',  # AVRO doesn't have decimal, use string
        'date': {'type': 'int', 'logicalType': 'date'},
        'dateTime': {'type': 'long', 'logicalType': 'timestamp-millis'},
        'ISODateTime': {'type': 'long', 'logicalType': 'timestamp-millis'},
    }
    
    # Get base type (remove any prefix)
    base_type = xsd_type.split(':')[-1] if ':' in xsd_type else xsd_type
    
    # Default to string for complex types
    avro_type = type_mapping.get(base_type, 'string')
    
    # Handle arrays
    if is_array:
        avro_type = {
            'type': 'array',
            'items': avro_type
        }
    
    # Handle optional (union with null)
    if is_optional:
        avro_type = ['null', avro_type]
    
    return avro_type


def build_nested_structure(fields, parent_path=''):
    """Build nested AVRO record structure from flat field list."""
    result = []
    processed = set()
    
    # Group fields by immediate child under parent
    for field in fields:
        if field.path.count('/') <= parent_path.count('/'):
            continue
            
        if parent_path:
            if not field.path.startswith(parent_path + '/'):
                continue
            # Get immediate child name
            relative_path = field.path[len(parent_path)+1:]
        else:
            relative_path = field.path
        
        # Get first component
        if '/' in relative_path:
            child_name = relative_path.split('/')[0]
            child_path = f"{parent_path}/{child_name}" if parent_path else child_name
        else:
            child_name = relative_path
            child_path = field.path
        
        if child_name in processed:
            continue
        processed.add(child_name)
        
        # Find all fields under this child
        child_fields = [f for f in fields if f.path.startswith(child_path)]
        
        if len(child_fields) == 1 and child_fields[0].path == child_path:
            # Leaf field
            f = child_fields[0]
            field_def = {
                'name': f.name,
                'type': xsd_to_avro_type(f.data_type, f.multiplicity)
            }
            if f.definition:
                field_def['doc'] = f.definition
            if f.code_list:
                # Convert to enum
                field_def['type'] = {
                    'type': 'enum',
                    'name': f"{f.name}Enum",
                    'symbols': f.code_list
                }
                if f.is_optional():
                    field_def['type'] = ['null', field_def['type']]
            
            result.append(field_def)
        else:
            # Complex type with children
            nested_fields = build_nested_structure(child_fields, child_path)
            
            if nested_fields:
                is_optional = child_fields[0].is_optional() if child_fields else False
                is_array = 'unbounded' in child_fields[0].multiplicity if child_fields else False
                
                record_type = {
                    'type': 'record',
                    'name': child_name,
                    'fields': nested_fields
                }
                
                if is_array:
                    record_type = {
                        'type': 'array',
                        'items': record_type
                    }
                
                if is_optional:
                    record_type = ['null', record_type]
                
                result.append({
                    'name': child_name,
                    'type': record_type
                })
    
    return result


# Load XSD schema
print("Loading pain.001.001.12 XSD schema...")
agent = ISO20022SchemaAgent()
agent.load_schema('schemas/pain.001.001.12.xsd')
fields = agent.extract_fields()

print(f"Loaded {len(fields)} fields")
print("Converting to AVRO format...")

# Build AVRO schema
avro_schema = {
    'type': 'record',
    'name': 'pain_001_001_12',
    'namespace': 'org.iso20022.pain',
    'doc': 'ISO 20022 Customer Credit Transfer Initiation (pain.001.001.12) - Converted from XSD',
    'fields': build_nested_structure(fields)
}

# Save AVRO schema
output_path = 'schemas/pain.001.001.12.avsc'
with open(output_path, 'w') as f:
    json.dump(avro_schema, f, indent=2)

print(f"✓ AVRO schema saved to: {output_path}")
print(f"✓ Contains {len(fields)} fields")
print(f"✓ Root record has {len(avro_schema['fields'])} top-level fields")
