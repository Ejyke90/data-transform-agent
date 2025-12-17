"""
Field data models for ISO 20022 message schemas.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any


class FieldRequirement(Enum):
    """Classification of field requirements."""
    MANDATORY = "mandatory"
    OPTIONAL = "optional"
    CONDITIONAL = "conditional"


@dataclass
class ISO20022Field:
    """Represents a field in an ISO 20022 message schema."""
    
    name: str
    path: str
    data_type: str
    multiplicity: str
    requirement: FieldRequirement
    definition: str
    constraints: Dict[str, Any] = field(default_factory=dict)
    code_list: Optional[List[str]] = None
    parent_path: Optional[str] = None
    
    def is_mandatory(self) -> bool:
        """Check if field is mandatory."""
        return self.requirement == FieldRequirement.MANDATORY
    
    def is_optional(self) -> bool:
        """Check if field is optional."""
        return self.requirement == FieldRequirement.OPTIONAL
    
    def is_conditional(self) -> bool:
        """Check if field is conditional."""
        return self.requirement == FieldRequirement.CONDITIONAL
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert field to dictionary representation."""
        return {
            'fieldName': self.name,
            'path': self.path,
            'dataType': self.data_type,
            'multiplicity': self.multiplicity,
            'requirement': self.requirement.value,
            'definition': self.definition,
            'constraints': self.constraints,
            'codeList': self.code_list,
            'parentPath': self.parent_path
        }
    
    def __repr__(self) -> str:
        return f"ISO20022Field(name={self.name}, path={self.path}, requirement={self.requirement.value})"
