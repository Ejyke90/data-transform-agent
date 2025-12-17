"""
Unit tests for ISO20022Field class
"""

import pytest
from iso20022_agent.field import ISO20022Field, FieldRequirement


def test_field_creation():
    """Test creating a field."""
    field = ISO20022Field(
        name="MessageIdentification",
        path="Document/GrpHdr/MsgId",
        data_type="Max35Text",
        multiplicity="1..1",
        requirement=FieldRequirement.MANDATORY,
        definition="Message identification",
        constraints={"maxLength": 35}
    )
    
    assert field.name == "MessageIdentification"
    assert field.path == "Document/GrpHdr/MsgId"
    assert field.is_mandatory()
    assert not field.is_optional()


def test_field_requirement_checks():
    """Test requirement checking methods."""
    mandatory_field = ISO20022Field(
        name="Test",
        path="Test/Path",
        data_type="Text",
        multiplicity="1..1",
        requirement=FieldRequirement.MANDATORY,
        definition="Test"
    )
    
    optional_field = ISO20022Field(
        name="Test",
        path="Test/Path",
        data_type="Text",
        multiplicity="0..1",
        requirement=FieldRequirement.OPTIONAL,
        definition="Test"
    )
    
    assert mandatory_field.is_mandatory()
    assert not mandatory_field.is_optional()
    
    assert optional_field.is_optional()
    assert not optional_field.is_mandatory()


def test_field_to_dict():
    """Test converting field to dictionary."""
    field = ISO20022Field(
        name="Test",
        path="Test/Path",
        data_type="Text",
        multiplicity="1..1",
        requirement=FieldRequirement.MANDATORY,
        definition="Test definition",
        constraints={"maxLength": 10},
        code_list=["A", "B", "C"]
    )
    
    field_dict = field.to_dict()
    
    assert field_dict['fieldName'] == "Test"
    assert field_dict['path'] == "Test/Path"
    assert field_dict['requirement'] == "mandatory"
    assert field_dict['constraints'] == {"maxLength": 10}
    assert field_dict['codeList'] == ["A", "B", "C"]
