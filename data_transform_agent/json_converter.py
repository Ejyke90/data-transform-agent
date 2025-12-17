"""
JSON Schema Converter Module.

This module converts XSD schema information to JSON Schema format.
"""

from typing import Dict, Any, Optional


class JSONSchemaConverter:
    """Converter from XSD schema info to JSON Schema."""

    # XSD to JSON Schema type mappings
    TYPE_MAPPINGS = {
        "string": "string",
        "normalizedString": "string",
        "token": "string",
        "int": "integer",
        "integer": "integer",
        "positiveInteger": "integer",
        "negativeInteger": "integer",
        "nonNegativeInteger": "integer",
        "nonPositiveInteger": "integer",
        "long": "integer",
        "short": "integer",
        "byte": "integer",
        "unsignedLong": "integer",
        "unsignedInt": "integer",
        "unsignedShort": "integer",
        "unsignedByte": "integer",
        "decimal": "number",
        "float": "number",
        "double": "number",
        "boolean": "boolean",
        "date": "string",
        "time": "string",
        "dateTime": "string",
        "duration": "string",
        "base64Binary": "string",
        "hexBinary": "string",
        "anyURI": "string",
    }

    def __init__(self, xsd_info: Dict[str, Any]):
        """
        Initialize the JSON Schema converter.

        Args:
            xsd_info: XSD schema information dictionary
        """
        self.xsd_info = xsd_info

    def convert(self) -> Dict[str, Any]:
        """
        Convert XSD schema info to JSON Schema.

        Returns:
            JSON Schema as a dictionary
        """
        json_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": self.xsd_info.get("target_namespace", ""),
            "type": "object",
            "properties": {},
            "definitions": {},
        }

        # Convert types to definitions
        for type_name, type_info in self.xsd_info.get("types", {}).items():
            json_schema["definitions"][type_name] = self._convert_type(type_info)

        # Convert elements to properties
        for elem_name, elem_info in self.xsd_info.get("elements", {}).items():
            json_schema["properties"][elem_name] = self._convert_element(elem_info)

        return json_schema

    def _convert_type(self, type_info: Dict[str, Any]) -> Dict[str, Any]:
        """Convert a single type definition."""
        if type_info.get("category") == "simple":
            base_type = type_info.get("base_type", "string")
            json_type = self._map_xsd_type_to_json(base_type)
            return {"type": json_type}

        elif type_info.get("category") == "complex":
            return self._convert_complex_type(type_info.get("content", {}))

        return {"type": "object"}

    def _convert_complex_type(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Convert a complex type definition."""
        schema = {"type": "object", "properties": {}, "required": []}

        # Convert elements
        for elem_name, elem_info in content.get("elements", {}).items():
            schema["properties"][elem_name] = self._convert_element(elem_info)

            # Add to required if minOccurs >= 1
            if elem_info.get("min_occurs", 0) >= 1:
                schema["required"].append(elem_name)

        # Convert attributes
        for attr_name, attr_info in content.get("attributes", {}).items():
            attr_type = self._map_xsd_type_to_json(attr_info.get("type", "string"))
            schema["properties"][attr_name] = {"type": attr_type}

            # Add to required if use is "required"
            if attr_info.get("use") == "required":
                schema["required"].append(attr_name)

        # Remove empty required array
        if not schema["required"]:
            del schema["required"]

        return schema

    def _convert_element(self, elem_info: Dict[str, Any]) -> Dict[str, Any]:
        """Convert an element definition."""
        elem_type = elem_info.get("type", "string")
        json_type = self._map_xsd_type_to_json(elem_type)

        schema = {"type": json_type}

        # Handle arrays (maxOccurs > 1 or unbounded)
        max_occurs = elem_info.get("max_occurs")
        if max_occurs is None or (isinstance(max_occurs, (int, float)) and max_occurs > 1):
            schema = {"type": "array", "items": {"type": json_type}}

        # Handle nullable
        if elem_info.get("nillable"):
            if isinstance(schema.get("type"), str):
                schema["type"] = [schema["type"], "null"]

        return schema

    def _map_xsd_type_to_json(self, xsd_type: str) -> str:
        """
        Map XSD type to JSON Schema type.

        Args:
            xsd_type: XSD type name

        Returns:
            JSON Schema type
        """
        # Extract local name if it's a qualified name
        if ":" in xsd_type:
            xsd_type = xsd_type.split(":")[-1]

        # Remove namespace prefixes
        xsd_type = xsd_type.replace("{http://www.w3.org/2001/XMLSchema}", "")

        return self.TYPE_MAPPINGS.get(xsd_type, "string")

    def to_json_schema(self) -> Dict[str, Any]:
        """
        Alias for convert method.

        Returns:
            JSON Schema as a dictionary
        """
        return self.convert()
