"""
XSD Schema Parser Module.

This module handles parsing of XSD (XML Schema Definition) files
and extracts schema structure and type information.
"""

import xmlschema
from typing import Dict, Any, Optional
from pathlib import Path
import xml.etree.ElementTree as ET


class XSDParser:
    """Parser for XSD schema files."""

    def __init__(self, xsd_path: str):
        """
        Initialize the XSD parser.

        Args:
            xsd_path: Path to the XSD file
        """
        self.xsd_path = Path(xsd_path)
        self.schema = None
        self._load_schema()

    def _load_schema(self) -> None:
        """Load and validate the XSD schema."""
        if not self.xsd_path.exists():
            raise FileNotFoundError(f"XSD file not found: {self.xsd_path}")

        try:
            self.schema = xmlschema.XMLSchema(str(self.xsd_path))
        except Exception as e:
            raise ValueError(f"Failed to parse XSD schema: {e}")

    def get_schema_info(self) -> Dict[str, Any]:
        """
        Extract schema information.

        Returns:
            Dictionary containing schema structure and metadata
        """
        if not self.schema:
            raise RuntimeError("Schema not loaded")

        info = {
            "target_namespace": self.schema.target_namespace,
            "elements": self._extract_elements(),
            "types": self._extract_types(),
            "attributes": self._extract_attributes(),
        }
        return info

    def _extract_elements(self) -> Dict[str, Any]:
        """Extract global elements from the schema."""
        elements = {}
        for name, element in self.schema.elements.items():
            elements[name] = {
                "type": str(element.type.name) if hasattr(element.type, "name") else "anonymous",
                "min_occurs": element.min_occurs,
                "max_occurs": element.max_occurs,
                "nillable": element.nillable,
            }
        return elements

    def _extract_types(self) -> Dict[str, Any]:
        """Extract type definitions from the schema."""
        types = {}
        for name, type_def in self.schema.types.items():
            type_info = {"name": name}

            # Check if it's a complex type
            if hasattr(type_def, "content"):
                type_info["category"] = "complex"
                type_info["content"] = self._extract_complex_type(type_def)
            else:
                type_info["category"] = "simple"
                if hasattr(type_def, "base_type"):
                    type_info["base_type"] = str(type_def.base_type.name)

            types[name] = type_info
        return types

    def _extract_complex_type(self, complex_type) -> Dict[str, Any]:
        """Extract information from a complex type."""
        content = {}

        if hasattr(complex_type, "content") and complex_type.content:
            content["elements"] = {}
            for element in complex_type.content.iter_elements():
                elem_name = element.name
                content["elements"][elem_name] = {
                    "type": str(element.type.name)
                    if hasattr(element.type, "name")
                    else "anonymous",
                    "min_occurs": element.min_occurs,
                    "max_occurs": element.max_occurs,
                }

        if hasattr(complex_type, "attributes"):
            content["attributes"] = {}
            for attr_name, attr in complex_type.attributes.items():
                content["attributes"][attr_name] = {
                    "type": str(attr.type.name) if hasattr(attr.type, "name") else "string",
                    "use": attr.use,
                }

        return content

    def _extract_attributes(self) -> Dict[str, Any]:
        """Extract global attributes from the schema."""
        attributes = {}
        for name, attr in self.schema.attributes.items():
            attributes[name] = {
                "type": str(attr.type.name) if hasattr(attr.type, "name") else "string",
                "use": attr.use if hasattr(attr, "use") else "optional",
            }
        return attributes

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the XSD schema to a dictionary representation.

        Returns:
            Dictionary representation of the schema
        """
        return self.get_schema_info()
