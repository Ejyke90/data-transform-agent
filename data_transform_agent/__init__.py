"""
Data Transform Agent - AI-powered schema transformation tool.

This package provides tools to transform data schemas from XSD format
to JSON Schema and Avro schema formats using AI assistance.
"""

from .transformer import SchemaTransformer, OutputFormat

__version__ = "0.1.0"
__all__ = ["SchemaTransformer", "OutputFormat"]
