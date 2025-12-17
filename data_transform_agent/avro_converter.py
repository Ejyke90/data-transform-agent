"""
Avro Schema Converter Module.

This module converts XSD schema information to Avro schema format.
"""

from typing import Dict, Any, List, Union


class AvroSchemaConverter:
    """Converter from XSD schema info to Avro Schema."""

    # XSD to Avro type mappings
    TYPE_MAPPINGS = {
        "string": "string",
        "normalizedString": "string",
        "token": "string",
        "int": "int",
        "integer": "long",
        "positiveInteger": "long",
        "negativeInteger": "long",
        "nonNegativeInteger": "long",
        "nonPositiveInteger": "long",
        "long": "long",
        "short": "int",
        "byte": "int",
        "unsignedLong": "long",
        "unsignedInt": "long",
        "unsignedShort": "int",
        "unsignedByte": "int",
        "decimal": "double",
        "float": "float",
        "double": "double",
        "boolean": "boolean",
        "date": "string",
        "time": "string",
        "dateTime": "string",
        "duration": "string",
        "base64Binary": "bytes",
        "hexBinary": "bytes",
        "anyURI": "string",
    }

    def __init__(self, xsd_info: Dict[str, Any], namespace: str = "com.example"):
        """
        Initialize the Avro Schema converter.

        Args:
            xsd_info: XSD schema information dictionary
            namespace: Avro namespace for the schema
        """
        self.xsd_info = xsd_info
        self.namespace = namespace or "com.example"

    def convert(self) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Convert XSD schema info to Avro Schema.

        Returns:
            Avro Schema as a dictionary or list of dictionaries
        """
        schemas = []

        # Convert types to Avro records
        for type_name, type_info in self.xsd_info.get("types", {}).items():
            if type_info.get("category") == "complex":
                avro_record = self._convert_complex_type_to_record(type_name, type_info)
                schemas.append(avro_record)

        # Convert root elements to records if not already covered
        for elem_name, elem_info in self.xsd_info.get("elements", {}).items():
            elem_type = elem_info.get("type")
            if elem_type == "anonymous" or elem_type not in self.xsd_info.get("types", {}):
                # Create a record for this element
                record = {
                    "type": "record",
                    "name": elem_name,
                    "namespace": self.namespace,
                    "fields": [{"name": "value", "type": self._convert_element_type(elem_info)}],
                }
                schemas.append(record)

        # Return single schema if only one, otherwise return array
        if len(schemas) == 1:
            return schemas[0]
        elif len(schemas) == 0:
            # Return a default empty record
            return {
                "type": "record",
                "name": "Root",
                "namespace": self.namespace,
                "fields": [],
            }
        else:
            return schemas

    def _convert_complex_type_to_record(
        self, type_name: str, type_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Convert a complex type to an Avro record."""
        record = {
            "type": "record",
            "name": type_name,
            "namespace": self.namespace,
            "fields": [],
        }

        content = type_info.get("content", {})

        # Convert elements to fields
        for elem_name, elem_info in content.get("elements", {}).items():
            field = {"name": elem_name, "type": self._convert_element_type(elem_info)}

            # Add default value for optional fields
            if elem_info.get("min_occurs", 0) == 0:
                # Make field nullable
                if isinstance(field["type"], list):
                    if "null" not in field["type"]:
                        field["type"].insert(0, "null")
                else:
                    field["type"] = ["null", field["type"]]
                field["default"] = None

            record["fields"].append(field)

        # Convert attributes to fields
        for attr_name, attr_info in content.get("attributes", {}).items():
            attr_type = self._map_xsd_type_to_avro(attr_info.get("type", "string"))
            field = {"name": attr_name, "type": attr_type}

            # Make optional attributes nullable
            if attr_info.get("use") != "required":
                field["type"] = ["null", attr_type]
                field["default"] = None

            record["fields"].append(field)

        return record

    def _convert_element_type(self, elem_info: Dict[str, Any]) -> Union[str, Dict, List]:
        """Convert an element type to Avro type."""
        elem_type = elem_info.get("type", "string")
        avro_type = self._map_xsd_type_to_avro(elem_type)

        # Handle arrays (maxOccurs > 1 or unbounded)
        max_occurs = elem_info.get("max_occurs")
        if max_occurs is None or (isinstance(max_occurs, (int, float)) and max_occurs > 1):
            avro_type = {"type": "array", "items": avro_type}

        # Handle nullable
        if elem_info.get("nillable"):
            avro_type = ["null", avro_type]

        return avro_type

    def _map_xsd_type_to_avro(self, xsd_type: str) -> str:
        """
        Map XSD type to Avro type.

        Args:
            xsd_type: XSD type name

        Returns:
            Avro type
        """
        # Remove namespace prefixes (both forms)
        xsd_type = xsd_type.replace("{http://www.w3.org/2001/XMLSchema}", "")
        
        # Extract local name if it's a qualified name with colon
        if ":" in xsd_type:
            xsd_type = xsd_type.split(":")[-1]

        # Check if it's a reference to a complex type
        if xsd_type in self.xsd_info.get("types", {}):
            return xsd_type

        return self.TYPE_MAPPINGS.get(xsd_type, "string")

    def to_avro_schema(self) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Alias for convert method.

        Returns:
            Avro Schema as a dictionary or list
        """
        return self.convert()
