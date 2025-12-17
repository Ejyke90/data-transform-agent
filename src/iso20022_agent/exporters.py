"""
Export utilities for field catalogs.
"""

import csv
import json
from typing import List, Dict, Any
from pathlib import Path
import re

from .field import ISO20022Field


class BaseExporter:
    """Base class for exporters."""
    
    def export(self, fields: List[ISO20022Field], output_path: str, metadata: Dict[str, Any]) -> None:
        """Export fields to file."""
        raise NotImplementedError


class CSVExporter(BaseExporter):
    """Export field catalog as CSV."""
    
    def export(self, fields: List[ISO20022Field], output_path: str, metadata: Dict[str, Any]) -> None:
        """Export fields to CSV file."""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            # Write header comments
            f.write(f"# Message Type: {metadata.get('messageType', 'unknown')}\n")
            f.write(f"# Total Fields: {metadata.get('totalFields', 0)}\n")
            f.write(f"# Mandatory Fields: {metadata.get('mandatoryCount', 0)}\n")
            f.write(f"# Optional Fields: {metadata.get('optionalCount', 0)}\n")
            f.write(f"# Extraction Date: {metadata.get('extractionDate', '')}\n")
            f.write("#\n")
            
            # Write CSV data
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['FieldName', 'Path', 'Multiplicity', 'Constraints', 'Definition'])
            
            for field in fields:
                writer.writerow([
                    field.name,
                    field.path,
                    field.multiplicity,
                    self._format_constraints(field),
                    field.definition
                ])
    
    def _format_constraints(self, field: ISO20022Field) -> str:
        """Format constraints as a single string."""
        constraint_parts = []
        
        # Add data type for complex types
        if field.data_type and not any(x in field.data_type for x in ['Max', 'ISODate', 'ISODateTime', 'Decimal']):
            constraint_parts.append(f"Type: {field.data_type}")
        
        # Add length constraints
        if 'maxLength' in field.constraints:
            constraint_parts.append(f"MaxLength: {field.constraints['maxLength']}")
        if 'minLength' in field.constraints:
            constraint_parts.append(f"MinLength: {field.constraints['minLength']}")
        
        # Add pattern
        if 'pattern' in field.constraints:
            pattern = field.constraints['pattern']
            # Escape quotes in pattern
            pattern = pattern.replace('"', '""')
            constraint_parts.append(f"Pattern: {pattern}")
        
        # Add decimal constraints
        if 'totalDigits' in field.constraints:
            constraint_parts.append(f"TotalDigits: {field.constraints['totalDigits']}")
        if 'fractionDigits' in field.constraints:
            constraint_parts.append(f"FractionDigits: {field.constraints['fractionDigits']}")
        
        # Add code list
        if field.code_list:
            codes = ', '.join(field.code_list[:5])  # Limit to first 5
            if len(field.code_list) > 5:
                codes += f" (+ {len(field.code_list) - 5} more)"
            constraint_parts.append(f"Codes: {codes}")
        
        # Add format hints for date/time
        if field.data_type == 'ISODate':
            constraint_parts.append("Format: ISODate (YYYY-MM-DD)")
        elif field.data_type == 'ISODateTime':
            constraint_parts.append("Format: ISODateTime")
        
        return '; '.join(constraint_parts) if constraint_parts else 'None'


class JSONExporter(BaseExporter):
    """Export field catalog as JSON."""
    
    def export(self, fields: List[ISO20022Field], output_path: str, metadata: Dict[str, Any]) -> None:
        """Export fields to JSON file."""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        catalog = {
            'metadata': metadata,
            'fields': [field.to_dict() for field in fields]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(catalog, f, indent=2, ensure_ascii=False)


class MarkdownExporter(BaseExporter):
    """Export field catalog as Markdown."""
    
    def export(self, fields: List[ISO20022Field], output_path: str, metadata: Dict[str, Any]) -> None:
        """Export fields to Markdown file."""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            # Write header
            f.write(f"# {metadata.get('messageType', 'Unknown')} Field Catalog\n\n")
            
            # Write metadata
            f.write("## Metadata\n\n")
            f.write(f"- **Message Type:** {metadata.get('messageType', 'unknown')}\n")
            f.write(f"- **Total Fields:** {metadata.get('totalFields', 0)}\n")
            f.write(f"- **Mandatory Fields:** {metadata.get('mandatoryCount', 0)}\n")
            f.write(f"- **Optional Fields:** {metadata.get('optionalCount', 0)}\n")
            f.write(f"- **Extraction Date:** {metadata.get('extractionDate', '')}\n\n")
            
            # Separate mandatory and optional fields
            mandatory = [f for f in fields if f.is_mandatory()]
            optional = [f for f in fields if f.is_optional()]
            
            # Write mandatory fields
            f.write("## Mandatory Fields\n\n")
            f.write("| Field Name | Path | Multiplicity | Constraints | Definition |\n")
            f.write("|------------|------|--------------|-------------|------------|\n")
            for field in mandatory:
                constraints = self._format_constraints(field)
                definition = field.definition.replace('|', '\\|').replace('\n', ' ')[:100]
                f.write(f"| {field.name} | `{field.path}` | {field.multiplicity} | {constraints} | {definition}... |\n")
            
            # Write optional fields
            f.write("\n## Optional Fields\n\n")
            f.write("| Field Name | Path | Multiplicity | Constraints | Definition |\n")
            f.write("|------------|------|--------------|-------------|------------|\n")
            for field in optional:
                constraints = self._format_constraints(field)
                definition = field.definition.replace('|', '\\|').replace('\n', ' ')[:100]
                f.write(f"| {field.name} | `{field.path}` | {field.multiplicity} | {constraints} | {definition}... |\n")
    
    def _format_constraints(self, field: ISO20022Field) -> str:
        """Format constraints for markdown."""
        parts = []
        
        if 'maxLength' in field.constraints:
            parts.append(f"MaxLen: {field.constraints['maxLength']}")
        if field.code_list:
            parts.append(f"Codes: {len(field.code_list)}")
        if 'pattern' in field.constraints:
            parts.append("Pattern")
        
        return ', '.join(parts) if parts else '-'
