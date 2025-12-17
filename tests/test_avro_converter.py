"""Tests for Avro Schema Converter."""

import pytest
from data_transform_agent.xsd_parser import XSDParser
from data_transform_agent.avro_converter import AvroSchemaConverter
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


def test_avro_converter_initialization(person_xsd_info):
    """Test Avro converter initialization."""
    converter = AvroSchemaConverter(person_xsd_info)
    assert converter.xsd_info is not None
    assert converter.namespace == "com.example"


def test_avro_converter_custom_namespace(person_xsd_info):
    """Test Avro converter with custom namespace."""
    converter = AvroSchemaConverter(person_xsd_info, namespace="com.test")
    assert converter.namespace == "com.test"


def test_convert_to_avro_schema(person_xsd_info):
    """Test converting to Avro schema."""
    converter = AvroSchemaConverter(person_xsd_info)
    avro_schema = converter.convert()

    assert isinstance(avro_schema, (dict, list))
    if isinstance(avro_schema, dict):
        assert "type" in avro_schema
        assert avro_schema["type"] == "record"
        assert "name" in avro_schema
        assert "namespace" in avro_schema


def test_avro_schema_has_fields(person_xsd_info):
    """Test that Avro schema has fields."""
    converter = AvroSchemaConverter(person_xsd_info)
    avro_schema = converter.convert()

    if isinstance(avro_schema, dict):
        assert "fields" in avro_schema
    elif isinstance(avro_schema, list):
        assert len(avro_schema) > 0


def test_type_mapping():
    """Test XSD to Avro type mappings."""
    converter = AvroSchemaConverter({})

    assert converter._map_xsd_type_to_avro("string") == "string"
    assert converter._map_xsd_type_to_avro("int") == "int"
    assert converter._map_xsd_type_to_avro("boolean") == "boolean"
    assert converter._map_xsd_type_to_avro("long") == "long"


def test_to_avro_schema_alias(person_xsd_info):
    """Test to_avro_schema alias method."""
    converter = AvroSchemaConverter(person_xsd_info)
    avro_schema = converter.to_avro_schema()

    assert isinstance(avro_schema, (dict, list))


def test_complex_type_to_record(book_xsd_info):
    """Test converting complex types to Avro records."""
    converter = AvroSchemaConverter(book_xsd_info)
    avro_schema = converter.convert()

    # Should produce at least one record
    if isinstance(avro_schema, list):
        assert len(avro_schema) > 0
        assert avro_schema[0]["type"] == "record"
    else:
        assert avro_schema["type"] == "record"
