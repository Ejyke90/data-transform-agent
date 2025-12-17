"""
Unit tests for ISO20022SchemaAgent
"""

import pytest
from iso20022_agent import ISO20022SchemaAgent


def test_agent_initialization():
    """Test agent initialization."""
    agent = ISO20022SchemaAgent()
    
    assert agent is not None
    assert agent.fields == []
    assert not agent.schema_loaded


def test_agent_configuration():
    """Test agent with configuration."""
    config = {
        'strict_validation': True,
        'extract_annotations': True
    }
    
    agent = ISO20022SchemaAgent(config=config)
    assert agent.config == config


def test_get_mandatory_fields():
    """Test getting mandatory fields."""
    agent = ISO20022SchemaAgent()
    # Would need actual schema for full test
    assert agent.get_mandatory_fields() == []


def test_get_statistics():
    """Test getting statistics."""
    agent = ISO20022SchemaAgent()
    stats = agent.get_statistics()
    
    assert 'messageType' in stats
    assert 'totalFields' in stats
    assert 'mandatoryCount' in stats
    assert 'optionalCount' in stats
