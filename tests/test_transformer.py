"""Tests for Schema Transformer."""

import pytest
from pathlib import Path
from data_transform_agent.transformer import SchemaTransformer


@pytest.fixture
def person_xsd_path():
    """Return path to person.xsd example."""
    return str(Path(__file__).parent.parent / "examples" / "person.xsd")


@pytest.fixture
def book_xsd_path():
    """Return path to book.xsd example."""
    return str(Path(__file__).parent.parent / "examples" / "book.xsd")


def test_transformer_initialization():
    """Test transformer initialization."""
    transformer = SchemaTransformer(use_ai=False)
    assert transformer.ai_agent is None


def test_transformer_with_ai():
    """Test transformer initialization with AI."""
    transformer = SchemaTransformer(use_ai=True)
    assert transformer.ai_agent is not None


def test_transform_to_json(person_xsd_path, tmp_path):
    """Test transforming XSD to JSON schema."""
    transformer = SchemaTransformer(use_ai=False)
    output_path = tmp_path / "output.json"

    result = transformer.transform_to_json(person_xsd_path, str(output_path))

    assert isinstance(result, dict)
    assert "$schema" in result
    assert output_path.exists()


def test_transform_to_avro(person_xsd_path, tmp_path):
    """Test transforming XSD to Avro schema."""
    transformer = SchemaTransformer(use_ai=False)
    output_path = tmp_path / "output.avsc"

    result = transformer.transform_to_avro(person_xsd_path, str(output_path))

    assert isinstance(result, (dict, list))
    assert output_path.exists()


def test_transform_with_format_parameter(book_xsd_path, tmp_path):
    """Test transform method with format parameter."""
    transformer = SchemaTransformer(use_ai=False)
    output_path = tmp_path / "output.json"

    result = transformer.transform(book_xsd_path, "json", str(output_path))

    assert isinstance(result, dict)
    assert output_path.exists()


def test_transform_invalid_format(person_xsd_path):
    """Test transform with invalid format."""
    transformer = SchemaTransformer(use_ai=False)

    with pytest.raises(ValueError):
        transformer.transform(person_xsd_path, "invalid")


def test_transform_with_namespace(person_xsd_path, tmp_path):
    """Test transform with custom namespace."""
    transformer = SchemaTransformer(use_ai=False)
    output_path = tmp_path / "output.avsc"

    result = transformer.transform(
        person_xsd_path, "avro", str(output_path), namespace="com.test"
    )

    assert isinstance(result, (dict, list))
    if isinstance(result, dict):
        assert result.get("namespace") == "com.test"
