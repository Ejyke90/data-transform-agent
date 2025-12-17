"""
XSD Schema Parser for ISO 20022 message definitions.
"""

import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import re

from .field import ISO20022Field, FieldRequirement


class XSDParser:
    """Parser for ISO 20022 XSD schema files."""
    
    # Common XSD namespaces
    XSD_NS = "http://www.w3.org/2001/XMLSchema"
    
    def __init__(self):
        self.namespaces: Dict[str, str] = {}
        self.root: Optional[ET.Element] = None
        self.tree: Optional[ET.ElementTree] = None
        self.schema_path: Optional[str] = None
        self.message_type: Optional[str] = None
        self.complex_types: Dict[str, ET.Element] = {}
        self.simple_types: Dict[str, ET.Element] = {}
        
    def parse_file(self, schema_path: str) -> None:
        """Parse an XSD schema file."""
        path = Path(schema_path)
        if not path.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_path}")
        
        self.schema_path = str(path)
        self.tree = ET.parse(self.schema_path)
        self.root = self.tree.getroot()
        
        # Extract namespaces
        self._extract_namespaces()
        
        # Identify message type
        self._identify_message_type()
        
        # Build type registry
        self._build_type_registry()
    
    def _extract_namespaces(self) -> None:
        """Extract namespace declarations from schema."""
        if self.root is None or self.schema_path is None:
            return
        
        # Get namespace from root
        for prefix, uri in ET.iterparse(self.schema_path, events=['start-ns']):
            self.namespaces[prefix] = uri
        
        # Re-parse after iterparse (which consumed the file)
        self.tree = ET.parse(self.schema_path)
        self.root = self.tree.getroot()
        
        # Ensure xsd namespace is present
        if 'xs' not in self.namespaces:
            self.namespaces['xs'] = self.XSD_NS
        if '' not in self.namespaces and self.root.tag.startswith('{'):
            # Extract default namespace
            default_ns = self.root.tag[1:self.root.tag.index('}')]
            self.namespaces[''] = default_ns
    
    def _identify_message_type(self) -> None:
        """Identify the message type from schema."""
        if self.root is None:
            return
        
        # Try to extract from targetNamespace
        target_ns = self.root.get('targetNamespace', '')
        
        # Pattern: urn:iso:std:iso:20022:tech:xsd:pain.001.001.09
        pattern = r':xsd:([a-z]{4}\.\d{3}\.\d{3}\.\d{2})'
        match = re.search(pattern, target_ns)
        if match:
            self.message_type = match.group(1)
        else:
            # Try to extract from schema location or other attributes
            self.message_type = "unknown"
    
    def _build_type_registry(self) -> None:
        """Build registry of complex and simple types."""
        if self.root is None:
            return
        
        # Find all complexType definitions
        for complex_type in self.root.findall('.//{%s}complexType' % self.XSD_NS):
            name = complex_type.get('name')
            if name:
                self.complex_types[name] = complex_type
        
        # Find all simpleType definitions
        for simple_type in self.root.findall('.//{%s}simpleType' % self.XSD_NS):
            name = simple_type.get('name')
            if name:
                self.simple_types[name] = simple_type
    
    def extract_fields(self) -> List[ISO20022Field]:
        """Extract all fields from the schema."""
        fields: List[ISO20022Field] = []
        
        if self.root is None:
            return fields
        
        # Find the root Document element
        document_element = self._find_document_element()
        if document_element is not None:
            self._parse_element_recursive(document_element, "Document", fields)
        
        return fields
    
    def _find_document_element(self) -> Optional[ET.Element]:
        """Find the Document root element in the schema."""
        if self.root is None:
            return None
        
        # Look for element named "Document"
        for element in self.root.findall('.//{%s}element' % self.XSD_NS):
            if element.get('name') == 'Document':
                return element
        
        return None
    
    def _parse_element_recursive(
        self, 
        element: ET.Element, 
        current_path: str, 
        fields: List[ISO20022Field],
        parent_path: str = ""
    ) -> None:
        """Recursively parse XML schema elements."""
        
        # Get element properties
        name = element.get('name')
        if not name:
            return
        
        element_type = element.get('type', '')
        min_occurs = element.get('minOccurs', '1')
        max_occurs = element.get('maxOccurs', '1')
        
        # Build path
        full_path = f"{current_path}/{name}" if current_path else name
        
        # Determine multiplicity
        multiplicity = f"{min_occurs}..{max_occurs}"
        
        # Determine requirement
        requirement = self._determine_requirement(min_occurs)
        
        # Extract definition
        definition = self._extract_definition(element)
        
        # Extract constraints
        constraints = self._extract_constraints(element, element_type)
        
        # Extract code list if applicable
        code_list = self._extract_code_list(element, element_type)
        
        # Create field object
        field = ISO20022Field(
            name=name,
            path=full_path,
            data_type=element_type,
            multiplicity=multiplicity,
            requirement=requirement,
            definition=definition,
            constraints=constraints,
            code_list=code_list,
            parent_path=parent_path
        )
        
        fields.append(field)
        
        # Parse child elements if complex type
        if element_type:
            self._parse_complex_type(element_type, full_path, fields, full_path)
        
        # Parse inline complex type
        inline_complex = element.find('{%s}complexType' % self.XSD_NS)
        if inline_complex is not None:
            self._parse_complex_type_element(inline_complex, full_path, fields, full_path)
    
    def _parse_complex_type(
        self, 
        type_name: str, 
        current_path: str, 
        fields: List[ISO20022Field],
        parent_path: str
    ) -> None:
        """Parse a complex type definition."""
        
        # Remove namespace prefix if present
        type_name = type_name.split(':')[-1]
        
        if type_name not in self.complex_types:
            return
        
        complex_type = self.complex_types[type_name]
        self._parse_complex_type_element(complex_type, current_path, fields, parent_path)
    
    def _parse_complex_type_element(
        self, 
        complex_type: ET.Element, 
        current_path: str, 
        fields: List[ISO20022Field],
        parent_path: str
    ) -> None:
        """Parse elements within a complex type."""
        
        # Find sequence or choice
        sequence = complex_type.find('{%s}sequence' % self.XSD_NS)
        if sequence is not None:
            for child in sequence.findall('{%s}element' % self.XSD_NS):
                self._parse_element_recursive(child, current_path, fields, parent_path)
        
        choice = complex_type.find('{%s}choice' % self.XSD_NS)
        if choice is not None:
            for child in choice.findall('{%s}element' % self.XSD_NS):
                self._parse_element_recursive(child, current_path, fields, parent_path)
    
    def _determine_requirement(self, min_occurs: str) -> FieldRequirement:
        """Determine field requirement based on minOccurs."""
        try:
            min_val = int(min_occurs)
            if min_val >= 1:
                return FieldRequirement.MANDATORY
            else:
                return FieldRequirement.OPTIONAL
        except (ValueError, TypeError):
            return FieldRequirement.OPTIONAL
    
    def _extract_definition(self, element: ET.Element) -> str:
        """Extract field definition from annotation."""
        annotation = element.find('{%s}annotation' % self.XSD_NS)
        if annotation is not None:
            documentation = annotation.find('{%s}documentation' % self.XSD_NS)
            if documentation is not None and documentation.text:
                return documentation.text.strip()
        return ""
    
    def _extract_constraints(self, element: ET.Element, element_type: str) -> Dict:
        """Extract validation constraints from element or type."""
        constraints = {}
        
        # Check for inline simple type restrictions
        simple_type = element.find('{%s}simpleType' % self.XSD_NS)
        if simple_type is not None:
            restriction = simple_type.find('{%s}restriction' % self.XSD_NS)
            if restriction is not None:
                constraints.update(self._parse_restriction(restriction))
        
        # Check type definitions
        type_name = element_type.split(':')[-1]
        if type_name in self.simple_types:
            simple_type_def = self.simple_types[type_name]
            restriction = simple_type_def.find('{%s}restriction' % self.XSD_NS)
            if restriction is not None:
                constraints.update(self._parse_restriction(restriction))
        
        # Add type-specific constraints
        if 'Max' in type_name and 'Text' in type_name:
            # Extract max length from type name (e.g., Max35Text -> 35)
            match = re.search(r'Max(\d+)Text', type_name)
            if match:
                constraints['maxLength'] = int(match.group(1))
        
        return constraints
    
    def _parse_restriction(self, restriction: ET.Element) -> Dict:
        """Parse restriction facets."""
        constraints = {}
        
        # Max length
        max_length = restriction.find('{%s}maxLength' % self.XSD_NS)
        if max_length is not None:
            constraints['maxLength'] = int(max_length.get('value', '0'))
        
        # Min length
        min_length = restriction.find('{%s}minLength' % self.XSD_NS)
        if min_length is not None:
            constraints['minLength'] = int(min_length.get('value', '0'))
        
        # Pattern
        pattern = restriction.find('{%s}pattern' % self.XSD_NS)
        if pattern is not None:
            constraints['pattern'] = pattern.get('value', '')
        
        # Total digits
        total_digits = restriction.find('{%s}totalDigits' % self.XSD_NS)
        if total_digits is not None:
            constraints['totalDigits'] = int(total_digits.get('value', '0'))
        
        # Fraction digits
        fraction_digits = restriction.find('{%s}fractionDigits' % self.XSD_NS)
        if fraction_digits is not None:
            constraints['fractionDigits'] = int(fraction_digits.get('value', '0'))
        
        return constraints
    
    def _extract_code_list(self, element: ET.Element, element_type: str) -> Optional[List[str]]:
        """Extract enumeration values if present."""
        codes = []
        
        # Check inline simple type
        simple_type = element.find('{%s}simpleType' % self.XSD_NS)
        if simple_type is not None:
            restriction = simple_type.find('{%s}restriction' % self.XSD_NS)
            if restriction is not None:
                codes.extend(self._get_enumerations(restriction))
        
        # Check type definitions
        type_name = element_type.split(':')[-1]
        if type_name in self.simple_types:
            simple_type_def = self.simple_types[type_name]
            restriction = simple_type_def.find('{%s}restriction' % self.XSD_NS)
            if restriction is not None:
                codes.extend(self._get_enumerations(restriction))
        
        return codes if codes else None
    
    def _get_enumerations(self, restriction: ET.Element) -> List[str]:
        """Get enumeration values from restriction."""
        codes = []
        for enumeration in restriction.findall('{%s}enumeration' % self.XSD_NS):
            value = enumeration.get('value')
            if value:
                codes.append(value)
        return codes
    
    def get_message_type(self) -> str:
        """Get the identified message type."""
        return self.message_type or "unknown"
    
    def get_namespaces(self) -> Dict[str, str]:
        """Get schema namespaces."""
        return self.namespaces.copy()
