"""Tests for XSD Parser."""

import pytest
from pathlib import Path
from data_transform_agent.xsd_parser import XSDParser


@pytest.fixture
def person_xsd_path():
    """Return path to person.xsd example."""
    return Path(__file__).parent.parent / "examples" / "person.xsd"


@pytest.fixture
def book_xsd_path():
    """Return path to book.xsd example."""
    return Path(__file__).parent.parent / "examples" / "book.xsd"


def test_xsd_parser_initialization(person_xsd_path):
    """Test XSD parser initialization."""
    parser = XSDParser(str(person_xsd_path))
    assert parser.schema is not None


def test_xsd_parser_file_not_found():
    """Test XSD parser with non-existent file."""
    with pytest.raises(FileNotFoundError):
        XSDParser("nonexistent.xsd")


def test_get_schema_info(person_xsd_path):
    """Test extracting schema information."""
    parser = XSDParser(str(person_xsd_path))
    info = parser.get_schema_info()

    assert "target_namespace" in info
    assert "elements" in info
    assert "types" in info
    assert "attributes" in info


def test_extract_elements(person_xsd_path):
    """Test extracting elements from schema."""
    parser = XSDParser(str(person_xsd_path))
    info = parser.get_schema_info()

    elements = info["elements"]
    assert len(elements) > 0
    assert "Person" in elements


def test_extract_types(person_xsd_path):
    """Test extracting type definitions."""
    parser = XSDParser(str(person_xsd_path))
    info = parser.get_schema_info()

    types = info["types"]
    assert isinstance(types, dict)


def test_complex_type_parsing(book_xsd_path):
    """Test parsing complex types."""
    parser = XSDParser(str(book_xsd_path))
    info = parser.get_schema_info()

    types = info["types"]
    assert len(types) > 0


def test_to_dict(person_xsd_path):
    """Test converting schema to dictionary."""
    parser = XSDParser(str(person_xsd_path))
    schema_dict = parser.to_dict()

    assert isinstance(schema_dict, dict)
    assert "elements" in schema_dict
    assert "types" in schema_dict
