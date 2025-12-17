"""
Schema Transformer Module.

Main orchestrator for schema transformations from XSD to JSON/Avro formats.
"""

import json
from typing import Dict, Any, Optional, Literal
from pathlib import Path

from .xsd_parser import XSDParser
from .json_converter import JSONSchemaConverter
from .avro_converter import AvroSchemaConverter
from .ai_agent import AIAgent


class SchemaTransformer:
    """Main class for orchestrating schema transformations."""

    def __init__(self, use_ai: bool = False, api_key: Optional[str] = None):
        """
        Initialize the schema transformer.

        Args:
            use_ai: Whether to use AI enhancement for transformations
            api_key: OpenAI API key for AI features
        """
        self.use_ai = use_ai
        self.ai_agent = AIAgent(api_key) if use_ai else None

    def transform(
        self,
        xsd_path: str,
        output_format: Literal["json", "avro"],
        output_path: Optional[str] = None,
        namespace: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Transform XSD schema to target format.

        Args:
            xsd_path: Path to the XSD file
            output_format: Target format ('json' or 'avro')
            output_path: Optional output file path
            namespace: Namespace for Avro schemas

        Returns:
            Converted schema as dictionary
        """
        # Parse XSD
        print(f"Parsing XSD schema from: {xsd_path}")
        parser = XSDParser(xsd_path)
        xsd_info = parser.get_schema_info()

        # Get AI suggestions if enabled
        if self.use_ai and self.ai_agent and self.ai_agent.is_available():
            print(f"Getting AI suggestions for {output_format} conversion...")
            suggestions = self.ai_agent.suggest_improvements(xsd_info, output_format)
            print("AI Suggestions:")
            for suggestion in suggestions.get("suggestions", []):
                print(f"  - {suggestion}")

        # Convert to target format
        print(f"Converting to {output_format.upper()} schema...")
        if output_format == "json":
            converter = JSONSchemaConverter(xsd_info)
            converted_schema = converter.convert()
        elif output_format == "avro":
            converter = AvroSchemaConverter(xsd_info, namespace or "com.example")
            converted_schema = converter.convert()
        else:
            raise ValueError(f"Unsupported output format: {output_format}")

        # Enhance with AI if enabled
        if self.use_ai and self.ai_agent and self.ai_agent.is_available():
            print("Enhancing schema with AI...")
            converted_schema = self.ai_agent.enhance_schema_conversion(
                xsd_info, output_format, converted_schema
            )

        # Save to file if output path is provided
        if output_path:
            self._save_schema(converted_schema, output_path)
            print(f"Schema saved to: {output_path}")

        return converted_schema

    def transform_to_json(
        self, xsd_path: str, output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Transform XSD to JSON Schema.

        Args:
            xsd_path: Path to the XSD file
            output_path: Optional output file path

        Returns:
            JSON Schema as dictionary
        """
        return self.transform(xsd_path, "json", output_path)

    def transform_to_avro(
        self, xsd_path: str, output_path: Optional[str] = None, namespace: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Transform XSD to Avro Schema.

        Args:
            xsd_path: Path to the XSD file
            output_path: Optional output file path
            namespace: Namespace for Avro schema

        Returns:
            Avro Schema as dictionary
        """
        return self.transform(xsd_path, "avro", output_path, namespace)

    def _save_schema(self, schema: Any, output_path: str) -> None:
        """Save schema to file."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w") as f:
            json.dump(schema, f, indent=2)
