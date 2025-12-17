"""
Message validation utilities.
"""

import xml.etree.ElementTree as ET
from typing import List, Dict, Any
import re

from .field import ISO20022Field


class MessageValidator:
    """Validator for ISO 20022 message instances."""
    
    def __init__(self, fields: List[ISO20022Field]):
        """
        Initialize validator with field definitions.
        
        Args:
            fields: List of ISO20022Field objects from schema
        """
        self.fields = fields
        self.mandatory_fields = [f for f in fields if f.is_mandatory()]
    
    def validate(self, message_xml: str) -> Dict[str, Any]:
        """
        Validate a message instance.
        
        Args:
            message_xml: XML content of the message
            
        Returns:
            Dictionary with validation results
        """
        results = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Parse XML
        try:
            root = ET.fromstring(message_xml)
        except ET.ParseError as e:
            results['valid'] = False
            results['errors'].append(f"XML parsing error: {e}")
            return results
        
        # Check mandatory fields
        for field in self.mandatory_fields:
            if not self._field_exists(root, field.path):
                results['valid'] = False
                results['errors'].append(
                    f"Missing mandatory field: {field.name} at path {field.path}"
                )
        
        # Validate field values and constraints
        for field in self.fields:
            field_values = self._get_field_values(root, field.path)
            for value in field_values:
                constraint_errors = self._validate_constraints(field, value)
                if constraint_errors:
                    results['valid'] = False
                    results['errors'].extend(constraint_errors)
        
        return results
    
    def _field_exists(self, root: ET.Element, path: str) -> bool:
        """Check if a field exists in the message."""
        # Simple path-based search
        xpath = self._path_to_xpath(path)
        try:
            elements = root.findall(xpath)
            return len(elements) > 0
        except Exception:
            return False
    
    def _get_field_values(self, root: ET.Element, path: str) -> List[str]:
        """Get all values for a field path."""
        xpath = self._path_to_xpath(path)
        values = []
        try:
            elements = root.findall(xpath)
            for element in elements:
                if element.text:
                    values.append(element.text)
        except Exception:
            pass
        return values
    
    def _path_to_xpath(self, path: str) -> str:
        """Convert field path to XPath expression."""
        # Simple conversion: Document/GrpHdr/MsgId -> .//GrpHdr/MsgId
        parts = path.split('/')
        if parts and parts[0] == 'Document':
            parts = parts[1:]  # Remove Document root
        return './/' + '/'.join(parts) if parts else path
    
    def _validate_constraints(self, field: ISO20022Field, value: str) -> List[str]:
        """Validate field value against constraints."""
        errors = []
        
        # Check max length
        if 'maxLength' in field.constraints:
            max_len = field.constraints['maxLength']
            if len(value) > max_len:
                errors.append(
                    f"{field.name}: Value exceeds maximum length {max_len} "
                    f"(got {len(value)} characters)"
                )
        
        # Check min length
        if 'minLength' in field.constraints:
            min_len = field.constraints['minLength']
            if len(value) < min_len:
                errors.append(
                    f"{field.name}: Value below minimum length {min_len} "
                    f"(got {len(value)} characters)"
                )
        
        # Check pattern
        if 'pattern' in field.constraints:
            pattern = field.constraints['pattern']
            try:
                if not re.match(pattern, value):
                    errors.append(
                        f"{field.name}: Value '{value}' does not match required pattern"
                    )
            except re.error:
                pass  # Invalid regex in schema
        
        # Check code list
        if field.code_list and value not in field.code_list:
            errors.append(
                f"{field.name}: Invalid value '{value}'. "
                f"Must be one of: {', '.join(field.code_list)}"
            )
        
        return errors
