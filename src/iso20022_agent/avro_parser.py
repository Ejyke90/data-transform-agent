"""
AVRO Schema Parser for ISO 20022-like message definitions.
Converts AVRO schemas (.avsc) to field catalogs similar to XSD parsing.
"""

import json
from typing import Dict, List, Optional, Any
from pathlib import Path

from .field import ISO20022Field, FieldRequirement


class AVROParser:
    """Parser for AVRO schema files (.avsc)."""
    
    def __init__(self):
        self.schema: Optional[Dict] = None
        self.message_type: Optional[str] = None
        self.namespace: Optional[str] = None
        self.fields: List[ISO20022Field] = []
        
    def parse_file(self, schema_path: str) -> None:
        """Parse an AVRO schema file."""
        path = Path(schema_path)
        if not path.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_path}")
        
        with open(schema_path, 'r') as f:
            self.schema = json.load(f)
        
        # Extract namespace and message type
        self.namespace = self.schema.get('namespace', '')
        self.message_type = self.schema.get('name', 'unknown')
        
    def get_message_type(self) -> str:
        """Get the message type identifier."""
        return self.message_type or 'unknown'
    
    def extract_fields(self) -> List[ISO20022Field]:
        """Extract all fields from the AVRO schema."""
        if not self.schema:
            return []
        
        self.fields = []
        
        # Start parsing from root record
        if self.schema.get('type') == 'record':
            self._parse_record(
                self.schema,
                self.schema.get('name', 'Root'),
                ''
            )
        
        return self.fields
    
    def _parse_record(
        self, 
        record: Dict[str, Any], 
        record_name: str,
        parent_path: str
    ) -> None:
        """Recursively parse AVRO record type."""
        fields = record.get('fields', [])
        
        for field_def in fields:
            self._parse_field(field_def, parent_path)
    
    def _parse_field(
        self,
        field_def: Dict[str, Any],
        parent_path: str
    ) -> None:
        """Parse a single AVRO field."""
        field_name = field_def.get('name', 'unknown')
        field_type = field_def.get('type')
        default = field_def.get('default')
        doc = field_def.get('doc', '')
        
        # Build path with dot notation
        if parent_path:
            full_path = f"{parent_path}.{field_name}"
        else:
            full_path = field_name
        
        # Parse type to determine if optional/mandatory and data type
        is_optional, data_type, is_array = self._parse_type(field_type)
        
        # Determine requirement based on optional flag and default
        if is_optional or default is not None:
            requirement = FieldRequirement.OPTIONAL
            min_occurs = '0'
        else:
            requirement = FieldRequirement.MANDATORY
            min_occurs = '1'
        
        # Determine max occurs
        if is_array:
            max_occurs = 'unbounded'
        else:
            max_occurs = '1'
        
        multiplicity = f"{min_occurs}..{max_occurs}"
        
        # Extract constraints
        constraints = self._extract_constraints(field_def, data_type)
        
        # Extract code list (enum values)
        code_list = self._extract_enum_values(field_type)
        
        # Create field object
        field = ISO20022Field(
            name=field_name,
            path=full_path,
            data_type=data_type,
            multiplicity=multiplicity,
            requirement=requirement,
            definition=doc,
            constraints=constraints,
            code_list=code_list
        )
        
        self.fields.append(field)
        
        # Recursively parse nested records
        if isinstance(field_type, dict) and field_type.get('type') == 'record':
            self._parse_record(field_type, field_name, full_path)
        elif isinstance(field_type, list):
            # Union type - check for nested records
            for union_type in field_type:
                if isinstance(union_type, dict) and union_type.get('type') == 'record':
                    self._parse_record(union_type, field_name, full_path)
        elif isinstance(field_type, dict) and field_type.get('type') == 'array':
            # Array type - check items for records
            items = field_type.get('items')
            if isinstance(items, dict) and items.get('type') == 'record':
                self._parse_record(items, field_name, full_path)
    
    def _parse_type(self, field_type: Any) -> tuple:
        """
        Parse AVRO type to determine if optional, data type, and if array.
        
        Returns:
            (is_optional, data_type, is_array)
        """
        is_optional = False
        data_type = 'string'
        is_array = False
        
        # Handle union types (e.g., ["null", "string"] means optional string)
        if isinstance(field_type, list):
            # Union type
            non_null_types = [t for t in field_type if t != 'null']
            is_optional = 'null' in field_type
            
            if non_null_types:
                # Get first non-null type
                primary_type = non_null_types[0]
                if isinstance(primary_type, str):
                    data_type = primary_type
                elif isinstance(primary_type, dict):
                    data_type = primary_type.get('type', 'record')
                    if data_type == 'array':
                        is_array = True
                        items = primary_type.get('items')
                        if isinstance(items, str):
                            data_type = f"array<{items}>"
                        elif isinstance(items, dict):
                            data_type = f"array<{items.get('type', 'record')}>"
        
        # Handle dict types (complex types)
        elif isinstance(field_type, dict):
            type_name = field_type.get('type')
            
            if type_name == 'array':
                is_array = True
                items = field_type.get('items')
                if isinstance(items, str):
                    data_type = f"array<{items}>"
                elif isinstance(items, dict):
                    data_type = f"array<{items.get('type', 'record')}>"
                else:
                    data_type = 'array'
            
            elif type_name == 'enum':
                data_type = field_type.get('name', 'enum')
            
            elif type_name == 'record':
                data_type = field_type.get('name', 'record')
            
            else:
                data_type = type_name or 'unknown'
        
        # Handle primitive types
        elif isinstance(field_type, str):
            data_type = field_type
        
        return is_optional, data_type, is_array
    
    def _extract_constraints(
        self, 
        field_def: Dict[str, Any],
        data_type: str
    ) -> Dict[str, Any]:
        """Extract constraints from AVRO field definition."""
        constraints = {}
        
        # Check for logical type annotations
        if isinstance(field_def.get('type'), dict):
            logical_type = field_def['type'].get('logicalType')
            if logical_type:
                constraints['logicalType'] = logical_type
        
        # Check for custom properties (common AVRO pattern)
        for key in ['maxLength', 'minLength', 'pattern', 'minimum', 'maximum']:
            if key in field_def:
                constraints[key] = field_def[key]
        
        # Add data type to constraints
        if data_type:
            constraints['type'] = data_type
        
        return constraints
    
    def _extract_enum_values(self, field_type: Any) -> Optional[List[str]]:
        """Extract enum values if field is an enum type."""
        # Direct enum
        if isinstance(field_type, dict) and field_type.get('type') == 'enum':
            return field_type.get('symbols', [])
        
        # Union type containing enum
        if isinstance(field_type, list):
            for union_type in field_type:
                if isinstance(union_type, dict) and union_type.get('type') == 'enum':
                    return union_type.get('symbols', [])
        
        return None
