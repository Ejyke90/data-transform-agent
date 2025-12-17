"""Tests for AI Agent."""

import pytest
from data_transform_agent.ai_agent import AIAgent
import json


@pytest.fixture
def sample_xsd_info():
    """Return sample XSD info for testing."""
    return {
        "target_namespace": "http://example.com/test",
        "elements": {"TestElement": {"type": "string", "min_occurs": 1, "max_occurs": 1}},
        "types": {},
        "attributes": {},
    }


def test_ai_agent_initialization_without_key():
    """Test AI agent initialization without API key."""
    agent = AIAgent()
    assert agent.client is None
    assert not agent.is_available()


def test_ai_agent_initialization_with_key():
    """Test AI agent initialization with API key."""
    agent = AIAgent(api_key="test-key")
    # May or may not have client depending on OpenAI library availability
    assert hasattr(agent, "api_key")


def test_ai_agent_is_available():
    """Test checking if AI agent is available."""
    agent = AIAgent()
    result = agent.is_available()
    assert isinstance(result, bool)


def test_enhance_schema_without_client(sample_xsd_info):
    """Test schema enhancement without AI client."""
    agent = AIAgent()
    converted_schema = {"type": "object"}

    result = agent.enhance_schema_conversion(sample_xsd_info, "json", converted_schema)

    # Should return original schema when AI not available
    assert result == converted_schema


def test_suggest_improvements_without_client(sample_xsd_info):
    """Test getting suggestions without AI client."""
    agent = AIAgent()

    result = agent.suggest_improvements(sample_xsd_info, "json")

    assert isinstance(result, dict)
    assert "suggestions" in result


def test_extract_json_from_response():
    """Test extracting JSON from AI response."""
    agent = AIAgent()

    # Test with valid JSON
    json_str = '{"type": "object"}'
    result = agent._extract_json_from_response(json_str)
    assert result == {"type": "object"}

    # Test with markdown code block
    markdown_response = '```json\n{"type": "string"}\n```'
    result = agent._extract_json_from_response(markdown_response)
    assert result == {"type": "string"}

    # Test with surrounding text
    text_response = 'Here is the schema: {"type": "number"} which is valid.'
    result = agent._extract_json_from_response(text_response)
    assert result == {"type": "number"}

    # Test with invalid JSON
    invalid_response = "This is not JSON"
    result = agent._extract_json_from_response(invalid_response)
    assert result is None
