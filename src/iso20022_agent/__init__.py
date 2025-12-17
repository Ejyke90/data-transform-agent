"""
ISO 20022 Payment Schema Agent

A comprehensive toolkit for parsing, analyzing, and validating ISO 20022 payment message schemas.
"""

__version__ = "0.1.0"
__author__ = "ISO 20022 Schema Agent Team"

from .schema_agent import ISO20022SchemaAgent
from .field import ISO20022Field, FieldRequirement

__all__ = [
    "ISO20022SchemaAgent",
    "ISO20022Field",
    "FieldRequirement",
]
