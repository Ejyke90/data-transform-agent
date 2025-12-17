"""
Utility functions for schema conversion.
"""

import re


def normalize_xsd_type(xsd_type: str) -> str:
    """
    Normalize XSD type by removing namespace prefixes.
    
    Handles both forms:
    - Curly brace notation: {http://www.w3.org/2001/XMLSchema}int or {namespace}Type
    - Colon notation: xs:int
    
    Args:
        xsd_type: XSD type name
        
    Returns:
        Normalized type name (e.g., 'int', 'string', 'PersonType')
    """
    # Remove any namespace in curly brace notation
    xsd_type = re.sub(r'\{[^}]+\}', '', xsd_type)
    
    # Extract local name if it's a qualified name with colon
    if ":" in xsd_type:
        xsd_type = xsd_type.split(":")[-1]
    
    return xsd_type
