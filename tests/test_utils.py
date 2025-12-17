"""Tests for utility functions."""

import pytest
from data_transform_agent.utils import normalize_xsd_type


def test_normalize_xsd_type_with_curly_braces():
    """Test normalizing XSD type with curly brace notation."""
    result = normalize_xsd_type("{http://www.w3.org/2001/XMLSchema}int")
    assert result == "int"


def test_normalize_xsd_type_with_colon():
    """Test normalizing XSD type with colon notation."""
    result = normalize_xsd_type("xs:string")
    assert result == "string"


def test_normalize_xsd_type_plain():
    """Test normalizing plain XSD type."""
    result = normalize_xsd_type("string")
    assert result == "string"


def test_normalize_xsd_type_complex():
    """Test normalizing complex type name."""
    result = normalize_xsd_type("{http://example.com/person}PersonType")
    assert result == "PersonType"


def test_normalize_xsd_type_with_both_notations():
    """Test normalizing type with both namespace forms."""
    # This shouldn't happen in practice, but test the order
    result = normalize_xsd_type("{http://www.w3.org/2001/XMLSchema}xs:int")
    assert result == "int"
