"""Tests for JSON Schema Converter."""

import pytest
from data_transform_agent.xsd_parser import XSDParser
from data_transform_agent.json_converter import JSONSchemaConverter
from pathlib import Path


@pytest.fixture
def person_xsd_info():
    """Return parsed person XSD info."""
    xsd_path = Path(__file__).parent.parent / "examples" / "person.xsd"
    parser = XSDParser(str(xsd_path))
    return parser.get_schema_info()


@pytest.fixture
def book_xsd_info():
    """Return parsed book XSD info."""
    xsd_path = Path(__file__).parent.parent / "examples" / "book.xsd"
    parser = XSDParser(str(xsd_path))
    return parser.get_schema_info()


def test_json_converter_initialization(person_xsd_info):
    """Test JSON converter initialization."""
    converter = JSONSchemaConverter(person_xsd_info)
    assert converter.xsd_info is not None


def test_convert_to_json_schema(person_xsd_info):
    """Test converting to JSON schema."""
    converter = JSONSchemaConverter(person_xsd_info)
    json_schema = converter.convert()

    assert "$schema" in json_schema
    assert "type" in json_schema
    assert json_schema["type"] == "object"


def test_json_schema_has_properties(person_xsd_info):
    """Test that JSON schema has properties."""
    converter = JSONSchemaConverter(person_xsd_info)
    json_schema = converter.convert()

    assert "properties" in json_schema or "definitions" in json_schema


def test_type_mapping():
    """Test XSD to JSON type mappings."""
    converter = JSONSchemaConverter({})

    assert converter._map_xsd_type_to_json("string") == "string"
    assert converter._map_xsd_type_to_json("int") == "integer"
    assert converter._map_xsd_type_to_json("boolean") == "boolean"
    assert converter._map_xsd_type_to_json("decimal") == "number"


def test_to_json_schema_alias(person_xsd_info):
    """Test to_json_schema alias method."""
    converter = JSONSchemaConverter(person_xsd_info)
    json_schema = converter.to_json_schema()

    assert isinstance(json_schema, dict)
    assert "$schema" in json_schema


def test_complex_type_conversion(book_xsd_info):
    """Test converting complex types."""
    converter = JSONSchemaConverter(book_xsd_info)
    json_schema = converter.convert()

    assert "definitions" in json_schema or "properties" in json_schema
